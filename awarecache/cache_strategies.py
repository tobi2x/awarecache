from collections import Counter, OrderedDict, deque, defaultdict


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


class MRUCache:
    """
    A Most Recently Used (MRU) cache implementation.

    Attributes:
        capacity (int): The maximum number of items the cache can hold.
        cache (OrderedDict): An ordered dictionary to maintain the order of items.
    """

    def __init__(self, capacity):
        """
        Initializes the MRUCache with a specified capacity.

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
            self.cache.popitem(last=True)


class FIFOCache:
    """
    A First-In, First-Out (FIFO) cache implementation.

    Attributes:
        capacity (int): The maximum number of items the cache can hold.
        cache (dict): A dictionary to store cache items.
        order (deque): A deque to maintain the order of items.
    """

    def __init__(self, capacity):
        """
        Initializes the FIFOCache with a specified capacity.

        Args:
            capacity (int): The maximum number of items the cache can hold.

        Raises:
            ValueError: If the capacity is non-positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.cache = {}
        self.order = deque()
        self.capacity = capacity

    def get(self, key):
        """
        Retrieves a value from the cache.

        Args:
            key (str): The key to retrieve.

        Returns:
            The value associated with the key, or -1 if the key is not present.
        """
        return self.cache.get(key, -1)

    def put(self, key, value):
        """
        Inserts a key-value pair into the cache.

        Args:
            key (str): The key to insert.
            value: The value to insert.
        """
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.popleft()
            del self.cache[oldest]
        self.cache[key] = value
        self.order.append(key)
        


class TinyLFUCache:
    """
    A TinyLFU cache implementation with an LRU eviction policy.

    Attributes:
        capacity (int): The maximum number of items the cache can hold.
        cache (OrderedDict): An ordered dictionary to maintain the order of items.
        frequency (Counter): A counter to maintain access frequencies.
    """

    def __init__(self, capacity):
        """
        Initializes the TinyLFUCache with a specified capacity.

        Args:
            capacity (int): The maximum number of items the cache can hold.

        Raises:
            ValueError: If the capacity is non-positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.cache = OrderedDict()
        self.frequency = Counter()
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
        self.frequency[key] += 1
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
        else:
            if len(self.cache) >= self.capacity:
                self._evict()
            self.cache[key] = value
            self.frequency[key] += 1

    def _evict(self):
        """
        Evicts the least frequently used item.
        """
        least_frequent_key = min(self.cache, key=lambda k: self.frequency[k])
        del self.cache[least_frequent_key]
        del self.frequency[least_frequent_key]


class SLRUCache:
    """
    A Segmented Least Recently Used (SLRU) cache implementation.

    Attributes:
        capacity (int): The maximum number of items the cache can hold.
        probation (deque): A deque to hold items in the probation segment.
        protected (deque): A deque to hold items in the protected segment.
        probation_cache (dict): A dictionary to store cache items in the probation segment.
        protected_cache (dict): A dictionary to store cache items in the protected segment.
        protected_capacity (int): The capacity of the protected segment.
        probation_capacity (int): The capacity of the probation segment.
    """

    def __init__(self, capacity, protected_ratio=0.5):
        """
        Initializes the SLRUCache with a specified capacity.

        Args:
            capacity (int): The maximum number of items the cache can hold.
            protected_ratio (float): The ratio of protected segment capacity to total capacity.

        Raises:
            ValueError: If the capacity is non-positive or protected_ratio is invalid.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        if not (0 < protected_ratio < 1):
            raise ValueError("Protected ratio must be between 0 and 1.")

        self.protected_capacity = int(capacity * protected_ratio)
        self.probation_capacity = capacity - self.protected_capacity

        self.probation = deque()
        self.protected = deque()
        self.probation_cache = {}
        self.protected_cache = {}

    def get(self, key):
        """
        Retrieves a value from the cache.

        Args:
            key (str): The key to retrieve.

        Returns:
            The value associated with the key, or -1 if the key is not present.
        """
        if key in self.protected_cache:
            return self.protected_cache[key]
        if key in self.probation_cache:
            value = self.probation_cache.pop(key)
            self.probation.remove(key)
            self._promote_to_protected(key, value)
            return value
        return -1

    def put(self, key, value):
        """
        Inserts a key-value pair into the cache.

        Args:
            key (str): The key to insert.
            value: The value to insert.
        """
        if key in self.protected_cache:
            self.protected_cache[key] = value
        elif key in self.probation_cache:
            self.probation_cache[key] = value
            self._promote_to_protected(key, value)
        else:
            if len(self.probation_cache) >= self.probation_capacity:
                oldest = self.probation.popleft()
                del self.probation_cache[oldest]
            self.probation_cache[key] = value
            self.probation.append(key)

    def _promote_to_protected(self, key, value):
        """
        Promotes a key-value pair from probation to protected segment.
        """
        if len(self.protected_cache) >= self.protected_capacity:
            oldest = self.protected.popleft()
            del self.protected_cache[oldest]
        self.protected_cache[key] = value
        self.protected.append(key)


class ClockCache:
    """
    A Clock (Second Chance) cache implementation.

    Attributes:
        capacity (int): The maximum number of items the cache can hold.
        cache (dict): A dictionary to store cache items.
        reference_bits (dict): A dictionary to store reference bits for each item.
        pointer (int): The current pointer for the clock algorithm.
    """

    def __init__(self, capacity):
        """
        Initializes the ClockCache with a specified capacity.

        Args:
            capacity (int): The maximum number of items the cache can hold.

        Raises:
            ValueError: If the capacity is non-positive.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.cache = {}
        self.reference_bits = {}
        self.pointer = 0
        self.capacity = capacity
        self.keys = []

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
        self.reference_bits[key] = 1
        return self.cache[key]

    def put(self, key, value):
        """
        Inserts a key-value pair into the cache.

        Args:
            key (str): The key to insert.
            value: The value to insert.
        """
        if key in self.cache:
            self.cache[key] = value
            self.reference_bits[key] = 1
            return

        if len(self.cache) < self.capacity:
            self.cache[key] = value
            self.reference_bits[key] = 1
            self.keys.append(key)
        else:
            while True:
                current_key = self.keys[self.pointer]
                if self.reference_bits[current_key] == 0:
                    del self.cache[current_key]
                    del self.reference_bits[current_key]
                    self.cache[key] = value
                    self.reference_bits[key] = 1
                    self.keys[self.pointer] = key
                    break
                else:
                    self.reference_bits[current_key] = 0
                self.pointer = (self.pointer + 1) % self.capacity
