# Table of Contents

* [yaml](#yaml)
  * [scan](#yaml.scan)
  * [parse](#yaml.parse)
  * [compose](#yaml.compose)
  * [compose\_all](#yaml.compose_all)
  * [load](#yaml.load)
  * [load\_all](#yaml.load_all)
  * [full\_load](#yaml.full_load)
  * [full\_load\_all](#yaml.full_load_all)
  * [safe\_load](#yaml.safe_load)
  * [safe\_load\_all](#yaml.safe_load_all)
  * [unsafe\_load](#yaml.unsafe_load)
  * [unsafe\_load\_all](#yaml.unsafe_load_all)
  * [emit](#yaml.emit)
  * [serialize\_all](#yaml.serialize_all)
  * [serialize](#yaml.serialize)
  * [dump\_all](#yaml.dump_all)
  * [dump](#yaml.dump)
  * [safe\_dump\_all](#yaml.safe_dump_all)
  * [safe\_dump](#yaml.safe_dump)
  * [add\_implicit\_resolver](#yaml.add_implicit_resolver)
  * [add\_path\_resolver](#yaml.add_path_resolver)
  * [add\_constructor](#yaml.add_constructor)
  * [add\_multi\_constructor](#yaml.add_multi_constructor)
  * [add\_representer](#yaml.add_representer)
  * [add\_multi\_representer](#yaml.add_multi_representer)
  * [YAMLObjectMetaclass](#yaml.YAMLObjectMetaclass)
  * [YAMLObject](#yaml.YAMLObject)
    * [\_\_slots\_\_](#yaml.YAMLObject.__slots__)
    * [from\_yaml](#yaml.YAMLObject.from_yaml)
    * [to\_yaml](#yaml.YAMLObject.to_yaml)

<a id="yaml"></a>

# yaml

<a id="yaml.scan"></a>

#### scan

```python
def scan(stream, Loader=Loader)
```

Scan a YAML stream and produce scanning tokens.

<a id="yaml.parse"></a>

#### parse

```python
def parse(stream, Loader=Loader)
```

Parse a YAML stream and produce parsing events.

<a id="yaml.compose"></a>

#### compose

```python
def compose(stream, Loader=Loader)
```

Parse the first YAML document in a stream
and produce the corresponding representation tree.

<a id="yaml.compose_all"></a>

#### compose\_all

```python
def compose_all(stream, Loader=Loader)
```

Parse all YAML documents in a stream
and produce corresponding representation trees.

<a id="yaml.load"></a>

#### load

```python
def load(stream, Loader)
```

Parse the first YAML document in a stream
and produce the corresponding Python object.

<a id="yaml.load_all"></a>

#### load\_all

```python
def load_all(stream, Loader)
```

Parse all YAML documents in a stream
and produce corresponding Python objects.

<a id="yaml.full_load"></a>

#### full\_load

```python
def full_load(stream)
```

Parse the first YAML document in a stream
and produce the corresponding Python object.

Resolve all tags except those known to be
unsafe on untrusted input.

<a id="yaml.full_load_all"></a>

#### full\_load\_all

```python
def full_load_all(stream)
```

Parse all YAML documents in a stream
and produce corresponding Python objects.

Resolve all tags except those known to be
unsafe on untrusted input.

<a id="yaml.safe_load"></a>

#### safe\_load

```python
def safe_load(stream)
```

Parse the first YAML document in a stream
and produce the corresponding Python object.

Resolve only basic YAML tags. This is known
to be safe for untrusted input.

<a id="yaml.safe_load_all"></a>

#### safe\_load\_all

```python
def safe_load_all(stream)
```

Parse all YAML documents in a stream
and produce corresponding Python objects.

Resolve only basic YAML tags. This is known
to be safe for untrusted input.

<a id="yaml.unsafe_load"></a>

#### unsafe\_load

```python
def unsafe_load(stream)
```

Parse the first YAML document in a stream
and produce the corresponding Python object.

Resolve all tags, even those known to be
unsafe on untrusted input.

<a id="yaml.unsafe_load_all"></a>

#### unsafe\_load\_all

```python
def unsafe_load_all(stream)
```

Parse all YAML documents in a stream
and produce corresponding Python objects.

Resolve all tags, even those known to be
unsafe on untrusted input.

<a id="yaml.emit"></a>

#### emit

```python
def emit(events,
         stream=None,
         Dumper=Dumper,
         canonical=None,
         indent=None,
         width=None,
         allow_unicode=None,
         line_break=None)
```

Emit YAML parsing events into a stream.
If stream is None, return the produced string instead.

<a id="yaml.serialize_all"></a>

#### serialize\_all

```python
def serialize_all(nodes,
                  stream=None,
                  Dumper=Dumper,
                  canonical=None,
                  indent=None,
                  width=None,
                  allow_unicode=None,
                  line_break=None,
                  encoding=None,
                  explicit_start=None,
                  explicit_end=None,
                  version=None,
                  tags=None)
```

Serialize a sequence of representation trees into a YAML stream.
If stream is None, return the produced string instead.

<a id="yaml.serialize"></a>

#### serialize

```python
def serialize(node, stream=None, Dumper=Dumper, **kwds)
```

Serialize a representation tree into a YAML stream.
If stream is None, return the produced string instead.

<a id="yaml.dump_all"></a>

#### dump\_all

```python
def dump_all(documents,
             stream=None,
             Dumper=Dumper,
             default_style=None,
             default_flow_style=False,
             canonical=None,
             indent=None,
             width=None,
             allow_unicode=None,
             line_break=None,
             encoding=None,
             explicit_start=None,
             explicit_end=None,
             version=None,
             tags=None,
             sort_keys=True)
```

Serialize a sequence of Python objects into a YAML stream.
If stream is None, return the produced string instead.

<a id="yaml.dump"></a>

#### dump

```python
def dump(data, stream=None, Dumper=Dumper, **kwds)
```

Serialize a Python object into a YAML stream.
If stream is None, return the produced string instead.

<a id="yaml.safe_dump_all"></a>

#### safe\_dump\_all

```python
def safe_dump_all(documents, stream=None, **kwds)
```

Serialize a sequence of Python objects into a YAML stream.
Produce only basic YAML tags.
If stream is None, return the produced string instead.

<a id="yaml.safe_dump"></a>

#### safe\_dump

```python
def safe_dump(data, stream=None, **kwds)
```

Serialize a Python object into a YAML stream.
Produce only basic YAML tags.
If stream is None, return the produced string instead.

<a id="yaml.add_implicit_resolver"></a>

#### add\_implicit\_resolver

```python
def add_implicit_resolver(tag, regexp, first=None, Loader=None, Dumper=Dumper)
```

Add an implicit scalar detector.
If an implicit scalar value matches the given regexp,
the corresponding tag is assigned to the scalar.
first is a sequence of possible initial characters or None.

<a id="yaml.add_path_resolver"></a>

#### add\_path\_resolver

```python
def add_path_resolver(tag, path, kind=None, Loader=None, Dumper=Dumper)
```

Add a path based resolver for the given tag.
A path is a list of keys that forms a path
to a node in the representation tree.
Keys can be string values, integers, or None.

<a id="yaml.add_constructor"></a>

#### add\_constructor

```python
def add_constructor(tag, constructor, Loader=None)
```

Add a constructor for the given tag.
Constructor is a function that accepts a Loader instance
and a node object and produces the corresponding Python object.

<a id="yaml.add_multi_constructor"></a>

#### add\_multi\_constructor

```python
def add_multi_constructor(tag_prefix, multi_constructor, Loader=None)
```

Add a multi-constructor for the given tag prefix.
Multi-constructor is called for a node if its tag starts with tag_prefix.
Multi-constructor accepts a Loader instance, a tag suffix,
and a node object and produces the corresponding Python object.

<a id="yaml.add_representer"></a>

#### add\_representer

```python
def add_representer(data_type, representer, Dumper=Dumper)
```

Add a representer for the given type.
Representer is a function accepting a Dumper instance
and an instance of the given data type
and producing the corresponding representation node.

<a id="yaml.add_multi_representer"></a>

#### add\_multi\_representer

```python
def add_multi_representer(data_type, multi_representer, Dumper=Dumper)
```

Add a representer for the given type.
Multi-representer is a function accepting a Dumper instance
and an instance of the given data type or subtype
and producing the corresponding representation node.

<a id="yaml.YAMLObjectMetaclass"></a>

## YAMLObjectMetaclass Objects

```python
class YAMLObjectMetaclass(type)
```

The metaclass for YAMLObject.

<a id="yaml.YAMLObject"></a>

## YAMLObject Objects

```python
class YAMLObject(metaclass=YAMLObjectMetaclass)
```

An object that can dump itself to a YAML stream
and load itself from a YAML stream.

<a id="yaml.YAMLObject.__slots__"></a>

#### \_\_slots\_\_

no direct instantiation, so allow immutable subclasses

<a id="yaml.YAMLObject.from_yaml"></a>

#### from\_yaml

```python
@classmethod
def from_yaml(cls, loader, node)
```

Convert a representation node to a Python object.

<a id="yaml.YAMLObject.to_yaml"></a>

#### to\_yaml

```python
@classmethod
def to_yaml(cls, dumper, data)
```

Convert a Python object to a representation node.

