# Table of Contents

* [rich](#rich)
  * [get\_console](#rich.get_console)
  * [reconfigure](#rich.reconfigure)
  * [print](#rich.print)
  * [print\_json](#rich.print_json)
  * [inspect](#rich.inspect)

<a id="rich"></a>

# rich

Rich text and beautiful formatting in the terminal.

<a id="rich.get_console"></a>

#### get\_console

```python
def get_console() -> "Console"
```

Get a global :class:`~rich.console.Console` instance. This function is used when Rich requires a Console,
and hasn't been explicitly given one.

**Returns**:

- `Console` - A console instance.

<a id="rich.reconfigure"></a>

#### reconfigure

```python
def reconfigure(*args: Any, **kwargs: Any) -> None
```

Reconfigures the global console by replacing it with another.

**Arguments**:

- `*args` _Any_ - Positional arguments for the replacement :class:`~rich.console.Console`.
- `**kwargs` _Any_ - Keyword arguments for the replacement :class:`~rich.console.Console`.

<a id="rich.print"></a>

#### print

```python
def print(*objects: Any,
          sep: str = " ",
          end: str = "\n",
          file: Optional[IO[str]] = None,
          flush: bool = False) -> None
```

Print object(s) supplied via positional arguments.
This function has an identical signature to the built-in print.
For more advanced features, see the :class:`~rich.console.Console` class.

**Arguments**:

- `sep` _str, optional_ - Separator between printed objects. Defaults to " ".
- `end` _str, optional_ - Character to write at end of output. Defaults to "\\n".
- `file` _IO[str], optional_ - File to write to, or None for stdout. Defaults to None.
- `flush` _bool, optional_ - Has no effect as Rich always flushes output. Defaults to False.

<a id="rich.print_json"></a>

#### print\_json

```python
def print_json(json: Optional[str] = None,
               *,
               data: Any = None,
               indent: Union[None, int, str] = 2,
               highlight: bool = True,
               skip_keys: bool = False,
               ensure_ascii: bool = False,
               check_circular: bool = True,
               allow_nan: bool = True,
               default: Optional[Callable[[Any], Any]] = None,
               sort_keys: bool = False) -> None
```

Pretty prints JSON. Output will be valid JSON.

**Arguments**:

- `json` _str_ - A string containing JSON.
- `data` _Any_ - If json is not supplied, then encode this data.
- `indent` _int, optional_ - Number of spaces to indent. Defaults to 2.
- `highlight` _bool, optional_ - Enable highlighting of output: Defaults to True.
- `skip_keys` _bool, optional_ - Skip keys not of a basic type. Defaults to False.
- `ensure_ascii` _bool, optional_ - Escape all non-ascii characters. Defaults to False.
- `check_circular` _bool, optional_ - Check for circular references. Defaults to True.
- `allow_nan` _bool, optional_ - Allow NaN and Infinity values. Defaults to True.
- `default` _Callable, optional_ - A callable that converts values that can not be encoded
  in to something that can be JSON encoded. Defaults to None.
- `sort_keys` _bool, optional_ - Sort dictionary keys. Defaults to False.

<a id="rich.inspect"></a>

#### inspect

```python
def inspect(obj: Any,
            *,
            console: Optional["Console"] = None,
            title: Optional[str] = None,
            help: bool = False,
            methods: bool = False,
            docs: bool = True,
            private: bool = False,
            dunder: bool = False,
            sort: bool = True,
            all: bool = False,
            value: bool = True) -> None
```

Inspect any Python object.

* inspect(<OBJECT>) to see summarized info.
* inspect(<OBJECT>, methods=True) to see methods.
* inspect(<OBJECT>, help=True) to see full (non-abbreviated) help.
* inspect(<OBJECT>, private=True) to see private attributes (single underscore).
* inspect(<OBJECT>, dunder=True) to see attributes beginning with double underscore.
* inspect(<OBJECT>, all=True) to see all attributes.

**Arguments**:

- `obj` _Any_ - An object to inspect.
- `title` _str, optional_ - Title to display over inspect result, or None use type. Defaults to None.
- `help` _bool, optional_ - Show full help text rather than just first paragraph. Defaults to False.
- `methods` _bool, optional_ - Enable inspection of callables. Defaults to False.
- `docs` _bool, optional_ - Also render doc strings. Defaults to True.
- `private` _bool, optional_ - Show private attributes (beginning with underscore). Defaults to False.
- `dunder` _bool, optional_ - Show attributes starting with double underscore. Defaults to False.
- `sort` _bool, optional_ - Sort attributes alphabetically. Defaults to True.
- `all` _bool, optional_ - Show all attributes. Defaults to False.
- `value` _bool, optional_ - Pretty print value. Defaults to True.

