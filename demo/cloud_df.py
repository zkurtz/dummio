"""Show how to use dummio for IO of a pandas data frame vs a cloud location.

This should work for any cloud supported by universal_pathlib. For this demo, we use Google Cloud Storage.

Set up:
1. Create a Google Cloud Storage bucket.
2. Set up Google Cloud SDK.
  - mac: `brew install --cask google-cloud-sdk`
3. `gcloud init` and follow the web-browser pop-up instructions.
4. `gcloud auth application-default login` and follow the web-browser pop-up instructions.

Run this script from the repo root like
```
python demo/cloud_df.py --path="gcs://dummio-demo/dataframes"
```
"""

import click
import pandas as pd
from upath import UPath

from dummio.pandas import df_csv, df_parquet


@click.command()
@click.option(
    "--path",
    type=str,
    required=True,
    help="Cloud directory path parsable by universal_pathlib.",
)
def example(path: str) -> None:
    """Show how to use dummio for IO of a pandas data frame vs a cloud location."""
    base_path = UPath(path)
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    # parquet:
    parquet_path = base_path / "data.parquet"
    print(f"Doing IO of df against {parquet_path}")
    df_parquet.save(data=df, filepath=parquet_path)
    assert df_parquet.load(filepath=parquet_path).equals(df)

    # csv:
    csv_path = base_path / "data.csv"
    print(f"Doing IO of df against {csv_path}")
    df_csv.save(data=df, filepath=csv_path)
    assert df_csv.load(filepath=csv_path).equals(df)


if __name__ == "__main__":
    example()
