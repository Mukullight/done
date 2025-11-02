import pandas as pd
from flask_caching import Cache
from pathlib import Path
from dashboard.data.loader import loader

TIMEOUT = 60 * 60 * 24  # Cache data for approximately 1 day

cache = Cache(config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache"})






@cache.memoize(timeout=TIMEOUT)
def cleaned_data() -> pd.DataFrame:
    """Function used to cache data."""
    data = loader()
    return data
