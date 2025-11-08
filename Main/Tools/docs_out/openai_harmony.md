# Table of Contents

* [openai\_harmony](#openai_harmony)
  * [Role](#openai_harmony.Role)
  * [HarmonyEncoding](#openai_harmony.HarmonyEncoding)
    * [render\_conversation\_for\_completion](#openai_harmony.HarmonyEncoding.render_conversation_for_completion)
    * [render\_conversation](#openai_harmony.HarmonyEncoding.render_conversation)
    * [render\_conversation\_for\_training](#openai_harmony.HarmonyEncoding.render_conversation_for_training)
    * [render](#openai_harmony.HarmonyEncoding.render)
    * [decode\_utf8](#openai_harmony.HarmonyEncoding.decode_utf8)
    * [encode](#openai_harmony.HarmonyEncoding.encode)
    * [decode](#openai_harmony.HarmonyEncoding.decode)
    * [is\_special\_token](#openai_harmony.HarmonyEncoding.is_special_token)
  * [StreamableParser](#openai_harmony.StreamableParser)
    * [state\_data](#openai_harmony.StreamableParser.state_data)
  * [load\_harmony\_encoding](#openai_harmony.load_harmony_encoding)

<a id="openai_harmony"></a>

# openai\_harmony

Python wrapper around the Rust implementation of *harmony*.

The heavy lifting (tokenisation, rendering, parsing, …) is implemented in
Rust.  The thin bindings are available through the private ``openai_harmony``
extension module which is compiled via *maturin* / *PyO3*.

This package provides a small, typed convenience layer that mirrors the public
API of the Rust crate so that it can be used from Python code in an
idiomatic way (``dataclasses``, ``Enum``s, …).

<a id="openai_harmony.Role"></a>

## Role Objects

```python
class Role(str, Enum)
```

The role of a message author (mirrors ``chat::Role``).

<a id="openai_harmony.HarmonyEncoding"></a>

## HarmonyEncoding Objects

```python
class HarmonyEncoding()
```

High-level wrapper around the Rust ``PyHarmonyEncoding`` class.

<a id="openai_harmony.HarmonyEncoding.render_conversation_for_completion"></a>

#### render\_conversation\_for\_completion

```python
def render_conversation_for_completion(
        conversation: Conversation,
        next_turn_role: Role,
        config: Optional[RenderConversationConfig] = None) -> List[int]
```

Render a conversation for completion.

**Arguments**:

- `conversation` - Conversation object
- `next_turn_role` - Role for the next turn
- `config` - Optional RenderConversationConfig (default auto_drop_analysis=True)

<a id="openai_harmony.HarmonyEncoding.render_conversation"></a>

#### render\_conversation

```python
def render_conversation(
        conversation: Conversation,
        config: Optional[RenderConversationConfig] = None) -> List[int]
```

Render a conversation without appending a new role.

<a id="openai_harmony.HarmonyEncoding.render_conversation_for_training"></a>

#### render\_conversation\_for\_training

```python
def render_conversation_for_training(
        conversation: Conversation,
        config: Optional[RenderConversationConfig] = None) -> List[int]
```

Render a conversation for training.

<a id="openai_harmony.HarmonyEncoding.render"></a>

#### render

```python
def render(message: Message,
           render_options: Optional[RenderOptions] = None) -> List[int]
```

Render a single message into tokens.

<a id="openai_harmony.HarmonyEncoding.decode_utf8"></a>

#### decode\_utf8

```python
def decode_utf8(tokens: Sequence[int]) -> str
```

Decode a list of tokens into a UTF-8 string. Will raise an error if the tokens result in invalid UTF-8. Use decode if you want to replace invalid UTF-8 with the unicode replacement character.

<a id="openai_harmony.HarmonyEncoding.encode"></a>

#### encode

```python
def encode(
        text: str,
        *,
        allowed_special: Literal["all"] | AbstractSet[str] = set(),
        disallowed_special: Literal["all"] | Collection[str] = "all"
) -> list[int]
```

Encodes a string into tokens.

Special tokens are artificial tokens used to unlock capabilities from a model,
such as fill-in-the-middle. So we want to be careful about accidentally encoding special
tokens, since they can be used to trick a model into doing something we don't want it to do.

Hence, by default, encode will raise an error if it encounters text that corresponds
to a special token. This can be controlled on a per-token level using the `allowed_special`
and `disallowed_special` parameters. In particular:
- Setting `disallowed_special` to () will prevent this function from raising errors and
  cause all text corresponding to special tokens to be encoded as natural text.
- Setting `allowed_special` to "all" will cause this function to treat all text
  corresponding to special tokens to be encoded as special tokens.

```
>>> enc.encode("hello world")
[31373, 995]
>>> enc.encode("<|endoftext|>", allowed_special={"<|endoftext|>"})
[50256]
>>> enc.encode("<|endoftext|>", allowed_special="all")
[50256]
>>> enc.encode("<|endoftext|>")
# Raises ValueError
>>> enc.encode("<|endoftext|>", disallowed_special=())
[27, 91, 437, 1659, 5239, 91, 29]
```

<a id="openai_harmony.HarmonyEncoding.decode"></a>

#### decode

```python
def decode(tokens: Sequence[int], errors: str = "replace") -> str
```

Decodes a list of tokens into a string.

WARNING: the default behaviour of this function is lossy, since decoded bytes are not
guaranteed to be valid UTF-8. You can use `decode_utf8` if you want to raise an error on invalid UTF-8.

```
>>> enc.decode([31373, 995])
'hello world'
```

<a id="openai_harmony.HarmonyEncoding.is_special_token"></a>

#### is\_special\_token

```python
def is_special_token(token: int) -> bool
```

Returns if an individual token is a special token

<a id="openai_harmony.StreamableParser"></a>

## StreamableParser Objects

```python
class StreamableParser()
```

Incremental parser over completion tokens.

<a id="openai_harmony.StreamableParser.state_data"></a>

#### state\_data

```python
@property
def state_data() -> Dict[str, Any]
```

Return a JSON string representing the parser's internal state.

<a id="openai_harmony.load_harmony_encoding"></a>

#### load\_harmony\_encoding

```python
def load_harmony_encoding(
        name: str | "HarmonyEncodingName") -> HarmonyEncoding
```

Load an encoding by *name* (delegates to the Rust implementation).

