# Table of Contents

* [marko](#marko)
  * [Markdown](#marko.Markdown)
    * [use](#marko.Markdown.use)
    * [convert](#marko.Markdown.convert)
    * [parse](#marko.Markdown.parse)
    * [render](#marko.Markdown.render)
  * [convert](#marko.convert)
  * [parse](#marko.parse)
  * [render](#marko.render)

<a id="marko"></a>

# marko

_    _     _     ___   _  _    ___
| \  / |   /_\   | _ \ | |/ /  / _ \
| |\/| |  / _ \  |   / | ' <  | (_) |
|_|  |_| /_/ \_\ |_|_\ |_|\_\  \___/

A markdown parser with high extensibility.

Licensed under MIT.
Created by Frost Ming<mianghong@gmail.com>

<a id="marko.Markdown"></a>

## Markdown Objects

```python
class Markdown()
```

The main class to convert markdown documents.

Attributes:
    * parser: an instance of :class:`marko.parser.Parser`
    * renderer: an instance of :class:`marko.renderer.Renderer`

**Arguments**:

- `parser`: a subclass of :class:`marko.parser.Parser`.
- `renderer`: a subclass of :class:`marko.renderer.Renderer`.
- `extensions`: a list of extensions to register on the object.
See document of :meth:`Markdown.use()`.

.. note::
    This class is not thread-safe. Create a new instance for each thread.

<a id="marko.Markdown.use"></a>

#### use

```python
def use(*extensions: str | MarkoExtension) -> None
```

Register extensions to Markdown object.

An extension should be either an object providing ``elements``, `parser_mixins``
, ``renderer_mixins`` or all attributes, or a string representing the
corresponding extension in ``marko.ext`` module.

**Arguments**:

- `\*extensions`: string or :class:`marko.helpers.MarkoExtension` object.
.. note:: Marko uses a mixin based extension system, the order of extensions
    matters: An extension preceding in order will have higher priorty.

<a id="marko.Markdown.convert"></a>

#### convert

```python
def convert(text: str) -> str
```

Parse and render the given text.

<a id="marko.Markdown.parse"></a>

#### parse

```python
def parse(text: str) -> Document
```

Call ``self.parser.parse(text)``.

Override this to preprocess text or handle parsed result.

<a id="marko.Markdown.render"></a>

#### render

```python
def render(parsed: Document) -> str
```

Call ``self.renderer.render(text)``.

Override this to handle parsed result.

<a id="marko.convert"></a>

#### convert

```python
def convert(text: str) -> str
```

Parse and render the given text.

**Arguments**:

- `text`: text to convert.

**Returns**:

The rendered result.

<a id="marko.parse"></a>

#### parse

```python
def parse(text: str) -> Document
```

Parse the text to a structured data object.

**Arguments**:

- `text`: text to parse.

**Returns**:

the parsed object

<a id="marko.render"></a>

#### render

```python
def render(parsed: Document) -> str
```

Render the parsed object to text.

**Arguments**:

- `parsed`: the parsed object

**Returns**:

the rendered result.

