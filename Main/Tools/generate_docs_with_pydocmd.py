#!/usr/bin/env python3
"""
Generate Markdown API docs for 'docling' and all of its installed dependencies using pydoc-markdown.

- Discovers dependencies from the installed distribution metadata (importlib.metadata).
- Maps project names to top-level importable modules.
- Writes a pydoc-markdown.yml and runs pydoc-markdown to emit Markdown.
- Output directory: ./_api_docs/out

Prereqs:
  python -m pip install pydoc-markdown

Example:
  python generate_docs_with_pydocmd.py --package docling
  python generate_docs_with_pydocmd.py --package docling --source-path /path/to/docling
"""

import argparse
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

try:
    # Python 3.8+
    from importlib import metadata as importlib_metadata
except ImportError:
    import importlib_metadata  # type: ignore


# Some known PyPI-name -> import-name mismatches or multi-import packages.
# Extend as needed.
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
    "tenacity": "tenacity",  # example of identity mapping kept for clarity
}


def normalize_project_name(name: str) -> str:
    """PEP 503 normalization (PyPI simple API)."""
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirement(req: str) -> str:
    """
    Extract the base project name from a requirement string (ignoring version specs and markers).
    Examples:
      'foo>=1.0; python_version>="3.9"' -> 'foo'
      'bar[extra1,extra2]==2.3' -> 'bar'
    """
    # Split off environment markers
    req = req.split(";")[0].strip()
    # Split off version spec and extras
    # Patterns like: name[extras]==1.2.3, >=, <=, ~=, etc.
    m = re.match(r"^\s*([A-Za-z0-9_.\-]+)", req)
    if not m:
        return ""
    return m.group(1)


def project_to_import_name(project: str) -> str:
    """
    Best-effort mapping from PyPI project name to top-level import name.
    """
    proj_norm = normalize_project_name(project)
    # Known overrides first
    for k, v in KNOWN_IMPORT_NAME_OVERRIDES.items():
        if normalize_project_name(k) == proj_norm:
            return v

    # Default heuristic: replace '-' with '_' and keep dots/underscores
    candidate = project.replace("-", "_")
    return candidate


def is_importable(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except Exception:
        return False


def resolve_top_level_modules(projects):
    """
    Convert a set of PyPI project names to a deduplicated set of importable top-level module names.
    """
    modules = set()
    for proj in sorted(projects):
        mod = project_to_import_name(proj)
        # Some packages expose multiple top-level packages; try the basic one first.
        # If that fails, we could attempt to inspect dist-files (top_level.txt), but not all dists ship it.
        if is_importable(mod):
            modules.add(mod)
        else:
            # Try a fallback: check common alternates (rarely necessary).
            alternates = []
            # Heuristic alternates: dotted vs underscore variants
            if "_" in mod:
                alternates.append(mod.replace("_", ""))
            if "-" in proj:
                alternates.append(proj)  # sometimes works if hyphenated module exists (rare)

            for alt in alternates:
                if is_importable(alt):
                    modules.add(alt)
                    break
            else:
                # Skip non-importable; pydoc-markdown would error on it otherwise
                pass
    return modules


def get_distribution_requirements(dist_name: str):
    """
    Get immediate install requires from installed dist metadata (no recursive resolution here).
    """
    try:
        dist = importlib_metadata.distribution(dist_name)
    except importlib_metadata.PackageNotFoundError:
        return set()

    reqs = set()
    for r in dist.requires or []:
        base = parse_requirement(r)
        if base:
            reqs.add(base)
    return reqs


def get_recursive_runtime_dependencies(root_dist: str, max_depth: int = 3):
    """
    Walk dependency graph to collect runtime dependencies up to a small depth to avoid explosion.
    """
    seen = set()
    frontier = {root_dist}
    depth = 0

    while frontier and depth <= max_depth:
        next_frontier = set()
        for dist in frontier:
            if dist in seen:
                continue
            seen.add(dist)
            for dep in get_distribution_requirements(dist):
                # ignore extras/dev/test-only deps if not installed
                next_frontier.add(dep)
        frontier = next_frontier
        depth += 1

    return seen


def ensure_pydoc_markdown_installed():
    try:
        import pydoc_markdown  # noqa: F401
    except Exception:
        print("pydoc-markdown is not installed in this interpreter. Install it with:", file=sys.stderr)
        print("  python -m pip install pydoc-markdown", file=sys.stderr)
        sys.exit(1)


def write_pydocmd_yaml(modules, out_dir: Path, yml_path: Path):
    """
    Create a minimal pydoc-markdown config that:
    - loads all top-level modules provided
    - renders Markdown into out_dir
    """
    # We’ll use the PythonLoader with modules list.
    # Tip: You can switch to Google/Numpy style processors by adding processors.
    config = f"""\
loaders:
  - type: python
    modules:
{''.join([f"      - {m}\n" for m in sorted(modules)])}
    
processors:
  - type: smart  # autolinks, crossrefs, etc.

renderers:
  - type: markdown
    output_directory: "{out_dir.as_posix()}"
"""
    yml_path.write_text(config, encoding="utf-8")


def run_pydoc_markdown(yml_path: Path):
    cmd = f'python -m pydoc_markdown --build --config "{yml_path.as_posix()}"'
    print(f"Running: {cmd}")
    try:
        subprocess.check_call(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        print("pydoc-markdown failed. You can inspect the config and try locally:", file=sys.stderr)
        print(f"  {cmd}", file=sys.stderr)
        sys.exit(e.returncode)


def main():
    parser = argparse.ArgumentParser(description="Generate API docs for docling and its dependencies using pydoc-markdown.")
    parser.add_argument("--package", required=True, help="Root package/distribution name (e.g., docling)")
    parser.add_argument(
        "--source-path",
        default=None,
        help="Optional path to local source checkout of the package (not strictly required)."
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Max dependency graph depth to traverse (default: 2)."
    )
    parser.add_argument(
        "--out-root",
        default="_api_docs",
        help="Directory where config and output will be created (default: _api_docs)"
    )
    args = parser.parse_args()

    ensure_pydoc_markdown_installed()

    out_root = Path(args.out_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    out_dir = out_root / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    yml_path = out_root / "pydoc-markdown.yml"

    # If given a source path, prepend it to sys.path so pydoc-markdown can import it if not installed editable.
    if args.source_path:
        src = Path(args.source_path).resolve()
        if not src.exists():
            print(f"--source-path not found: {src}", file=sys.stderr)
            sys.exit(1)
        # Prepend to PYTHONPATH for subprocess invocation
        os.environ["PYTHONPATH"] = f"{src}{os.pathsep}{os.environ.get('PYTHONPATH','')}"

    root_dist = normalize_project_name(args.package)

    # Ensure root package is importable (from site-packages or source-path)
    root_import_name = project_to_import_name(root_dist)
    if not is_importable(root_import_name):
        print(f"Warning: Root package '{args.package}' (import name '{root_import_name}') is not importable in this interpreter.", file=sys.stderr)
        print("Proceeding anyway; pydoc-markdown may fail to import it.", file=sys.stderr)

    # Discover dependencies from installed metadata. This reflects what's actually available to import.
    # We collect the recursive set including the root itself.
    graph = get_recursive_runtime_dependencies(root_dist, max_depth=args.max_depth)

    # Build the set of module import names to document: root + its deps
    projects = set(graph)
    projects.add(root_dist)

    modules = resolve_top_level_modules(projects)
    # Always ensure root is included even if import check failed; pydoc-markdown might still succeed if source-path is set.
    modules.add(root_import_name)

    if not modules:
        print("No importable modules resolved. Aborting.", file=sys.stderr)
        sys.exit(2)

    print("Will document these top-level modules:")
    for m in sorted(modules):
        print(f"  - {m}")

    write_pydocmd_yaml(modules, out_dir=out_dir, yml_path=yml_path)
    print(f"Wrote config: {yml_path}")

    run_pydoc_markdown(yml_path)
    print(f"Done. Markdown files are in: {out_dir}")


if __name__ == "__main__":
    main()