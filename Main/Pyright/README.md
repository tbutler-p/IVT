# Pyright Export Workflow

This directory stores Pyright artefacts for Docling and all runtimes that ship
with the active virtual environment.

## Prerequisites
- Activate the project virtual environment: `source .venv/bin/activate`
- Ensure Pyright is installed in that environment (`pip install pyright`)
- Install/upgrade the target packages (`pip install -r requirements.txt`)

## Regenerating stubs and symbol catalogs
1. Produce fresh stubs and dependency manifest:
   ```bash
   python Main/Tools/generate_pyright_assets.py --package docling
   ```
   - Creates per-module stub trees under `Main/Pyright/<import-name>`
   - Writes the processed distribution/module mapping to `Main/Pyright/packages.json`
2. Build the JSON symbol catalog for every listed package:
   ```bash
   python Main/Tools/generate_symbol_catalog.py
   ```
   - Traverses the stub trees
   - Writes `Main/Pyright/<distribution>/<distribution>.json`
   - Populates each JSON file with all public modules, classes, functions,
     variables, enums, typed dicts, protocols, and type aliases discovered in
     the stubs

## Adding new packages
- Install the package in `.venv`
- Re-run the steps above; `generate_pyright_assets.py` automatically includes all
  importable runtime dependencies for `docling`
- To target a different root distribution, pass `--package <name>`

## JSON structure
Each `<distribution>.json` follows this schema:
```json
{
  "package": "docling",
  "version": "2.61.1",
  "modules": [
    {
      "name": "docling.pipeline.simple_pipeline",
      "path": "pipeline/simple_pipeline.pyi",
      "docstring": "...",
      "classes": [...],
      "enums": [...],
      "typedDicts": [...],
      "protocols": [...],
      "functions": [...],
      "variables": [...],
      "typeAliases": [...]
    }
  ]
}
```
- Each `classes[...]` entry captures base classes, decorators, and public
  members (class vars, attributes, methods with overloads, etc.)
- Function overloads list positional/keyword parameters, type annotations,
  defaults, return types, and decorators
- Variables retain any declared annotations and literal values when present

## Verification
- Run `pyright -p .` from the repository root to validate configuration
- Spot-check JSON output for expected APIs, e.g. open
  `Main/Pyright/docling/docling.json` and ensure signature metadata is present

