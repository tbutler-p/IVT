# Table of Contents

* [tokenizers](#tokenizers)
  * [TextInputSequence](#tokenizers.TextInputSequence)
  * [PreTokenizedInputSequence](#tokenizers.PreTokenizedInputSequence)
  * [TextEncodeInput](#tokenizers.TextEncodeInput)
  * [PreTokenizedEncodeInput](#tokenizers.PreTokenizedEncodeInput)
  * [InputSequence](#tokenizers.InputSequence)
  * [EncodeInput](#tokenizers.EncodeInput)

<a id="tokenizers"></a>

# tokenizers

<a id="tokenizers.TextInputSequence"></a>

#### TextInputSequence

A :obj:`str` that represents an input sequence

<a id="tokenizers.PreTokenizedInputSequence"></a>

#### PreTokenizedInputSequence

A pre-tokenized input sequence. Can be one of:

- A :obj:`List` of :obj:`str`
- A :obj:`Tuple` of :obj:`str`

<a id="tokenizers.TextEncodeInput"></a>

#### TextEncodeInput

Represents a textual input for encoding. Can be either:

- A single sequence: :data:`~tokenizers.TextInputSequence`
- A pair of sequences:

  - A :obj:`Tuple` of :data:`~tokenizers.TextInputSequence`
  - Or a :obj:`List` of :data:`~tokenizers.TextInputSequence` of size 2

<a id="tokenizers.PreTokenizedEncodeInput"></a>

#### PreTokenizedEncodeInput

Represents a pre-tokenized input for encoding. Can be either:

- A single sequence: :data:`~tokenizers.PreTokenizedInputSequence`
- A pair of sequences:

  - A :obj:`Tuple` of :data:`~tokenizers.PreTokenizedInputSequence`
  - Or a :obj:`List` of :data:`~tokenizers.PreTokenizedInputSequence` of size 2

<a id="tokenizers.InputSequence"></a>

#### InputSequence

Represents all the possible types of input sequences for encoding. Can be:

- When ``is_pretokenized=False``: :data:`~TextInputSequence`
- When ``is_pretokenized=True``: :data:`~PreTokenizedInputSequence`

<a id="tokenizers.EncodeInput"></a>

#### EncodeInput

Represents all the possible types of input for encoding. Can be:

- When ``is_pretokenized=False``: :data:`~TextEncodeInput`
- When ``is_pretokenized=True``: :data:`~PreTokenizedEncodeInput`

