# Table of Contents

* [pybase64](#pybase64)
  * [get\_license\_text](#pybase64.get_license_text)
  * [get\_version](#pybase64.get_version)
  * [standard\_b64encode](#pybase64.standard_b64encode)
  * [standard\_b64decode](#pybase64.standard_b64decode)
  * [urlsafe\_b64encode](#pybase64.urlsafe_b64encode)
  * [urlsafe\_b64decode](#pybase64.urlsafe_b64decode)

<a id="pybase64"></a>

# pybase64

<a id="pybase64.get_license_text"></a>

#### get\_license\_text

```python
def get_license_text() -> str
```

Returns pybase64 license information as a :class:`str` object.

The result includes libbase64 license information as well.

<a id="pybase64.get_version"></a>

#### get\_version

```python
def get_version() -> str
```

Returns pybase64 version as a :class:`str` object.

The result reports if the C extension is used or not.
e.g. `1.0.0 (C extension active - AVX2)`

<a id="pybase64.standard_b64encode"></a>

#### standard\_b64encode

```python
def standard_b64encode(s: Buffer) -> bytes
```

Encode bytes using the standard Base64 alphabet.

Argument ``s`` is a :term:`bytes-like object` to encode.

The result is returned as a :class:`bytes` object.

<a id="pybase64.standard_b64decode"></a>

#### standard\_b64decode

```python
def standard_b64decode(s: str | Buffer) -> bytes
```

Decode bytes encoded with the standard Base64 alphabet.

Argument ``s`` is a :term:`bytes-like object` or ASCII string to
decode.

The result is returned as a :class:`bytes` object.

A :exc:`binascii.Error` is raised if the input is incorrectly padded.

Characters that are not in the standard alphabet are discarded prior
to the padding check.

<a id="pybase64.urlsafe_b64encode"></a>

#### urlsafe\_b64encode

```python
def urlsafe_b64encode(s: Buffer) -> bytes
```

Encode bytes using the URL- and filesystem-safe Base64 alphabet.

Argument ``s`` is a :term:`bytes-like object` to encode.

The result is returned as a :class:`bytes` object.

The alphabet uses '-' instead of '+' and '_' instead of '/'.

<a id="pybase64.urlsafe_b64decode"></a>

#### urlsafe\_b64decode

```python
def urlsafe_b64decode(s: str | Buffer) -> bytes
```

Decode bytes using the URL- and filesystem-safe Base64 alphabet.

Argument ``s`` is a :term:`bytes-like object` or ASCII string to
decode.

The result is returned as a :class:`bytes` object.

A :exc:`binascii.Error` is raised if the input is incorrectly padded.

Characters that are not in the URL-safe base-64 alphabet, and are not
a plus '+' or slash '/', are discarded prior to the padding check.

The alphabet uses '-' instead of '+' and '_' instead of '/'.

