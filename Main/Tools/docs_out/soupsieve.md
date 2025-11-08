# Table of Contents

* [soupsieve](#soupsieve)
  * [compile](#soupsieve.compile)
  * [purge](#soupsieve.purge)
  * [closest](#soupsieve.closest)
  * [match](#soupsieve.match)
  * [filter](#soupsieve.filter)
  * [select\_one](#soupsieve.select_one)
  * [select](#soupsieve.select)
  * [iselect](#soupsieve.iselect)
  * [escape](#soupsieve.escape)

<a id="soupsieve"></a>

# soupsieve

Soup Sieve.

A CSS selector filter for BeautifulSoup4.

MIT License

Copyright (c) 2018 Isaac Muse

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<a id="soupsieve.compile"></a>

#### compile

```python
def compile(pattern: str,
            namespaces: dict[str, str] | None = None,
            flags: int = 0,
            *,
            custom: dict[str, str] | None = None,
            **kwargs: Any) -> cm.SoupSieve
```

Compile CSS pattern.

<a id="soupsieve.purge"></a>

#### purge

```python
def purge() -> None
```

Purge cached patterns.

<a id="soupsieve.closest"></a>

#### closest

```python
def closest(select: str,
            tag: bs4.Tag,
            namespaces: dict[str, str] | None = None,
            flags: int = 0,
            *,
            custom: dict[str, str] | None = None,
            **kwargs: Any) -> bs4.Tag | None
```

Match closest ancestor.

<a id="soupsieve.match"></a>

#### match

```python
def match(select: str,
          tag: bs4.Tag,
          namespaces: dict[str, str] | None = None,
          flags: int = 0,
          *,
          custom: dict[str, str] | None = None,
          **kwargs: Any) -> bool
```

Match node.

<a id="soupsieve.filter"></a>

#### filter

```python
def filter(select: str,
           iterable: Iterable[bs4.Tag],
           namespaces: dict[str, str] | None = None,
           flags: int = 0,
           *,
           custom: dict[str, str] | None = None,
           **kwargs: Any) -> list[bs4.Tag]
```

Filter list of nodes.

<a id="soupsieve.select_one"></a>

#### select\_one

```python
def select_one(select: str,
               tag: bs4.Tag,
               namespaces: dict[str, str] | None = None,
               flags: int = 0,
               *,
               custom: dict[str, str] | None = None,
               **kwargs: Any) -> bs4.Tag | None
```

Select a single tag.

<a id="soupsieve.select"></a>

#### select

```python
def select(select: str,
           tag: bs4.Tag,
           namespaces: dict[str, str] | None = None,
           limit: int = 0,
           flags: int = 0,
           *,
           custom: dict[str, str] | None = None,
           **kwargs: Any) -> list[bs4.Tag]
```

Select the specified tags.

<a id="soupsieve.iselect"></a>

#### iselect

```python
def iselect(select: str,
            tag: bs4.Tag,
            namespaces: dict[str, str] | None = None,
            limit: int = 0,
            flags: int = 0,
            *,
            custom: dict[str, str] | None = None,
            **kwargs: Any) -> Iterator[bs4.Tag]
```

Iterate the specified tags.

<a id="soupsieve.escape"></a>

#### escape

```python
def escape(ident: str) -> str
```

Escape identifier.

