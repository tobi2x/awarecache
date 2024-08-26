from .cache_metrics import CacheMetrics
from .cache_strategies import (
    LFUCache,
    LRUCache,
    TinyLFUCache,
    MRUCache,
    FIFOCache,
    SLRUCache,
    ClockCache,
)


class Cache:
    """
    A context-aware caching system that supports different eviction policies and tracks cache metrics.

    Attributes:
        default_policy (str): The default eviction policy ('LRU', 'LFU', 'MRU', 'FIFO', 'TinyLFU', 'SLRU', 'Clock').
        default_capacity (int): The default capacity of the cache.
        context_cache (dict): A dictionary holding caches for different contexts.
        context_policies (dict): A dictionary holding policies and capacities for different contexts.
        metrics (CacheMetrics): An instance of CacheMetrics for tracking cache performance.
    """

    POLICY_MAP = {
        "LRU": LRUCache,
        "LFU": LFUCache,
        "MRU": MRUCache,
        "FIFO": FIFOCache,
        "TinyLFU": TinyLFUCache,
        "SLRU": SLRUCache,
        "Clock": ClockCache,
    }

    def __init__(self, default_policy="LRU", default_capacity=100):
        """
        Initializes the Cache with a default policy and capacity.

        Args:
            default_policy (str): The default eviction policy ('LRU', 'LFU', 'MRU', 'FIFO', 'TinyLFU', 'SLRU', 'Clock').
            default_capacity (int): The default capacity of the cache.
        """
        self.default_policy = default_policy
        self.default_capacity = default_capacity
        self.context_cache = {}
        self.context_policies = {}
        self.metrics = CacheMetrics()

    def set_context_policy(self, context, policy, capacity=None):
        """
        Sets the eviction policy and capacity for a specific context.

        Args:
            context (str): The context for which to set the policy.
            policy (str): The eviction policy ('LRU', 'LFU', 'MRU', 'FIFO', 'TinyLFU', 'SLRU', 'Clock').
            capacity (int, optional): The capacity of the cache for this context. Defaults to the default capacity.

        Raises:
            ValueError: If context is empty, policy is invalid, or capacity is non-positive.
        """
        if not context:
            raise ValueError("Context must be a non-empty string.")
        if policy not in self.POLICY_MAP:
            raise ValueError(
                "Policy must be one of ['LRU', 'LFU', 'MRU', 'FIFO', 'TinyLFU', 'SLRU', 'Clock']."
            )
        if capacity is not None and capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")

        self.context_policies[context] = {
            "policy": policy,
            "capacity": capacity or self.default_capacity,
        }
        self.context_cache[context] = self._create_cache(policy, capacity)

    def _create_cache(self, policy, capacity):
        """
        Creates a cache based on the specified policy.

        Args:
            policy (str): The eviction policy ('LRU', 'LFU', 'MRU', 'FIFO', 'TinyLFU', 'SLRU', 'Clock').
            capacity (int): The capacity of the cache.

        Returns:
            Cache: An instance of the appropriate cache implementation based on the policy.

        Raises:
            ValueError: If the policy is unknown.
        """
        if policy in self.POLICY_MAP:
            return self.POLICY_MAP[policy](capacity)
        else:
            raise ValueError(f"Unknown policy: {policy}")

    def get_cache(self, context):
        """
        Retrieves the cache for a specific context.

        Args:
            context (str): The context for which to retrieve the cache.

        Returns:
            Cache: The cache instance for the specified context.

        Raises:
            ValueError: If the context does not exist.
        """
        if context not in self.context_cache:
            raise ValueError(f"Context '{context}' not set or does not exist.")
        return self.context_cache[context]

    def get(self, key, context):
        """
        Retrieves a value from the cache for a specific context.

        Args:
            key (str): The key to retrieve.
            context (str): The context for which to retrieve the value.

        Returns:
            The value associated with the key, or -1 if the key is not present.

        Raises:
            ValueError: If the key is empty or the context does not exist.
        """
        if not key:
            raise ValueError("Key must be a non-empty string.")
        cache = self.get_cache(context)
        value = cache.get(key)
        if value != -1:
            self.metrics.record_hit()
        else:
            self.metrics.record_miss()
        return value

    def put(self, key, value, context):
        """
        Inserts a key-value pair into the cache for a specific context.

        Args:
            key (str): The key to insert.
            value: The value to insert.
            context (str): The context for which to insert the key-value pair.

        Raises:
            ValueError: If the key is empty or the context does not exist.
        """
        if not key:
            raise ValueError("Key must be a non-empty string.")
        if context not in self.context_cache:
            raise ValueError(f"Context '{context}' not set or does not exist.")
        cache = self.get_cache(context)
        cache.put(key, value)
        self.metrics.record_miss()  # Assuming put implies a miss initially

    def clear_cache(self, context=None):
        """
        Clears the cache for a specific context or for all contexts if no context is specified.

        Args:
            context (str, optional): The context for which to clear the cache. If None, clears all caches.

        Raises:
            ValueError: If the context does not exist.
        """
        if context:
            if context not in self.context_cache:
                raise ValueError(f"Context '{context}' not set or does not exist.")
            self.context_cache[context].clear()
        else:
            for cache in self.context_cache.values():
                cache.clear()

    def get_metrics(self) -> dict[str, int]:
        """
        Retrieves the cache performance metrics.

        Returns:
            dict: A dictionary containing the number of hits and misses.
        """
        return self.metrics.get_metrics()
