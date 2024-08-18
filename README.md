# AwareCache

A context-aware caching library with customizable eviction policies and performance metrics. `awarecache` supports various cache eviction strategies, allowing you to choose the one that best fits your application's needs.

## Features

- **Context-Aware Caching**: Manage different caches for different contexts.
- **Customizable Eviction Policies**: Choose from LRU, LFU, MRU, FIFO, TinyLFU, SLRU, and Clock caching strategies.
- **Cache Metrics**: Track cache performance with hit and miss statistics.

## Installation

You can install `awarecache` via pip:

```bash
pip install awarecache