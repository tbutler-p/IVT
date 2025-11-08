# Table of Contents

* [black](#black)
  * [read\_pyproject\_toml](#black.read_pyproject_toml)
  * [target\_version\_option\_callback](#black.target_version_option_callback)
  * [enable\_unstable\_feature\_callback](#black.enable_unstable_feature_callback)
  * [re\_compile\_maybe\_verbose](#black.re_compile_maybe_verbose)
  * [main](#black.main)
  * [get\_sources](#black.get_sources)
  * [path\_empty](#black.path_empty)
  * [reformat\_code](#black.reformat_code)
  * [reformat\_one](#black.reformat_one)
  * [format\_file\_in\_place](#black.format_file_in_place)
  * [format\_stdin\_to\_stdout](#black.format_stdin_to_stdout)
  * [check\_stability\_and\_equivalence](#black.check_stability_and_equivalence)
  * [format\_file\_contents](#black.format_file_contents)
  * [format\_cell](#black.format_cell)
  * [validate\_metadata](#black.validate_metadata)
  * [format\_ipynb\_string](#black.format_ipynb_string)
  * [format\_str](#black.format_str)
  * [decode\_bytes](#black.decode_bytes)
  * [get\_features\_used](#black.get_features_used)
  * [detect\_target\_versions](#black.detect_target_versions)
  * [get\_future\_imports](#black.get_future_imports)
  * [assert\_equivalent](#black.assert_equivalent)
  * [assert\_stable](#black.assert_stable)
  * [nullcontext](#black.nullcontext)

<a id="black"></a>

# black

<a id="black.read_pyproject_toml"></a>

#### read\_pyproject\_toml

```python
def read_pyproject_toml(ctx: click.Context, param: click.Parameter,
                        value: Optional[str]) -> Optional[str]
```

Inject Black configuration from "pyproject.toml" into defaults in `ctx`.

Returns the path to a successfully found and read configuration file, None
otherwise.

<a id="black.target_version_option_callback"></a>

#### target\_version\_option\_callback

```python
def target_version_option_callback(c: click.Context, p: Union[click.Option,
                                                              click.Parameter],
                                   v: tuple[str, ...]) -> list[TargetVersion]
```

Compute the target versions from a --target-version flag.

This is its own function because mypy couldn't infer the type correctly
when it was a lambda, causing mypyc trouble.

<a id="black.enable_unstable_feature_callback"></a>

#### enable\_unstable\_feature\_callback

```python
def enable_unstable_feature_callback(c: click.Context,
                                     p: Union[click.Option, click.Parameter],
                                     v: tuple[str, ...]) -> list[Preview]
```

Compute the features from an --enable-unstable-feature flag.

<a id="black.re_compile_maybe_verbose"></a>

#### re\_compile\_maybe\_verbose

```python
def re_compile_maybe_verbose(regex: str) -> Pattern[str]
```

Compile a regular expression string in `regex`.

If it contains newlines, use verbose mode.

<a id="black.main"></a>

#### main

```python
@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    # While Click does set this field automatically using the docstring, mypyc
    # (annoyingly) strips 'em so we need to set it here too.
    help="The uncompromising code formatter.",
)
@click.option("-c",
              "--code",
              type=str,
              help="Format the code passed in as a string.")
@click.option(
    "-l",
    "--line-length",
    type=int,
    default=DEFAULT_LINE_LENGTH,
    help="How many characters per line to allow.",
    show_default=True,
)
@click.option(
    "-t",
    "--target-version",
    type=click.Choice([v.name.lower() for v in TargetVersion]),
    callback=target_version_option_callback,
    multiple=True,
    help=
    ("Python versions that should be supported by Black's output. You should"
     " include all versions that your code supports. By default, Black will infer"
     " target versions from the project metadata in pyproject.toml. If this does"
     " not yield conclusive results, Black will use per-file auto-detection."),
)
@click.option(
    "--pyi",
    is_flag=True,
    help=
    ("Format all input files like typing stubs regardless of file extension. This"
     " is useful when piping source on standard input."),
)
@click.option(
    "--ipynb",
    is_flag=True,
    help=
    ("Format all input files like Jupyter Notebooks regardless of file extension."
     " This is useful when piping source on standard input."),
)
@click.option(
    "--python-cell-magics",
    multiple=True,
    help=("When processing Jupyter Notebooks, add the given magic to the list"
          f" of known python-magics ({', '.join(sorted(PYTHON_CELL_MAGICS))})."
          " Useful for formatting cells with custom python magics."),
    default=[],
)
@click.option(
    "-x",
    "--skip-source-first-line",
    is_flag=True,
    help="Skip the first line of the source code.",
)
@click.option(
    "-S",
    "--skip-string-normalization",
    is_flag=True,
    help="Don't normalize string quotes or prefixes.",
)
@click.option(
    "-C",
    "--skip-magic-trailing-comma",
    is_flag=True,
    help="Don't use trailing commas as a reason to split lines.",
)
@click.option(
    "--preview",
    is_flag=True,
    help=
    ("Enable potentially disruptive style changes that may be added to Black's main"
     " functionality in the next major release."),
)
@click.option(
    "--unstable",
    is_flag=True,
    help=
    ("Enable potentially disruptive style changes that have known bugs or are not"
     " currently expected to make it into the stable style Black's next major"
     " release. Implies --preview."),
)
@click.option(
    "--enable-unstable-feature",
    type=click.Choice([v.name for v in Preview]),
    callback=enable_unstable_feature_callback,
    multiple=True,
    help=(
        "Enable specific features included in the `--unstable` style. Requires"
        " `--preview`. No compatibility guarantees are provided on the behavior"
        " or existence of any unstable features."),
)
@click.option(
    "--check",
    is_flag=True,
    help=
    ("Don't write the files back, just return the status. Return code 0 means"
     " nothing would change. Return code 1 means some files would be reformatted."
     " Return code 123 means there was an internal error."),
)
@click.option(
    "--diff",
    is_flag=True,
    help=
    ("Don't write the files back, just output a diff to indicate what changes"
     " Black would've made. They are printed to stdout so capturing them is simple."
     ),
)
@click.option(
    "--color/--no-color",
    is_flag=True,
    help=
    "Show (or do not show) colored diff. Only applies when --diff is given.",
)
@click.option(
    "--line-ranges",
    multiple=True,
    metavar="START-END",
    help=
    ("When specified, Black will try its best to only format these lines. This"
     " option can be specified multiple times, and a union of the lines will be"
     " formatted. Each range must be specified as two integers connected by a `-`:"
     " `<START>-<END>`. The `<START>` and `<END>` integer indices are 1-based and"
     " inclusive on both ends."),
    default=(),
)
@click.option(
    "--fast/--safe",
    is_flag=True,
    help=
    ("By default, Black performs an AST safety check after formatting your code."
     " The --fast flag turns off this check and the --safe flag explicitly enables"
     " it. [default: --safe]"),
)
@click.option(
    "--required-version",
    type=str,
    help=
    ("Require a specific version of Black to be running. This is useful for"
     " ensuring that all contributors to your project are using the same"
     " version, because different versions of Black may format code a little"
     " differently. This option can be set in a configuration file for consistent"
     " results across environments."),
)
@click.option(
    "--exclude",
    type=str,
    callback=validate_regex,
    help=
    ("A regular expression that matches files and directories that should be"
     " excluded on recursive searches. An empty value means no paths are excluded."
     " Use forward slashes for directories on all platforms (Windows, too)."
     " By default, Black also ignores all paths listed in .gitignore. Changing this"
     f" value will override all default exclusions. [default: {DEFAULT_EXCLUDES}]"
     ),
    show_default=False,
)
@click.option(
    "--extend-exclude",
    type=str,
    callback=validate_regex,
    help=
    ("Like --exclude, but adds additional files and directories on top of the"
     " default values instead of overriding them."),
)
@click.option(
    "--force-exclude",
    type=str,
    callback=validate_regex,
    help=
    ("Like --exclude, but files and directories matching this regex will be excluded"
     " even when they are passed explicitly as arguments. This is useful when"
     " invoking Black programmatically on changed files, such as in a pre-commit"
     " hook or editor plugin."),
)
@click.option(
    "--stdin-filename",
    type=str,
    is_eager=True,
    help=
    ("The name of the file when passing it through stdin. Useful to make sure Black"
     " will respect the --force-exclude option on some editors that rely on using"
     " stdin."),
)
@click.option(
    "--include",
    type=str,
    default=DEFAULT_INCLUDES,
    callback=validate_regex,
    help=
    ("A regular expression that matches files and directories that should be"
     " included on recursive searches. An empty value means all files are included"
     " regardless of the name. Use forward slashes for directories on all platforms"
     " (Windows, too). Overrides all exclusions, including from .gitignore and"
     " command line options."),
    show_default=True,
)
@click.option(
    "-W",
    "--workers",
    type=click.IntRange(min=1),
    default=None,
    help=
    ("When Black formats multiple files, it may use a process pool to speed up"
     " formatting. This option controls the number of parallel workers. This can"
     " also be specified via the BLACK_NUM_WORKERS environment variable. Defaults"
     " to the number of CPUs in the system."),
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help=
    ("Stop emitting all non-critical output. Error messages will still be emitted"
     " (which can silenced by 2>/dev/null)."),
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help=
    ("Emit messages about files that were not changed or were ignored due to"
     " exclusion patterns. If Black is using a configuration file, a message"
     " detailing which one it is using will be emitted."),
)
@click.version_option(
    version=__version__,
    message=
    (f"%(prog)s, %(version)s (compiled: {'yes' if COMPILED else 'no'})\n"
     f"Python ({platform.python_implementation()}) {platform.python_version()}"
     ),
)
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(exists=True,
                    file_okay=True,
                    dir_okay=True,
                    readable=True,
                    allow_dash=True),
    is_eager=True,
    metavar="SRC ...",
)
@click.option(
    "--config",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        allow_dash=False,
        path_type=str,
    ),
    is_eager=True,
    callback=read_pyproject_toml,
    help="Read configuration options from a configuration file.",
)
@click.pass_context
def main(ctx: click.Context, code: Optional[str], line_length: int,
         target_version: list[TargetVersion], check: bool, diff: bool,
         line_ranges: Sequence[str], color: bool, fast: bool, pyi: bool,
         ipynb: bool, python_cell_magics: Sequence[str],
         skip_source_first_line: bool, skip_string_normalization: bool,
         skip_magic_trailing_comma: bool, preview: bool, unstable: bool,
         enable_unstable_feature: list[Preview], quiet: bool, verbose: bool,
         required_version: Optional[str], include: Pattern[str],
         exclude: Optional[Pattern[str]],
         extend_exclude: Optional[Pattern[str]],
         force_exclude: Optional[Pattern[str]], stdin_filename: Optional[str],
         workers: Optional[int], src: tuple[str, ...],
         config: Optional[str]) -> None
```

The uncompromising code formatter.

<a id="black.get_sources"></a>

#### get\_sources

```python
def get_sources(*, root: Path, src: tuple[str,
                                          ...], quiet: bool, verbose: bool,
                include: Pattern[str], exclude: Optional[Pattern[str]],
                extend_exclude: Optional[Pattern[str]],
                force_exclude: Optional[Pattern[str]], report: "Report",
                stdin_filename: Optional[str]) -> set[Path]
```

Compute the set of files to be formatted.

<a id="black.path_empty"></a>

#### path\_empty

```python
def path_empty(src: Sized, msg: str, quiet: bool, verbose: bool,
               ctx: click.Context) -> None
```

Exit if there is no `src` provided for formatting

<a id="black.reformat_code"></a>

#### reformat\_code

```python
def reformat_code(content: str,
                  fast: bool,
                  write_back: WriteBack,
                  mode: Mode,
                  report: Report,
                  *,
                  lines: Collection[tuple[int, int]] = ()) -> None
```

Reformat and print out `content` without spawning child processes.
Similar to `reformat_one`, but for string content.

`fast`, `write_back`, and `mode` options are passed to
:func:`format_file_in_place` or :func:`format_stdin_to_stdout`.

<a id="black.reformat_one"></a>

#### reformat\_one

```python
@mypyc_attr(patchable=True)
def reformat_one(src: Path,
                 fast: bool,
                 write_back: WriteBack,
                 mode: Mode,
                 report: "Report",
                 *,
                 lines: Collection[tuple[int, int]] = ()) -> None
```

Reformat a single file under `src` without spawning child processes.

`fast`, `write_back`, and `mode` options are passed to
:func:`format_file_in_place` or :func:`format_stdin_to_stdout`.

<a id="black.format_file_in_place"></a>

#### format\_file\_in\_place

```python
def format_file_in_place(src: Path,
                         fast: bool,
                         mode: Mode,
                         write_back: WriteBack = WriteBack.NO,
                         lock: Any = None,
                         *,
                         lines: Collection[tuple[int, int]] = ()) -> bool
```

Format file under `src` path. Return True if changed.

If `write_back` is DIFF, write a diff to stdout. If it is YES, write reformatted
code to the file.
`mode` and `fast` options are passed to :func:`format_file_contents`.

<a id="black.format_stdin_to_stdout"></a>

#### format\_stdin\_to\_stdout

```python
def format_stdin_to_stdout(
    fast: bool,
    *,
    content: Optional[str] = None,
    write_back: WriteBack = WriteBack.NO,
    mode: Mode,
    lines: Collection[tuple[int, int]] = ()) -> bool
```

Format file on stdin. Return True if changed.

If content is None, it's read from sys.stdin.

If `write_back` is YES, write reformatted code back to stdout. If it is DIFF,
write a diff to stdout. The `mode` argument is passed to
:func:`format_file_contents`.

<a id="black.check_stability_and_equivalence"></a>

#### check\_stability\_and\_equivalence

```python
def check_stability_and_equivalence(
    src_contents: str,
    dst_contents: str,
    *,
    mode: Mode,
    lines: Collection[tuple[int, int]] = ()) -> None
```

Perform stability and equivalence checks.

Raise AssertionError if source and destination contents are not
equivalent, or if a second pass of the formatter would format the
content differently.

<a id="black.format_file_contents"></a>

#### format\_file\_contents

```python
def format_file_contents(
    src_contents: str,
    *,
    fast: bool,
    mode: Mode,
    lines: Collection[tuple[int, int]] = ()) -> FileContent
```

Reformat contents of a file and return new contents.

If `fast` is False, additionally confirm that the reformatted code is
valid by calling :func:`assert_equivalent` and :func:`assert_stable` on it.
`mode` is passed to :func:`format_str`.

<a id="black.format_cell"></a>

#### format\_cell

```python
def format_cell(src: str, *, fast: bool, mode: Mode) -> str
```

Format code in given cell of Jupyter notebook.

General idea is:

  - if cell has trailing semicolon, remove it;
  - if cell has IPython magics, mask them;
  - format cell;
  - reinstate IPython magics;
  - reinstate trailing semicolon (if originally present);
  - strip trailing newlines.

Cells with syntax errors will not be processed, as they
could potentially be automagics or multi-line magics, which
are currently not supported.

<a id="black.validate_metadata"></a>

#### validate\_metadata

```python
def validate_metadata(nb: MutableMapping[str, Any]) -> None
```

If notebook is marked as non-Python, don't format it.

All notebook metadata fields are optional, see
https://nbformat.readthedocs.io/en/latest/format_description.html. So
if a notebook has empty metadata, we will try to parse it anyway.

<a id="black.format_ipynb_string"></a>

#### format\_ipynb\_string

```python
def format_ipynb_string(src_contents: str, *, fast: bool,
                        mode: Mode) -> FileContent
```

Format Jupyter notebook.

Operate cell-by-cell, only on code cells, only for Python notebooks.
If the ``.ipynb`` originally had a trailing newline, it'll be preserved.

<a id="black.format_str"></a>

#### format\_str

```python
def format_str(src_contents: str,
               *,
               mode: Mode,
               lines: Collection[tuple[int, int]] = ()) -> str
```

Reformat a string and return new contents.

`mode` determines formatting options, such as how many characters per line are
allowed.  Example:

>>> import black
>>> print(black.format_str("def f(arg:str='')->None:...", mode=black.Mode()))
def f(arg: str = "") -> None:
...

A more complex example:

>>> print(
...   black.format_str(
...     "def f(arg:str='')->None: hey",
...     mode=black.Mode(
...       target_versions={black.TargetVersion.PY36},
...       line_length=10,
...       string_normalization=False,
...       is_pyi=False,
...     ),
...   ),
... )
def f(
arg: str = '',
) -> None:
hey

<a id="black.decode_bytes"></a>

#### decode\_bytes

```python
def decode_bytes(src: bytes,
                 mode: Mode) -> tuple[FileContent, Encoding, NewLine]
```

Return a tuple of (decoded_contents, encoding, newline).

`newline` is either CRLF or LF but `decoded_contents` is decoded with
universal newlines (i.e. only contains LF).

<a id="black.get_features_used"></a>

#### get\_features\_used

```python
def get_features_used(
        node: Node,
        *,
        future_imports: Optional[set[str]] = None) -> set[Feature]
```

Return a set of (relatively) new Python features used in this file.

Currently looking for:
- f-strings;
- self-documenting expressions in f-strings (f"{x=}");
- underscores in numeric literals;
- trailing commas after * or ** in function signatures and calls;
- positional only arguments in function signatures and lambdas;
- assignment expression;
- relaxed decorator syntax;
- usage of __future__ flags (annotations);
- print / exec statements;
- parenthesized context managers;
- match statements;
- except* clause;
- variadic generics;

<a id="black.detect_target_versions"></a>

#### detect\_target\_versions

```python
def detect_target_versions(
        node: Node,
        *,
        future_imports: Optional[set[str]] = None) -> set[TargetVersion]
```

Detect the version to target based on the nodes used.

<a id="black.get_future_imports"></a>

#### get\_future\_imports

```python
def get_future_imports(node: Node) -> set[str]
```

Return a set of __future__ imports in the file.

<a id="black.assert_equivalent"></a>

#### assert\_equivalent

```python
def assert_equivalent(src: str, dst: str) -> None
```

Raise AssertionError if `src` and `dst` aren't equivalent.

<a id="black.assert_stable"></a>

#### assert\_stable

```python
def assert_stable(src: str,
                  dst: str,
                  mode: Mode,
                  *,
                  lines: Collection[tuple[int, int]] = ()) -> None
```

Raise AssertionError if `dst` reformats differently the second time.

<a id="black.nullcontext"></a>

#### nullcontext

```python
@contextmanager
def nullcontext() -> Iterator[None]
```

Return an empty context manager.

To be used like `nullcontext` in Python 3.7.

