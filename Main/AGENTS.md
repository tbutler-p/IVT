# Main Agents Guide

## Pyright Reference Assets
- Review the per-module `.pyi` stubs and JSON symbol catalogs under `Main/Pyright` to understand public APIs of installed packages.
- Each distribution folder contains searchable signatures, docstrings, and type metadata that mirror the runtime environment (`.venv`).
- Prefer these artifacts when navigating unfamiliar dependencies before diving into external docs.

## Updating Documentation When Packages Change
- After installing or upgrading packages in `.venv`, regenerate the Pyright assets to keep the documentation in sync:
  1. `python Main/Tools/generate_pyright_assets.py --package docling`
  2. `python Main/Tools/generate_symbol_catalog.py`
- Commit the refreshed stubs and JSON files so future agents have an up-to-date view of the dependency surface area.
