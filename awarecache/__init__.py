from .cache import Cache
from .cache_strategies import (
    LFUCache,
    LRUCache,
    TinyLFUCache,
    MRUCache,
    FIFOCache,
    SLRUCache,
    ClockCache,
)
from .cache_metrics import CacheMetrics

__all__ = [
    "Cache",
    "LRUCache",
    "LFUCache",
    "TinyLFUCache",
    "MRUCache",
    "FIFOCache",
    "SLRUCache",
    "ClockCache",
    "CacheMetrics",
]

__version__ = "1.5.12"
__author__ = "Tobi Ayodeji"
__email__ = "philayodeji07@gmail.com"


def get_version():
    return __version__
