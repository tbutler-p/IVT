#!/usr/bin/env python3
"""
inventory_docling.py

Generate an API inventory for the Docling package by inspecting either:
- A local source tree (preferred for accuracy before install), or
- The installed package at runtime.

Outputs:
- <out>.json : machine-readable inventory
- <out>.md   : human-readable summary

Usage:
  python inventory_docling.py --package docling --out artifacts/docling_api
  python inventory_docling.py --source-path external/docling/src --package docling --out artifacts/docling_api

Notes:
- This is best-effort static + runtime reflection. It won’t perfectly extract all enums or dynamic APIs.
- Review the JSON/MD outputs and adjust the extraction rules as needed.
"""

import argparse
import importlib
import importlib.util
import inspect
import io
import json
import os
import pkgutil
import re
import sys
import textwrap
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Heuristics for argument choice extraction
# Keep patterns simple and well-balanced to avoid 3.13 parsing issues.
CHOICE_HINT_PATTERNS = [
    # e.g., convertTo("docling-json")
    re.compile(r'convertTo\((?:self,\s*)?["\']([\w\-]+)["\']\)'),
    # e.g., choices = ["a", "b", "c"]
    re.compile(r'choices\s*=\s*\[([^\]]+)\]'),
    # e.g., ALLOWED_TARGETS = ["a", "b"] or {...}
    re.compile(r'ALLOWED_[A-Z_]+\s*=\s*(?:\[[^\]]+\]|\{[^}]+\})'),
]

# Used to pull individual quoted string literals from a matched group
STRING_LITERAL_PATTERN = re.compile(r'["\']([\w\-.]+)["\']')


@dataclass
class ParamInfo:
    name: str
    annotation: Optional[str]
    default: Optional[str]
    kind: str


@dataclass
class CallableInfo:
    name: str
    qualname: str
    obj_type: str  # 'function' or 'method' or 'builtin_function_or_method'
    signature: Optional[str]
    doc: Optional[str]
    file: Optional[str]
    line: Optional[int]
    arg_choices: Dict[str, List[str]]  # param -> allowed values (heuristic)


@dataclass
class ClassInfo:
    name: str
    qualname: str
    bases: List[str]
    doc: Optional[str]
    file: Optional[str]
    line: Optional[int]
    methods: List[CallableInfo]


@dataclass
class ModuleInfo:
    name: str
    file: Optional[str]
    doc: Optional[str]
    classes: List[ClassInfo]
    functions: List[CallableInfo]
    variables: List[str]


def short_doc(doc: Optional[str], width: int = 300) -> Optional[str]:
    if not doc:
        return None
    first = doc.strip().splitlines()[0].strip()
    return textwrap.shorten(first, width=width)


def safe_signature(obj) -> Optional[str]:
    try:
        sig = inspect.signature(obj)
        return str(sig)
    except (TypeError, ValueError):
        return None


def get_source_location(obj) -> Tuple[Optional[str], Optional[int]]:
    try:
        src = inspect.getsourcefile(obj) or inspect.getfile(obj)
        _, line = inspect.getsourcelines(obj)
        return src, line
    except Exception:
        return None, None


def extract_string_choices_from_source(source_text: str) -> List[str]:
    # Best-effort extraction of plausible string constants
    # Find clusters near known patterns
    candidates: List[str] = []
    for pat in CHOICE_HINT_PATTERNS:
        for m in pat.finditer(source_text):
            group_text = m.group(1) if m.groups() else m.group(0)
            candidates.extend(STRING_LITERAL_PATTERN.findall(group_text))
    # Deduplicate while preserving order
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def read_text_if_exists(path: Optional[str]) -> str:
    if not path:
        return ""
    try:
        with io.open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def is_public(name: str) -> bool:
    return not name.startswith("_")


def collect_runtime_module_names(root_pkg: str) -> List[str]:
    modules = []
    try:
        pkg = importlib.import_module(root_pkg)
    except Exception as e:
        print(f"[warn] Could not import {root_pkg}: {e}", file=sys.stderr)
        return modules

    pkg_path_list = getattr(pkg, "__path__", None)
    if not pkg_path_list:
        # Single file module
        return [root_pkg]

    for finder, name, ispkg in pkgutil.walk_packages(pkg_path_list, prefix=pkg.__name__ + "."):
        modules.append(name)
    # Ensure including the root itself
    if root_pkg not in modules:
        modules.insert(0, root_pkg)
    return modules


def load_module_from_source(module_name: str, module_file: Path) -> Optional[Any]:
    spec = importlib.util.spec_from_file_location(module_name, module_file)
    if not spec or not spec.loader:
        return None
    try:
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        print(f"[warn] Failed to load {module_name} from {module_file}: {e}", file=sys.stderr)
        return None


def collect_source_module_files(source_root: Path, package: str) -> Dict[str, Path]:
    """
    Map dotted module names to file paths from a source tree that contains the package directory.
    Expecting a layout like: <source_root>/<package>/...
    """
    pkg_dir = source_root / package.replace(".", "/")
    module_map: Dict[str, Path] = {}

    if not pkg_dir.exists():
        print(f"[warn] Source package dir not found: {pkg_dir}", file=sys.stderr)
        return module_map

    for path in pkg_dir.rglob("*.py"):
        rel = path.relative_to(source_root).with_suffix("")
        dotted = ".".join(rel.parts)
        module_map[dotted] = path
    return module_map


def inspect_module(mod) -> ModuleInfo:
    m_name = getattr(mod, "__name__", "UNKNOWN")
    m_file = getattr(mod, "__file__", None)
    m_doc = short_doc(getattr(mod, "__doc__", None))

    classes: List[ClassInfo] = []
    functions: List[CallableInfo] = []
    variables: List[str] = []

    # Build a lookup of source text once per module for choice extraction
    m_source_text = read_text_if_exists(m_file)

    for name, obj in inspect.getmembers(mod):
        if not is_public(name):
            continue
        try:
            if inspect.isclass(obj) and obj.__module__ == m_name:
                file, line = get_source_location(obj)
                bases = [b.__name__ for b in getattr(obj, "__mro__", [])[1:-1]] if hasattr(obj, "__mro__") else []
                methods: List[CallableInfo] = []
                for meth_name, meth in inspect.getmembers(obj, predicate=inspect.isfunction):
                    if not is_public(meth_name):
                        continue
                    if getattr(meth, "__qualname__", "").split(".")[0] != obj.__name__:
                        continue
                    mfile, mline = get_source_location(meth)
                    choices = {}
                    # Heuristic: if method name hints convert-like behavior, try to find string literal choices
                    if m_source_text and "convert" in meth_name.lower():
                        choices_list = extract_string_choices_from_source(m_source_text)
                        if choices_list:
                            # Put under a generic parameter name if we can't infer param name
                            choices["target_or_format"] = choices_list
                    methods.append(
                        CallableInfo(
                            name=meth_name,
                            qualname=getattr(meth, "__qualname__", meth_name),
                            obj_type="method",
                            signature=safe_signature(meth),
                            doc=short_doc(inspect.getdoc(meth)),
                            file=mfile,
                            line=mline,
                            arg_choices=choices,
                        )
                    )
                classes.append(
                    ClassInfo(
                        name=name,
                        qualname=getattr(obj, "__qualname__", name),
                        bases=bases,
                        doc=short_doc(inspect.getdoc(obj)),
                        file=file,
                        line=line,
                        methods=methods,
                    )
                )
            elif inspect.isfunction(obj) and obj.__module__ == m_name:
                file, line = get_source_location(obj)
                choices = {}
                if m_source_text and "convert" in name.lower():
                    choices_list = extract_string_choices_from_source(m_source_text)
                    if choices_list:
                        choices["target_or_format"] = choices_list
                functions.append(
                    CallableInfo(
                        name=name,
                        qualname=getattr(obj, "__qualname__", name),
                        obj_type="function",
                        signature=safe_signature(obj),
                        doc=short_doc(inspect.getdoc(obj)),
                        file=file,
                        line=line,
                        arg_choices=choices,
                    )
                )
            else:
                # Variables/constants
                if not callable(obj) and not inspect.ismodule(obj) and not inspect.isclass(obj):
                    variables.append(name)
        except Exception:
            # Continue on any reflected member error
            continue

    return ModuleInfo(
        name=m_name,
        file=m_file,
        doc=m_doc,
        classes=classes,
        functions=functions,
        variables=variables,
    )


def generate_inventory(
    package: str,
    source_path: Optional[Path],
) -> Dict[str, Any]:
    inventory: Dict[str, Any] = {
        "package": package,
        "source_mode": bool(source_path),
        "modules": [],
        "errors": [],
    }

    modules_to_inspect: List[str] = []
    module_file_map: Dict[str, Path] = {}

    if source_path:
        module_file_map = collect_source_module_files(source_path, package)
        modules_to_inspect = sorted(module_file_map.keys())
    else:
        modules_to_inspect = collect_runtime_module_names(package)

    for mname in modules_to_inspect:
        try:
            if source_path:
                mfile = module_file_map.get(mname)
                if not mfile:
                    continue
                mod = load_module_from_source(mname, mfile)
                if not mod:
                    inventory["errors"].append(f"Failed to load {mname} from {mfile}")
                    continue
            else:
                mod = importlib.import_module(mname)

            info = inspect_module(mod)
            inventory["modules"].append(asdict(info))
        except Exception as e:
            inventory["errors"].append(f"{mname}: {e}")

    return inventory


def write_outputs(inventory: Dict[str, Any], out_base: Path) -> None:
    out_json = out_base.with_suffix(".json")
    out_md = out_base.with_suffix(".md")

    out_json.parent.mkdir(parents=True, exist_ok=True)

    with io.open(out_json, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)

    # Markdown summary
    lines: List[str] = []
    lines.append(f"# API Inventory: {inventory['package']}")
    lines.append("")
    lines.append(f"- Source mode: {inventory['source_mode']}")
    lines.append(f"- Modules: {len(inventory['modules'])}")
    if inventory["errors"]:
        lines.append(f"- Errors: {len(inventory['errors'])}")
    lines.append("")

    for mod in inventory["modules"]:
        lines.append(f"## Module `{mod['name']}`")
        lines.append(f"- File: {mod.get('file')}")
        if mod.get("doc"):
            lines.append(f"- Doc: {mod['doc']}")
        if mod["variables"]:
            lines.append(f"- Variables: {', '.join(mod['variables'][:20])}{' ...' if len(mod['variables'])>20 else ''}")
        lines.append("")
        if mod["classes"]:
            lines.append("### Classes")
            for cls in mod["classes"]:
                lines.append(f"- `{cls['name']}` (file: {cls.get('file')}:{cls.get('line')})")
                if cls.get("doc"):
                    lines.append(f"  - {cls['doc']}")
                if cls["methods"]:
                    lines.append(f"  - Methods:")
                    for meth in cls["methods"]:
                        sig = meth["signature"] or "()"
                        lines.append(f"    - `{meth['name']}{sig}` (file: {meth.get('file')}:{meth.get('line')})")
                        if meth.get("doc"):
                            lines.append(f"      - {meth['doc']}")
                        if meth["arg_choices"]:
                            for pname, choices in meth["arg_choices"].items():
                                lines.append(f"      - Choices for `{pname}`: {sorted(set(choices))}")
        if mod["functions"]:
            lines.append("")
            lines.append("### Functions")
            for fn in mod["functions"]:
                sig = fn["signature"] or "()"
                lines.append(f"- `{fn['name']}{sig}` (file: {fn.get('file')}:{fn.get('line')})")
                if fn.get("doc"):
                    lines.append(f"  - {fn['doc']}")
                if fn["arg_choices"]:
                    for pname, choices in fn["arg_choices"].items():
                        lines.append(f"  - Choices for `{pname}`: {sorted(set(choices))}")
        lines.append("")

    if inventory["errors"]:
        lines.append("## Errors")
        for e in inventory["errors"]:
            lines.append(f"- {e}")
        lines.append("")

    with io.open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote: {out_json}")
    print(f"Wrote: {out_md}")


def main():
    parser = argparse.ArgumentParser(description="Generate API inventory for Docling.")
    parser.add_argument("--package", default="docling", help="Root package name (default: docling)")
    parser.add_argument("--source-path", type=str, default=None, help="Path to source root that contains the package directory (e.g., external/docling/src)")
    parser.add_argument("--out", type=str, required=True, help="Output base path without extension (e.g., artifacts/docling_api)")
    args = parser.parse_args()

    source_path = Path(args.source_path) if args.source_path else None

    if source_path and not source_path.exists():
        print(f"[error] Source path not found: {source_path}", file=sys.stderr)
        sys.exit(2)

    # Ensure the source path is importable when using source mode
    if source_path and str(source_path) not in sys.path:
        sys.path.insert(0, str(source_path))

    inv = generate_inventory(args.package, source_path)
    write_outputs(inv, Path(args.out))


if __name__ == "__main__":
    main()