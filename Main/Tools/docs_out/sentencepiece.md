# Table of Contents

* [sentencepiece](#sentencepiece)
  * [SentencePieceProcessor](#sentencepiece.SentencePieceProcessor)
    * [Init](#sentencepiece.SentencePieceProcessor.Init)
    * [Encode](#sentencepiece.SentencePieceProcessor.Encode)
    * [NBestEncode](#sentencepiece.SentencePieceProcessor.NBestEncode)
    * [SampleEncodeAndScore](#sentencepiece.SentencePieceProcessor.SampleEncodeAndScore)
    * [Decode](#sentencepiece.SentencePieceProcessor.Decode)
    * [CalculateEntropy](#sentencepiece.SentencePieceProcessor.CalculateEntropy)
    * [Load](#sentencepiece.SentencePieceProcessor.Load)
  * [SentencePieceNormalizer](#sentencepiece.SentencePieceNormalizer)
    * [Init](#sentencepiece.SentencePieceNormalizer.Init)

<a id="sentencepiece"></a>

# sentencepiece

<a id="sentencepiece.SentencePieceProcessor"></a>

## SentencePieceProcessor Objects

```python
class SentencePieceProcessor(object)
```

<a id="sentencepiece.SentencePieceProcessor.Init"></a>

#### Init

```python
def Init(model_file=None,
         model_proto=None,
         out_type=int,
         add_bos=False,
         add_eos=False,
         reverse=False,
         emit_unk_piece=False,
         enable_sampling=False,
         nbest_size=-1,
         alpha=0.1,
         num_threads=-1)
```

Initialzie sentencepieceProcessor.

**Arguments**:

- `model_file` - The sentencepiece model file path.
- `model_proto` - The sentencepiece model serialized proto.
- `out_type` - output type. int or str.
- `add_bos` - Add <s> to the result (Default = false)
- `add_eos` - Add </s> to the result (Default = false) <s>/</s> is added after
  reversing (if enabled).
- `reverse` - Reverses the tokenized sequence (Default = false)
- `emit_unk_piece` - Emits the unk literal string (Default = false)
- `nbest_size` - sampling parameters for unigram. Invalid in BPE-Dropout.
  nbest_size = {0,1}: No sampling is performed.
  nbest_size > 1: samples from the nbest_size results.
  nbest_size < 0: assuming that nbest_size is infinite and samples
  from the all hypothesis (lattice) using
  forward-filtering-and-backward-sampling algorithm.
- `alpha` - Soothing parameter for unigram sampling, and dropout probability of
  merge operations for BPE-dropout.
- `num_threads` - number of threads in batch processing (Default = -1, auto-detected)

<a id="sentencepiece.SentencePieceProcessor.Encode"></a>

#### Encode

```python
def Encode(input,
           out_type=None,
           add_bos=None,
           add_eos=None,
           reverse=None,
           emit_unk_piece=None,
           enable_sampling=None,
           nbest_size=None,
           alpha=None,
           num_threads=None)
```

Encode text input to segmented ids or tokens.

**Arguments**:

- `input` - input string. accepsts list of string.
- `out_type` - output type. int or str.
- `add_bos` - Add <s> to the result (Default = false)
- `add_eos` - Add </s> to the result (Default = false) <s>/</s> is added after
  reversing (if enabled).
- `reverse` - Reverses the tokenized sequence (Default = false)
- `emit_unk_piece` - Emits the unk literal string (Default = false)
- `nbest_size` - sampling parameters for unigram. Invalid in BPE-Dropout.
  nbest_size = {0,1}: No sampling is performed.
  nbest_size > 1: samples from the nbest_size results.
  nbest_size < 0: assuming that nbest_size is infinite and samples
  from the all hypothesis (lattice) using
  forward-filtering-and-backward-sampling algorithm.
- `alpha` - Soothing parameter for unigram sampling, and merge probability for
  BPE-dropout (probablity 'p' in BPE-dropout paper).
- `num_threads` - the number of threads used in the batch processing (Default = -1).

<a id="sentencepiece.SentencePieceProcessor.NBestEncode"></a>

#### NBestEncode

```python
def NBestEncode(input,
                out_type=None,
                add_bos=None,
                add_eos=None,
                reverse=None,
                emit_unk_piece=None,
                nbest_size=None)
```

NBestEncode text input to segmented ids or tokens.

**Arguments**:

- `input` - input string. accepsts list of string.
- `out_type` - output type. int or str.
- `add_bos` - Add <s> to the result (Default = false)
- `add_eos` - Add </s> to the result (Default = false) <s>/</s> is added after reversing (if enabled).
- `reverse` - Reverses the tokenized sequence (Default = false)
- `emit_unk_piece` - Emits the unk literal string (Default = false)
- `nbest_size` - nbest size

<a id="sentencepiece.SentencePieceProcessor.SampleEncodeAndScore"></a>

#### SampleEncodeAndScore

```python
def SampleEncodeAndScore(input,
                         out_type=None,
                         add_bos=None,
                         add_eos=None,
                         reverse=None,
                         emit_unk_piece=None,
                         num_samples=None,
                         alpha=None,
                         wor=None,
                         include_best=None)
```

SampleEncodeAndScore text input to segmented ids or tokens.

**Arguments**:

- `input` - input string. accepsts list of string.
- `out_type` - output type. int or str or 'serialized_proto' or 'immutable_proto'
- `add_bos` - Add <s> to the result (Default = false)
- `add_eos` - Add </s> to the result (Default = false) <s>/</s> is added after reversing (if enabled).
- `reverse` - Reverses the tokenized sequence (Default = false)
- `emit_unk_piece` - Emits the unk literal string (Default = false)
- `num_samples` - How many samples to return (Default = 1)
- `alpha` - inverse temperature for sampling
- `wor` - whether to sample without replacement (Default = false)
- `include_best` - whether to include the best tokenization, requires wor=True (Default = false)

<a id="sentencepiece.SentencePieceProcessor.Decode"></a>

#### Decode

```python
def Decode(input, out_type=str, num_threads=None)
```

Decode processed id or token sequences.

**Arguments**:

- `out_type` - output type. str, bytes or 'serialized_proto' or 'immutable_proto' (Default = str)
- `num_threads` - the number of threads used in the batch processing (Default = -1).

<a id="sentencepiece.SentencePieceProcessor.CalculateEntropy"></a>

#### CalculateEntropy

```python
def CalculateEntropy(input, alpha, num_threads=None)
```

Calculate sentence entropy

<a id="sentencepiece.SentencePieceProcessor.Load"></a>

#### Load

```python
def Load(model_file=None, model_proto=None)
```

Overwride SentencePieceProcessor.Load to support both model_file and model_proto.

**Arguments**:

- `model_file` - The sentencepiece model file path.
- `model_proto` - The sentencepiece model serialized proto. Either `model_file`
  or `model_proto` must be set.

<a id="sentencepiece.SentencePieceNormalizer"></a>

## SentencePieceNormalizer Objects

```python
class SentencePieceNormalizer(object)
```

<a id="sentencepiece.SentencePieceNormalizer.Init"></a>

#### Init

```python
def Init(model_file=None,
         model_proto=None,
         rule_tsv=None,
         rule_name=None,
         add_dummy_prefix=False,
         escape_whitespaces=False,
         remove_extra_whitespaces=False)
```

Initialzie sentencePieceNormalizer.

**Arguments**:

- `model_file` - The sentencepiece model file path.
- `model_proto` - The sentencepiece model serialized proto.
- `rule_tsv` - The normalization rule file in TSV format.
- `rule_name` - Pre-defined normalization name.
- `add_dummy_prefix` - add dummy prefix.
- `escape_whitespaces` - escape whitespaces.
- `remove_extra_whitespaces` - remove extra whitespaces.

