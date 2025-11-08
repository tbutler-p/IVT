# Table of Contents

* [annotated\_types](#annotated_types)
  * [BaseMetadata](#annotated_types.BaseMetadata)
  * [Gt](#annotated_types.Gt)
  * [Ge](#annotated_types.Ge)
  * [Lt](#annotated_types.Lt)
  * [Le](#annotated_types.Le)
  * [GroupedMetadata](#annotated_types.GroupedMetadata)
  * [Interval](#annotated_types.Interval)
    * [\_\_iter\_\_](#annotated_types.Interval.__iter__)
  * [MultipleOf](#annotated_types.MultipleOf)
  * [MinLen](#annotated_types.MinLen)
  * [MaxLen](#annotated_types.MaxLen)
  * [Len](#annotated_types.Len)
    * [\_\_iter\_\_](#annotated_types.Len.__iter__)
  * [Timezone](#annotated_types.Timezone)
  * [Unit](#annotated_types.Unit)
  * [Predicate](#annotated_types.Predicate)
  * [LowerCase](#annotated_types.LowerCase)
  * [UpperCase](#annotated_types.UpperCase)
  * [IsDigits](#annotated_types.IsDigits)
  * [IsAscii](#annotated_types.IsAscii)
  * [IsFinite](#annotated_types.IsFinite)
  * [IsNotFinite](#annotated_types.IsNotFinite)
  * [IsNan](#annotated_types.IsNan)
  * [IsNotNan](#annotated_types.IsNotNan)
  * [IsInfinite](#annotated_types.IsInfinite)
  * [IsNotInfinite](#annotated_types.IsNotInfinite)

<a id="annotated_types"></a>

# annotated\_types

<a id="annotated_types.BaseMetadata"></a>

## BaseMetadata Objects

```python
class BaseMetadata()
```

Base class for all metadata.

This exists mainly so that implementers
can do `isinstance(..., BaseMetadata)` while traversing field annotations.

<a id="annotated_types.Gt"></a>

## Gt Objects

```python
@dataclass(frozen=True, **SLOTS)
class Gt(BaseMetadata)
```

Gt(gt=x) implies that the value must be greater than x.

It can be used with any type that supports the ``>`` operator,
including numbers, dates and times, strings, sets, and so on.

<a id="annotated_types.Ge"></a>

## Ge Objects

```python
@dataclass(frozen=True, **SLOTS)
class Ge(BaseMetadata)
```

Ge(ge=x) implies that the value must be greater than or equal to x.

It can be used with any type that supports the ``>=`` operator,
including numbers, dates and times, strings, sets, and so on.

<a id="annotated_types.Lt"></a>

## Lt Objects

```python
@dataclass(frozen=True, **SLOTS)
class Lt(BaseMetadata)
```

Lt(lt=x) implies that the value must be less than x.

It can be used with any type that supports the ``<`` operator,
including numbers, dates and times, strings, sets, and so on.

<a id="annotated_types.Le"></a>

## Le Objects

```python
@dataclass(frozen=True, **SLOTS)
class Le(BaseMetadata)
```

Le(le=x) implies that the value must be less than or equal to x.

It can be used with any type that supports the ``<=`` operator,
including numbers, dates and times, strings, sets, and so on.

<a id="annotated_types.GroupedMetadata"></a>

## GroupedMetadata Objects

```python
@runtime_checkable
class GroupedMetadata(Protocol)
```

A grouping of multiple objects, like typing.Unpack.

`GroupedMetadata` on its own is not metadata and has no meaning.
All of the constraints and metadata should be fully expressable
in terms of the `BaseMetadata`'s returned by `GroupedMetadata.__iter__()`.

Concrete implementations should override `GroupedMetadata.__iter__()`
to add their own metadata.
For example:

>>> @dataclass
>>> class Field(GroupedMetadata):
>>>     gt: float | None = None
>>>     description: str | None = None
...
>>>     def __iter__(self) -> Iterable[object]:
>>>         if self.gt is not None:
>>>             yield Gt(self.gt)
>>>         if self.description is not None:
>>>             yield Description(self.gt)

Also see the implementation of `Interval` below for an example.

Parsers should recognize this and unpack it so that it can be used
both with and without unpacking:

- `Annotated[int, Field(...)]` (parser must unpack Field)
- `Annotated[int, *Field(...)]` (PEP-646)

<a id="annotated_types.Interval"></a>

## Interval Objects

```python
@dataclass(frozen=True, **KW_ONLY, **SLOTS)
class Interval(GroupedMetadata)
```

Interval can express inclusive or exclusive bounds with a single object.

It accepts keyword arguments ``gt``, ``ge``, ``lt``, and/or ``le``, which
are interpreted the same way as the single-bound constraints.

<a id="annotated_types.Interval.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> Iterator[BaseMetadata]
```

Unpack an Interval into zero or more single-bounds.

<a id="annotated_types.MultipleOf"></a>

## MultipleOf Objects

```python
@dataclass(frozen=True, **SLOTS)
class MultipleOf(BaseMetadata)
```

MultipleOf(multiple_of=x) might be interpreted in two ways:

1. Python semantics, implying ``value % multiple_of == 0``, or
2. JSONschema semantics, where ``int(value / multiple_of) == value / multiple_of``

We encourage users to be aware of these two common interpretations,
and libraries to carefully document which they implement.

<a id="annotated_types.MinLen"></a>

## MinLen Objects

```python
@dataclass(frozen=True, **SLOTS)
class MinLen(BaseMetadata)
```

MinLen() implies minimum inclusive length,
e.g. ``len(value) >= min_length``.

<a id="annotated_types.MaxLen"></a>

## MaxLen Objects

```python
@dataclass(frozen=True, **SLOTS)
class MaxLen(BaseMetadata)
```

MaxLen() implies maximum inclusive length,
e.g. ``len(value) <= max_length``.

<a id="annotated_types.Len"></a>

## Len Objects

```python
@dataclass(frozen=True, **SLOTS)
class Len(GroupedMetadata)
```

Len() implies that ``min_length <= len(value) <= max_length``.

Upper bound may be omitted or ``None`` to indicate no upper length bound.

<a id="annotated_types.Len.__iter__"></a>

#### \_\_iter\_\_

```python
def __iter__() -> Iterator[BaseMetadata]
```

Unpack a Len into zone or more single-bounds.

<a id="annotated_types.Timezone"></a>

## Timezone Objects

```python
@dataclass(frozen=True, **SLOTS)
class Timezone(BaseMetadata)
```

Timezone(tz=...) requires a datetime to be aware (or ``tz=None``, naive).

``Annotated[datetime, Timezone(None)]`` must be a naive datetime.
``Timezone[...]`` (the ellipsis literal) expresses that the datetime must be
tz-aware but any timezone is allowed.

You may also pass a specific timezone string or tzinfo object such as
``Timezone(timezone.utc)`` or ``Timezone("Africa/Abidjan")`` to express that
you only allow a specific timezone, though we note that this is often
a symptom of poor design.

<a id="annotated_types.Unit"></a>

## Unit Objects

```python
@dataclass(frozen=True, **SLOTS)
class Unit(BaseMetadata)
```

Indicates that the value is a physical quantity with the specified unit.

It is intended for usage with numeric types, where the value represents the
magnitude of the quantity. For example, ``distance: Annotated[float, Unit('m')]``
or ``speed: Annotated[float, Unit('m/s')]``.

Interpretation of the unit string is left to the discretion of the consumer.
It is suggested to follow conventions established by python libraries that work
with physical quantities, such as

- ``pint`` : <https://pint.readthedocs.io/en/stable/>
- ``astropy.units``: <https://docs.astropy.org/en/stable/units/>

For indicating a quantity with a certain dimensionality but without a specific unit
it is recommended to use square brackets, e.g. `Annotated[float, Unit('[time]')]`.
Note, however, ``annotated_types`` itself makes no use of the unit string.

<a id="annotated_types.Predicate"></a>

## Predicate Objects

```python
@dataclass(frozen=True, **SLOTS)
class Predicate(BaseMetadata)
```

``Predicate(func: Callable)`` implies `func(value)` is truthy for valid values.

Users should prefer statically inspectable metadata, but if you need the full
power and flexibility of arbitrary runtime predicates... here it is.

We provide a few predefined predicates for common string constraints:
``IsLower = Predicate(str.islower)``, ``IsUpper = Predicate(str.isupper)``, and
``IsDigits = Predicate(str.isdigit)``. Users are encouraged to use methods which
can be given special handling, and avoid indirection like ``lambda s: s.lower()``.

Some libraries might have special logic to handle certain predicates, e.g. by
checking for `str.isdigit` and using its presence to both call custom logic to
enforce digit-only strings, and customise some generated external schema.

We do not specify what behaviour should be expected for predicates that raise
an exception.  For example `Annotated[int, Predicate(str.isdigit)]` might silently
skip invalid constraints, or statically raise an error; or it might try calling it
and then propagate or discard the resulting exception.

<a id="annotated_types.LowerCase"></a>

#### LowerCase

Return True if the string is a lowercase string, False otherwise.

A string is lowercase if all cased characters in the string are lowercase and there is at least one cased character in the string.

<a id="annotated_types.UpperCase"></a>

#### UpperCase

Return True if the string is an uppercase string, False otherwise.

A string is uppercase if all cased characters in the string are uppercase and there is at least one cased character in the string.

<a id="annotated_types.IsDigits"></a>

#### IsDigits

Return True if the string is a digit string, False otherwise.

A string is a digit string if all characters in the string are digits and there is at least one character in the string.

<a id="annotated_types.IsAscii"></a>

#### IsAscii

Return True if all characters in the string are ASCII, False otherwise.

ASCII characters have code points in the range U+0000-U+007F. Empty string is ASCII too.

<a id="annotated_types.IsFinite"></a>

#### IsFinite

Return True if x is neither an infinity nor a NaN, and False otherwise.

<a id="annotated_types.IsNotFinite"></a>

#### IsNotFinite

Return True if x is one of infinity or NaN, and False otherwise

<a id="annotated_types.IsNan"></a>

#### IsNan

Return True if x is a NaN (not a number), and False otherwise.

<a id="annotated_types.IsNotNan"></a>

#### IsNotNan

Return True if x is anything but NaN (not a number), and False otherwise.

<a id="annotated_types.IsInfinite"></a>

#### IsInfinite

Return True if x is a positive or negative infinity, and False otherwise.

<a id="annotated_types.IsNotInfinite"></a>

#### IsNotInfinite

Return True if x is neither a positive or negative infinity, and False otherwise.

