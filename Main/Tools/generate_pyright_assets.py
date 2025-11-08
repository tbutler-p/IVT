#!/usr/bin/env python3
"""Automation helpers for Pyright Option A workflow.

This script discovers the runtime dependency graph for a given Python
distribution (default: ``docling``), resolves the importable top-level
modules, and invokes Pyright's ``--createstub`` command for each module.
The generated stub tree is relocated to ``Main/Pyright/<module>/_raw`` to
make room for subsequent consolidation steps handled elsewhere.

Example:
    python Main/Tools/generate_pyright_assets.py --package docling
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set

from packaging.markers import default_environment
from packaging.requirements import Requirement
from typing import Dict

try:
    from importlib import metadata as importlib_metadata
except ImportError:  # pragma: no cover
    import importlib_metadata  # type: ignore


DEFAULT_OVERRIDES: Dict[str, Sequence[str]] = {
    "beautifulsoup4": ["bs4"],
    "pillow": ["PIL"],
    "python-docx": ["docx"],
    "python-pptx": ["pptx"],
    "pypdfium2": ["pypdfium2", "pypdfium2_raw"],
}


@dataclass(frozen=True)
class PackageSpec:
    """Represents a distribution and its importable modules."""

    distribution: str
    modules: Sequence[str]


def normalize_dist_name(dist_name: str) -> str:
    """Return the canonical normalized distribution name."""

    return dist_name.lower().replace("_", "-")


def evaluate_requirement(req_str: str) -> Requirement:
    """Parse a requirement string into a :class:`Requirement` instance."""

    return Requirement(req_str)


def runtime_dependencies(root_dist: str) -> Set[str]:
    """Return direct runtime dependencies for ``root_dist`` in this env.

    Environment markers are evaluated against the current interpreter
    (e.g., platform == 'darwin', python_version == '3.13').
    """

    try:
        distribution = importlib_metadata.distribution(root_dist)
    except importlib_metadata.PackageNotFoundError as exc:
        raise SystemExit(f"Distribution '{root_dist}' is not installed: {exc}") from exc

    env: Dict[str, str] = {str(k): str(v) for k, v in default_environment().items()}
    env["extra"] = ""

    deps: Set[str] = set()
    for requirement_str in distribution.requires or []:
        requirement = evaluate_requirement(requirement_str)
        if requirement.marker and not requirement.marker.evaluate(env):
            continue
        deps.add(requirement.name)
    return deps


def importable_modules(dist_name: str, overrides: Dict[str, Sequence[str]]) -> Sequence[str]:
    """Resolve importable modules for a distribution.

    Args:
        dist_name: PyPI distribution name.
        overrides: Explicit mapping overrides for known mismatches.
    """

    normalized = normalize_dist_name(dist_name)
    if normalized in overrides:
        candidates = overrides[normalized]
    else:
        candidates = []
        try:
            text = importlib_metadata.distribution(dist_name).read_text("top_level.txt")
            if text:
                candidates = [line.strip() for line in text.splitlines() if line.strip()]
        except (FileNotFoundError, importlib_metadata.PackageNotFoundError):
            candidates = []
        if not candidates:
            candidates = [dist_name.replace("-", "_")]

    valid: List[str] = []
    for candidate in candidates:
        try:
            __import__(candidate)
        except Exception:
            continue
        valid.append(candidate)
    return valid


def resolve_package_specs(root_dist: str) -> List[PackageSpec]:
    """Collect package specs for ``root_dist`` and its runtime dependencies."""

    distributions = runtime_dependencies(root_dist) | {root_dist}
    specs: List[PackageSpec] = []
    for dist in sorted(distributions):
        modules = importable_modules(dist, DEFAULT_OVERRIDES)
        if not modules:
            continue
        specs.append(PackageSpec(distribution=dist, modules=modules))
    return specs


def ensure_stub_root(stub_root: Path) -> None:
    """Ensure the stub output directory exists."""

    stub_root.mkdir(parents=True, exist_ok=True)


def run_pyright_createstub(module: str, cwd: Path) -> None:
    """Invoke ``pyright --createstub module`` within the given directory."""

    result = subprocess.run(
        ["pyright", "--createstub", module],
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"pyright --createstub {module} failed with exit code {result.returncode}:\n"
            f"{result.stderr.strip()}"
        )


def relocate_raw_stubs(package_dir: Path) -> None:
    """Move freshly generated stub contents into ``_raw``."""

    raw_dir = package_dir / "_raw"
    if raw_dir.exists():
        shutil.rmtree(raw_dir)
    raw_dir.mkdir()

    for entry in list(package_dir.iterdir()):
        if entry.name == "_raw":
            continue
        shutil.move(str(entry), raw_dir / entry.name)


def generate_stubs(specs: Iterable[PackageSpec], stub_root: Path) -> None:
    """Generate Pyright stubs for each module described by ``specs``."""

    for spec in specs:
        for module in spec.modules:
            run_pyright_createstub(module, cwd=Path.cwd())
            package_dir = stub_root / module
            relocate_raw_stubs(package_dir)


def write_manifest(specs: Sequence[PackageSpec], manifest_path: Path) -> None:
    """Persist the generated package metadata to ``manifest_path``."""

    payload = {
        "root": manifest_path.parent.name,
        "packages": [asdict(spec) for spec in specs],
    }
    manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--package",
        default="docling",
        help="Root distribution to process (default: docling).",
    )
    parser.add_argument(
        "--stub-root",
        default="Main/Pyright",
        help="Directory where Pyright stub trees are generated.",
    )
    parser.add_argument(
        "--manifest",
        default="Main/Pyright/packages.json",
        help="Path to write the package manifest JSON.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Script entry point."""

    args = parse_args(argv or sys.argv[1:])
    stub_root = Path(args.stub_root).resolve()
    ensure_stub_root(stub_root)

    specs = resolve_package_specs(args.package)
    if not specs:
        raise SystemExit(f"No importable modules resolved for package '{args.package}'.")

    print(f"[info] Generating stubs for {len(specs)} distributions.")
    generate_stubs(specs, stub_root=stub_root)

    manifest_path = Path(args.manifest).resolve()
    write_manifest(specs, manifest_path)
    print(f"[info] Wrote manifest to {manifest_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
