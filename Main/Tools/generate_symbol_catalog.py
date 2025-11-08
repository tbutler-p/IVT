#!/usr/bin/env python3
"""Build structured symbol catalogs from Pyright-generated type stubs.

The script reads ``Main/Pyright/packages.json`` (produced by
``generate_pyright_assets.py``), walks the stub trees for each package,
and emits JSON summaries describing public modules, classes, functions,
variables, and related members.  The output layout matches the Option A
requirements, creating ``<Package>/<Package>.json`` under ``Main/Pyright``.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

try:
    from importlib import metadata as importlib_metadata
except ImportError:  # pragma: no cover
    import importlib_metadata  # type: ignore


ROOT = Path("Main/Pyright").resolve()
MANIFEST = ROOT / "packages.json"


def load_manifest() -> Dict[str, Sequence[str]]:
    """Return mapping from distribution -> modules."""

    if not MANIFEST.exists():
        raise SystemExit(f"Manifest not found: {MANIFEST}")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mapping: Dict[str, Sequence[str]] = {}
    for entry in data.get("packages", []):
        dist = entry["distribution"]
        modules = entry["modules"]
        mapping[dist] = modules
    return mapping


def ast_to_str(node: Optional[ast.AST]) -> Optional[str]:
    """Render an AST node back to source text."""

    if node is None:
        return None
    try:
        return ast.unparse(node)
    except Exception:  # pragma: no cover
        return None


def format_default(node: Optional[ast.AST]) -> Optional[str]:
    """Return a user-friendly default value representation."""

    text = ast_to_str(node)
    return text


def is_public(name: str) -> bool:
    """Return True if the symbol should be considered public."""

    if name.startswith("__") and name.endswith("__"):
        return name in {"__all__", "__version__"}
    return not name.startswith("_")


def split_defaults(
    args: ast.arguments,
) -> Tuple[Dict[str, Optional[ast.AST]], Dict[str, Optional[ast.AST]]]:
    """Return mapping of arg name -> default for positional and kw-only args."""

    positional = list(args.posonlyargs) + list(args.args)
    defaults = args.defaults or []
    start = len(positional) - len(defaults)
    positional_defaults: Dict[str, Optional[ast.AST]] = {}
    for idx, arg in enumerate(positional):
        default_idx = idx - start
        positional_defaults[arg.arg] = defaults[default_idx] if default_idx >= 0 else None

    kw_defaults = args.kw_defaults or []
    kwonly_defaults: Dict[str, Optional[ast.AST]] = {}
    for arg, default in zip(args.kwonlyargs, kw_defaults):
        kwonly_defaults[arg.arg] = default

    return positional_defaults, kwonly_defaults


def param_entry(arg: ast.arg, kind: str, default: Optional[ast.AST]) -> Dict[str, Optional[str]]:
    """Format a parameter entry for the JSON schema."""

    return {
        "name": arg.arg,
        "kind": kind,
        "type": ast_to_str(arg.annotation),
        "default": format_default(default),
    }


FunctionNode = Union[ast.FunctionDef, ast.AsyncFunctionDef]


def collect_function_overloads(nodes: Sequence[FunctionNode]) -> List[Dict[str, object]]:
    """Group function definitions into overload entries."""

    overloads: List[Dict[str, object]] = []
    for func in nodes:
        positional_defaults, kwonly_defaults = split_defaults(func.args)
        params: List[Dict[str, Optional[str]]] = []

        for arg in func.args.posonlyargs:
            params.append(param_entry(arg, "positional-only", positional_defaults.get(arg.arg)))
        for arg in func.args.args:
            params.append(param_entry(arg, "positional-or-keyword", positional_defaults.get(arg.arg)))
        if func.args.vararg:
            params.append(
                {
                    "name": func.args.vararg.arg,
                    "kind": "var-positional",
                    "type": ast_to_str(func.args.vararg.annotation),
                    "default": None,
                }
            )
        for arg in func.args.kwonlyargs:
            params.append(param_entry(arg, "keyword-only", kwonly_defaults.get(arg.arg)))
        if func.args.kwarg:
            params.append(
                {
                    "name": func.args.kwarg.arg,
                    "kind": "var-keyword",
                    "type": ast_to_str(func.args.kwarg.annotation),
                    "default": None,
                }
            )

        overloads.append(
            {
                "params": params,
                "return": ast_to_str(func.returns),
                "decorators": [value for value in (ast_to_str(dec) for dec in func.decorator_list) if value],
            }
        )
    return overloads


def collect_functions(nodes: Sequence[ast.AST]) -> List[Dict[str, object]]:
    """Collect function descriptors from a module or class body."""

    grouped: Dict[str, List[FunctionNode]] = {}
    for node in nodes:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            grouped.setdefault(node.name, []).append(node)

    functions: List[Dict[str, object]] = []
    for name, defs in grouped.items():
        if not is_public(name):
            continue
        decorators: List[str] = [
            value for func in defs for value in (ast_to_str(dec) for dec in func.decorator_list) if value
        ]
        overloads = collect_function_overloads(defs)
        functions.append(
            {
                "name": name,
                "decorators": decorators,
                "overloads": overloads,
            }
        )
    return functions


def collect_assignments(nodes: Sequence[ast.AST]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """Return (variables, type_aliases) from a module body."""

    variables: List[Dict[str, object]] = []
    aliases: List[Dict[str, object]] = []
    for node in nodes:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
            if not is_public(name):
                continue
            type_text = ast_to_str(node.annotation)
            value_text = ast_to_str(node.value)
            variables.append({"name": name, "type": type_text, "value": value_text})
        elif isinstance(node, ast.Assign):
            if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                continue
            name = node.targets[0].id
            if not is_public(name):
                continue
            value_text = ast_to_str(node.value)
            # Heuristic: treat assignments ending with "TypeAlias" or typing alias as type aliases.
            if isinstance(node.value, (ast.Subscript, ast.Name, ast.Attribute)):
                aliases.append({"name": name, "target": value_text})
            else:
                variables.append({"name": name, "type": None, "value": value_text})
    return variables, aliases


def classify_class_bases(node: ast.ClassDef) -> Tuple[List[str], str]:
    """Return (bases, category) where category hints typed dict/protocol/enum."""

    bases = [ast_to_str(base) or "" for base in node.bases]
    category = "class"
    lowered = [b.lower() for b in bases if b]
    if any("enum" in b for b in lowered):
        category = "enum"
    elif any("typeddict" in b for b in lowered):
        category = "typeddict"
    elif any("protocol" in b for b in lowered):
        category = "protocol"
    return bases, category


def collect_class_members(node: ast.ClassDef) -> Dict[str, List[Dict[str, object]]]:
    """Collect detailed member information for a class definition."""

    class_vars: List[Dict[str, object]] = []
    attributes: List[Dict[str, object]] = []
    methods: List[Dict[str, object]] = collect_functions(node.body)

    for child in node.body:
        if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            name = child.target.id
            if not is_public(name):
                continue
            class_vars.append(
                {
                    "name": name,
                    "type": ast_to_str(child.annotation),
                    "value": ast_to_str(child.value),
                }
            )
        elif isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name) and is_public(target.id):
                    attributes.append(
                        {
                            "name": target.id,
                            "type": None,
                            "value": ast_to_str(child.value),
                        }
                    )

    return {
        "classVars": class_vars,
        "attributes": attributes,
        "methods": methods,
        "enums": [],
        "typedDicts": [],
        "protocols": [],
        "typeAliases": [],
    }


def classify_class(node: ast.ClassDef) -> Tuple[Dict[str, object], str]:
    """Produce the JSON payload for a class definition."""

    bases, category = classify_class_bases(node)
    members = collect_class_members(node)
    entry = {
        "name": node.name,
        "bases": bases,
        "decorators": [ast_to_str(dec) for dec in node.decorator_list],
        "members": members,
    }
    return entry, category


def collect_classes(nodes: Sequence[ast.AST]) -> Dict[str, List[Dict[str, object]]]:
    """Collect classes partitioned by category."""

    classes: List[Dict[str, object]] = []
    enums: List[Dict[str, object]] = []
    typeddicts: List[Dict[str, object]] = []
    protocols: List[Dict[str, object]] = []

    for node in nodes:
        if isinstance(node, ast.ClassDef) and is_public(node.name):
            entry, category = classify_class(node)
            if category == "enum":
                enums.append(entry)
            elif category == "typeddict":
                typeddicts.append(entry)
            elif category == "protocol":
                protocols.append(entry)
            else:
                classes.append(entry)

    return {
        "classes": classes,
        "enums": enums,
        "typedDicts": typeddicts,
        "protocols": protocols,
    }


@dataclass
class ModuleSummary:
    """Holds the collected data for a module stub."""

    name: str
    path: str
    docstring: Optional[str]
    classes: List[Dict[str, object]] = field(default_factory=list)
    functions: List[Dict[str, object]] = field(default_factory=list)
    variables: List[Dict[str, object]] = field(default_factory=list)
    enums: List[Dict[str, object]] = field(default_factory=list)
    typed_dicts: List[Dict[str, object]] = field(default_factory=list)
    protocols: List[Dict[str, object]] = field(default_factory=list)
    type_aliases: List[Dict[str, object]] = field(default_factory=list)

    def as_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "path": self.path,
            "docstring": self.docstring,
            "classes": self.classes,
            "enums": self.enums,
            "typedDicts": self.typed_dicts,
            "protocols": self.protocols,
            "functions": self.functions,
            "variables": self.variables,
            "typeAliases": self.type_aliases,
        }


def module_name_from_path(root_module: str, relative: Path) -> str:
    """Convert a stub file path to its fully qualified module name."""

    parts = list(relative.parts)
    if not parts:
        return root_module
    filename = parts[-1]
    stem = Path(filename).stem

    if stem == "__init__":
        parts = parts[:-1]
    else:
        parts[-1] = stem
    if parts:
        return ".".join([root_module] + parts)
    return root_module


def sanitize_stub_source(text: str) -> str:
    """Apply lightweight fixes to known stub syntax issues."""

    import re

    pattern = re.compile(
        r"(deprecated_args\s*=\s*'[^']+')((?:\s*,\s*'[^']+')+)(?=\s*,\s*[a-zA-Z_]+=|\s*\))"
    )

    def repl(match: re.Match[str]) -> str:
        first = match.group(1).split("=", 1)[1].strip()
        # first still in the form "'value'"
        first_value = first.strip()
        rest_values = re.findall(r"'([^']+)'", match.group(2))
        all_values = [first_value] + [f"'{val}'" for val in rest_values]
        cleaned = ", ".join(v for v in all_values)
        cleaned = cleaned.replace("''", "'")  # safety
        return f"deprecated_args=({cleaned})"

    return pattern.sub(repl, text)


def collect_from_module(root_module: str, file_path: Path, rel_path: Path) -> ModuleSummary:
    """Parse a single .pyi stub to create a module summary."""

    source = file_path.read_text(encoding="utf-8")
    source = sanitize_stub_source(source)
    tree = ast.parse(source)
    docstring = ast.get_docstring(tree)

    module_name = module_name_from_path(root_module, rel_path)
    body = tree.body

    functions = collect_functions(body)
    variables, aliases = collect_assignments(body)
    class_groups = collect_classes(body)

    summary = ModuleSummary(
        name=module_name,
        path=str(rel_path),
        docstring=docstring,
        classes=class_groups["classes"],
        enums=class_groups["enums"],
        typed_dicts=class_groups["typedDicts"],
        protocols=class_groups["protocols"],
        functions=functions,
        variables=variables,
        type_aliases=aliases,
    )
    return summary


def build_package_payload(distribution: str, modules: Sequence[str]) -> Dict[str, object]:
    """Create the JSON payload for a package."""

    try:
        version = importlib_metadata.version(distribution)
    except importlib_metadata.PackageNotFoundError:
        version = "unknown"

    module_summaries: List[ModuleSummary] = []
    for module in modules:
        stub_root = ROOT / module
        if not stub_root.exists():
            continue
        for file_path in stub_root.rglob("*.pyi"):
            rel_path = file_path.relative_to(stub_root)
            summary = collect_from_module(module, file_path, rel_path)
            module_summaries.append(summary)

    return {
        "package": distribution,
        "version": version,
        "modules": [summary.as_dict() for summary in sorted(module_summaries, key=lambda item: item.name)],
    }


def write_package_payload(distribution: str, payload: Dict[str, object]) -> None:
    """Persist the JSON payload alongside the stubs."""

    out_dir = ROOT / distribution
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{distribution}.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    mapping = load_manifest()
    for distribution, modules in mapping.items():
        payload = build_package_payload(distribution, modules)
        write_package_payload(distribution, payload)


if __name__ == "__main__":  # pragma: no cover
    main()
