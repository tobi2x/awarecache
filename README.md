# AwareCache

## Overview

`AwareCache` is a versatile caching library that provides context-aware caching with customizable eviction policies (LRU and LFU) and detailed cache metrics. It allows you to manage different caches for different contexts with various caching strategies, and track performance metrics such as cache hits and misses.

## Features

- **Context-Aware Caching**: Manage separate caches for different contexts, each with its own eviction policy and capacity.
- **Customizable Policies**: Choose between LRU (Least Recently Used) and LFU (Least Frequently Used) caching strategies.
- **Cache Metrics**: Track cache hits and misses to monitor the performance of your caching system.
- **Simple API**: Easy-to-use API for interacting with caches and managing policies.

## Installation

You can install the package via pip:

```bash
pip install awarecache
