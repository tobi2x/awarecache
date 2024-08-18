from .awarecache.cacher import Cache, LFUCache, LRUCache, CacheMetrics

__all__ = [
    'Cache',
    'LRUCache',
    'LFUCache',
    'CacheMetrics'
]

__version__ = '1.1.0'
__author__ = 'Tobi Ayodeji'
__email__ = 'philayodeji07@gmail.com'

def get_version():
    return __version__
