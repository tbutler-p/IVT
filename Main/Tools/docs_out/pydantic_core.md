# Table of Contents

* [pydantic\_core](#pydantic_core)
  * [ErrorDetails](#pydantic_core.ErrorDetails)
    * [type](#pydantic_core.ErrorDetails.type)
    * [loc](#pydantic_core.ErrorDetails.loc)
    * [msg](#pydantic_core.ErrorDetails.msg)
    * [input](#pydantic_core.ErrorDetails.input)
    * [ctx](#pydantic_core.ErrorDetails.ctx)
    * [url](#pydantic_core.ErrorDetails.url)
  * [InitErrorDetails](#pydantic_core.InitErrorDetails)
    * [type](#pydantic_core.InitErrorDetails.type)
    * [loc](#pydantic_core.InitErrorDetails.loc)
    * [input](#pydantic_core.InitErrorDetails.input)
    * [ctx](#pydantic_core.InitErrorDetails.ctx)
  * [ErrorTypeInfo](#pydantic_core.ErrorTypeInfo)
    * [type](#pydantic_core.ErrorTypeInfo.type)
    * [message\_template\_python](#pydantic_core.ErrorTypeInfo.message_template_python)
    * [example\_message\_python](#pydantic_core.ErrorTypeInfo.example_message_python)
    * [message\_template\_json](#pydantic_core.ErrorTypeInfo.message_template_json)
    * [example\_message\_json](#pydantic_core.ErrorTypeInfo.example_message_json)
    * [example\_context](#pydantic_core.ErrorTypeInfo.example_context)
  * [MultiHostHost](#pydantic_core.MultiHostHost)
    * [username](#pydantic_core.MultiHostHost.username)
    * [password](#pydantic_core.MultiHostHost.password)
    * [host](#pydantic_core.MultiHostHost.host)
    * [port](#pydantic_core.MultiHostHost.port)
  * [MISSING](#pydantic_core.MISSING)

<a id="pydantic_core"></a>

# pydantic\_core

<a id="pydantic_core.ErrorDetails"></a>

## ErrorDetails Objects

```python
class ErrorDetails(_TypedDict)
```

<a id="pydantic_core.ErrorDetails.type"></a>

#### type

The type of error that occurred, this is an identifier designed for
programmatic use that will change rarely or never.

`type` is unique for each error message, and can hence be used as an identifier to build custom error messages.

<a id="pydantic_core.ErrorDetails.loc"></a>

#### loc

Tuple of strings and ints identifying where in the schema the error occurred.

<a id="pydantic_core.ErrorDetails.msg"></a>

#### msg

A human readable error message.

<a id="pydantic_core.ErrorDetails.input"></a>

#### input

The input data at this `loc` that caused the error.

<a id="pydantic_core.ErrorDetails.ctx"></a>

#### ctx

Values which are required to render the error message, and could hence be useful in rendering custom error messages.
Also useful for passing custom error data forward.

<a id="pydantic_core.ErrorDetails.url"></a>

#### url

The documentation URL giving information about the error. No URL is available if
a [`PydanticCustomError`][pydantic_core.PydanticCustomError] is used.

<a id="pydantic_core.InitErrorDetails"></a>

## InitErrorDetails Objects

```python
class InitErrorDetails(_TypedDict)
```

<a id="pydantic_core.InitErrorDetails.type"></a>

#### type

The type of error that occurred, this should be a "slug" identifier that changes rarely or never.

<a id="pydantic_core.InitErrorDetails.loc"></a>

#### loc

Tuple of strings and ints identifying where in the schema the error occurred.

<a id="pydantic_core.InitErrorDetails.input"></a>

#### input

The input data at this `loc` that caused the error.

<a id="pydantic_core.InitErrorDetails.ctx"></a>

#### ctx

Values which are required to render the error message, and could hence be useful in rendering custom error messages.
Also useful for passing custom error data forward.

<a id="pydantic_core.ErrorTypeInfo"></a>

## ErrorTypeInfo Objects

```python
class ErrorTypeInfo(_TypedDict)
```

Gives information about errors.

<a id="pydantic_core.ErrorTypeInfo.type"></a>

#### type

The type of error that occurred, this should be a "slug" identifier that changes rarely or never.

<a id="pydantic_core.ErrorTypeInfo.message_template_python"></a>

#### message\_template\_python

String template to render a human readable error message from using context, when the input is Python.

<a id="pydantic_core.ErrorTypeInfo.example_message_python"></a>

#### example\_message\_python

Example of a human readable error message, when the input is Python.

<a id="pydantic_core.ErrorTypeInfo.message_template_json"></a>

#### message\_template\_json

String template to render a human readable error message from using context, when the input is JSON data.

<a id="pydantic_core.ErrorTypeInfo.example_message_json"></a>

#### example\_message\_json

Example of a human readable error message, when the input is JSON data.

<a id="pydantic_core.ErrorTypeInfo.example_context"></a>

#### example\_context

Example of context values.

<a id="pydantic_core.MultiHostHost"></a>

## MultiHostHost Objects

```python
class MultiHostHost(_TypedDict)
```

A host part of a multi-host URL.

<a id="pydantic_core.MultiHostHost.username"></a>

#### username

The username part of this host, or `None`.

<a id="pydantic_core.MultiHostHost.password"></a>

#### password

The password part of this host, or `None`.

<a id="pydantic_core.MultiHostHost.host"></a>

#### host

The host part of this host, or `None`.

<a id="pydantic_core.MultiHostHost.port"></a>

#### port

The port part of this host, or `None`.

<a id="pydantic_core.MISSING"></a>

#### MISSING

A singleton indicating a field value was not provided during validation.

This singleton can be used a default value, as an alternative to `None` when it has
an explicit meaning. During serialization, any field with `MISSING` as a value is excluded
from the output.

**Example**:

    ```python
    from pydantic import BaseModel

    from pydantic_core import MISSING


    class Configuration(BaseModel):
        timeout: int | None | MISSING = MISSING


    # configuration defaults, stored somewhere else:
    defaults = {'timeout': 200}

    conf = Configuration.model_validate({...})
    timeout = conf.timeout if timeout.timeout is not MISSING else defaults['timeout']

