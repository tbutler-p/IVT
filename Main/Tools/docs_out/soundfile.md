# Table of Contents

* [soundfile](#soundfile)
  * [read](#soundfile.read)
  * [write](#soundfile.write)
  * [blocks](#soundfile.blocks)
  * [info](#soundfile.info)
  * [available\_formats](#soundfile.available_formats)
  * [available\_subtypes](#soundfile.available_subtypes)
  * [check\_format](#soundfile.check_format)
  * [default\_subtype](#soundfile.default_subtype)
  * [SoundFile](#soundfile.SoundFile)
    * [\_\_init\_\_](#soundfile.SoundFile.__init__)
    * [name](#soundfile.SoundFile.name)
    * [mode](#soundfile.SoundFile.mode)
    * [samplerate](#soundfile.SoundFile.samplerate)
    * [frames](#soundfile.SoundFile.frames)
    * [channels](#soundfile.SoundFile.channels)
    * [format](#soundfile.SoundFile.format)
    * [subtype](#soundfile.SoundFile.subtype)
    * [endian](#soundfile.SoundFile.endian)
    * [format\_info](#soundfile.SoundFile.format_info)
    * [subtype\_info](#soundfile.SoundFile.subtype_info)
    * [sections](#soundfile.SoundFile.sections)
    * [closed](#soundfile.SoundFile.closed)
    * [compression\_level](#soundfile.SoundFile.compression_level)
    * [bitrate\_mode](#soundfile.SoundFile.bitrate_mode)
    * [extra\_info](#soundfile.SoundFile.extra_info)
    * [\_\_setattr\_\_](#soundfile.SoundFile.__setattr__)
    * [\_\_getattr\_\_](#soundfile.SoundFile.__getattr__)
    * [seekable](#soundfile.SoundFile.seekable)
    * [seek](#soundfile.SoundFile.seek)
    * [tell](#soundfile.SoundFile.tell)
    * [read](#soundfile.SoundFile.read)
    * [buffer\_read](#soundfile.SoundFile.buffer_read)
    * [buffer\_read\_into](#soundfile.SoundFile.buffer_read_into)
    * [write](#soundfile.SoundFile.write)
    * [buffer\_write](#soundfile.SoundFile.buffer_write)
    * [blocks](#soundfile.SoundFile.blocks)
    * [truncate](#soundfile.SoundFile.truncate)
    * [flush](#soundfile.SoundFile.flush)
    * [close](#soundfile.SoundFile.close)
    * [copy\_metadata](#soundfile.SoundFile.copy_metadata)
  * [SoundFileError](#soundfile.SoundFileError)
  * [SoundFileRuntimeError](#soundfile.SoundFileRuntimeError)
  * [LibsndfileError](#soundfile.LibsndfileError)
    * [error\_string](#soundfile.LibsndfileError.error_string)

<a id="soundfile"></a>

# soundfile

python-soundfile is an audio library based on libsndfile, CFFI and NumPy.

Sound files can be read or written directly using the functions
`read()` and `write()`.
To read a sound file in a block-wise fashion, use `blocks()`.
Alternatively, sound files can be opened as `SoundFile` objects.

For further information, see https://python-soundfile.readthedocs.io/.

<a id="soundfile.read"></a>

#### read

```python
def read(file,
         frames=-1,
         start=0,
         stop=None,
         dtype='float64',
         always_2d=False,
         fill_value=None,
         out=None,
         samplerate=None,
         channels=None,
         format=None,
         subtype=None,
         endian=None,
         closefd=True)
```

Provide audio data from a sound file as NumPy array.

By default, the whole file is read from the beginning, but the
position to start reading can be specified with *start* and the
number of frames to read can be specified with *frames*.
Alternatively, a range can be specified with *start* and *stop*.

If there is less data left in the file than requested, the rest of
the frames are filled with *fill_value*.
If no *fill_value* is specified, a smaller array is returned.

Parameters
----------
file : str or int or file-like object
    The file to read from.  See `SoundFile` for details.
frames : int, optional
    The number of frames to read. If *frames* is negative, the whole
    rest of the file is read.  Not allowed if *stop* is given.
start : int, optional
    Where to start reading.  A negative value counts from the end.
stop : int, optional
    The index after the last frame to be read.  A negative value
    counts from the end.  Not allowed if *frames* is given.
dtype : {'float64', 'float32', 'int32', 'int16'}, optional
    Data type of the returned array, by default ``'float64'``.
    Floating point audio data is typically in the range from
    ``-1.0`` to ``1.0``.  Integer data is in the range from
    ``-2**15`` to ``2**15-1`` for ``'int16'`` and from ``-2**31`` to
    ``2**31-1`` for ``'int32'``.

    .. note:: Reading int values from a float file will *not*
        scale the data to [-1.0, 1.0). If the file contains
        ``np.array([42.6], dtype='float32')``, you will read
        ``np.array([43], dtype='int32')`` for ``dtype='int32'``.

Returns
-------
audiodata : `numpy.ndarray` or type(out)
    A two-dimensional (frames x channels) NumPy array is returned.
    If the sound file has only one channel, a one-dimensional array
    is returned.  Use ``always_2d=True`` to return a two-dimensional
    array anyway.

    If *out* was specified, it is returned.  If *out* has more
    frames than available in the file (or if *frames* is smaller
    than the length of *out*) and no *fill_value* is given, then
    only a part of *out* is overwritten and a view containing all
    valid frames is returned.
samplerate : int
    The sample rate of the audio file.

Other Parameters
----------------
always_2d : bool, optional
    By default, reading a mono sound file will return a
    one-dimensional array.  With ``always_2d=True``, audio data is
    always returned as a two-dimensional array, even if the audio
    file has only one channel.
fill_value : float, optional
    If more frames are requested than available in the file, the
    rest of the output is be filled with *fill_value*.  If
    *fill_value* is not specified, a smaller array is returned.
out : `numpy.ndarray` or subclass, optional
    If *out* is specified, the data is written into the given array
    instead of creating a new array.  In this case, the arguments
    *dtype* and *always_2d* are silently ignored!  If *frames* is
    not given, it is obtained from the length of *out*.
samplerate, channels, format, subtype, endian, closefd
    See `SoundFile`.

Examples
--------
>>> import soundfile as sf
>>> data, samplerate = sf.read('stereo_file.wav')
>>> data
array([[ 0.71329652,  0.06294799],
       [-0.26450912, -0.38874483],
       ...
       [ 0.67398441, -0.11516333]])
>>> samplerate
44100

<a id="soundfile.write"></a>

#### write

```python
def write(file,
          data,
          samplerate,
          subtype=None,
          endian=None,
          format=None,
          closefd=True,
          compression_level=None,
          bitrate_mode=None)
```

Write data to a sound file.

.. note:: If *file* exists, it will be truncated and overwritten!

Parameters
----------
file : str or int or file-like object
    The file to write to.  See `SoundFile` for details.
data : array_like
    The data to write.  Usually two-dimensional (frames x channels),
    but one-dimensional *data* can be used for mono files.
    Only the data types ``'float64'``, ``'float32'``, ``'int32'``
    and ``'int16'`` are supported.

    .. note:: The data type of *data* does **not** select the data
              type of the written file. Audio data will be
              converted to the given *subtype*. Writing int values
              to a float file will *not* scale the values to
              [-1.0, 1.0). If you write the value ``np.array([42],
              dtype='int32')``, to a ``subtype='FLOAT'`` file, the
              file will then contain ``np.array([42.],
              dtype='float32')``.

samplerate : int
    The sample rate of the audio data.
subtype : str, optional
    See `default_subtype()` for the default value and
    `available_subtypes()` for all possible values.

Other Parameters
----------------
format, endian, closefd, compression_level, bitrate_mode
    See `SoundFile`.

Examples
--------
Write 10 frames of random data to a new file:

>>> import numpy as np
>>> import soundfile as sf
>>> sf.write('stereo_file.wav', np.random.randn(10, 2), 44100, 'PCM_24')

<a id="soundfile.blocks"></a>

#### blocks

```python
def blocks(file,
           blocksize=None,
           overlap=0,
           frames=-1,
           start=0,
           stop=None,
           dtype='float64',
           always_2d=False,
           fill_value=None,
           out=None,
           samplerate=None,
           channels=None,
           format=None,
           subtype=None,
           endian=None,
           closefd=True)
```

Return a generator for block-wise reading.

By default, iteration starts at the beginning and stops at the end
of the file.  Use *start* to start at a later position and *frames*
or *stop* to stop earlier.

If you stop iterating over the generator before it's exhausted,
the sound file is not closed. This is normally not a problem
because the file is opened in read-only mode. To close the file
properly, the generator's ``close()`` method can be called.

Parameters
----------
file : str or int or file-like object
    The file to read from.  See `SoundFile` for details.
blocksize : int
    The number of frames to read per block.
    Either this or *out* must be given.
overlap : int, optional
    The number of frames to rewind between each block.

Yields
------
`numpy.ndarray` or type(out)
    Blocks of audio data.
    If *out* was given, and the requested frames are not an integer
    multiple of the length of *out*, and no *fill_value* was given,
    the last block will be a smaller view into *out*.

Other Parameters
----------------
frames, start, stop
    See `read()`.
dtype : {'float64', 'float32', 'int32', 'int16'}, optional
    See `read()`.
always_2d, fill_value, out
    See `read()`.
samplerate, channels, format, subtype, endian, closefd
    See `SoundFile`.

Examples
--------
>>> import soundfile as sf
>>> for block in sf.blocks('stereo_file.wav', blocksize=1024):
>>>     pass  # do something with 'block'

<a id="soundfile.info"></a>

#### info

```python
def info(file, verbose=False)
```

Returns an object with information about a `SoundFile`.

Parameters
----------
verbose : bool
    Whether to print additional information.

<a id="soundfile.available_formats"></a>

#### available\_formats

```python
def available_formats()
```

Return a dictionary of available major formats.

Examples
--------
>>> import soundfile as sf
>>> sf.available_formats()
{'FLAC': 'FLAC (FLAC Lossless Audio Codec)',
 'OGG': 'OGG (OGG Container format)',
 'WAV': 'WAV (Microsoft)',
 'AIFF': 'AIFF (Apple/SGI)',
 ...
 'WAVEX': 'WAVEX (Microsoft)',
 'RAW': 'RAW (header-less)',
 'MAT5': 'MAT5 (GNU Octave 2.1 / Matlab 5.0)'}

<a id="soundfile.available_subtypes"></a>

#### available\_subtypes

```python
def available_subtypes(format=None)
```

Return a dictionary of available subtypes.

Parameters
----------
format : str
    If given, only compatible subtypes are returned.

Examples
--------
>>> import soundfile as sf
>>> sf.available_subtypes('FLAC')
{'PCM_24': 'Signed 24 bit PCM',
 'PCM_16': 'Signed 16 bit PCM',
 'PCM_S8': 'Signed 8 bit PCM'}

<a id="soundfile.check_format"></a>

#### check\_format

```python
def check_format(format, subtype=None, endian=None)
```

Check if the combination of format/subtype/endian is valid.

Examples
--------
>>> import soundfile as sf
>>> sf.check_format('WAV', 'PCM_24')
True
>>> sf.check_format('FLAC', 'VORBIS')
False

<a id="soundfile.default_subtype"></a>

#### default\_subtype

```python
def default_subtype(format)
```

Return the default subtype for a given format.

Examples
--------
>>> import soundfile as sf
>>> sf.default_subtype('WAV')
'PCM_16'
>>> sf.default_subtype('MAT5')
'DOUBLE'

<a id="soundfile.SoundFile"></a>

## SoundFile Objects

```python
class SoundFile(object)
```

A sound file.

For more documentation see the __init__() docstring (which is also
used for the online documentation (https://python-soundfile.readthedocs.io/).

<a id="soundfile.SoundFile.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file,
             mode='r',
             samplerate=None,
             channels=None,
             subtype=None,
             endian=None,
             format=None,
             closefd=True,
             compression_level=None,
             bitrate_mode=None)
```

Open a sound file.

If a file is opened with `mode` ``'r'`` (the default) or
``'r+'``, no sample rate, channels or file format need to be
given because the information is obtained from the file. An
exception is the ``'RAW'`` data format, which always requires
these data points.

File formats consist of three case-insensitive strings:

* a *major format* which is by default obtained from the
  extension of the file name (if known) and which can be
  forced with the format argument (e.g. ``format='WAVEX'``).
* a *subtype*, e.g. ``'PCM_24'``. Most major formats have a
  default subtype which is used if no subtype is specified.
* an *endian-ness*, which doesn't have to be specified at all in
  most cases.

A `SoundFile` object is a *context manager*, which means
if used in a "with" statement, `close()` is automatically
called when reaching the end of the code block inside the "with"
statement.

Parameters
----------
file : str or int or file-like object
    The file to open.  This can be a file name, a file
    descriptor or a Python file object (or a similar object with
    the methods ``read()``/``readinto()``, ``write()``,
    ``seek()`` and ``tell()``).
mode : {'r', 'r+', 'w', 'w+', 'x', 'x+'}, optional
    Open mode.  Has to begin with one of these three characters:
    ``'r'`` for reading, ``'w'`` for writing (truncates *file*)
    or ``'x'`` for writing (raises an error if *file* already
    exists).  Additionally, it may contain ``'+'`` to open
    *file* for both reading and writing.
    The character ``'b'`` for *binary mode* is implied because
    all sound files have to be opened in this mode.
    If *file* is a file descriptor or a file-like object,
    ``'w'`` doesn't truncate and ``'x'`` doesn't raise an error.
samplerate : int
    The sample rate of the file.  If `mode` contains ``'r'``,
    this is obtained from the file (except for ``'RAW'`` files).
channels : int
    The number of channels of the file.
    If `mode` contains ``'r'``, this is obtained from the file
    (except for ``'RAW'`` files).
subtype : str, sometimes optional
    The subtype of the sound file.  If `mode` contains ``'r'``,
    this is obtained from the file (except for ``'RAW'``
    files), if not, the default value depends on the selected
    `format` (see `default_subtype()`).
    See `available_subtypes()` for all possible subtypes for
    a given `format`.
endian : {'FILE', 'LITTLE', 'BIG', 'CPU'}, sometimes optional
    The endian-ness of the sound file.  If `mode` contains
    ``'r'``, this is obtained from the file (except for
    ``'RAW'`` files), if not, the default value is ``'FILE'``,
    which is correct in most cases.
format : str, sometimes optional
    The major format of the sound file.  If `mode` contains
    ``'r'``, this is obtained from the file (except for
    ``'RAW'`` files), if not, the default value is determined
    from the file extension.  See `available_formats()` for
    all possible values.
closefd : bool, optional
    Whether to close the file descriptor on `close()`. Only
    applicable if the *file* argument is a file descriptor.
compression_level : float, optional
    The compression level on 'write()'. The compression level
    should be between 0.0 (minimum compression level) and 1.0
    (highest compression level).
    See `libsndfile document <https://github.com/libsndfile/libsndfile/blob/c81375f070f3c6764969a738eacded64f53a076e/docs/command.md>`__.
bitrate_mode : {'CONSTANT', 'AVERAGE', 'VARIABLE'}, optional
    The bitrate mode on 'write()'. 
    See `libsndfile document <https://github.com/libsndfile/libsndfile/blob/c81375f070f3c6764969a738eacded64f53a076e/docs/command.md>`__.

Examples
--------
>>> from soundfile import SoundFile

Open an existing file for reading:

>>> myfile = SoundFile('existing_file.wav')
>>> # do something with myfile
>>> myfile.close()

Create a new sound file for reading and writing using a with
statement:

>>> with SoundFile('new_file.wav', 'x+', 44100, 2) as myfile:
>>>     # do something with myfile
>>>     # ...
>>>     assert not myfile.closed
>>>     # myfile.close() is called automatically at the end
>>> assert myfile.closed

<a id="soundfile.SoundFile.name"></a>

#### name

The file name of the sound file.

<a id="soundfile.SoundFile.mode"></a>

#### mode

The open mode the sound file was opened with.

<a id="soundfile.SoundFile.samplerate"></a>

#### samplerate

The sample rate of the sound file.

<a id="soundfile.SoundFile.frames"></a>

#### frames

The number of frames in the sound file.

<a id="soundfile.SoundFile.channels"></a>

#### channels

The number of channels in the sound file.

<a id="soundfile.SoundFile.format"></a>

#### format

The major format of the sound file.

<a id="soundfile.SoundFile.subtype"></a>

#### subtype

The subtype of data in the the sound file.

<a id="soundfile.SoundFile.endian"></a>

#### endian

The endian-ness of the data in the sound file.

<a id="soundfile.SoundFile.format_info"></a>

#### format\_info

A description of the major format of the sound file.

<a id="soundfile.SoundFile.subtype_info"></a>

#### subtype\_info

A description of the subtype of the sound file.

<a id="soundfile.SoundFile.sections"></a>

#### sections

The number of sections of the sound file.

<a id="soundfile.SoundFile.closed"></a>

#### closed

Whether the sound file is closed or not.

<a id="soundfile.SoundFile.compression_level"></a>

#### compression\_level

The compression level on 'write()'

<a id="soundfile.SoundFile.bitrate_mode"></a>

#### bitrate\_mode

The bitrate mode on 'write()'

<a id="soundfile.SoundFile.extra_info"></a>

#### extra\_info

```python
@property
def extra_info()
```

Retrieve the log string generated when opening the file.

<a id="soundfile.SoundFile.__setattr__"></a>

#### \_\_setattr\_\_

```python
def __setattr__(name, value)
```

Write text meta-data in the sound file through properties.

<a id="soundfile.SoundFile.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name)
```

Read text meta-data in the sound file through properties.

<a id="soundfile.SoundFile.seekable"></a>

#### seekable

```python
def seekable()
```

Return True if the file supports seeking.

<a id="soundfile.SoundFile.seek"></a>

#### seek

```python
def seek(frames, whence=SEEK_SET)
```

Set the read/write position.

Parameters
----------
frames : int
    The frame index or offset to seek.
whence : {SEEK_SET, SEEK_CUR, SEEK_END}, optional
    By default (``whence=SEEK_SET``), *frames* are counted from
    the beginning of the file.
    ``whence=SEEK_CUR`` seeks from the current position
    (positive and negative values are allowed for *frames*).
    ``whence=SEEK_END`` seeks from the end (use negative value
    for *frames*).

Returns
-------
int
    The new absolute read/write position in frames.

Examples
--------
>>> from soundfile import SoundFile, SEEK_END
>>> myfile = SoundFile('stereo_file.wav')

Seek to the beginning of the file:

>>> myfile.seek(0)
0

Seek to the end of the file:

>>> myfile.seek(0, SEEK_END)
44100  # this is the file length

<a id="soundfile.SoundFile.tell"></a>

#### tell

```python
def tell()
```

Return the current read/write position.

<a id="soundfile.SoundFile.read"></a>

#### read

```python
def read(frames=-1,
         dtype='float64',
         always_2d=False,
         fill_value=None,
         out=None)
```

Read from the file and return data as NumPy array.

Reads the given number of frames in the given data format
starting at the current read/write position.  This advances the
read/write position by the same number of frames.
By default, all frames from the current read/write position to
the end of the file are returned.
Use `seek()` to move the current read/write position.

Parameters
----------
frames : int, optional
    The number of frames to read. If ``frames < 0``, the whole
    rest of the file is read.
dtype : {'float64', 'float32', 'int32', 'int16'}, optional
    Data type of the returned array, by default ``'float64'``.
    Floating point audio data is typically in the range from
    ``-1.0`` to ``1.0``. Integer data is in the range from
    ``-2**15`` to ``2**15-1`` for ``'int16'`` and from
    ``-2**31`` to ``2**31-1`` for ``'int32'``.

    .. note:: Reading int values from a float file will *not*
        scale the data to [-1.0, 1.0). If the file contains
        ``np.array([42.6], dtype='float32')``, you will read
        ``np.array([43], dtype='int32')`` for
        ``dtype='int32'``.

Returns
-------
audiodata : `numpy.ndarray` or type(out)
    A two-dimensional NumPy (frames x channels) array is
    returned. If the sound file has only one channel, a
    one-dimensional array is returned. Use ``always_2d=True``
    to return a two-dimensional array anyway.

    If *out* was specified, it is returned. If *out* has more
    frames than available in the file (or if *frames* is
    smaller than the length of *out*) and no *fill_value* is
    given, then only a part of *out* is overwritten and a view
    containing all valid frames is returned.

Other Parameters
----------------
always_2d : bool, optional
    By default, reading a mono sound file will return a
    one-dimensional array. With ``always_2d=True``, audio data
    is always returned as a two-dimensional array, even if the
    audio file has only one channel.
fill_value : float, optional
    If more frames are requested than available in the file,
    the rest of the output is be filled with *fill_value*. If
    *fill_value* is not specified, a smaller array is
    returned.
out : `numpy.ndarray` or subclass, optional
    If *out* is specified, the data is written into the given
    array instead of creating a new array. In this case, the
    arguments *dtype* and *always_2d* are silently ignored! If
    *frames* is not given, it is obtained from the length of
    *out*.

Examples
--------
>>> from soundfile import SoundFile
>>> myfile = SoundFile('stereo_file.wav')

Reading 3 frames from a stereo file:

>>> myfile.read(3)
array([[ 0.71329652,  0.06294799],
       [-0.26450912, -0.38874483],
       [ 0.67398441, -0.11516333]])
>>> myfile.close()

See Also
--------
buffer_read, .write

<a id="soundfile.SoundFile.buffer_read"></a>

#### buffer\_read

```python
def buffer_read(frames=-1, dtype=None)
```

Read from the file and return data as buffer object.

Reads the given number of *frames* in the given data format
starting at the current read/write position.  This advances the
read/write position by the same number of frames.
By default, all frames from the current read/write position to
the end of the file are returned.
Use `seek()` to move the current read/write position.

Parameters
----------
frames : int, optional
    The number of frames to read. If ``frames < 0``, the whole
    rest of the file is read.
dtype : {'float64', 'float32', 'int32', 'int16'}
    Audio data will be converted to the given data type.

Returns
-------
buffer
    A buffer containing the read data.

See Also
--------
buffer_read_into, .read, buffer_write

<a id="soundfile.SoundFile.buffer_read_into"></a>

#### buffer\_read\_into

```python
def buffer_read_into(buffer, dtype)
```

Read from the file into a given buffer object.

Fills the given *buffer* with frames in the given data format
starting at the current read/write position (which can be
changed with `seek()`) until the buffer is full or the end
of the file is reached.  This advances the read/write position
by the number of frames that were read.

Parameters
----------
buffer : writable buffer
    Audio frames from the file are written to this buffer.
dtype : {'float64', 'float32', 'int32', 'int16'}
    The data type of *buffer*.

Returns
-------
int
    The number of frames that were read from the file.
    This can be less than the size of *buffer*.
    The rest of the buffer is not filled with meaningful data.

See Also
--------
buffer_read, .read

<a id="soundfile.SoundFile.write"></a>

#### write

```python
def write(data)
```

Write audio data from a NumPy array to the file.

Writes a number of frames at the read/write position to the
file. This also advances the read/write position by the same
number of frames and enlarges the file if necessary.

Note that writing int values to a float file will *not* scale
the values to [-1.0, 1.0). If you write the value
``np.array([42], dtype='int32')``, to a ``subtype='FLOAT'``
file, the file will then contain ``np.array([42.],
dtype='float32')``.

Parameters
----------
data : array_like
    The data to write. Usually two-dimensional (frames x
    channels), but one-dimensional *data* can be used for mono
    files. Only the data types ``'float64'``, ``'float32'``,
    ``'int32'`` and ``'int16'`` are supported.

    .. note:: The data type of *data* does **not** select the
          data type of the written file. Audio data will be
          converted to the given *subtype*. Writing int values
          to a float file will *not* scale the values to
          [-1.0, 1.0). If you write the value ``np.array([42],
          dtype='int32')``, to a ``subtype='FLOAT'`` file, the
          file will then contain ``np.array([42.],
          dtype='float32')``.

Examples
--------
>>> import numpy as np
>>> from soundfile import SoundFile
>>> myfile = SoundFile('stereo_file.wav')

Write 10 frames of random data to a new file:

>>> with SoundFile('stereo_file.wav', 'w', 44100, 2, 'PCM_24') as f:
>>>     f.write(np.random.randn(10, 2))

See Also
--------
buffer_write, .read

<a id="soundfile.SoundFile.buffer_write"></a>

#### buffer\_write

```python
def buffer_write(data, dtype)
```

Write audio data from a buffer/bytes object to the file.

Writes the contents of *data* to the file at the current
read/write position.
This also advances the read/write position by the number of
frames that were written and enlarges the file if necessary.

Parameters
----------
data : buffer or bytes
    A buffer or bytes object containing the audio data to be
    written.
dtype : {'float64', 'float32', 'int32', 'int16'}
    The data type of the audio data stored in *data*.

See Also
--------
.write, buffer_read

<a id="soundfile.SoundFile.blocks"></a>

#### blocks

```python
def blocks(blocksize=None,
           overlap=0,
           frames=-1,
           dtype='float64',
           always_2d=False,
           fill_value=None,
           out=None)
```

Return a generator for block-wise reading.

By default, the generator yields blocks of the given
*blocksize* (using a given *overlap*) until the end of the file
is reached; *frames* can be used to stop earlier.

Parameters
----------
blocksize : int
    The number of frames to read per block. Either this or *out*
    must be given.
overlap : int, optional
    The number of frames to rewind between each block.
frames : int, optional
    The number of frames to read.
    If ``frames < 0``, the file is read until the end.
dtype : {'float64', 'float32', 'int32', 'int16'}, optional
    See `read()`.

Yields
------
`numpy.ndarray` or type(out)
    Blocks of audio data.
    If *out* was given, and the requested frames are not an
    integer multiple of the length of *out*, and no
    *fill_value* was given, the last block will be a smaller
    view into *out*.


Other Parameters
----------------
always_2d, fill_value, out
    See `read()`.
fill_value : float, optional
    See `read()`.
out : `numpy.ndarray` or subclass, optional
    If *out* is specified, the data is written into the given
    array instead of creating a new array. In this case, the
    arguments *dtype* and *always_2d* are silently ignored!

Examples
--------
>>> from soundfile import SoundFile
>>> with SoundFile('stereo_file.wav') as f:
>>>     for block in f.blocks(blocksize=1024):
>>>         pass  # do something with 'block'

<a id="soundfile.SoundFile.truncate"></a>

#### truncate

```python
def truncate(frames=None)
```

Truncate the file to a given number of frames.

After this command, the read/write position will be at the new
end of the file.

Parameters
----------
frames : int, optional
    Only the data before *frames* is kept, the rest is deleted.
    If not specified, the current read/write position is used.

<a id="soundfile.SoundFile.flush"></a>

#### flush

```python
def flush()
```

Write unwritten data to the file system.

Data written with `write()` is not immediately written to
the file system but buffered in memory to be written at a later
time.  Calling `flush()` makes sure that all changes are
actually written to the file system.

This has no effect on files opened in read-only mode.

<a id="soundfile.SoundFile.close"></a>

#### close

```python
def close()
```

Close the file.  Can be called multiple times.

<a id="soundfile.SoundFile.copy_metadata"></a>

#### copy\_metadata

```python
def copy_metadata()
```

Get all metadata present in this SoundFile

Returns
-------

metadata: dict[str, str]
    A dict with all metadata. Possible keys are: 'title', 'copyright',
    'software', 'artist', 'comment', 'date', 'album', 'license',
    'tracknumber' and 'genre'.

<a id="soundfile.SoundFileError"></a>

## SoundFileError Objects

```python
class SoundFileError(Exception)
```

Base class for all soundfile-specific errors.

<a id="soundfile.SoundFileRuntimeError"></a>

## SoundFileRuntimeError Objects

```python
class SoundFileRuntimeError(SoundFileError, RuntimeError)
```

soundfile module runtime error.

Errors that used to be `RuntimeError`.

<a id="soundfile.LibsndfileError"></a>

## LibsndfileError Objects

```python
class LibsndfileError(SoundFileRuntimeError)
```

libsndfile errors.


Attributes
----------
code
    libsndfile internal error number.

<a id="soundfile.LibsndfileError.error_string"></a>

#### error\_string

```python
@property
def error_string()
```

Raw libsndfile error message.

