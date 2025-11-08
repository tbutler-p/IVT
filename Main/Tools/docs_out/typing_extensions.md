# Table of Contents

* [typing\_extensions](#typing_extensions)
  * [T](#typing_extensions.T)
  * [KT](#typing_extensions.KT)
  * [VT](#typing_extensions.VT)
  * [T\_co](#typing_extensions.T_co)
  * [T\_contra](#typing_extensions.T_contra)
  * [Sentinel](#typing_extensions.Sentinel)

<a id="typing_extensions"></a>

# typing\_extensions

<a id="typing_extensions.T"></a>

#### T

Any type.

<a id="typing_extensions.KT"></a>

#### KT

Key type.

<a id="typing_extensions.VT"></a>

#### VT

Value type.

<a id="typing_extensions.T_co"></a>

#### T\_co

Any type covariant containers.

<a id="typing_extensions.T_contra"></a>

#### T\_contra

Ditto contravariant.

<a id="typing_extensions.Sentinel"></a>

## Sentinel Objects

```python
class Sentinel()
```

Create a unique sentinel object.

*name* should be the name of the variable to which the return value shall be assigned.

*repr*, if supplied, will be used for the repr of the sentinel object.
If not provided, "<name>" will be used.

