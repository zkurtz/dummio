"""Show how to use dummio for IO of a pandas data frame vs cloud locations.

This should work for any cloud supported by universal_pathlib. For this demo, we use Google Cloud Storage.

GCS setup:
1. Create a Google Cloud Storage bucket.
2. Set up Google Cloud SDK.
    - mac: `brew install --cask google-cloud-sdk`
3. `gcloud init` and follow the web-browser pop-up instructions.
4. `gcloud auth application-default login` and follow the web-browser pop-up instructions.

s3 setup:
1. Create an S3 bucket.
2. Set up AWS CLI (maybe not necessary?).
    - mac: `brew install awscli`
3. Set up an IAM user in the AWS console, create access keys, and use them to configure environment variables:
    - `AWS_ACCESS_KEY_ID`
    - `AWS_SECRET_ACCESS_KEY`

Azure setup:
1. Create an Azure Storage container.
2. Set up Azure CLI.
    - mac: `brew install azure-cli`
4. `az login` and follow the web-browser pop-up instructions.

Run this script from the repo root like
```
python demo/cloud.py --path="gcs://dummio-demo/dataframes"
python demo/cloud.py --path="s3://dummio-demo/dataframes"
python demo/cloud.py --path="az://dummio/demo/dataframes"
```
"""

import click
import pandas as pd
from upath import UPath
from upath.implementations.cloud import AzurePath

from dummio.pandas import df_csv, df_feather, df_parquet


@click.command()
@click.option(
    "--path",
    type=str,
    required=True,
    help="Cloud directory path parsable by universal_pathlib.",
)
def example(path: str) -> None:
    """Show how to use dummio for IO of a pandas data frame vs a cloud location."""
    directory = UPath(path)

    # set up is more complex for azure, requiring explicit credential passing:
    if isinstance(directory, AzurePath):
        from adlfs import AzureBlobFileSystem
        from azure.identity import DefaultAzureCredential

        azure_creds = DefaultAzureCredential()
        token = azure_creds.get_token("https://storage.azure.com/.default").token
        abfs = AzureBlobFileSystem(account_name="dummio", credential=token)
        directory = UPath(path, fs=abfs)

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    csv_path = directory / "data.csv"
    parquet_path = directory / "data.parquet"
    feather_path = directory / "data.feather"

    print("Trying native pandas methods:")
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path)
    df.to_feather(feather_path)
    assert pd.read_csv(csv_path).equals(df)
    assert pd.read_parquet(parquet_path).equals(df)
    assert pd.read_feather(feather_path).equals(df)
    for univ_path in [csv_path, parquet_path, feather_path]:
        univ_path.unlink()

    print(f"Doing IO of df against {csv_path}")
    df_csv.save(data=df, filepath=csv_path)
    assert df_csv.load(filepath=csv_path).equals(df)

    print(f"Doing IO of df against {parquet_path}")
    df_parquet.save(data=df, filepath=parquet_path)
    assert df_parquet.load(filepath=parquet_path).equals(df)

    print(f"Doing IO of df against {feather_path}")
    df_feather.save(data=df, filepath=feather_path)
    assert df_feather.load(filepath=feather_path).equals(df)


if __name__ == "__main__":
    example()
