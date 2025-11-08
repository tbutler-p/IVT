# Table of Contents

* [setuptools](#setuptools)
  * [Command](#setuptools.Command)
    * [distribution](#setuptools.Command.distribution)
    * [\_\_init\_\_](#setuptools.Command.__init__)
    * [ensure\_string\_list](#setuptools.Command.ensure_string_list)
    * [initialize\_options](#setuptools.Command.initialize_options)
    * [finalize\_options](#setuptools.Command.finalize_options)
    * [run](#setuptools.Command.run)
  * [findall](#setuptools.findall)
  * [sic](#setuptools.sic)

<a id="setuptools"></a>

# setuptools

Extensions to the 'distutils' for large or complex distributions

<a id="setuptools.Command"></a>

## Command Objects

```python
class Command(_Command)
```

Setuptools internal actions are organized using a *command design pattern*.
This means that each action (or group of closely related actions) executed during
the build should be implemented as a ``Command`` subclass.

These commands are abstractions and do not necessarily correspond to a command that
can (or should) be executed via a terminal, in a CLI fashion (although historically
they would).

When creating a new command from scratch, custom defined classes **SHOULD** inherit
from ``setuptools.Command`` and implement a few mandatory methods.
Between these mandatory methods, are listed:
:meth:`initialize_options`, :meth:`finalize_options` and :meth:`run`.

A useful analogy for command classes is to think of them as subroutines with local
variables called "options".  The options are "declared" in :meth:`initialize_options`
and "defined" (given their final values, aka "finalized") in :meth:`finalize_options`,
both of which must be defined by every command class. The "body" of the subroutine,
(where it does all the work) is the :meth:`run` method.
Between :meth:`initialize_options` and :meth:`finalize_options`, ``setuptools`` may set
the values for options/attributes based on user's input (or circumstance),
which means that the implementation should be careful to not overwrite values in
:meth:`finalize_options` unless necessary.

Please note that other commands (or other parts of setuptools) may also overwrite
the values of the command's options/attributes multiple times during the build
process.
Therefore it is important to consistently implement :meth:`initialize_options` and
:meth:`finalize_options`. For example, all derived attributes (or attributes that
depend on the value of other attributes) **SHOULD** be recomputed in
:meth:`finalize_options`.

When overwriting existing commands, custom defined classes **MUST** abide by the
same APIs implemented by the original class. They also **SHOULD** inherit from the
original class.

<a id="setuptools.Command.distribution"></a>

#### distribution

override distutils.dist.Distribution with setuptools.dist.Distribution

<a id="setuptools.Command.__init__"></a>

#### \_\_init\_\_

```python
def __init__(dist: Distribution, **kw) -> None
```

Construct the command for dist, updating
vars(self) with any keyword parameters.

<a id="setuptools.Command.ensure_string_list"></a>

#### ensure\_string\_list

```python
def ensure_string_list(option: str) -> None
```

Ensure that 'option' is a list of strings.  If 'option' is
currently a string, we split it either on /,\s*/ or /\s+/, so
"foo bar baz", "foo,bar,baz", and "foo,   bar baz" all become
["foo", "bar", "baz"].

..
   TODO: This method seems to be similar to the one in ``distutils.cmd``
   Probably it is just here for backward compatibility with old Python versions?

:meta private:

<a id="setuptools.Command.initialize_options"></a>

#### initialize\_options

```python
@abstractmethod
def initialize_options() -> None
```

Set or (reset) all options/attributes/caches used by the command
to their default values. Note that these values may be overwritten during
the build.

<a id="setuptools.Command.finalize_options"></a>

#### finalize\_options

```python
@abstractmethod
def finalize_options() -> None
```

Set final values for all options/attributes used by the command.
Most of the time, each option/attribute/cache should only be set if it does not
have any value yet (e.g. ``if self.attr is None: self.attr = val``).

<a id="setuptools.Command.run"></a>

#### run

```python
@abstractmethod
def run() -> None
```

Execute the actions intended by the command.
(Side effects **SHOULD** only take place when :meth:`run` is executed,
for example, creating new files or writing to the terminal output).

<a id="setuptools.findall"></a>

#### findall

```python
def findall(dir=os.curdir)
```

Find all files under 'dir' and return the list of full filenames.
Unless dir is '.', return full filenames with dir prepended.

<a id="setuptools.sic"></a>

## sic Objects

```python
class sic(str)
```

Treat this string as-is (https://en.wikipedia.org/wiki/Sic)

