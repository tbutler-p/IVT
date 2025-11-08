# Table of Contents

* [cachetools](#cachetools)
  * [Cache](#cachetools.Cache)
    * [maxsize](#cachetools.Cache.maxsize)
    * [currsize](#cachetools.Cache.currsize)
    * [getsizeof](#cachetools.Cache.getsizeof)
  * [FIFOCache](#cachetools.FIFOCache)
    * [popitem](#cachetools.FIFOCache.popitem)
  * [LFUCache](#cachetools.LFUCache)
    * [popitem](#cachetools.LFUCache.popitem)
  * [LRUCache](#cachetools.LRUCache)
    * [popitem](#cachetools.LRUCache.popitem)
  * [RRCache](#cachetools.RRCache)
    * [choice](#cachetools.RRCache.choice)
    * [popitem](#cachetools.RRCache.popitem)
  * [\_TimedCache](#cachetools._TimedCache)
    * [timer](#cachetools._TimedCache.timer)
  * [TTLCache](#cachetools.TTLCache)
    * [ttl](#cachetools.TTLCache.ttl)
    * [expire](#cachetools.TTLCache.expire)
    * [popitem](#cachetools.TTLCache.popitem)
  * [TLRUCache](#cachetools.TLRUCache)
    * [ttu](#cachetools.TLRUCache.ttu)
    * [expire](#cachetools.TLRUCache.expire)
    * [popitem](#cachetools.TLRUCache.popitem)
  * [cached](#cachetools.cached)
  * [cachedmethod](#cachetools.cachedmethod)

<a id="cachetools"></a>

# cachetools

Extensible memoizing collections and decorators.

<a id="cachetools.Cache"></a>

## Cache Objects

```python
class Cache(collections.abc.MutableMapping)
```

Mutable mapping to serve as a simple cache or cache base class.

<a id="cachetools.Cache.maxsize"></a>

#### maxsize

```python
@property
def maxsize()
```

The maximum size of the cache.

<a id="cachetools.Cache.currsize"></a>

#### currsize

```python
@property
def currsize()
```

The current size of the cache.

<a id="cachetools.Cache.getsizeof"></a>

#### getsizeof

```python
@staticmethod
def getsizeof(value)
```

Return the size of a cache element's value.

<a id="cachetools.FIFOCache"></a>

## FIFOCache Objects

```python
class FIFOCache(Cache)
```

First In First Out (FIFO) cache implementation.

<a id="cachetools.FIFOCache.popitem"></a>

#### popitem

```python
def popitem()
```

Remove and return the `(key, value)` pair first inserted.

<a id="cachetools.LFUCache"></a>

## LFUCache Objects

```python
class LFUCache(Cache)
```

Least Frequently Used (LFU) cache implementation.

<a id="cachetools.LFUCache.popitem"></a>

#### popitem

```python
def popitem()
```

Remove and return the `(key, value)` pair least frequently used.

<a id="cachetools.LRUCache"></a>

## LRUCache Objects

```python
class LRUCache(Cache)
```

Least Recently Used (LRU) cache implementation.

<a id="cachetools.LRUCache.popitem"></a>

#### popitem

```python
def popitem()
```

Remove and return the `(key, value)` pair least recently used.

<a id="cachetools.RRCache"></a>

## RRCache Objects

```python
class RRCache(Cache)
```

Random Replacement (RR) cache implementation.

<a id="cachetools.RRCache.choice"></a>

#### choice

```python
@property
def choice()
```

The `choice` function used by the cache.

<a id="cachetools.RRCache.popitem"></a>

#### popitem

```python
def popitem()
```

Remove and return a random `(key, value)` pair.

<a id="cachetools._TimedCache"></a>

## \_TimedCache Objects

```python
class _TimedCache(Cache)
```

Base class for time aware cache implementations.

<a id="cachetools._TimedCache.timer"></a>

#### timer

```python
@property
def timer()
```

The timer function used by the cache.

<a id="cachetools.TTLCache"></a>

## TTLCache Objects

```python
class TTLCache(_TimedCache)
```

LRU Cache implementation with per-item time-to-live (TTL) value.

<a id="cachetools.TTLCache.ttl"></a>

#### ttl

```python
@property
def ttl()
```

The time-to-live value of the cache's items.

<a id="cachetools.TTLCache.expire"></a>

#### expire

```python
def expire(time=None)
```

Remove expired items from the cache and return an iterable of the
expired `(key, value)` pairs.

<a id="cachetools.TTLCache.popitem"></a>

#### popitem

```python
def popitem()
```

Remove and return the `(key, value)` pair least recently used that
has not already expired.

<a id="cachetools.TLRUCache"></a>

## TLRUCache Objects

```python
class TLRUCache(_TimedCache)
```

Time aware Least Recently Used (TLRU) cache implementation.

<a id="cachetools.TLRUCache.ttu"></a>

#### ttu

```python
@property
def ttu()
```

The local time-to-use function used by the cache.

<a id="cachetools.TLRUCache.expire"></a>

#### expire

```python
def expire(time=None)
```

Remove expired items from the cache and return an iterable of the
expired `(key, value)` pairs.

<a id="cachetools.TLRUCache.popitem"></a>

#### popitem

```python
def popitem()
```

Remove and return the `(key, value)` pair least recently used that
has not already expired.

<a id="cachetools.cached"></a>

#### cached

```python
def cached(cache, key=keys.hashkey, lock=None, condition=None, info=False)
```

Decorator to wrap a function with a memoizing callable that saves
results in a cache.

<a id="cachetools.cachedmethod"></a>

#### cachedmethod

```python
def cachedmethod(cache, key=keys.methodkey, lock=None, condition=None)
```

Decorator to wrap a class or instance method with a memoizing
callable that saves results in a cache.

