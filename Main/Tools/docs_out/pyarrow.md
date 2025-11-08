# Table of Contents

* [pyarrow](#pyarrow)
  * [show\_versions](#pyarrow.show_versions)
  * [show\_info](#pyarrow.show_info)
  * [get\_include](#pyarrow.get_include)
  * [get\_libraries](#pyarrow.get_libraries)
  * [create\_library\_symlinks](#pyarrow.create_library_symlinks)
  * [get\_library\_dirs](#pyarrow.get_library_dirs)

<a id="pyarrow"></a>

# pyarrow

PyArrow is the python implementation of Apache Arrow.

Apache Arrow is a cross-language development platform for in-memory data.
It specifies a standardized language-independent columnar memory format for
flat and hierarchical data, organized for efficient analytic operations on
modern hardware. It also provides computational libraries and zero-copy
streaming messaging and interprocess communication.

For more information see the official page at https://arrow.apache.org

<a id="pyarrow.show_versions"></a>

#### show\_versions

```python
def show_versions()
```

Print various version information, to help with error reporting.

<a id="pyarrow.show_info"></a>

#### show\_info

```python
def show_info()
```

Print detailed version and platform information, for error reporting

<a id="pyarrow.get_include"></a>

#### get\_include

```python
def get_include()
```

Return absolute path to directory containing Arrow C++ include
headers. Similar to numpy.get_include

<a id="pyarrow.get_libraries"></a>

#### get\_libraries

```python
def get_libraries()
```

Return list of library names to include in the `libraries` argument for C
or Cython extensions using pyarrow

<a id="pyarrow.create_library_symlinks"></a>

#### create\_library\_symlinks

```python
def create_library_symlinks()
```

With Linux and macOS wheels, the bundled shared libraries have an embedded
ABI version like libarrow.so.17 or libarrow.17.dylib and so linking to them
with -larrow won't work unless we create symlinks at locations like
site-packages/pyarrow/libarrow.so. This unfortunate workaround addresses
prior problems we had with shipping two copies of the shared libraries to
permit third party projects like turbodbc to build their C++ extensions
against the pyarrow wheels.

This function must only be invoked once and only when the shared libraries
are bundled with the Python package, which should only apply to wheel-based
installs. It requires write access to the site-packages/pyarrow directory
and so depending on your system may need to be run with root.

<a id="pyarrow.get_library_dirs"></a>

#### get\_library\_dirs

```python
def get_library_dirs()
```

Return lists of directories likely to contain Arrow C++ libraries for
linking C or Cython extensions using pyarrow

