# AwareCache


`awarecache` is a versatile caching library that provides context-aware caching with customizable eviction policies and detailed cache metrics. It allows you to manage different caches for different contexts with various caching strategies, and track performance metrics such as cache hits and misses.

## Features

- **Context-Aware Caching**: Manage different caches for different contexts.
- **Customizable Eviction Policies**: Choose from LRU, LFU, MRU, FIFO, TinyLFU, SLRU, and Clock caching strategies.
- **Cache Metrics**: Track cache performance with hit and miss statistics.

## Use Cases

1. **Web Applications**: Manage different caches for user sessions, API responses, and static content with context-specific eviction policies.
2. **Data Processing Pipelines**: Use specialized caches for different stages of data processing to optimize performance and resource usage.
3. **Microservices**: Maintain separate caches for different services or components, each with its own eviction strategy.

## Installation

You can install `awarecache` via pip:

```bash
pip install awarecache
```

## Usage

### Basic Example

Here's a quick example to get you started:

```python
from awarecache import Cache

# Create a Cache instance with default LRU policy and a capacity of 100
cache = Cache()

# Set context-specific policies
cache.set_context_policy('user_sessions', 'LRU', capacity=50)
cache.set_context_policy('api_responses', 'LFU', capacity=200)

# Add and retrieve items from the 'user_sessions' cache
cache.put('session1', 'data1', context='user_sessions')
print(cache.get('session1', context='user_sessions'))  # Output: data1

# Add and retrieve items from the 'api_responses' cache
cache.put('response1', 'data2', context='api_responses')
print(cache.get('response1', context='api_responses'))  # Output: data2

# Get cache performance metrics
print(cache.get_metrics())  # Output: {'hits': 2, 'misses': 0}
```

### Supported Eviction Policies

- **LRU (Least Recently Used)**: Removes the least recently accessed item.
- **LFU (Least Frequently Used)**: Removes the least frequently accessed item.
- **MRU (Most Recently Used)**: Removes the most recently accessed item.
- **FIFO (First In, First Out)**: Removes the oldest item.
- **TinyLFU**: A variant of LFU that uses a probabilistic approach for cache eviction.
- **SLRU (Segmented LRU)**: Combines LRU with a segmented approach to differentiate between frequently and infrequently accessed items.
- **Clock**: A circular buffer approach to manage cache items with a clock-like replacement strategy.
