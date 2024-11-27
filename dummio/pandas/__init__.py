try:
    import pandas

    del pandas
except ImportError:
    raise ImportError("Please install pandas to use dummio.pandas")

from dummio.pandas import df_csv as df_csv
from dummio.pandas import df_parquet as df_parquet
