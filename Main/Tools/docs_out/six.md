# Table of Contents

* [six](#six)
  * [\_SixMetaPathImporter](#six._SixMetaPathImporter)
    * [is\_package](#six._SixMetaPathImporter.is_package)
    * [get\_code](#six._SixMetaPathImporter.get_code)
    * [get\_source](#six._SixMetaPathImporter.get_source)
  * [Module\_six\_moves\_urllib\_parse](#six.Module_six_moves_urllib_parse)
  * [Module\_six\_moves\_urllib\_error](#six.Module_six_moves_urllib_error)
  * [Module\_six\_moves\_urllib\_request](#six.Module_six_moves_urllib_request)
  * [Module\_six\_moves\_urllib\_response](#six.Module_six_moves_urllib_response)
  * [Module\_six\_moves\_urllib\_robotparser](#six.Module_six_moves_urllib_robotparser)
  * [Module\_six\_moves\_urllib](#six.Module_six_moves_urllib)
  * [add\_move](#six.add_move)
  * [remove\_move](#six.remove_move)
  * [with\_metaclass](#six.with_metaclass)
  * [add\_metaclass](#six.add_metaclass)
  * [ensure\_binary](#six.ensure_binary)
  * [ensure\_str](#six.ensure_str)
  * [ensure\_text](#six.ensure_text)
  * [python\_2\_unicode\_compatible](#six.python_2_unicode_compatible)
  * [\_\_package\_\_](#six.__package__)

<a id="six"></a>

# six

Utilities for writing code that runs on Python 2 and 3

<a id="six._SixMetaPathImporter"></a>

## \_SixMetaPathImporter Objects

```python
class _SixMetaPathImporter(object)
```

A meta path importer to import six.moves and its submodules.

This class implements a PEP302 finder and loader. It should be compatible
with Python 2.5 and all existing versions of Python3

<a id="six._SixMetaPathImporter.is_package"></a>

#### is\_package

```python
def is_package(fullname)
```

Return true, if the named module is a package.

We need this method to get correct spec objects with
Python 3.4 (see PEP451)

<a id="six._SixMetaPathImporter.get_code"></a>

#### get\_code

```python
def get_code(fullname)
```

Return None

Required, if is_package is implemented

<a id="six._SixMetaPathImporter.get_source"></a>

#### get\_source

same as get_code

<a id="six.Module_six_moves_urllib_parse"></a>

## Module\_six\_moves\_urllib\_parse Objects

```python
class Module_six_moves_urllib_parse(_LazyModule)
```

Lazy loading of moved objects in six.moves.urllib_parse

<a id="six.Module_six_moves_urllib_error"></a>

## Module\_six\_moves\_urllib\_error Objects

```python
class Module_six_moves_urllib_error(_LazyModule)
```

Lazy loading of moved objects in six.moves.urllib_error

<a id="six.Module_six_moves_urllib_request"></a>

## Module\_six\_moves\_urllib\_request Objects

```python
class Module_six_moves_urllib_request(_LazyModule)
```

Lazy loading of moved objects in six.moves.urllib_request

<a id="six.Module_six_moves_urllib_response"></a>

## Module\_six\_moves\_urllib\_response Objects

```python
class Module_six_moves_urllib_response(_LazyModule)
```

Lazy loading of moved objects in six.moves.urllib_response

<a id="six.Module_six_moves_urllib_robotparser"></a>

## Module\_six\_moves\_urllib\_robotparser Objects

```python
class Module_six_moves_urllib_robotparser(_LazyModule)
```

Lazy loading of moved objects in six.moves.urllib_robotparser

<a id="six.Module_six_moves_urllib"></a>

## Module\_six\_moves\_urllib Objects

```python
class Module_six_moves_urllib(types.ModuleType)
```

Create a six.moves.urllib namespace that resembles the Python 3 namespace

<a id="six.add_move"></a>

#### add\_move

```python
def add_move(move)
```

Add an item to six.moves.

<a id="six.remove_move"></a>

#### remove\_move

```python
def remove_move(name)
```

Remove item from six.moves.

<a id="six.with_metaclass"></a>

#### with\_metaclass

```python
def with_metaclass(meta, *bases)
```

Create a base class with a metaclass.

<a id="six.add_metaclass"></a>

#### add\_metaclass

```python
def add_metaclass(metaclass)
```

Class decorator for creating a class with a metaclass.

<a id="six.ensure_binary"></a>

#### ensure\_binary

```python
def ensure_binary(s, encoding='utf-8', errors='strict')
```

Coerce **s** to six.binary_type.

For Python 2:
  - `unicode` -> encoded to `str`
  - `str` -> `str`

For Python 3:
  - `str` -> encoded to `bytes`
  - `bytes` -> `bytes`

<a id="six.ensure_str"></a>

#### ensure\_str

```python
def ensure_str(s, encoding='utf-8', errors='strict')
```

Coerce *s* to `str`.

For Python 2:
  - `unicode` -> encoded to `str`
  - `str` -> `str`

For Python 3:
  - `str` -> `str`
  - `bytes` -> decoded to `str`

<a id="six.ensure_text"></a>

#### ensure\_text

```python
def ensure_text(s, encoding='utf-8', errors='strict')
```

Coerce *s* to six.text_type.

For Python 2:
  - `unicode` -> `unicode`
  - `str` -> `unicode`

For Python 3:
  - `str` -> `str`
  - `bytes` -> decoded to `str`

<a id="six.python_2_unicode_compatible"></a>

#### python\_2\_unicode\_compatible

```python
def python_2_unicode_compatible(klass)
```

A class decorator that defines __unicode__ and __str__ methods under Python 2.
Under Python 3 it does nothing.

To support Python 2 and 3 with a single code base, define a __str__ method
returning text and apply this decorator to the class.

<a id="six.__package__"></a>

#### \_\_package\_\_

see PEP 366 @ReservedAssignment

