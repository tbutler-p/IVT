# Table of Contents

* [dill](#dill)
  * [load\_types](#dill.load_types)
  * [extend](#dill.extend)
  * [license](#dill.license)
  * [citation](#dill.citation)

<a id="dill"></a>

# dill

<a id="dill.load_types"></a>

#### load\_types

```python
def load_types(pickleable=True, unpickleable=True)
```

load pickleable and/or unpickleable types to ``dill.types``

``dill.types`` is meant to mimic the ``types`` module, providing a
registry of object types.  By default, the module is empty (for import
speed purposes). Use the ``load_types`` function to load selected object
types to the ``dill.types`` module.

**Arguments**:

- `pickleable` _bool, default=True_ - if True, load pickleable types.
- `unpickleable` _bool, default=True_ - if True, load unpickleable types.
  

**Returns**:

  None

<a id="dill.extend"></a>

#### extend

```python
def extend(use_dill=True)
```

add (or remove) dill types to/from the pickle registry

by default, ``dill`` populates its types to ``pickle.Pickler.dispatch``.
Thus, all ``dill`` types are available upon calling ``'import pickle'``.
To drop all ``dill`` types from the ``pickle`` dispatch, *use_dill=False*.

**Arguments**:

- `use_dill` _bool, default=True_ - if True, extend the dispatch table.
  

**Returns**:

  None

<a id="dill.license"></a>

#### license

```python
def license()
```

print license

<a id="dill.citation"></a>

#### citation

```python
def citation()
```

print citation

