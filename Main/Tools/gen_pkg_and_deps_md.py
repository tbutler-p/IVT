#!/usr/bin/env python3
"""
Generate Markdown API docs for a package and all (installed) dependencies
using Pydoc-Markdown, producing one .md file per top-level module.

It uses:
- importlib.metadata to discover installed dependency graph
- a mapping to resolve PyPI project names -> importable module names
- the pydoc-markdown CLI in per-module mode (-m), capturing stdout to .md files

Docs referenced:
- CLI usage and API: https://niklasrosenstein.github.io/pydoc-markdown/usage/cli-and-api/
- CLI options: https://niklasrosenstein.github.io/pydoc-markdown/api/cli/

Prereq: pip install pydoc-markdown
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Set, List

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    import importlib_metadata  # type: ignore

# Known PyPI project name -> import name mismatches
KNOWN_IMPORT_NAME_OVERRIDES = {
    "huggingface-hub": "huggingface_hub",
    "pillow": "PIL",
    "beautifulsoup4": "bs4",
    "pyyaml": "yaml",
    "opencv-python": "cv2",
    "scikit-learn": "sklearn",
    "google-auth": "google.oauth2",
    "python-dateutil": "dateutil",
    "importlib-metadata": "importlib_metadata",
    "prompt-toolkit": "prompt_toolkit",
    "pyjwt": "jwt",
    "pydantic-core": "pydantic_core",
    "readme_renderer": "readme_renderer",  # example identity
}

# Default “heavy” modules that are often slow/problematic to import
DEFAULT_HEAVY_MODULE_PATTERNS = [
    r"^torch(\.|$)",
    r"^torchvision(\.|$)",
    r"^torchaudio(\.|$)",
    r"^tensorflow(\.|$)",
    r"^onnxruntime(\.|$)",
    r"^cv2(\.|$)",
    r"^vllm(\.|$)",
    r"^xformers(\.|$)",
]


def normalize_project_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirement(req: str) -> str:
    # Remove environment markers
    req = req.split(";")[0].strip()
    # Base project name
    m = re.match(r"^\s*([A-Za-z0-9_.\-]+)", req)
    return m.group(1) if m else ""


def get_distribution_requires(dist_name: str) -> Set[str]:
    try:
        dist = importlib_metadata.distribution(dist_name)
    except importlib_metadata.PackageNotFoundError:
        return set()
    reqs = set()
    for r in (dist.requires or []):
        base = parse_requirement(r)
        if base:
            reqs.add(base)
    return reqs


def get_recursive_deps(root_dist: str, max_depth: int) -> Set[str]:
    seen = set()
    frontier = {root_dist}
    depth = 0
    while frontier and depth <= max_depth:
        next_frontier = set()
        for d in frontier:
            if d in seen:
                continue
            seen.add(d)
            next_frontier.update(get_distribution_requires(d))
        frontier = next_frontier
        depth += 1
    return seen


def project_to_import_name(project: str) -> str:
    proj_norm = normalize_project_name(project)
    for k, v in KNOWN_IMPORT_NAME_OVERRIDES.items():
        if normalize_project_name(k) == proj_norm:
            return v
    return project.replace("-", "_")


def is_importable(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except Exception:
        return False


def any_matches(patterns: List[str], text: str) -> bool:
    return any(re.search(p, text) for p in patterns)


def resolve_modules(projects: Iterable[str]) -> Set[str]:
    mods = set()
    for proj in sorted(set(projects)):
        mod = project_to_import_name(proj)
        if is_importable(mod):
            mods.add(mod)
        else:
            # Allow a dotted import override in overrides
            if "." in mod and is_importable(mod.split(".")[0]):
                mods.add(mod)
    return mods


def ensure_pydoc_markdown_on_path() -> str:
    # Find the console script
    from shutil import which
    exe = which("pydoc-markdown")
    if not exe:
        print("pydoc-markdown not found on PATH. Install with:", file=sys.stderr)
        print("  python -m pip install pydoc-markdown", file=sys.stderr)
        sys.exit(1)
    return exe


def render_module_to_md(pydoc_md_exe: str, module: str, render_toc: bool = True) -> str:
    """
    Run: pydoc-markdown -m MODULE [--render-toc]
    Capture stdout and return the markdown text.
    """
    cmd = [pydoc_md_exe, "-m", module]
    if render_toc:
        cmd.append("--render-toc")
    # As per official docs, -m renders to stdout:
    # https://niklasrosenstein.github.io/pydoc-markdown/usage/cli-and-api/
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"pydoc-markdown failed for {module}:\n{proc.stderr.strip()}")
    return proc.stdout


def main():
    ap = argparse.ArgumentParser(description="Generate Markdown for a package and its installed deps using pydoc-markdown.")
    ap.add_argument("--package", required=True, help="Root PyPI distribution/package name (e.g., docling)")
    ap.add_argument("--max-depth", type=int, default=2, help="Dependency traversal depth (default: 2)")
    ap.add_argument("--out-dir", default="pkg_api_md", help="Output directory for Markdown files")
    ap.add_argument("--include-heavy", action="store_true", help="Include heavy modules (torch, cv2, onnxruntime, etc.)")
    ap.add_argument("--no-toc", action="store_true", help="Do not render table of contents")
    ap.add_argument("--extra-mod", action="append", default=[], help="Additional module names to include (can repeat)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    root_proj = normalize_project_name(args.package)

    # Collect recursive dependencies (by distribution/project name)
    deps = get_recursive_deps(root_proj, max_depth=args.max_depth)
    projects = set(deps) | {root_proj}

    # Resolve to importable top-level module names
    modules = resolve_modules(projects)

    # Always try to include the root import name even if import check failed
    root_import = project_to_import_name(root_proj)
    modules.add(root_import)

    # Add any user-specified modules
    modules |= set(args.extra_mod)

    # Filter out heavy modules unless requested
    if not args.include_heavy:
        modules = {m for m in modules if not any_matches(DEFAULT_HEAVY_MODULE_PATTERNS, m)}

    # Remove clearly non-importable now (e.g., after adding root)
    modules = {m for m in modules if is_importable(m)}

    if not modules:
        print("No importable modules resolved. Aborting.", file=sys.stderr)
        sys.exit(2)

    print("Modules to document:")
    for m in sorted(modules):
        print(f"  - {m}")

    exe = ensure_pydoc_markdown_on_path()

    failures = []
    successes = 0

    for module in sorted(modules):
        try:
            md = render_module_to_md(exe, module, render_toc=not args.no_toc)
        except Exception as e:
            failures.append((module, str(e)))
            continue

        # Sanitize filename: module -> module.md
        fname = module.replace("/", ".") + ".md"
        out_path = out_dir / fname
        out_path.write_text(md, encoding="utf-8")
        successes += 1
        print(f"Wrote {out_path}")

    print(f"\nDone. Wrote {successes} Markdown files to: {out_dir}")
    if failures:
        print("\nSome modules failed to render:", file=sys.stderr)
        for mod, err in failures:
            print(f"  - {mod}: {err.splitlines()[-1]}", file=sys.stderr)
        print("Tip: Re-run with --include-heavy or add --extra-mod for specific modules if needed.", file=sys.stderr)


if __name__ == "__main__":
    main()