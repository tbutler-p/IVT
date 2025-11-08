# Table of Contents

* [jsonref](#jsonref)
  * [JsonRef](#jsonref.JsonRef)
    * [replace\_refs](#jsonref.JsonRef.replace_refs)
    * [resolve\_pointer](#jsonref.JsonRef.resolve_pointer)
  * [URIDict](#jsonref.URIDict)
  * [jsonloader](#jsonref.jsonloader)
  * [replace\_refs](#jsonref.replace_refs)
  * [load](#jsonref.load)
  * [loads](#jsonref.loads)
  * [load\_uri](#jsonref.load_uri)
  * [dump](#jsonref.dump)
  * [dumps](#jsonref.dumps)

<a id="jsonref"></a>

# jsonref

<a id="jsonref.JsonRef"></a>

## JsonRef Objects

```python
class JsonRef(LazyProxy)
```

A lazy loading proxy to the dereferenced data pointed to by a JSON
Reference object.

<a id="jsonref.JsonRef.replace_refs"></a>

#### replace\_refs

```python
@classmethod
def replace_refs(cls,
                 obj,
                 base_uri="",
                 loader=None,
                 jsonschema=False,
                 load_on_repr=True)
```

.. deprecated:: 0.4

Use :func:`replace_refs` instead.

Returns a deep copy of `obj` with all contained JSON reference objects
replaced with :class:`JsonRef` instances.

**Arguments**:

- `obj`: If this is a JSON reference object, a :class:`JsonRef`
instance will be created. If `obj` is not a JSON reference object,
a deep copy of it will be created with all contained JSON
reference objects replaced by :class:`JsonRef` instances
- `base_uri`: URI to resolve relative references against
- `loader`: Callable that takes a URI and returns the parsed JSON
(defaults to global ``jsonloader``)
- `jsonschema`: Flag to turn on `JSON Schema mode
<http://json-schema.org/latest/json-schema-core.html#anchor25>`_.
'id' keyword changes the `base_uri` for references contained within
the object
- `load_on_repr`: If set to ``False``, :func:`repr` call on a
:class:`JsonRef` object will not cause the reference to be loaded
if it hasn't already. (defaults to ``True``)

<a id="jsonref.JsonRef.resolve_pointer"></a>

#### resolve\_pointer

```python
def resolve_pointer(document, pointer)
```

Resolve a json pointer ``pointer`` within the referenced ``document``.

**Arguments**:

- `document`: the referent document
- `pointer` (`str`): a json pointer URI fragment to resolve within it

<a id="jsonref.URIDict"></a>

## URIDict Objects

```python
class URIDict(MutableMapping)
```

Dictionary which uses normalized URIs as keys.

<a id="jsonref.jsonloader"></a>

#### jsonloader

```python
def jsonloader(uri, **kwargs)
```

Provides a callable which takes a URI, and returns the loaded JSON referred
to by that URI. Uses :mod:`requests` if available for HTTP URIs, and falls
back to :mod:`urllib`.

<a id="jsonref.replace_refs"></a>

#### replace\_refs

```python
def replace_refs(obj,
                 base_uri="",
                 loader=jsonloader,
                 jsonschema=False,
                 load_on_repr=True,
                 merge_props=False,
                 proxies=True,
                 lazy_load=True)
```

Returns a deep copy of `obj` with all contained JSON reference objects

replaced with :class:`JsonRef` instances.

**Arguments**:

- `obj`: If this is a JSON reference object, a :class:`JsonRef`
instance will be created. If `obj` is not a JSON reference object,
a deep copy of it will be created with all contained JSON
reference objects replaced by :class:`JsonRef` instances
- `base_uri`: URI to resolve relative references against
- `loader`: Callable that takes a URI and returns the parsed JSON
(defaults to global ``jsonloader``, a :class:`JsonLoader` instance)
- `jsonschema`: Flag to turn on `JSON Schema mode
<http://json-schema.org/latest/json-schema-core.html#anchor25>`_.
'id' or '$id' keyword changes the `base_uri` for references contained
within the object
- `load_on_repr`: If set to ``False``, :func:`repr` call on a
:class:`JsonRef` object will not cause the reference to be loaded
if it hasn't already. (defaults to ``True``)
- `merge_props`: When ``True``, JSON reference objects that
have extra keys other than '$ref' in them will be merged into the
document resolved by the reference (if it is a dictionary.) NOTE: This
is not part of the JSON Reference spec, and may not behave the same as
other libraries.
- `proxies`: If `True`, references will be replaced with transparent
proxy objects. Otherwise, they will be replaced directly with the
referred data. (defaults to ``True``)
- `lazy_load`: When proxy objects are used, and this is `True`, the
references will not be resolved until that section of the JSON
document is accessed. (defaults to ``True``)

<a id="jsonref.load"></a>

#### load

```python
def load(fp,
         base_uri="",
         loader=None,
         jsonschema=False,
         load_on_repr=True,
         merge_props=False,
         proxies=True,
         lazy_load=True,
         **kwargs)
```

Drop in replacement for :func:`json.load`, where JSON references are

proxied to their referent data.

**Arguments**:

- `fp`: File-like object containing JSON document
- `**kwargs`: This function takes any of the keyword arguments from
:func:`replace_refs`. Any other keyword arguments will be passed to
:func:`json.load`

<a id="jsonref.loads"></a>

#### loads

```python
def loads(s,
          base_uri="",
          loader=None,
          jsonschema=False,
          load_on_repr=True,
          merge_props=False,
          proxies=True,
          lazy_load=True,
          **kwargs)
```

Drop in replacement for :func:`json.loads`, where JSON references are

proxied to their referent data.

**Arguments**:

- `s`: String containing JSON document
- `**kwargs`: This function takes any of the keyword arguments from
:func:`replace_refs`. Any other keyword arguments will be passed to
:func:`json.loads`

<a id="jsonref.load_uri"></a>

#### load\_uri

```python
def load_uri(uri,
             base_uri=None,
             loader=None,
             jsonschema=False,
             load_on_repr=True,
             merge_props=False,
             proxies=True,
             lazy_load=True)
```

Load JSON data from ``uri`` with JSON references proxied to their referent

data.

**Arguments**:

- `uri`: URI to fetch the JSON from
- `**kwargs`: This function takes any of the keyword arguments from
:func:`replace_refs`

<a id="jsonref.dump"></a>

#### dump

```python
def dump(obj, fp, **kwargs)
```

Serialize `obj`, which may contain :class:`JsonRef` objects, as a JSON

formatted stream to file-like `fp`. `JsonRef` objects will be dumped as the
original reference object they were created from.

**Arguments**:

- `obj`: Object to serialize
- `fp`: File-like to output JSON string
- `kwargs`: Keyword arguments are the same as to :func:`json.dump`

<a id="jsonref.dumps"></a>

#### dumps

```python
def dumps(obj, **kwargs)
```

Serialize `obj`, which may contain :class:`JsonRef` objects, to a JSON

formatted string. `JsonRef` objects will be dumped as the original
reference object they were created from.

**Arguments**:

- `obj`: Object to serialize
- `kwargs`: Keyword arguments are the same as to :func:`json.dumps`

