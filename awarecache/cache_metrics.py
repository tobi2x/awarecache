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
        return {"hits": self.hits, "misses": self.misses}
