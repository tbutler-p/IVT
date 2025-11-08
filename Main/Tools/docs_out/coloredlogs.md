# Table of Contents

* [coloredlogs](#coloredlogs)
  * [DEFAULT\_LOG\_LEVEL](#coloredlogs.DEFAULT_LOG_LEVEL)
  * [DEFAULT\_LOG\_FORMAT](#coloredlogs.DEFAULT_LOG_FORMAT)
  * [DEFAULT\_DATE\_FORMAT](#coloredlogs.DEFAULT_DATE_FORMAT)
  * [CHROOT\_FILES](#coloredlogs.CHROOT_FILES)
  * [DEFAULT\_FIELD\_STYLES](#coloredlogs.DEFAULT_FIELD_STYLES)
  * [DEFAULT\_LEVEL\_STYLES](#coloredlogs.DEFAULT_LEVEL_STYLES)
  * [DEFAULT\_FORMAT\_STYLE](#coloredlogs.DEFAULT_FORMAT_STYLE)
  * [FORMAT\_STYLE\_PATTERNS](#coloredlogs.FORMAT_STYLE_PATTERNS)
  * [auto\_install](#coloredlogs.auto_install)
  * [install](#coloredlogs.install)
  * [check\_style](#coloredlogs.check_style)
  * [increase\_verbosity](#coloredlogs.increase_verbosity)
  * [decrease\_verbosity](#coloredlogs.decrease_verbosity)
  * [is\_verbose](#coloredlogs.is_verbose)
  * [get\_level](#coloredlogs.get_level)
  * [set\_level](#coloredlogs.set_level)
  * [adjust\_level](#coloredlogs.adjust_level)
  * [find\_defined\_levels](#coloredlogs.find_defined_levels)
  * [level\_to\_number](#coloredlogs.level_to_number)
  * [find\_level\_aliases](#coloredlogs.find_level_aliases)
  * [parse\_encoded\_styles](#coloredlogs.parse_encoded_styles)
  * [find\_hostname](#coloredlogs.find_hostname)
  * [find\_program\_name](#coloredlogs.find_program_name)
  * [find\_username](#coloredlogs.find_username)
  * [replace\_handler](#coloredlogs.replace_handler)
  * [find\_handler](#coloredlogs.find_handler)
  * [match\_stream\_handler](#coloredlogs.match_stream_handler)
  * [walk\_propagation\_tree](#coloredlogs.walk_propagation_tree)
  * [BasicFormatter](#coloredlogs.BasicFormatter)
    * [formatTime](#coloredlogs.BasicFormatter.formatTime)
  * [ColoredFormatter](#coloredlogs.ColoredFormatter)
    * [\_\_init\_\_](#coloredlogs.ColoredFormatter.__init__)
    * [colorize\_format](#coloredlogs.ColoredFormatter.colorize_format)
    * [format](#coloredlogs.ColoredFormatter.format)
  * [Empty](#coloredlogs.Empty)
  * [HostNameFilter](#coloredlogs.HostNameFilter)
    * [install](#coloredlogs.HostNameFilter.install)
    * [\_\_init\_\_](#coloredlogs.HostNameFilter.__init__)
    * [filter](#coloredlogs.HostNameFilter.filter)
  * [ProgramNameFilter](#coloredlogs.ProgramNameFilter)
    * [install](#coloredlogs.ProgramNameFilter.install)
    * [\_\_init\_\_](#coloredlogs.ProgramNameFilter.__init__)
    * [filter](#coloredlogs.ProgramNameFilter.filter)
  * [UserNameFilter](#coloredlogs.UserNameFilter)
    * [install](#coloredlogs.UserNameFilter.install)
    * [\_\_init\_\_](#coloredlogs.UserNameFilter.__init__)
    * [filter](#coloredlogs.UserNameFilter.filter)
  * [StandardErrorHandler](#coloredlogs.StandardErrorHandler)
    * [\_\_init\_\_](#coloredlogs.StandardErrorHandler.__init__)
    * [stream](#coloredlogs.StandardErrorHandler.stream)
  * [FormatStringParser](#coloredlogs.FormatStringParser)
    * [\_\_init\_\_](#coloredlogs.FormatStringParser.__init__)
    * [contains\_field](#coloredlogs.FormatStringParser.contains_field)
    * [get\_field\_names](#coloredlogs.FormatStringParser.get_field_names)
    * [get\_grouped\_pairs](#coloredlogs.FormatStringParser.get_grouped_pairs)
    * [get\_pairs](#coloredlogs.FormatStringParser.get_pairs)
    * [get\_pattern](#coloredlogs.FormatStringParser.get_pattern)
    * [get\_tokens](#coloredlogs.FormatStringParser.get_tokens)
  * [FormatStringToken](#coloredlogs.FormatStringToken)
  * [NameNormalizer](#coloredlogs.NameNormalizer)
    * [\_\_init\_\_](#coloredlogs.NameNormalizer.__init__)
    * [normalize\_name](#coloredlogs.NameNormalizer.normalize_name)
    * [normalize\_keys](#coloredlogs.NameNormalizer.normalize_keys)
    * [get](#coloredlogs.NameNormalizer.get)

<a id="coloredlogs"></a>

# coloredlogs

Colored terminal output for Python's :mod:`logging` module.

.. contents::
   :local:

Getting started
===============

The easiest way to get started is by importing :mod:`coloredlogs` and calling
:mod:`coloredlogs.install()` (similar to :func:`logging.basicConfig()`):

 >>> import coloredlogs, logging
 >>> coloredlogs.install(level='DEBUG')
 >>> logger = logging.getLogger('some.module.name')
 >>> logger.info("this is an informational message")
 2015-10-22 19:13:52 peter-macbook some.module.name[28036] INFO this is an informational message

The :mod:`~coloredlogs.install()` function creates a :class:`ColoredFormatter`
that injects `ANSI escape sequences`_ into the log output.

.. _ANSI escape sequences: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

Environment variables
=====================

The following environment variables can be used to configure the
:mod:`coloredlogs` module without writing any code:

=============================  ============================  ==================================
Environment variable           Default value                 Type of value
=============================  ============================  ==================================
``$COLOREDLOGS_AUTO_INSTALL``  'false'                       a boolean that controls whether
                                                             :func:`auto_install()` is called
``$COLOREDLOGS_LOG_LEVEL``     'INFO'                        a log level name
``$COLOREDLOGS_LOG_FORMAT``    :data:`DEFAULT_LOG_FORMAT`    a log format string
``$COLOREDLOGS_DATE_FORMAT``   :data:`DEFAULT_DATE_FORMAT`   a date/time format string
``$COLOREDLOGS_LEVEL_STYLES``  :data:`DEFAULT_LEVEL_STYLES`  see :func:`parse_encoded_styles()`
``$COLOREDLOGS_FIELD_STYLES``  :data:`DEFAULT_FIELD_STYLES`  see :func:`parse_encoded_styles()`
=============================  ============================  ==================================

If the environment variable `$NO_COLOR`_ is set (the value doesn't matter, even
an empty string will do) then :func:`coloredlogs.install()` will take this as a
hint that colors should not be used (unless the ``isatty=True`` override was
passed by the caller).

.. _$NO_COLOR: https://no-color.org/

Examples of customization
=========================

Here we'll take a look at some examples of how you can customize
:mod:`coloredlogs` using environment variables.

.. contents::
   :local:

About the defaults
------------------

Here's a screen shot of the default configuration for easy comparison with the
screen shots of the following customizations (this is the same screen shot that
is shown in the introduction):

.. image:: images/defaults.png
   :alt: Screen shot of colored logging with defaults.

The screen shot above was taken from ``urxvt`` which doesn't support faint text
colors, otherwise the color of green used for `debug` messages would have
differed slightly from the color of green used for `spam` messages.

Apart from the `faint` style of the `spam` level, the default configuration of
`coloredlogs` sticks to the eight color palette defined by the original ANSI
standard, in order to provide a somewhat consistent experience across terminals
and terminal emulators.

Available text styles and colors
--------------------------------

Of course you are free to customize the default configuration, in this case you
can use any text style or color that you know is supported by your terminal.
You can use the ``humanfriendly --demo`` command to try out the supported text
styles and colors:

.. image:: http://humanfriendly.readthedocs.io/en/latest/_images/ansi-demo.png
   :alt: Screen shot of the 'humanfriendly --demo' command.

Changing the log format
-----------------------

The simplest customization is to change the log format, for example:

.. literalinclude:: examples/custom-log-format.txt
   :language: console

Here's what that looks like in a terminal (I always work in terminals with a
black background and white text):

.. image:: images/custom-log-format.png
   :alt: Screen shot of colored logging with custom log format.

Changing the date/time format
-----------------------------

You can also change the date/time format, for example you can remove the date
part and leave only the time:

.. literalinclude:: examples/custom-datetime-format.txt
   :language: console

Here's what it looks like in a terminal:

.. image:: images/custom-datetime-format.png
   :alt: Screen shot of colored logging with custom date/time format.

Changing the colors/styles
--------------------------

Finally you can customize the colors and text styles that are used:

.. literalinclude:: examples/custom-colors.txt
   :language: console

Here's an explanation of the features used here:

- The numbers used in ``$COLOREDLOGS_LEVEL_STYLES`` demonstrate the use of 256
  color mode (the numbers refer to the 256 color mode palette which is fixed).

- The `success` level demonstrates the use of a text style (bold).

- The `critical` level demonstrates the use of a background color (red).

Of course none of this can be seen in the shell transcript quoted above, but
take a look at the following screen shot:

.. image:: images/custom-colors.png
   :alt: Screen shot of colored logging with custom colors.

.. _notes about log levels:

Some notes about log levels
===========================

With regards to the handling of log levels, the :mod:`coloredlogs` package
differs from Python's :mod:`logging` module in two aspects:

1. While the :mod:`logging` module uses the default logging level
   :data:`logging.WARNING`, the :mod:`coloredlogs` package has always used
   :data:`logging.INFO` as its default log level.

2. When logging to the terminal or system log is initialized by
   :func:`install()` or :func:`.enable_system_logging()` the effective
   level [#]_ of the selected logger [#]_ is compared against the requested
   level [#]_ and if the effective level is more restrictive than the requested
   level, the logger's level will be set to the requested level (this happens
   in :func:`adjust_level()`). The reason for this is to work around a
   combination of design choices in Python's :mod:`logging` module that can
   easily confuse people who aren't already intimately familiar with it:

   - All loggers are initialized with the level :data:`logging.NOTSET`.

   - When a logger's level is set to :data:`logging.NOTSET` the
     :func:`~logging.Logger.getEffectiveLevel()` method will
     fall back to the level of the parent logger.

   - The parent of all loggers is the root logger and the root logger has its
     level set to :data:`logging.WARNING` by default (after importing the
     :mod:`logging` module).

   Effectively all user defined loggers inherit the default log level
   :data:`logging.WARNING` from the root logger, which isn't very intuitive for
   those who aren't already familiar with the hierarchical nature of the
   :mod:`logging` module.

   By avoiding this potentially confusing behavior (see ``14``_, ``18``_, ``21``_,
   ``23``_ and ``24``_), while at the same time allowing the caller to specify a
   logger object, my goal and hope is to provide sane defaults that can easily
   be changed when the need arises.

   .. [#] Refer to :func:`logging.Logger.getEffectiveLevel()` for details.
   .. [#] The logger that is passed as an argument by the caller or the root
          logger which is selected as a default when no logger is provided.
   .. [#] The log level that is passed as an argument by the caller or the
          default log level :data:`logging.INFO` when no level is provided.

   .. _#14: https://github.com/xolox/python-coloredlogs/issues/14
   .. _#18: https://github.com/xolox/python-coloredlogs/issues/18
   .. _#21: https://github.com/xolox/python-coloredlogs/pull/21
   .. _#23: https://github.com/xolox/python-coloredlogs/pull/23
   .. _#24: https://github.com/xolox/python-coloredlogs/issues/24

Classes and functions
=====================

<a id="coloredlogs.DEFAULT_LOG_LEVEL"></a>

#### DEFAULT\_LOG\_LEVEL

The default log level for :mod:`coloredlogs` (:data:`logging.INFO`).

<a id="coloredlogs.DEFAULT_LOG_FORMAT"></a>

#### DEFAULT\_LOG\_FORMAT

The default log format for :class:`ColoredFormatter` objects (a string).

<a id="coloredlogs.DEFAULT_DATE_FORMAT"></a>

#### DEFAULT\_DATE\_FORMAT

The default date/time format for :class:`ColoredFormatter` objects (a string).

<a id="coloredlogs.CHROOT_FILES"></a>

#### CHROOT\_FILES

A list of filenames that indicate a chroot and contain the name of the chroot.

<a id="coloredlogs.DEFAULT_FIELD_STYLES"></a>

#### DEFAULT\_FIELD\_STYLES

Mapping of log format names to default font styles.

<a id="coloredlogs.DEFAULT_LEVEL_STYLES"></a>

#### DEFAULT\_LEVEL\_STYLES

Mapping of log level names to default font styles.

<a id="coloredlogs.DEFAULT_FORMAT_STYLE"></a>

#### DEFAULT\_FORMAT\_STYLE

The default logging format style (a single character).

<a id="coloredlogs.FORMAT_STYLE_PATTERNS"></a>

#### FORMAT\_STYLE\_PATTERNS

A dictionary that maps the `style` characters ``%``, ``{`` and ``$`` (see the
documentation of the :class:`python3:logging.Formatter` class in Python 3.2+)
to strings containing regular expression patterns that can be used to parse
format strings in the corresponding style:

``%``
 A string containing a regular expression that matches a "percent conversion
 specifier" as defined in the `String Formatting Operations`_ section of the
 Python documentation. Here's an example of a logging format string in this
 format: ``%(levelname)s:%(name)s:%(message)s``.

``{``
 A string containing a regular expression that matches a "replacement field" as
 defined in the `Format String Syntax`_ section of the Python documentation.
 Here's an example of a logging format string in this format:
 ``{levelname}:{name}:{message}``.

``$``
 A string containing a regular expression that matches a "substitution
 placeholder" as defined in the `Template Strings`_ section of the Python
 documentation. Here's an example of a logging format string in this format:
 ``$levelname:$name:$message``.

These regular expressions are used by :class:`FormatStringParser` to introspect
and manipulate logging format strings.

.. _String Formatting Operations: https://docs.python.org/2/library/stdtypes.html#string-formatting
.. _Format String Syntax: https://docs.python.org/2/library/string.html#formatstrings
.. _Template Strings: https://docs.python.org/3/library/string.html#template-strings

<a id="coloredlogs.auto_install"></a>

#### auto\_install

```python
def auto_install()
```

Automatically call :func:`install()` when ``$COLOREDLOGS_AUTO_INSTALL`` is set.

The `coloredlogs` package includes a `path configuration file`_ that
automatically imports the :mod:`coloredlogs` module and calls
:func:`auto_install()` when the environment variable
``$COLOREDLOGS_AUTO_INSTALL`` is set.

This function uses :func:`~humanfriendly.coerce_boolean()` to check whether
the value of ``$COLOREDLOGS_AUTO_INSTALL`` should be considered :data:`True`.

.. _path configuration file: https://docs.python.org/2/library/site.html#module-site

<a id="coloredlogs.install"></a>

#### install

```python
def install(level=None, **kw)
```

Enable colored terminal output for Python's :mod:`logging` module.

**Arguments**:

- `level`: The default logging level (an integer or a string with a
level name, defaults to :data:`DEFAULT_LOG_LEVEL`).
- `logger`: The logger to which the stream handler should be attached (a
:class:`~logging.Logger` object, defaults to the root logger).
- `fmt`: Set the logging format (a string like those accepted by
:class:`~logging.Formatter`, defaults to
:data:`DEFAULT_LOG_FORMAT`).
- `datefmt`: Set the date/time format (a string, defaults to
:data:`DEFAULT_DATE_FORMAT`).
- `style`: One of the characters ``%``, ``{`` or ``$`` (defaults to
:data:`DEFAULT_FORMAT_STYLE`). See the documentation of the
:class:`python3:logging.Formatter` class in Python 3.2+. On
older Python versions only ``%`` is supported.
- `milliseconds`: :data:`True` to show milliseconds like :mod:`logging`
does by default, :data:`False` to hide milliseconds
(the default is :data:`False`, see ``16``_).
- `level_styles`: A dictionary with custom level styles (defaults to
:data:`DEFAULT_LEVEL_STYLES`).
- `field_styles`: A dictionary with custom field styles (defaults to
:data:`DEFAULT_FIELD_STYLES`).
- `stream`: The stream where log messages should be written to (a
file-like object). This defaults to :data:`None` which
means :class:`StandardErrorHandler` is used.
- `isatty`: :data:`True` to use a :class:`ColoredFormatter`,
:data:`False` to use a normal :class:`~logging.Formatter`
(defaults to auto-detection using
:func:`~humanfriendly.terminal.terminal_supports_colors()`).
- `reconfigure`: If :data:`True` (the default) multiple calls to
:func:`coloredlogs.install()` will each override
the previous configuration.
- `use_chroot`: Refer to :class:`HostNameFilter`.
- `programname`: Refer to :class:`ProgramNameFilter`.
- `username`: Refer to :class:`UserNameFilter`.
- `syslog`: If :data:`True` then :func:`.enable_system_logging()` will
be called without arguments (defaults to :data:`False`). The
               `syslog` argument may also be a number or string, in this
               case it is assumed to be a logging level which is passed on
               to :func:`.enable_system_logging()`.

The :func:`coloredlogs.install()` function is similar to

<a id="coloredlogs.check_style"></a>

#### check\_style

```python
def check_style(value)
```

Validate a logging format style.

**Arguments**:

- `value`: The logging format style to validate (any value).

**Raises**:

- `None`: :exc:`~exceptions.ValueError` when the given style isn't supported.
On Python 3.2+ this function accepts the logging format styles ``%``, ``{``
and ``$`` while on older versions only ``%`` is accepted (because older
Python versions don't support alternative logging format styles).

**Returns**:

The logging format character (a string of one character).

<a id="coloredlogs.increase_verbosity"></a>

#### increase\_verbosity

```python
def increase_verbosity()
```

Increase the verbosity of the root handler by one defined level.

Understands custom logging levels like defined by my ``verboselogs``
module.

<a id="coloredlogs.decrease_verbosity"></a>

#### decrease\_verbosity

```python
def decrease_verbosity()
```

Decrease the verbosity of the root handler by one defined level.

Understands custom logging levels like defined by my ``verboselogs``
module.

<a id="coloredlogs.is_verbose"></a>

#### is\_verbose

```python
def is_verbose()
```

Check whether the log level of the root handler is set to a verbose level.

**Returns**:

``True`` if the root handler is verbose, ``False`` if not.

<a id="coloredlogs.get_level"></a>

#### get\_level

```python
def get_level()
```

Get the logging level of the root handler.

**Returns**:

The logging level of the root handler (an integer) or
:data:`DEFAULT_LOG_LEVEL` (if no root handler exists).

<a id="coloredlogs.set_level"></a>

#### set\_level

```python
def set_level(level)
```

Set the logging level of the root handler.

**Arguments**:

- `level`: The logging level to filter on (an integer or string).
If no root handler exists yet this automatically calls :func:`install()`.

<a id="coloredlogs.adjust_level"></a>

#### adjust\_level

```python
def adjust_level(logger, level)
```

Increase a logger's verbosity up to the requested level.

**Arguments**:

- `logger`: The logger to change (a :class:`~logging.Logger` object).
- `level`: The log level to enable (a string or number).
This function is used by functions like :func:`install()`,

<a id="coloredlogs.find_defined_levels"></a>

#### find\_defined\_levels

```python
def find_defined_levels()
```

Find the defined logging levels.

**Returns**:

A dictionary with level names as keys and integers as values.
Here's what the result looks like by default (when
no custom levels or level names have been defined):

>>> find_defined_levels()
{'NOTSET': 0,
 'DEBUG': 10,
 'INFO': 20,
 'WARN': 30,
 'WARNING': 30,
 'ERROR': 40,
 'FATAL': 50,
 'CRITICAL': 50}

<a id="coloredlogs.level_to_number"></a>

#### level\_to\_number

```python
def level_to_number(value)
```

Coerce a logging level name to a number.

**Arguments**:

- `value`: A logging level (integer or string).

**Returns**:

The number of the log level (an integer).
This function translates log level names into their numeric values..

<a id="coloredlogs.find_level_aliases"></a>

#### find\_level\_aliases

```python
def find_level_aliases()
```

Find log level names which are aliases of each other.

**Returns**:

A dictionary that maps aliases to their canonical name.
.. note:: Canonical names are chosen to be the alias with the longest
          string length so that e.g. ``WARN`` is an alias for ``WARNING``
          instead of the other way around.

Here's what the result looks like by default (when
no custom levels or level names have been defined):

>>> from coloredlogs import find_level_aliases
>>> find_level_aliases()
{'WARN': 'WARNING', 'FATAL': 'CRITICAL'}

<a id="coloredlogs.parse_encoded_styles"></a>

#### parse\_encoded\_styles

```python
def parse_encoded_styles(text, normalize_key=None)
```

Parse text styles encoded in a string into a nested data structure.

**Arguments**:

- `text`: The encoded styles (a string).

**Returns**:

A dictionary in the structure of the :data:`DEFAULT_FIELD_STYLES`
and :data:`DEFAULT_LEVEL_STYLES` dictionaries.

Here's an example of how this function works:

>>> from coloredlogs import parse_encoded_styles
>>> from pprint import pprint
>>> encoded_styles = 'debug=green;warning=yellow;error=red;critical=red,bold'
>>> pprint(parse_encoded_styles(encoded_styles))
{'debug': {'color': 'green'},
 'warning': {'color': 'yellow'},
 'error': {'color': 'red'},
 'critical': {'bold': True, 'color': 'red'}}

<a id="coloredlogs.find_hostname"></a>

#### find\_hostname

```python
def find_hostname(use_chroot=True)
```

Find the host name to include in log messages.

**Arguments**:

- `use_chroot`: Use the name of the chroot when inside a chroot?
(boolean, defaults to :data:`True`)

**Returns**:

A suitable host name (a string).
Looks for :data:`CHROOT_FILES` that have a nonempty first line (taken to be
the chroot name). If none are found then :func:`socket.gethostname()` is
used as a fall back.

<a id="coloredlogs.find_program_name"></a>

#### find\_program\_name

```python
def find_program_name()
```

Select a suitable program name to embed in log messages.

**Returns**:

One of the following strings (in decreasing order of preference):
1. The base name of the currently running Python program or
   script (based on the value at index zero of :data:`sys.argv`).
2. The base name of the Python executable (based on
   :data:`sys.executable`).
3. The string 'python'.

<a id="coloredlogs.find_username"></a>

#### find\_username

```python
def find_username()
```

Find the username to include in log messages.

**Returns**:

A suitable username (a string).
On UNIX systems this uses the :mod:`pwd` module which means ``root`` will
be reported when :man:`sudo` is used (as it should). If this fails (for
example on Windows) then :func:`getpass.getuser()` is used as a fall back.

<a id="coloredlogs.replace_handler"></a>

#### replace\_handler

```python
def replace_handler(logger, match_handler, reconfigure)
```

Prepare to replace a handler.

**Arguments**:

- `logger`: Refer to :func:`find_handler()`.
- `match_handler`: Refer to :func:`find_handler()`.
- `reconfigure`: :data:`True` if an existing handler should be replaced,
:data:`False` otherwise.

**Returns**:

A tuple of two values:
1. The matched :class:`~logging.Handler` object or :data:`None`
   if no handler was matched.
2. The :class:`~logging.Logger` to which the matched handler was
   attached or the logger given to :func:`replace_handler()`.

<a id="coloredlogs.find_handler"></a>

#### find\_handler

```python
def find_handler(logger, match_handler)
```

Find a (specific type of) handler in the propagation tree of a logger.

**Arguments**:

- `logger`: The logger to check (a :class:`~logging.Logger` object).
- `match_handler`: A callable that receives a :class:`~logging.Handler`
object and returns :data:`True` to match a handler or
:data:`False` to skip that handler and continue
searching for a match.

**Returns**:

A tuple of two values:
          1. The matched :class:`~logging.Handler` object or :data:`None`
             if no handler was matched.
          2. The :class:`~logging.Logger` object to which the handler is
             attached or :data:`None` if no handler was matched.

This function finds a logging handler (of the given type) attached to a
logger or one of its parents (see :func:`walk_propagation_tree()`). It uses
the undocumented :class:`~logging.Logger.handlers` attribute to find
handlers attached to a logger, however it won't raise an exception if the
attribute isn't available. The advantages of this approach are:

- This works regardless of whether :mod:`coloredlogs` attached the handler
  or other Python code attached the handler.

- This will correctly recognize the situation where the given logger has no
  handlers but :attr:`~logging.Logger.propagate` is enabled and the logger
  has a parent logger that does have a handler attached.

<a id="coloredlogs.match_stream_handler"></a>

#### match\_stream\_handler

```python
def match_stream_handler(handler, streams=[])
```

Identify stream handlers writing to the given streams(s).

**Arguments**:

- `handler`: The :class:`~logging.Handler` class to check.
- `streams`: A sequence of streams to match (defaults to matching
:data:`~sys.stdout` and :data:`~sys.stderr`).

**Returns**:

:data:`True` if the handler is a :class:`~logging.StreamHandler`
logging to the given stream(s), :data:`False` otherwise.

This function can be used as a callback for :func:`find_handler()`.

<a id="coloredlogs.walk_propagation_tree"></a>

#### walk\_propagation\_tree

```python
def walk_propagation_tree(logger)
```

Walk through the propagation hierarchy of the given logger.

**Arguments**:

- `logger`: The logger whose hierarchy to walk (a
:class:`~logging.Logger` object).

**Returns**:

A generator of :class:`~logging.Logger` objects.
.. note:: This uses the undocumented :class:`logging.Logger.parent`
          attribute to find higher level loggers, however it won't
          raise an exception if the attribute isn't available.

<a id="coloredlogs.BasicFormatter"></a>

## BasicFormatter Objects

```python
class BasicFormatter(logging.Formatter)
```

Log :class:`~logging.Formatter` that supports ``%f`` for millisecond formatting.

This class extends :class:`~logging.Formatter` to enable the use of ``%f``
for millisecond formatting in date/time strings, to allow for the type of
flexibility requested in issue ``45``_.

.. _#45: https://github.com/xolox/python-coloredlogs/issues/45

<a id="coloredlogs.BasicFormatter.formatTime"></a>

#### formatTime

```python
def formatTime(record, datefmt=None)
```

Format the date/time of a log record.

**Arguments**:

- `record`: A :class:`~logging.LogRecord` object.
- `datefmt`: A date/time format string (defaults to :data:`DEFAULT_DATE_FORMAT`).

**Returns**:

The formatted date/time (a string).
This method overrides :func:`~logging.Formatter.formatTime()` to set
`datefmt` to :data:`DEFAULT_DATE_FORMAT` when the caller hasn't
specified a date format.

When `datefmt` contains the token ``%f`` it will be replaced by the
value of ``%(msecs)03d`` (refer to issue ``45``_ for use cases).

<a id="coloredlogs.ColoredFormatter"></a>

## ColoredFormatter Objects

```python
class ColoredFormatter(BasicFormatter)
```

Log :class:`~logging.Formatter` that uses `ANSI escape sequences`_ to create colored logs.

:class:`ColoredFormatter` inherits from :class:`BasicFormatter` to enable
the use of ``%f`` for millisecond formatting in date/time strings.

.. note:: If you want to use :class:`ColoredFormatter` on Windows then you
          need to call :func:`~humanfriendly.terminal.enable_ansi_support()`.
          This is done for you when you call :func:`coloredlogs.install()`.

<a id="coloredlogs.ColoredFormatter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(fmt=None,
             datefmt=None,
             style=DEFAULT_FORMAT_STYLE,
             level_styles=None,
             field_styles=None)
```

Initialize a :class:`ColoredFormatter` object.

**Arguments**:

- `fmt`: A log format string (defaults to :data:`DEFAULT_LOG_FORMAT`).
- `datefmt`: A date/time format string (defaults to :data:`None`,
but see the documentation of
:func:`BasicFormatter.formatTime()`).
- `style`: One of the characters ``%``, ``{`` or ``$`` (defaults to
:data:`DEFAULT_FORMAT_STYLE`)
- `level_styles`: A dictionary with custom level styles
(defaults to :data:`DEFAULT_LEVEL_STYLES`).
- `field_styles`: A dictionary with custom field styles
(defaults to :data:`DEFAULT_FIELD_STYLES`).

**Raises**:

- `None`: Refer to :func:`check_style()`.
This initializer uses :func:`colorize_format()` to inject ANSI escape
sequences in the log format string before it is passed to the
initializer of the base class.

<a id="coloredlogs.ColoredFormatter.colorize_format"></a>

#### colorize\_format

```python
def colorize_format(fmt, style=DEFAULT_FORMAT_STYLE)
```

Rewrite a logging format string to inject ANSI escape sequences.

**Arguments**:

- `fmt`: The log format string.
- `style`: One of the characters ``%``, ``{`` or ``$`` (defaults to
:data:`DEFAULT_FORMAT_STYLE`).

**Returns**:

The logging format string with ANSI escape sequences.
This method takes a logging format string like the ones you give to

<a id="coloredlogs.ColoredFormatter.format"></a>

#### format

```python
def format(record)
```

Apply level-specific styling to log records.

**Arguments**:

- `record`: A :class:`~logging.LogRecord` object.

**Returns**:

The result of :func:`logging.Formatter.format()`.
This method injects ANSI escape sequences that are specific to the
level of each log record (because such logic cannot be expressed in the
syntax of a log format string). It works by making a copy of the log
record, changing the `msg` field inside the copy and passing the copy
into the :func:`~logging.Formatter.format()` method of the base
class.

<a id="coloredlogs.Empty"></a>

## Empty Objects

```python
class Empty(object)
```

An empty class used to copy :class:`~logging.LogRecord` objects without reinitializing them.

<a id="coloredlogs.HostNameFilter"></a>

## HostNameFilter Objects

```python
class HostNameFilter(logging.Filter)
```

Log filter to enable the ``%(hostname)s`` format.

Python's :mod:`logging` module doesn't expose the system's host name while
I consider this to be a valuable addition. Fortunately it's very easy to
expose additional fields in format strings: :func:`filter()` simply sets
the ``hostname`` attribute of each :class:`~logging.LogRecord` object it
receives and this is enough to enable the use of the ``%(hostname)s``
expression in format strings.

You can install this log filter as follows::

 >>> import coloredlogs, logging
 >>> handler = logging.StreamHandler()
 >>> handler.addFilter(coloredlogs.HostNameFilter())
 >>> handler.setFormatter(logging.Formatter('[%(hostname)s] %(message)s'))
 >>> logger = logging.getLogger()
 >>> logger.addHandler(handler)
 >>> logger.setLevel(logging.INFO)
 >>> logger.info("Does it work?")
 [peter-macbook] Does it work?

Of course :func:`coloredlogs.install()` does all of this for you :-).

<a id="coloredlogs.HostNameFilter.install"></a>

#### install

```python
@classmethod
def install(cls,
            handler,
            fmt=None,
            use_chroot=True,
            style=DEFAULT_FORMAT_STYLE)
```

Install the :class:`HostNameFilter` on a log handler (only if needed).

**Arguments**:

- `fmt`: The log format string to check for ``%(hostname)``.
- `style`: One of the characters ``%``, ``{`` or ``$`` (defaults to
:data:`DEFAULT_FORMAT_STYLE`).
- `handler`: The logging handler on which to install the filter.
- `use_chroot`: Refer to :func:`find_hostname()`.
If `fmt` is given the filter will only be installed if `fmt` uses the
``hostname`` field. If `fmt` is not given the filter is installed
unconditionally.

<a id="coloredlogs.HostNameFilter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(use_chroot=True)
```

Initialize a :class:`HostNameFilter` object.

**Arguments**:

- `use_chroot`: Refer to :func:`find_hostname()`.

<a id="coloredlogs.HostNameFilter.filter"></a>

#### filter

```python
def filter(record)
```

Set each :class:`~logging.LogRecord`'s `hostname` field.

<a id="coloredlogs.ProgramNameFilter"></a>

## ProgramNameFilter Objects

```python
class ProgramNameFilter(logging.Filter)
```

Log filter to enable the ``%(programname)s`` format.

Python's :mod:`logging` module doesn't expose the name of the currently
running program while I consider this to be a useful addition. Fortunately
it's very easy to expose additional fields in format strings:
:func:`filter()` simply sets the ``programname`` attribute of each
:class:`~logging.LogRecord` object it receives and this is enough to enable
the use of the ``%(programname)s`` expression in format strings.

Refer to :class:`HostNameFilter` for an example of how to manually install
these log filters.

<a id="coloredlogs.ProgramNameFilter.install"></a>

#### install

```python
@classmethod
def install(cls, handler, fmt, programname=None, style=DEFAULT_FORMAT_STYLE)
```

Install the :class:`ProgramNameFilter` (only if needed).

**Arguments**:

- `fmt`: The log format string to check for ``%(programname)``.
- `style`: One of the characters ``%``, ``{`` or ``$`` (defaults to
:data:`DEFAULT_FORMAT_STYLE`).
- `handler`: The logging handler on which to install the filter.
- `programname`: Refer to :func:`__init__()`.
If `fmt` is given the filter will only be installed if `fmt` uses the
``programname`` field. If `fmt` is not given the filter is installed
unconditionally.

<a id="coloredlogs.ProgramNameFilter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(programname=None)
```

Initialize a :class:`ProgramNameFilter` object.

**Arguments**:

- `programname`: The program name to use (defaults to the result of
:func:`find_program_name()`).

<a id="coloredlogs.ProgramNameFilter.filter"></a>

#### filter

```python
def filter(record)
```

Set each :class:`~logging.LogRecord`'s `programname` field.

<a id="coloredlogs.UserNameFilter"></a>

## UserNameFilter Objects

```python
class UserNameFilter(logging.Filter)
```

Log filter to enable the ``%(username)s`` format.

Python's :mod:`logging` module doesn't expose the username of the currently
logged in user as requested in ``76``_. Given that :class:`HostNameFilter`
and :class:`ProgramNameFilter` are already provided by `coloredlogs` it
made sense to provide :class:`UserNameFilter` as well.

Refer to :class:`HostNameFilter` for an example of how to manually install
these log filters.

.. _#76: https://github.com/xolox/python-coloredlogs/issues/76

<a id="coloredlogs.UserNameFilter.install"></a>

#### install

```python
@classmethod
def install(cls, handler, fmt, username=None, style=DEFAULT_FORMAT_STYLE)
```

Install the :class:`UserNameFilter` (only if needed).

**Arguments**:

- `fmt`: The log format string to check for ``%(username)``.
- `style`: One of the characters ``%``, ``{`` or ``$`` (defaults to
:data:`DEFAULT_FORMAT_STYLE`).
- `handler`: The logging handler on which to install the filter.
- `username`: Refer to :func:`__init__()`.
If `fmt` is given the filter will only be installed if `fmt` uses the
``username`` field. If `fmt` is not given the filter is installed
unconditionally.

<a id="coloredlogs.UserNameFilter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(username=None)
```

Initialize a :class:`UserNameFilter` object.

**Arguments**:

- `username`: The username to use (defaults to the
result of :func:`find_username()`).

<a id="coloredlogs.UserNameFilter.filter"></a>

#### filter

```python
def filter(record)
```

Set each :class:`~logging.LogRecord`'s `username` field.

<a id="coloredlogs.StandardErrorHandler"></a>

## StandardErrorHandler Objects

```python
class StandardErrorHandler(logging.StreamHandler)
```

A :class:`~logging.StreamHandler` that gets the value of :data:`sys.stderr` for each log message.

The :class:`StandardErrorHandler` class enables `monkey patching of
sys.stderr <https://github.com/xolox/python-coloredlogs/pull/31>`_. It's
basically the same as the ``logging._StderrHandler`` class present in
Python 3 but it will be available regardless of Python version. This
handler is used by :func:`coloredlogs.install()` to improve compatibility
with the Python standard library.

<a id="coloredlogs.StandardErrorHandler.__init__"></a>

#### \_\_init\_\_

```python
def __init__(level=logging.NOTSET)
```

Initialize a :class:`StandardErrorHandler` object.

<a id="coloredlogs.StandardErrorHandler.stream"></a>

#### stream

```python
@property
def stream()
```

Get the value of :data:`sys.stderr` (a file-like object).

<a id="coloredlogs.FormatStringParser"></a>

## FormatStringParser Objects

```python
class FormatStringParser(object)
```

Shallow logging format string parser.

This class enables introspection and manipulation of logging format strings
in the three styles supported by the :mod:`logging` module starting from
Python 3.2 (``%``, ``{`` and ``$``).

<a id="coloredlogs.FormatStringParser.__init__"></a>

#### \_\_init\_\_

```python
def __init__(style=DEFAULT_FORMAT_STYLE)
```

Initialize a :class:`FormatStringParser` object.

**Arguments**:

- `style`: One of the characters ``%``, ``{`` or ``$`` (defaults to
:data:`DEFAULT_FORMAT_STYLE`).

**Raises**:

- `None`: Refer to :func:`check_style()`.

<a id="coloredlogs.FormatStringParser.contains_field"></a>

#### contains\_field

```python
def contains_field(format_string, field_name)
```

Get the field names referenced by a format string.

**Arguments**:

- `format_string`: The logging format string.

**Returns**:

A list of strings with field names.

<a id="coloredlogs.FormatStringParser.get_field_names"></a>

#### get\_field\_names

```python
def get_field_names(format_string)
```

Get the field names referenced by a format string.

**Arguments**:

- `format_string`: The logging format string.

**Returns**:

A list of strings with field names.

<a id="coloredlogs.FormatStringParser.get_grouped_pairs"></a>

#### get\_grouped\_pairs

```python
def get_grouped_pairs(format_string)
```

Group the results of :func:`get_pairs()` separated by whitespace.

**Arguments**:

- `format_string`: The logging format string.

**Returns**:

A list of lists of :class:`FormatStringToken` objects.

<a id="coloredlogs.FormatStringParser.get_pairs"></a>

#### get\_pairs

```python
def get_pairs(format_string)
```

Tokenize a logging format string and extract field names from tokens.

**Arguments**:

- `format_string`: The logging format string.

**Returns**:

A generator of :class:`FormatStringToken` objects.

<a id="coloredlogs.FormatStringParser.get_pattern"></a>

#### get\_pattern

```python
def get_pattern(field_name)
```

Get a regular expression to match a formatting directive that references the given field name.

**Arguments**:

- `field_name`: The name of the field to match (a string).

**Returns**:

A compiled regular expression object.

<a id="coloredlogs.FormatStringParser.get_tokens"></a>

#### get\_tokens

```python
def get_tokens(format_string)
```

Tokenize a logging format string.

**Arguments**:

- `format_string`: The logging format string.

**Returns**:

A list of strings with formatting directives separated from surrounding text.

<a id="coloredlogs.FormatStringToken"></a>

## FormatStringToken Objects

```python
class FormatStringToken(
        collections.namedtuple('FormatStringToken', 'text, name'))
```

A named tuple for the results of :func:`FormatStringParser.get_pairs()`.

.. attribute:: name

   The field name referenced in `text` (a string). If `text` doesn't
   contain a formatting directive this will be :data:`None`.

.. attribute:: text

   The text extracted from the logging format string (a string).

<a id="coloredlogs.NameNormalizer"></a>

## NameNormalizer Objects

```python
class NameNormalizer(object)
```

Responsible for normalizing field and level names.

<a id="coloredlogs.NameNormalizer.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Initialize a :class:`NameNormalizer` object.

<a id="coloredlogs.NameNormalizer.normalize_name"></a>

#### normalize\_name

```python
def normalize_name(name)
```

Normalize a field or level name.

**Arguments**:

- `name`: The field or level name (a string).

**Returns**:

The normalized name (a string).
Transforms all strings to lowercase and resolves level name aliases
(refer to :func:`find_level_aliases()`) to their canonical name:

>>> from coloredlogs import NameNormalizer
>>> from humanfriendly import format_table
>>> nn = NameNormalizer()
>>> sample_names = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL']
>>> print(format_table([(n, nn.normalize_name(n)) for n in sample_names]))
-----------------------
| DEBUG    | debug    |
| INFO     | info     |
| WARN     | warning  |
| WARNING  | warning  |
| ERROR    | error    |
| FATAL    | critical |
| CRITICAL | critical |
-----------------------

<a id="coloredlogs.NameNormalizer.normalize_keys"></a>

#### normalize\_keys

```python
def normalize_keys(value)
```

Normalize the keys of a dictionary using :func:`normalize_name()`.

**Arguments**:

- `value`: The dictionary to normalize.

**Returns**:

A dictionary with normalized keys.

<a id="coloredlogs.NameNormalizer.get"></a>

#### get

```python
def get(normalized_dict, name)
```

Get a value from a dictionary after normalizing the key.

**Arguments**:

- `normalized_dict`: A dictionary produced by :func:`normalize_keys()`.
- `name`: A key to normalize and get from the dictionary.

**Returns**:

The value of the normalized key (if any).

