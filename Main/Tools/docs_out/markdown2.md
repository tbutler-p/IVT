# Table of Contents

* [markdown2](#markdown2)
  * [Stage](#markdown2.Stage)
    * [LINKS](#markdown2.Stage.LINKS)
  * [mark\_stage](#markdown2.mark_stage)
  * [Markdown](#markdown2.Markdown)
    * [html\_removed\_text](#markdown2.Markdown.html_removed_text)
    * [html\_removed\_text\_compat](#markdown2.Markdown.html_removed_text_compat)
    * [stage](#markdown2.Markdown.stage)
    * [order](#markdown2.Markdown.order)
    * [convert](#markdown2.Markdown.convert)
    * [postprocess](#markdown2.Markdown.postprocess)
    * [preprocess](#markdown2.Markdown.preprocess)
    * [header\_id\_from\_text](#markdown2.Markdown.header_id_from_text)
  * [MarkdownWithExtras](#markdown2.MarkdownWithExtras)
    * [extras](#markdown2.MarkdownWithExtras.extras)
  * [Extra](#markdown2.Extra)
    * [name](#markdown2.Extra.name)
    * [order](#markdown2.Extra.order)
    * [\_\_init\_\_](#markdown2.Extra.__init__)
    * [deregister](#markdown2.Extra.deregister)
    * [register](#markdown2.Extra.register)
    * [run](#markdown2.Extra.run)
    * [test](#markdown2.Extra.test)
  * [ItalicAndBoldProcessor](#markdown2.ItalicAndBoldProcessor)
  * [\_LinkProcessorExtraOpts](#markdown2._LinkProcessorExtraOpts)
    * [tags](#markdown2._LinkProcessorExtraOpts.tags)
    * [inline](#markdown2._LinkProcessorExtraOpts.inline)
    * [ref](#markdown2._LinkProcessorExtraOpts.ref)
  * [LinkProcessor](#markdown2.LinkProcessor)
    * [parse\_inline\_anchor\_or\_image](#markdown2.LinkProcessor.parse_inline_anchor_or_image)
    * [process\_link\_shortrefs](#markdown2.LinkProcessor.process_link_shortrefs)
    * [parse\_ref\_anchor\_or\_ref\_image](#markdown2.LinkProcessor.parse_ref_anchor_or_ref_image)
    * [process\_image](#markdown2.LinkProcessor.process_image)
    * [process\_anchor](#markdown2.LinkProcessor.process_anchor)
  * [Admonitions](#markdown2.Admonitions)
  * [Alerts](#markdown2.Alerts)
  * [\_BreaksExtraOpts](#markdown2._BreaksExtraOpts)
    * [on\_backslash](#markdown2._BreaksExtraOpts.on_backslash)
    * [on\_newline](#markdown2._BreaksExtraOpts.on_newline)
  * [CodeFriendly](#markdown2.CodeFriendly)
  * [FencedCodeBlocks](#markdown2.FencedCodeBlocks)
    * [tags](#markdown2.FencedCodeBlocks.tags)
  * [Latex](#markdown2.Latex)
  * [LinkPatterns](#markdown2.LinkPatterns)
  * [MarkdownInHTML](#markdown2.MarkdownInHTML)
  * [\_MarkdownFileLinksExtraOpts](#markdown2._MarkdownFileLinksExtraOpts)
    * [link\_defs](#markdown2._MarkdownFileLinksExtraOpts.link_defs)
  * [MarkdownFileLinks](#markdown2.MarkdownFileLinks)
  * [MiddleWordEm](#markdown2.MiddleWordEm)
    * [\_\_init\_\_](#markdown2.MiddleWordEm.__init__)
  * [Numbering](#markdown2.Numbering)
  * [PyShell](#markdown2.PyShell)
  * [SmartyPants](#markdown2.SmartyPants)
    * [run](#markdown2.SmartyPants.run)
  * [Strike](#markdown2.Strike)
  * [Tables](#markdown2.Tables)
    * [run](#markdown2.Tables.run)
  * [Underline](#markdown2.Underline)
  * [\_WavedromExtraOpts](#markdown2._WavedromExtraOpts)
    * [prefer\_embed\_svg](#markdown2._WavedromExtraOpts.prefer_embed_svg)
  * [Wavedrom](#markdown2.Wavedrom)
  * [WikiTables](#markdown2.WikiTables)
  * [calculate\_toc\_html](#markdown2.calculate_toc_html)
  * [UnicodeWithAttrs](#markdown2.UnicodeWithAttrs)
  * [\_memoized](#markdown2._memoized)
    * [\_\_repr\_\_](#markdown2._memoized.__repr__)

<a id="markdown2"></a>

# markdown2

A fast and complete Python implementation of Markdown.

[from http://daringfireball.net/projects/markdown/]
> Markdown is a text-to-HTML filter; it translates an easy-to-read /
> easy-to-write structured text format into HTML.  Markdown's text
> format is most similar to that of plain text email, and supports
> features such as headers, *emphasis*, code blocks, blockquotes, and
> links.
>
> Markdown's syntax is designed not as a generic markup language, but
> specifically to serve as a front-end to (X)HTML. You can use span-level
> HTML tags anywhere in a Markdown document, and you can use block level
> HTML tags (like <div> and <table> as well).

Module usage:

    >>> import markdown2
    >>> markdown2.markdown("*boo!*")  # or use `html = markdown_path(PATH)`
    u'<p><em>boo!</em></p>\n'

    >>> markdowner = Markdown()
    >>> markdowner.convert("*boo!*")
    u'<p><em>boo!</em></p>\n'
    >>> markdowner.convert("**boom!**")
    u'<p><strong>boom!</strong></p>\n'

This implementation of Markdown implements the full "core" syntax plus a
number of extras (e.g., code syntax coloring, footnotes) as described on
<https://github.com/trentm/python-markdown2/wiki/Extras>.

<a id="markdown2.Stage"></a>

## Stage Objects

```python
class Stage(IntEnum)
```

<a id="markdown2.Stage.LINKS"></a>

#### LINKS

and auto links

<a id="markdown2.mark_stage"></a>

#### mark\_stage

```python
def mark_stage(stage: Stage)
```

Decorator that handles executing relevant `Extra`s before and after this `Stage` executes.

<a id="markdown2.Markdown"></a>

## Markdown Objects

```python
class Markdown()
```

<a id="markdown2.Markdown.html_removed_text"></a>

#### html\_removed\_text

placeholder removed text that does not trigger bold

<a id="markdown2.Markdown.html_removed_text_compat"></a>

#### html\_removed\_text\_compat

for compat with markdown.py

<a id="markdown2.Markdown.stage"></a>

#### stage

Current "stage" of markdown conversion taking place

<a id="markdown2.Markdown.order"></a>

#### order

Same as `Stage` but will be +/- 0.5 of the value of `Stage`.
This allows extras to check if they are running before or after a particular stage
with `if md.order < md.stage`.

<a id="markdown2.Markdown.convert"></a>

#### convert

```python
def convert(text: str) -> 'UnicodeWithAttrs'
```

Convert the given text.

<a id="markdown2.Markdown.postprocess"></a>

#### postprocess

```python
@mark_stage(Stage.POSTPROCESS)
def postprocess(text: str) -> str
```

A hook for subclasses to do some postprocessing of the html, if
desired. This is called before unescaping of special chars and
unhashing of raw HTML spans.

<a id="markdown2.Markdown.preprocess"></a>

#### preprocess

```python
@mark_stage(Stage.PREPROCESS)
def preprocess(text: str) -> str
```

A hook for subclasses to do some preprocessing of the Markdown, if
desired. This is called after basic formatting of the text, but prior
to any extras, safe mode, etc. processing.

<a id="markdown2.Markdown.header_id_from_text"></a>

#### header\_id\_from\_text

```python
def header_id_from_text(text: str,
                        prefix: str,
                        n: Optional[int] = None) -> str
```

Generate a header id attribute value from the given header
HTML content.

This is only called if the "header-ids" extra is enabled.
Subclasses may override this for different header ids.

@param text {str} The text of the header tag
@param prefix {str} The requested prefix for header ids. This is the
    value of the "header-ids" extra key, if any. Otherwise, None.
@param n {int} (unused) The <hN> tag number, i.e. `1` for an <h1> tag.
@returns {str} The value for the header tag's "id" attribute. Return
    None to not have an id attribute and to exclude this header from
    the TOC (if the "toc" extra is specified).

<a id="markdown2.MarkdownWithExtras"></a>

## MarkdownWithExtras Objects

```python
class MarkdownWithExtras(Markdown)
```

A markdowner class that enables most extras:

- footnotes
- fenced-code-blocks (only highlights code if 'pygments' Python module on path)

These are not included:
- pyshell (specific to Python-related documenting)
- code-friendly (because it *disables* part of the syntax)
- link-patterns (because you need to specify some actual
  link-patterns anyway)

<a id="markdown2.MarkdownWithExtras.extras"></a>

#### extras

type: ignore

<a id="markdown2.Extra"></a>

## Extra Objects

```python
class Extra(ABC)
```

<a id="markdown2.Extra.name"></a>

#### name

An identifiable name that users can use to invoke the extra
in the Markdown class

<a id="markdown2.Extra.order"></a>

#### order

Tuple of two iterables containing the stages/extras this extra will run before and
after, respectively

<a id="markdown2.Extra.__init__"></a>

#### \_\_init\_\_

```python
def __init__(md: Markdown, options: Optional[dict])
```

**Arguments**:

- `md` - An instance of `Markdown`
- `options` - a dict of settings to alter the extra's behaviour

<a id="markdown2.Extra.deregister"></a>

#### deregister

```python
@classmethod
def deregister(cls)
```

Removes the class from the extras registry and unsets its execution order.

<a id="markdown2.Extra.register"></a>

#### register

```python
@classmethod
def register(cls)
```

Registers the class for use with `Markdown` and calculates its execution order based on
the `order` class attribute.

<a id="markdown2.Extra.run"></a>

#### run

```python
@abstractmethod
def run(text: str) -> str
```

Run the extra against the given text.

**Returns**:

  The new text after being modified by the extra

<a id="markdown2.Extra.test"></a>

#### test

```python
def test(text: str) -> bool
```

Check a section of markdown to see if this extra should be run upon it.
The default implementation will always return True but it's recommended to override
this behaviour to improve performance.

<a id="markdown2.ItalicAndBoldProcessor"></a>

## ItalicAndBoldProcessor Objects

```python
class ItalicAndBoldProcessor(Extra)
```

An ABC that provides hooks for dealing with italics and bold syntax.
This class is set to trigger both before AND after the italics and bold stage.
This allows any child classes to intercept instances of bold or italic syntax and
change the output or hash it to prevent it from being processed.

After the I&B stage any hashes in the `hash_tables` instance variable are replaced.

<a id="markdown2._LinkProcessorExtraOpts"></a>

## \_LinkProcessorExtraOpts Objects

```python
class _LinkProcessorExtraOpts(TypedDict)
```

Options for the `LinkProcessor` extra

<a id="markdown2._LinkProcessorExtraOpts.tags"></a>

#### tags

List of tags to be processed by the extra. Default is `['a', 'img']`

<a id="markdown2._LinkProcessorExtraOpts.inline"></a>

#### inline

Whether to process inline links. Default: True

<a id="markdown2._LinkProcessorExtraOpts.ref"></a>

#### ref

Whether to process reference links. Default: True

<a id="markdown2.LinkProcessor"></a>

## LinkProcessor Objects

```python
class LinkProcessor(Extra)
```

<a id="markdown2.LinkProcessor.parse_inline_anchor_or_image"></a>

#### parse\_inline\_anchor\_or\_image

```python
def parse_inline_anchor_or_image(
        text: str, _link_text: str,
        start_idx: int) -> Optional[Tuple[str, str, Optional[str], int]]
```

Parse a string and extract a link from it. This can be an inline anchor or an image.

**Arguments**:

- `text` - the whole text containing the link
- `link_text` - the human readable text inside the link
- `start_idx` - the index of the link within `text`
  

**Returns**:

  None if a link was not able to be parsed from `text`.
  If successful, a tuple is returned containing:
  
  1. potentially modified version of the `text` param
  2. the URL
  3. the title (can be None if not present)
  4. the index where the link ends within text

<a id="markdown2.LinkProcessor.process_link_shortrefs"></a>

#### process\_link\_shortrefs

```python
def process_link_shortrefs(text: str, link_text: str,
                           start_idx: int) -> Tuple[Optional[re.Match], str]
```

Detects shortref links within a string and converts them to normal references

**Arguments**:

- `text` - the whole text containing the link
- `link_text` - the human readable text inside the link
- `start_idx` - the index of the link within `text`
  

**Returns**:

  A tuple containing:
  
  1. A potential `re.Match` against the link reference within `text` (will be None if not found)
  2. potentially modified version of the `text` param

<a id="markdown2.LinkProcessor.parse_ref_anchor_or_ref_image"></a>

#### parse\_ref\_anchor\_or\_ref\_image

```python
def parse_ref_anchor_or_ref_image(
        text: str, link_text: str, start_idx: int
) -> Optional[Tuple[str, Optional[str], Optional[str], int]]
```

Parse a string and extract a link from it. This can be a reference anchor or image.

**Arguments**:

- `text` - the whole text containing the link
- `link_text` - the human readable text inside the link
- `start_idx` - the index of the link within `text`
  

**Returns**:

  None if a link was not able to be parsed from `text`.
  If successful, a tuple is returned containing:
  
  1. potentially modified version of the `text` param
  2. the URL (can be None if the reference doesn't exist)
  3. the title (can be None if not present)
  4. the index where the link ends within text

<a id="markdown2.LinkProcessor.process_image"></a>

#### process\_image

```python
def process_image(url: str, title_attr: str,
                  link_text: str) -> Tuple[str, int]
```

Takes a URL, title and link text and returns an HTML `<img>` tag

**Arguments**:

- `url` - the image URL/src
- `title_attr` - a string containing the title attribute of the tag (eg: `' title="..."'`)
- `link_text` - the human readable text portion of the link
  

**Returns**:

  A tuple containing:
  
  1. The HTML string
  2. The length of the opening HTML tag in the string. For `<img>` it's the whole string.
  This section will be skipped by the link processor

<a id="markdown2.LinkProcessor.process_anchor"></a>

#### process\_anchor

```python
def process_anchor(url: str, title_attr: str,
                   link_text: str) -> Tuple[str, int]
```

Takes a URL, title and link text and returns an HTML `<a>` tag

**Arguments**:

- `url` - the URL
- `title_attr` - a string containing the title attribute of the tag (eg: `' title="..."'`)
- `link_text` - the human readable text portion of the link
  

**Returns**:

  A tuple containing:
  
  1. The HTML string
  2. The length of the opening HTML tag in the string. This section will be skipped
  by the link processor

<a id="markdown2.Admonitions"></a>

## Admonitions Objects

```python
class Admonitions(Extra)
```

Enable parsing of RST admonitions

<a id="markdown2.Alerts"></a>

## Alerts Objects

```python
class Alerts(Extra)
```

Markdown Alerts as per
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts

<a id="markdown2._BreaksExtraOpts"></a>

## \_BreaksExtraOpts Objects

```python
class _BreaksExtraOpts(TypedDict)
```

Options for the `Breaks` extra

<a id="markdown2._BreaksExtraOpts.on_backslash"></a>

#### on\_backslash

Replace backslashes at the end of a line with <br>

<a id="markdown2._BreaksExtraOpts.on_newline"></a>

#### on\_newline

Replace single new line characters with <br> when True

<a id="markdown2.CodeFriendly"></a>

## CodeFriendly Objects

```python
class CodeFriendly(ItalicAndBoldProcessor)
```

Disable _ and __ for em and strong.

<a id="markdown2.FencedCodeBlocks"></a>

## FencedCodeBlocks Objects

```python
class FencedCodeBlocks(Extra)
```

Allows a code block to not have to be indented
by fencing it with '```' on a line before and after. Based on
<http://github.github.com/github-flavored-markdown/> with support for
syntax highlighting.

<a id="markdown2.FencedCodeBlocks.tags"></a>

#### tags

```python
def tags(lexer_name: str) -> tuple[str, str]
```

Returns the tags that the encoded code block will be wrapped in, based
upon the lexer name.

This function can be overridden by subclasses to piggy-back off of the
fenced code blocks syntax (see `Mermaid` extra).

**Returns**:

  The opening and closing tags, as strings within a tuple

<a id="markdown2.Latex"></a>

## Latex Objects

```python
class Latex(Extra)
```

Convert $ and $$ to <math> and </math> tags for inline and block math.

<a id="markdown2.LinkPatterns"></a>

## LinkPatterns Objects

```python
class LinkPatterns(Extra)
```

Auto-link given regex patterns in text (e.g. bug number
references, revision number references).

<a id="markdown2.MarkdownInHTML"></a>

## MarkdownInHTML Objects

```python
class MarkdownInHTML(Extra)
```

Allow the use of `markdown="1"` in a block HTML tag to
have markdown processing be done on its contents. Similar to
<http://michelf.com/projects/php-markdown/extra/`markdown`-attr> but with
some limitations.

<a id="markdown2._MarkdownFileLinksExtraOpts"></a>

## \_MarkdownFileLinksExtraOpts Objects

```python
class _MarkdownFileLinksExtraOpts(_LinkProcessorExtraOpts)
```

Options for the `MarkdownFileLinks` extra

<a id="markdown2._MarkdownFileLinksExtraOpts.link_defs"></a>

#### link\_defs

Whether to convert link definitions as well. Default: True

<a id="markdown2.MarkdownFileLinks"></a>

## MarkdownFileLinks Objects

```python
class MarkdownFileLinks(LinkProcessor)
```

Replace links to `.md` files with `.html` links

<a id="markdown2.MiddleWordEm"></a>

## MiddleWordEm Objects

```python
class MiddleWordEm(ItalicAndBoldProcessor)
```

Allows or disallows emphasis syntax in the middle of words,
defaulting to allow. Disabling this means that `this_text_here` will not be
converted to `this<em>text</em>here`.

<a id="markdown2.MiddleWordEm.__init__"></a>

#### \_\_init\_\_

```python
def __init__(md: Markdown, options: Union[dict, bool, None])
```

**Arguments**:

- `md` - the markdown instance
- `options` - can be bool for backwards compatibility but will be converted to a dict
  in the constructor. All options are:
  - allowed (bool): whether to allow emphasis in the middle of a word.
  If `options` is a bool it will be placed under this key.

<a id="markdown2.Numbering"></a>

## Numbering Objects

```python
class Numbering(Extra)
```

Support of generic counters.  Non standard extension to
allow sequential numbering of figures, tables, equations, exhibits etc.

<a id="markdown2.PyShell"></a>

## PyShell Objects

```python
class PyShell(Extra)
```

Treats unindented Python interactive shell sessions as <code>
blocks.

<a id="markdown2.SmartyPants"></a>

## SmartyPants Objects

```python
class SmartyPants(Extra)
```

Replaces ' and " with curly quotation marks or curly
apostrophes.  Replaces --, ---, ..., and . . . with en dashes, em dashes,
and ellipses.

<a id="markdown2.SmartyPants.run"></a>

#### run

```python
def run(text)
```

Fancifies 'single quotes', "double quotes", and apostrophes.
Converts --, ---, and ... into en dashes, em dashes, and ellipses.

Inspiration is: <http://daringfireball.net/projects/smartypants/>
See "test/tm-cases/smarty_pants.text" for a full discussion of the
support here and
<http://code.google.com/p/python-markdown2/issues/detail?id=42> for a
discussion of some diversion from the original SmartyPants.

<a id="markdown2.Strike"></a>

## Strike Objects

```python
class Strike(Extra)
```

Text inside of double tilde is ~~strikethrough~~

<a id="markdown2.Tables"></a>

## Tables Objects

```python
class Tables(Extra)
```

Tables using the same format as GFM
<https://help.github.com/articles/github-flavored-markdown#tables> and
PHP-Markdown Extra <https://michelf.ca/projects/php-markdown/extra/`table`>.

<a id="markdown2.Tables.run"></a>

#### run

```python
def run(text)
```

Copying PHP-Markdown and GFM table syntax. Some regex borrowed from
https://github.com/michelf/php-markdown/blob/lib/Michelf/Markdown.php#L2538

<a id="markdown2.Underline"></a>

## Underline Objects

```python
class Underline(Extra)
```

Text inside of double dash is --underlined--.

<a id="markdown2._WavedromExtraOpts"></a>

## \_WavedromExtraOpts Objects

```python
class _WavedromExtraOpts(TypedDict)
```

Options for the `Wavedrom` extra

<a id="markdown2._WavedromExtraOpts.prefer_embed_svg"></a>

#### prefer\_embed\_svg

Use the `wavedrom` library to convert diagrams to SVGs and embed them directly.
This will only work if the `wavedrom` library has been installed.

Defaults to `True`

<a id="markdown2.Wavedrom"></a>

## Wavedrom Objects

```python
class Wavedrom(Extra)
```

Support for generating Wavedrom digital timing diagrams

<a id="markdown2.WikiTables"></a>

## WikiTables Objects

```python
class WikiTables(Extra)
```

Google Code Wiki-style tables. See
<http://code.google.com/p/support/wiki/WikiSyntax#Tables>.

<a id="markdown2.calculate_toc_html"></a>

#### calculate\_toc\_html

```python
def calculate_toc_html(
        toc: Union[list[tuple[int, str, str]], None]) -> Optional[str]
```

Return the HTML for the current TOC.

This expects the `_toc` attribute to have been set on this instance.

<a id="markdown2.UnicodeWithAttrs"></a>

## UnicodeWithAttrs Objects

```python
class UnicodeWithAttrs(str)
```

A subclass of unicode used for the return value of conversion to
possibly attach some attributes. E.g. the "toc_html" attribute when
the "toc" extra is used.

<a id="markdown2._memoized"></a>

## \_memoized Objects

```python
class _memoized()
```

Decorator that caches a function's return value each time it is called.
If called later with the same arguments, the cached value is returned, and
not re-evaluated.

http://wiki.python.org/moin/PythonDecoratorLibrary

<a id="markdown2._memoized.__repr__"></a>

#### \_\_repr\_\_

```python
def __repr__()
```

Return the function's docstring.

