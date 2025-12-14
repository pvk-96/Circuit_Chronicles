import fastf1
import os

#fastf1.Cache.enable_cache("cache")

def enable_cache():
    cache_dir = "f1cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)

