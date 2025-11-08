# Table of Contents

* [urllib3](#urllib3)
  * [add\_stderr\_logger](#urllib3.add_stderr_logger)
  * [disable\_warnings](#urllib3.disable_warnings)
  * [request](#urllib3.request)

<a id="urllib3"></a>

# urllib3

Python HTTP library with thread-safe connection pooling, file post support, user friendly, and more

<a id="urllib3.add_stderr_logger"></a>

#### add\_stderr\_logger

```python
def add_stderr_logger(
        level: int = logging.DEBUG) -> logging.StreamHandler[typing.TextIO]
```

Helper for quickly adding a StreamHandler to the logger. Useful for
debugging.

Returns the handler after adding it.

<a id="urllib3.disable_warnings"></a>

#### disable\_warnings

```python
def disable_warnings(category: type[Warning] = exceptions.HTTPWarning) -> None
```

Helper for quickly disabling all urllib3 warnings.

<a id="urllib3.request"></a>

#### request

```python
def request(method: str,
            url: str,
            *,
            body: _TYPE_BODY | None = None,
            fields: _TYPE_FIELDS | None = None,
            headers: typing.Mapping[str, str] | None = None,
            preload_content: bool | None = True,
            decode_content: bool | None = True,
            redirect: bool | None = True,
            retries: Retry | bool | int | None = None,
            timeout: Timeout | float | int | None = 3,
            json: typing.Any | None = None) -> BaseHTTPResponse
```

A convenience, top-level request method. It uses a module-global ``PoolManager`` instance.

Therefore, its side effects could be shared across dependencies relying on it.
To avoid side effects create a new ``PoolManager`` instance and use it instead.
The method does not accept low-level ``**urlopen_kw`` keyword arguments.

**Arguments**:

- `method`: HTTP request method (such as GET, POST, PUT, etc.)
- `url`: The URL to perform the request on.
- `body`: Data to send in the request body, either :class:`str`, :class:`bytes`,
an iterable of :class:`str`/:class:`bytes`, or a file-like object.
- `fields`: Data to encode and send in the request body.
- `headers`: Dictionary of custom headers to send, such as User-Agent,
If-None-Match, etc.
- `preload_content` (`bool`): If True, the response's body will be preloaded into memory.
- `decode_content` (`bool`): If True, will attempt to decode the body based on the
'content-encoding' header.
- `redirect`: If True, automatically handle redirects (status codes 301, 302,
303, 307, 308). Each redirect counts as a retry. Disabling retries
will disable redirect, too.
- `retries` (`:class:`~urllib3.util.retry.Retry`, False, or an int.`): Configure the number of retries to allow before raising a
:class:`~urllib3.exceptions.MaxRetryError` exception.

If ``None`` (default) will retry 3 times, see ``Retry.DEFAULT``. Pass a
:class:`~urllib3.util.retry.Retry` object for fine-grained control
over different types of retries.
Pass an integer number to retry connection errors that many times,
but no other types of errors. Pass zero to never retry.

If ``False``, then retries are disabled and any exception is raised
immediately. Also, instead of raising a MaxRetryError on redirects,
the redirect response will be returned.
- `timeout`: If specified, overrides the default timeout for this one
request. It may be a float (in seconds) or an instance of
:class:`urllib3.util.Timeout`.
- `json`: Data to encode and send as JSON with UTF-encoded in the request body.
The ``"Content-Type"`` header will be set to ``"application/json"``
unless specified otherwise.

