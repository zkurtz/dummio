from dummio.pandas import df_csv as df_csv
from dummio.pandas import df_parquet as df_parquet
from dummio.pandas import series_parquet as series_parquet

try:
    from dummio.pandas import df_feather as df_feather
except ImportError:
    # this would require the optional dependency pyarrow
    pass

try:
    from dummio.pandas import df_vortex as df_vortex
except ImportError:
    # this would require the optional dependency vortex-data
    pass
