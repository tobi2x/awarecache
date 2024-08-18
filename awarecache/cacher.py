from collections import OrderedDict, defaultdict

class Cache:
    """
    A context-aware caching system that supports different eviction policies and tracks cache metrics.
    
    Attributes:
        default_policy (str): The default eviction policy ('LRU' or 'LFU').
        default_capacity (int): The default capacity of the cache.
        context_cache (dict): A dictionary holding caches for different contexts.
        context_policies (dict): A dictionary holding policies and capacities for different contexts.
        metrics (CacheMetrics): An instance of CacheMetrics for tracking cache performance.
    """

    def __init__(self, default_policy='LRU', default_capacity=100):
        """
        Initializes the Cache with a default policy and capacity.

        Args:
            default_policy (str): The default eviction policy ('LRU' or 'LFU').
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
            policy (str): The eviction policy ('LRU' or 'LFU').
            capacity (int, optional): The capacity of the cache for this context. Defaults to the default capacity.
        
        Raises:
            ValueError: If context is empty, policy is invalid, or capacity is non-positive.
        """
        if not context:
            raise ValueError("Context must be a non-empty string.")
        if policy not in ['LRU', 'LFU']:
            raise ValueError("Policy must be either 'LRU' or 'LFU'.")
        if capacity is not None and capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        
        self.context_policies[context] = {
            'policy': policy,
            'capacity': capacity or self.default_capacity
        }
        self.context_cache[context] = self._create_cache(policy, capacity)

    def _create_cache(self, policy, capacity):
        """
        Creates a cache based on the specified policy.

        Args:
            policy (str): The eviction policy ('LRU' or 'LFU').
            capacity (int): The capacity of the cache.

        Returns:
            Cache: An instance of LRUCache or LFUCache based on the policy.

        Raises:
            ValueError: If the policy is unknown.
        """
        if policy == 'LRU':
            return LRUCache(capacity)
        elif policy == 'LFU':
            return LFUCache(capacity)
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

    def get_metrics(self):
        """
        Retrieves the cache performance metrics.

        Returns:
            dict: A dictionary containing the number of hits and misses.
        """
        return self.metrics.get_metrics()

class LFUCache:
    """
    A Least Frequently Used (LFU) cache implementation.

    Attributes:
        capacity (int): The maximum number of items the cache can hold.
        cache (dict): A dictionary storing the cache items and their frequencies.
        freq (defaultdict): A dictionary storing keys grouped by their frequencies.
        min_freq (int): The minimum frequency of the cache items.
    """

    def __init__(self, capacity):
        """
        Initializes the LFUCache with a specified capacity.

        Args:
            capacity (int): The maximum number of items the cache can hold.

        Raises:
            ValueError: If the capacity is non-positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self.cache = {}
        self.freq = defaultdict(OrderedDict)
        self.min_freq = 0

    def get(self, key):
        """
        Retrieves a value from the cache.

        Args:
            key (str): The key to retrieve.

        Returns:
            The value associated with the key, or -1 if the key is not present.
        """
        if key not in self.cache:
            return -1
        value, freq = self.cache[key]
        self._update(key, value, freq)
        return value

    def put(self, key, value):
        """
        Inserts a key-value pair into the cache.

        Args:
            key (str): The key to insert.
            value: The value to insert.

        Raises:
            ValueError: If the capacity is non-positive.
        """
        if self.capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        if key in self.cache:
            self._update(key, value, self.cache[key][1])
        else:
            if len(self.cache) >= self.capacity:
                self._evict()
            self.cache[key] = (value, 1)
            self.freq[1][key] = None
            self.min_freq = 1

    def _update(self, key, value, freq):
        """
        Updates the frequency of a cache item.

        Args:
            key (str): The key of the item to update.
            value: The new value of the item.
            freq (int): The current frequency of the item.
        """
        self.cache[key] = (value, freq + 1)
        del self.freq[freq][key]
        if not self.freq[freq]:
            del self.freq[freq]
            if freq == self.min_freq:
                self.min_freq += 1
        self.freq[freq + 1][key] = None

    def _evict(self):
        """
        Evicts the least frequently used item from the cache.
        """
        key, _ = self.freq[self.min_freq].popitem(last=False)
        del self.cache[key]

class LRUCache:
    """
    A Least Recently Used (LRU) cache implementation.

    Attributes:
        capacity (int): The maximum number of items the cache can hold.
        cache (OrderedDict): An ordered dictionary to maintain the order of items.
    """

    def __init__(self, capacity):
        """
        Initializes the LRUCache with a specified capacity.

        Args:
            capacity (int): The maximum number of items the cache can hold.

        Raises:
            ValueError: If the capacity is non-positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        """
        Retrieves a value from the cache.

        Args:
            key (str): The key to retrieve.

        Returns:
            The value associated with the key, or -1 if the key is not present.
        """
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        """
        Inserts a key-value pair into the cache.

        Args:
            key (str): The key to insert.
            value: The value to insert.
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

class CacheMetrics:
    """
    A class for tracking cache performance metrics.

    Attributes:
        hits (int): The number of cache hits.
        misses (int): The number of cache misses.
    """

    def __init__(self):
        """
        Initializes the CacheMetrics with zero hits and misses.
        """
        self.hits = 0
        self.misses = 0

    def record_hit(self):
        """
        Records a cache hit.
        """
        self.hits += 1

    def record_miss(self):
        """
        Records a cache miss.
        """
        self.misses += 1

    def get_metrics(self):
        """
        Retrieves the cache performance metrics.

        Returns:
            dict: A dictionary containing the number of hits and misses.
        """
        return {'hits': self.hits, 'misses': self.misses}
