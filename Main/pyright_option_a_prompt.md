
# Pyright Option A Setup Prompt

## Goal
- Configure Pyright in this workspace to:
  1) Generate a complete, consolidated type stub file (.pyi) per package.
  2) Extract a comprehensive JSON catalog of public symbols per package (modules, classes, functions, attributes, enums, literals, overloads, etc.).
- Output layout (VS Code screenshot shows IVT/Main/Pyright exists):
  - Main/Pyright/<PackageName>/<PackageName>.pyi
  - Main/Pyright/<PackageName>/<PackageName>.json
- Apply this to:
  - docling (folder Main/Pyright/Docling)
  - Every runtime dependency of docling (e.g., huggingface_hub ⇒ Main/Pyright/huggingface_hub), and any other packages I add in the future.

## Authoritative references you must align with
- Pyright README (overview, CLI, and project basics): [GitHub: microsoft/pyright](https://github.com/microsoft/pyright?tab=readme-ov-file)
- Pyright docs home and command-line usage: [Pyright Docs Home](https://microsoft.github.io/pyright/#/) and [Pyright Command-Line](https://microsoft.github.io/pyright/#/command-line)
- Pyright type stub generation guidance: “pyright --createstub [import-name]” in Pyright docs (see Type Stubs page): [Type stubs docs in repo](https://github.com/microsoft/pyright/blob/main/docs/type-stubs.md)

## High-level approach
- Use Pyright as both:
  - CLI: to generate .pyi stubs (per Pyright’s documented --createstub flow).
  - Language Server (LSP): to enumerate symbols and derive structured JSON for each package using standard LSP requests (workspace/symbol, textDocument/documentSymbol, etc.), based on Pyright’s language server.
- Ensure Pyright analyzes the same environment VS Code uses (venv) so imports resolve correctly.
- For each package:
  - Generate initial tree of .pyi stubs with `pyright --createstub <import-name>`.
  - Consolidate that tree into a single package-level .pyi file (`<PackageName>.pyi`) that preserves public API. Keep the original generated tree in a temp area during consolidation.
  - Query the Pyright language server for all exported/public symbols for that package and write them into `<PackageName>.json` using the schema defined below.
  - Place both files in `Main/Pyright/<PackageName>`.

## Workspace assumptions
- Project root: the repository root “IVT”.
- Python virtual environment: `IVT/.venv` (if different, detect and use the current active venv).
- The folder structure includes: `IVT/Main/Pyright` (exists from the screenshot).

## Step-by-step tasks

### 1) Install Pyright and confirm environment
- Install Pyright. Either of these is acceptable (pick one and stick to it):
  - npm: `npm i -g pyright`
  - pip: `pip install pyright`
- Verify install: `pyright --version`
- (Optional) Install the VS Code extension for Pyright for local validation: “Pyright” extension (ms-pyright.pyright) referenced on [Pyright Docs Home](https://microsoft.github.io/pyright/#/).
- Confirm active Python interpreter is the project’s virtual environment (`IVT/.venv`). Ensure packages like `docling` are installed in this venv.

### 2) Create a project-level `pyrightconfig.json` at `IVT` (repo root)
- The config must align with Pyright docs; use these fields (adjust paths for OS):
  - `"include"`: `["Main"]` to scope analysis to the Main folder.
  - `"pythonVersion"`: match the local interpreter (e.g., `"3.13"`).
  - `"venvPath"`: `"./"` (the directory that contains `.venv`).
  - `"venv"`: `".venv"`.
  - `"extraPaths"`: add the site-packages for `IVT/.venv` so Pyright can resolve installed packages. Compute the exact path dynamically.
  - `"typeCheckingMode"`: `"basic"` (or `"strict"` if desired).
  - `"stubPath"`: `"Main/Pyright"` so `pyright --createstub` writes under `Main/Pyright` by default.
- Validate the config by running `pyright -p .` at `IVT`. If you see “No configuration file found”, fix path or run from `IVT`. If you see “stubPath ... is not a valid directory,” ensure the folder exists.

References: Pyright configuration and CLI are described in [Pyright README](https://github.com/microsoft/pyright?tab=readme-ov-file) and [Pyright Docs](https://microsoft.github.io/pyright/#/).

### 3) Enumerate target packages
- Start with:
  - `docling` (import name: `docling`)
- Determine `docling`’s runtime dependencies (installed in the active venv). Use the package metadata to get importable “top-level names” (import names can differ from distribution names). Record the import name(s) for each dependency you will generate.
- For each dependency (e.g., `huggingface_hub` ⇒ import name `huggingface_hub`), include it in the processing list.

### 4) For each package, create a dedicated output folder
- Create folder: `Main/Pyright/<PackageName>`
  - Example: `Main/Pyright/Docling`
  - For dependencies: `Main/Pyright/huggingface_hub`, etc.

### 5) Generate stubs using Pyright’s official method
- Important: This step must follow `pyright --createstub [import-name]`, as documented in [Type stubs page](https://github.com/microsoft/pyright/blob/main/docs/type-stubs.md) and referenced by the command-line docs ([Docs Home/CLI](https://microsoft.github.io/pyright/#/command-line)).
- From `IVT` (project root so pyright picks up `pyrightconfig.json`):
  - `pyright --createstub <import-name>`
    - This generates a tree of `.pyi` files under the configured `stubPath` (`Main/Pyright`) using the import-name path (e.g., `Main/Pyright/docling/... .pyi`).
- Move/organize results:
  - Keep the generated tree temporarily in a staging location under `Main/Pyright/_staging/<PackageName>` so you can consolidate into a single file cleanly without losing detail. Then you will write the single consolidated stub into `Main/Pyright/<PackageName>/<PackageName>.pyi`.

Notes
- The docs explicitly say type stubs are generated within the configured project and written to the stub path. See [Type stubs docs](https://github.com/microsoft/pyright/blob/main/docs/type-stubs.md): “Then type ‘pyright --createstub [import-name]’.”
- If imports fail, ensure the venv is correctly set via `venvPath`/`venv` and that site-packages is discoverable via `extraPaths`.

### 6) Consolidate the generated stub tree into a single `.pyi` per package
- Goal: Produce a single package-level `.pyi` that preserves the public API surface.
- Consolidation rules:
  - The output file must be named `<PackageName>.pyi` and live in `Main/Pyright/<PackageName>`.
  - Prefer explicit re-exports over star-imports. Provide module-qualified exports for clarity when feasible.
  - The consolidated stub must capture:
    - All public modules (top-level symbols exposed by `__init__`), public classes, functions, variables, `TypedDict`s, `Protocol`s, `Enum`s, `Literal`s, and overloads.
    - Widely used private-but-effectively-public symbols can be included if they’re commonly imported by users; otherwise omit private names with a single leading underscore.
  - If the package is a namespace across multiple top-level import names, merge their public APIs in the single file with separate module sections or comments.
- Keep the original machine-generated stubs under `Main/Pyright/_staging` for traceability until we sign off.

### 7) Start the Pyright language server (LSP) and enumerate symbols to build JSON
- Use the Pyright language server binary (`pyright-langserver`) that ships with Pyright. Launch it in stdio mode:
  - `pyright-langserver --stdio`
- Implement a small LSP client process that:
  - Sends `initialize` and `initialized` requests.
  - Ensures server’s workspace settings reflect `pyrightconfig.json` (rootUri points to `IVT`).
  - For the target package:
    - Enumerates top-level modules in the package (including submodules discovered from the installed package path).
    - Opens each module (either by providing `textDocument/didOpen` for the source or stub the server sees) and requests symbols with `textDocument/documentSymbol`.
    - Also use `workspace/symbol` queries (e.g., by package prefix) to catch cross-file exports if needed.
  - Traverses returned structures to collect a canonical symbol graph:
    - Modules with children (classes, functions, variables).
    - For classes: base classes, class attributes, instance attributes if resolvable, methods (with overloads and signatures).
    - For functions/methods: parameters (names, kinds, type annotations), return type, decorators, overloads.
    - For variables/constants: inferred or annotated types; include `Literal` values and `Final` constants when available.
    - Enums: members and values.
    - TypedDict/Protocol/TypeAlias: names and fields.
  - Respect the package’s public surface:
    - Prefer names exported by `__all__` if present; otherwise include non-underscore names at the package root.
    - Resolve re-exports (`from X import Y as Z`) so the JSON reflects the user-importable path.

#### JSON schema (use this shape, versioned):
```json
{
  "schemaVersion": "1.0",
  "package": "<import-name>",
  "distribution": "<pip_distribution_name>",
  "version": "<installed_version>",
  "rootModule": "<import-name>",
  "modules": [
    {
      "qname": "docling",
      "file": "<path or stub>",
      "exports": ["A", "B"],
      "classes": [
        {
          "name": "Document",
          "bases": ["BaseDoc"],
          "decorators": [],
          "members": {
            "classVars": [{"name": "X", "type": "int|Literal[...]", "value": "..."}],
            "attributes": [{"name": "y", "type": "str|None"}],
            "methods": [
              {
                "name": "parse",
                "overloads": [
                  {
                    "params": [{"name": "path", "type": "str"}],
                    "return": "ParsedDoc",
                    "decorators": []
                  }
                ]
              }
            ],
            "enums": [{"name": "Mode", "members": [{"name": "FAST", "value": 1}]}],
            "typedDicts": [{"name": "Cfg", "fields": [{"name":"a","type":"int","required":true}], "total": true}],
            "protocols": [{"name": "Readable", "members": ["read"]}],
            "typeAliases": [{"name": "PathLike", "target": "str|os.PathLike[str]"}]
          }
        }
      ],
      "functions": [
        {
          "name": "load",
          "overloads": [
            {"params": [{"name":"p", "type":"str"}], "return":"Document"}
          ],
          "decorators": []
        }
      ],
      "variables": [{"name":"__version__", "type":"str", "value":"..."}]
    }
  ]
}
```

### 8) Write outputs per package
- For each package P:
  - `Main/Pyright/P/P.json`: the symbol catalog using the schema above.
  - `Main/Pyright/P/P.pyi`: the consolidated stub produced in step 6.
- Ensure `P.json` lists the exact package/distribution version used to generate it.
- Keep line endings LF and ensure UTF-8 encoding.

### 9) Apply to `docling` and its dependencies
- Create `Main/Pyright/Docling/Docling.pyi` and `Main/Pyright/Docling/Docling.json` using the above process.
- Detect `docling`’s runtime dependencies (the ones actually importable in the venv) and produce corresponding subfolders and files, e.g.:
  - `Main/Pyright/huggingface_hub/huggingface_hub.pyi`
  - `Main/Pyright/huggingface_hub/huggingface_hub.json`
- Repeat for all dependencies discovered.

### 10) Verification and acceptance checks
- Validate stub generation step adheres to Pyright docs (“`pyright --createstub [import-name]`”), see [Type stubs docs](https://github.com/microsoft/pyright/blob/main/docs/type-stubs.md) and [CLI docs](https://microsoft.github.io/pyright/#/command-line).
- Run `pyright -p .` to confirm no fatal configuration or import resolution issues. The README and docs emphasize running within a configured project; ensure that’s satisfied: [Pyright README](https://github.com/microsoft/pyright?tab=readme-ov-file), [Docs Home](https://microsoft.github.io/pyright/#/).
- Spot-check that public APIs present in `<PackageName>.pyi` also appear in `<PackageName>.json` (names and signatures are coherent).
- Confirm that a typical user import (e.g., `from docling import Document`) is represented in both the `.pyi` and JSON.

### 11) Operational notes and pitfalls
- Import name vs distribution name: Always resolve the importable top-level module name (e.g., distribution “Pillow” ⇒ import name “PIL”). Use the import name with `--createstub`.
- `stubPath` behavior: Pyright writes stubs under the configured `stubPath`. We’re pointing `stubPath` to `"Main/Pyright"` so the generated tree appears there. We then consolidate and move to `Main/Pyright/<PackageName>/<PackageName>.pyi`.
- Private names: Prefer omitting single-underscore members unless they are re-exported publicly or widely used by the public API.
- `__all__`: If present, treat it as the authoritative export list for JSON and `.pyi` consolidation.
- Platform/version gates: If code uses platform checks or version-dependent imports, ensure `pythonVersion` and `pythonPlatform` settings reflect a realistic environment for our project so Pyright’s analysis matches runtime.
- Stubs completeness: You may run `pyright --verifytypes <package>` to get type completeness information (documented among CLI options) which can help evaluate the generated stubs’ coverage, see referenced CLI docs from [Pyright Docs](https://microsoft.github.io/pyright/#/command-line).
- Existing local stubs: If any custom stubs are already present in `Main/Pyright`, Pyright may prefer them in analysis. This is expected.

### 12) Final deliverables
- `pyrightconfig.json` at `IVT` root configured as above.
- For each package (docling and each of its dependencies):
  - `Main/Pyright/<PackageName>/<PackageName>.pyi`
  - `Main/Pyright/<PackageName>/<PackageName>.json`
- A short `README.md` in `Main/Pyright` that explains:
  - How to regenerate for a package (commands, environment assumptions).
  - How to add a new package to the set.
  - The JSON schema and intended use.

## Troubleshooting checklist
- “No configuration file found” or environment mismatch:
  - Run `pyright` from `IVT` root where `pyrightconfig.json` lives.
  - Verify `venvPath`/`venv` and `extraPaths` point to the active venv’s site-packages.
- “Cannot import package” during `--createstub`:
  - Ensure the package is installed in `IVT/.venv`.
  - Confirm the import name is correct (try `python -c "import <name>"`).
- Empty or partial symbols in JSON:
  - Ensure you opened the right documents in the LSP client and used `documentSymbol` and/or `workspace/symbol` with appropriate queries.
  - If pyright can’t resolve a module, add its path to `extraPaths`.
- Generated stub tree not appearing under `Main/Pyright`:
  - Confirm `stubPath` in `pyrightconfig.json` is `"Main/Pyright"` and the command is executed from `IVT` root as per the docs.

## Citations
- Overview, CLI and usage: [Pyright README](https://github.com/microsoft/pyright?tab=readme-ov-file)
- Docs site and CLI reference: [Pyright Docs](https://microsoft.github.io/pyright/#/) and [Command-Line](https://microsoft.github.io/pyright/#/command-line)
- Official guidance on generating stubs with `--createstub`: [Type Stubs Doc](https://github.com/microsoft/pyright/blob/main/docs/type-stubs.md)
