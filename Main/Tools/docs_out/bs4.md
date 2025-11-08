# Table of Contents

* [bs4](#bs4)
  * [BeautifulSoup](#bs4.BeautifulSoup)
    * [ROOT\_TAG\_NAME](#bs4.BeautifulSoup.ROOT_TAG_NAME)
    * [DEFAULT\_BUILDER\_FEATURES](#bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES)
    * [ASCII\_SPACES](#bs4.BeautifulSoup.ASCII_SPACES)
    * [element\_classes](#bs4.BeautifulSoup.element_classes)
    * [builder](#bs4.BeautifulSoup.builder)
    * [parse\_only](#bs4.BeautifulSoup.parse_only)
    * [markup](#bs4.BeautifulSoup.markup)
    * [current\_data](#bs4.BeautifulSoup.current_data)
    * [currentTag](#bs4.BeautifulSoup.currentTag)
    * [tagStack](#bs4.BeautifulSoup.tagStack)
    * [open\_tag\_counter](#bs4.BeautifulSoup.open_tag_counter)
    * [preserve\_whitespace\_tag\_stack](#bs4.BeautifulSoup.preserve_whitespace_tag_stack)
    * [string\_container\_stack](#bs4.BeautifulSoup.string_container_stack)
    * [original\_encoding](#bs4.BeautifulSoup.original_encoding)
    * [declared\_html\_encoding](#bs4.BeautifulSoup.declared_html_encoding)
    * [contains\_replacement\_characters](#bs4.BeautifulSoup.contains_replacement_characters)
    * [\_\_init\_\_](#bs4.BeautifulSoup.__init__)
    * [copy\_self](#bs4.BeautifulSoup.copy_self)
    * [reset](#bs4.BeautifulSoup.reset)
    * [new\_tag](#bs4.BeautifulSoup.new_tag)
    * [string\_container](#bs4.BeautifulSoup.string_container)
    * [new\_string](#bs4.BeautifulSoup.new_string)
    * [insert\_before](#bs4.BeautifulSoup.insert_before)
    * [insert\_after](#bs4.BeautifulSoup.insert_after)
    * [popTag](#bs4.BeautifulSoup.popTag)
    * [pushTag](#bs4.BeautifulSoup.pushTag)
    * [endData](#bs4.BeautifulSoup.endData)
    * [object\_was\_parsed](#bs4.BeautifulSoup.object_was_parsed)
    * [handle\_starttag](#bs4.BeautifulSoup.handle_starttag)
    * [handle\_endtag](#bs4.BeautifulSoup.handle_endtag)
    * [handle\_data](#bs4.BeautifulSoup.handle_data)
    * [decode](#bs4.BeautifulSoup.decode)
  * [BeautifulStoneSoup](#bs4.BeautifulStoneSoup)

<a id="bs4"></a>

# bs4

Beautiful Soup Elixir and Tonic - "The Screen-Scraper's Friend".

http://www.crummy.com/software/BeautifulSoup/

Beautiful Soup uses a pluggable XML or HTML parser to parse a
(possibly invalid) document into a tree representation. Beautiful Soup
provides methods and Pythonic idioms that make it easy to navigate,
search, and modify the parse tree.

Beautiful Soup works with Python 3.7 and up. It works better if lxml
and/or html5lib is installed, but they are not required.

For more than you ever wanted to know about Beautiful Soup, see the
documentation: http://www.crummy.com/software/BeautifulSoup/bs4/doc/

<a id="bs4.BeautifulSoup"></a>

## BeautifulSoup Objects

```python
class BeautifulSoup(Tag)
```

A data structure representing a parsed HTML or XML document.

Most of the methods you'll call on a BeautifulSoup object are inherited from
PageElement or Tag.

Internally, this class defines the basic interface called by the
tree builders when converting an HTML/XML document into a data
structure. The interface abstracts away the differences between
parsers. To write a new tree builder, you'll need to understand
these methods as a whole.

These methods will be called by the BeautifulSoup constructor:
  * reset()
  * feed(markup)

The tree builder may call these methods from its feed() implementation:
  * handle_starttag(name, attrs) # See note about return value
  * handle_endtag(name)
  * handle_data(data) # Appends to the current data node
  * endData(containerClass) # Ends the current data node

No matter how complicated the underlying parser is, you should be
able to build a tree using 'start tag' events, 'end tag' events,
'data' events, and "done with data" events.

If you encounter an empty-element tag (aka a self-closing tag,
like HTML's <br> tag), call handle_starttag and then
handle_endtag.

<a id="bs4.BeautifulSoup.ROOT_TAG_NAME"></a>

#### ROOT\_TAG\_NAME

Since `BeautifulSoup` subclasses `Tag`, it's possible to treat it as
a `Tag` with a `Tag.name`. Hoever, this name makes it clear the
`BeautifulSoup` object isn't a real markup tag.

<a id="bs4.BeautifulSoup.DEFAULT_BUILDER_FEATURES"></a>

#### DEFAULT\_BUILDER\_FEATURES

If the end-user gives no indication which tree builder they
want, look for one with these features.

<a id="bs4.BeautifulSoup.ASCII_SPACES"></a>

#### ASCII\_SPACES

A string containing all ASCII whitespace characters, used in
during parsing to detect data chunks that seem 'empty'.

<a id="bs4.BeautifulSoup.element_classes"></a>

#### element\_classes

:meta private:

<a id="bs4.BeautifulSoup.builder"></a>

#### builder

:meta private:

<a id="bs4.BeautifulSoup.parse_only"></a>

#### parse\_only

:meta private:

<a id="bs4.BeautifulSoup.markup"></a>

#### markup

:meta private:

<a id="bs4.BeautifulSoup.current_data"></a>

#### current\_data

:meta private:

<a id="bs4.BeautifulSoup.currentTag"></a>

#### currentTag

:meta private:

<a id="bs4.BeautifulSoup.tagStack"></a>

#### tagStack

:meta private:

<a id="bs4.BeautifulSoup.open_tag_counter"></a>

#### open\_tag\_counter

:meta private:

<a id="bs4.BeautifulSoup.preserve_whitespace_tag_stack"></a>

#### preserve\_whitespace\_tag\_stack

:meta private:

<a id="bs4.BeautifulSoup.string_container_stack"></a>

#### string\_container\_stack

:meta private:

<a id="bs4.BeautifulSoup.original_encoding"></a>

#### original\_encoding

Beautiful Soup's best guess as to the character encoding of the
original document.

<a id="bs4.BeautifulSoup.declared_html_encoding"></a>

#### declared\_html\_encoding

The character encoding, if any, that was explicitly defined
in the original document. This may or may not match
`BeautifulSoup.original_encoding`.

<a id="bs4.BeautifulSoup.contains_replacement_characters"></a>

#### contains\_replacement\_characters

This is True if the markup that was parsed contains
U+FFFD REPLACEMENT_CHARACTER characters which were not present
in the original markup. These mark character sequences that
could not be represented in Unicode.

<a id="bs4.BeautifulSoup.__init__"></a>

#### \_\_init\_\_

```python
def __init__(markup: _IncomingMarkup = "",
             features: Optional[Union[str, Sequence[str]]] = None,
             builder: Optional[Union[TreeBuilder, Type[TreeBuilder]]] = None,
             parse_only: Optional[SoupStrainer] = None,
             from_encoding: Optional[_Encoding] = None,
             exclude_encodings: Optional[_Encodings] = None,
             element_classes: Optional[Dict[Type[PageElement],
                                            Type[PageElement]]] = None,
             **kwargs: Any)
```

Constructor.

**Arguments**:

- `markup`: A string or a file-like object representing
markup to be parsed.
- `features`: Desirable features of the parser to be
used. This may be the name of a specific parser ("lxml",
"lxml-xml", "html.parser", or "html5lib") or it may be the
type of markup to be used ("html", "html5", "xml"). It's
recommended that you name a specific parser, so that
Beautiful Soup gives you the same results across platforms
and virtual environments.
- `builder`: A TreeBuilder subclass to instantiate (or
instance to use) instead of looking one up based on
`features`. You only need to use this if you've implemented a
custom TreeBuilder.
- `parse_only`: A SoupStrainer. Only parts of the document
matching the SoupStrainer will be considered. This is useful
when parsing part of a document that would otherwise be too
large to fit into memory.
- `from_encoding`: A string indicating the encoding of the
document to be parsed. Pass this in if Beautiful Soup is
guessing wrongly about the document's encoding.
- `exclude_encodings`: A list of strings indicating
encodings known to be wrong. Pass this in if you don't know
the document's encoding but you know Beautiful Soup's guess is
wrong.
- `element_classes`: A dictionary mapping BeautifulSoup
classes like Tag and NavigableString, to other classes you'd
like to be instantiated instead as the parse tree is
built. This is useful for subclassing Tag or NavigableString
to modify default behavior.
- `kwargs`: For backwards compatibility purposes, the
constructor accepts certain keyword arguments used in
Beautiful Soup 3. None of these arguments do anything in
Beautiful Soup 4; they will result in a warning and then be
ignored.

Apart from this, any keyword arguments passed into the
BeautifulSoup constructor are propagated to the TreeBuilder
constructor. This makes it possible to configure a
TreeBuilder by passing in arguments, not just by saying which
one to use.

<a id="bs4.BeautifulSoup.copy_self"></a>

#### copy\_self

```python
def copy_self() -> "BeautifulSoup"
```

Create a new BeautifulSoup object with the same TreeBuilder,
but not associated with any markup.

This is the first step of the deepcopy process.

<a id="bs4.BeautifulSoup.reset"></a>

#### reset

```python
def reset() -> None
```

Reset this object to a state as though it had never parsed any
markup.

<a id="bs4.BeautifulSoup.new_tag"></a>

#### new\_tag

```python
def new_tag(name: str,
            namespace: Optional[str] = None,
            nsprefix: Optional[str] = None,
            attrs: Optional[_RawAttributeValues] = None,
            sourceline: Optional[int] = None,
            sourcepos: Optional[int] = None,
            string: Optional[str] = None,
            **kwattrs: _RawAttributeValue) -> Tag
```

Create a new Tag associated with this BeautifulSoup object.

**Arguments**:

- `name`: The name of the new Tag.
- `namespace`: The URI of the new Tag's XML namespace, if any.
- `prefix`: The prefix for the new Tag's XML namespace, if any.
- `attrs`: A dictionary of this Tag's attribute values; can
be used instead of ``kwattrs`` for attributes like 'class'
that are reserved words in Python.
- `sourceline`: The line number where this tag was
(purportedly) found in its source document.
- `sourcepos`: The character position within ``sourceline`` where this
tag was (purportedly) found.
- `string`: String content for the new Tag, if any.
- `kwattrs`: Keyword arguments for the new Tag's attribute values.

<a id="bs4.BeautifulSoup.string_container"></a>

#### string\_container

```python
def string_container(
    base_class: Optional[Type[NavigableString]] = None
) -> Type[NavigableString]
```

Find the class that should be instantiated to hold a given kind of
string.

This may be a built-in Beautiful Soup class or a custom class passed
in to the BeautifulSoup constructor.

<a id="bs4.BeautifulSoup.new_string"></a>

#### new\_string

```python
def new_string(
        s: str,
        subclass: Optional[Type[NavigableString]] = None) -> NavigableString
```

Create a new `NavigableString` associated with this `BeautifulSoup`

object.

**Arguments**:

- `s`: The string content of the `NavigableString`
- `subclass`: The subclass of `NavigableString`, if any, to
use. If a document is being processed, an appropriate
subclass for the current location in the document will
be determined automatically.

<a id="bs4.BeautifulSoup.insert_before"></a>

#### insert\_before

```python
def insert_before(*args: _InsertableElement) -> List[PageElement]
```

This method is part of the PageElement API, but `BeautifulSoup` doesn't implement
it because there is nothing before or after it in the parse tree.

<a id="bs4.BeautifulSoup.insert_after"></a>

#### insert\_after

```python
def insert_after(*args: _InsertableElement) -> List[PageElement]
```

This method is part of the PageElement API, but `BeautifulSoup` doesn't implement
it because there is nothing before or after it in the parse tree.

<a id="bs4.BeautifulSoup.popTag"></a>

#### popTag

```python
def popTag() -> Optional[Tag]
```

Internal method called by _popToTag when a tag is closed.

:meta private:

<a id="bs4.BeautifulSoup.pushTag"></a>

#### pushTag

```python
def pushTag(tag: Tag) -> None
```

Internal method called by handle_starttag when a tag is opened.

:meta private:

<a id="bs4.BeautifulSoup.endData"></a>

#### endData

```python
def endData(containerClass: Optional[Type[NavigableString]] = None) -> None
```

Method called by the TreeBuilder when the end of a data segment

occurs.

**Arguments**:

- `containerClass`: The class to use when incorporating the
data segment into the parse tree.

<a id="bs4.BeautifulSoup.object_was_parsed"></a>

#### object\_was\_parsed

```python
def object_was_parsed(
        o: PageElement,
        parent: Optional[Tag] = None,
        most_recent_element: Optional[PageElement] = None) -> None
```

Method called by the TreeBuilder to integrate an object into the
parse tree.

:meta private:

<a id="bs4.BeautifulSoup.handle_starttag"></a>

#### handle\_starttag

```python
def handle_starttag(
        name: str,
        namespace: Optional[str],
        nsprefix: Optional[str],
        attrs: _RawAttributeValues,
        sourceline: Optional[int] = None,
        sourcepos: Optional[int] = None,
        namespaces: Optional[Dict[str, str]] = None) -> Optional[Tag]
```

Called by the tree builder when a new tag is encountered.

**Arguments**:

- `name`: Name of the tag.
- `nsprefix`: Namespace prefix for the tag.
- `attrs`: A dictionary of attribute values. Note that
attribute values are expected to be simple strings; processing
of multi-valued attributes such as "class" comes later.
- `sourceline`: The line number where this tag was found in its
source document.
- `sourcepos`: The character position within `sourceline` where this
tag was found.
- `namespaces`: A dictionary of all namespace prefix mappings
currently in scope in the document.

If this method returns None, the tag was rejected by an active
`ElementFilter`. You should proceed as if the tag had not occurred
in the document. For instance, if this was a self-closing tag,
don't call handle_endtag.

<a id="bs4.BeautifulSoup.handle_endtag"></a>

#### handle\_endtag

```python
def handle_endtag(name: str, nsprefix: Optional[str] = None) -> None
```

Called by the tree builder when an ending tag is encountered.

**Arguments**:

- `name`: Name of the tag.
- `nsprefix`: Namespace prefix for the tag.

<a id="bs4.BeautifulSoup.handle_data"></a>

#### handle\_data

```python
def handle_data(data: str) -> None
```

Called by the tree builder when a chunk of textual data is
encountered.

:meta private:

<a id="bs4.BeautifulSoup.decode"></a>

#### decode

```python
def decode(indent_level: Optional[int] = None,
           eventual_encoding: _Encoding = DEFAULT_OUTPUT_ENCODING,
           formatter: Union[Formatter, str] = "minimal",
           iterator: Optional[Iterator[PageElement]] = None,
           **kwargs: Any) -> str
```

Returns a string representation of the parse tree

as a full HTML or XML document.

**Arguments**:

- `indent_level`: Each line of the rendering will be
indented this many levels. (The ``formatter`` decides what a
'level' means, in terms of spaces or other characters
output.) This is used internally in recursive calls while
pretty-printing.
- `eventual_encoding`: The encoding of the final document.
If this is None, the document will be a Unicode string.
- `formatter`: Either a `Formatter` object, or a string naming one of
the standard formatters.
- `iterator`: The iterator to use when navigating over the
parse tree. This is only used by `Tag.decode_contents` and
you probably won't need to use it.

<a id="bs4.BeautifulStoneSoup"></a>

## BeautifulStoneSoup Objects

```python
class BeautifulStoneSoup(BeautifulSoup)
```

Deprecated interface to an XML parser.

