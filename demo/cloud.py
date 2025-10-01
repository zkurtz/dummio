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
python demo/cloud.py --directory="s3://dummio-demo" --file_type="text"
python demo/cloud.py --directory="s3://dummio-demo" --file_type="yaml"
python demo/cloud.py --directory="gcs://dummio-demo" --file_type="json"
python demo/cloud.py --directory="gcs://dummio-demo" --file_type="orjson"
python demo/cloud.py --directory="s3://dummio-demo" --file_type="pickle"
python demo/cloud.py --directory="s3://dummio-demo" --file_type="dill"
python demo/cloud.py --directory="s3://dummio-demo" --file_type="pydantic"
python demo/cloud.py --directory="gcs://dummio-demo" --file_type="onnx"
python demo/cloud.py --directory="gcs://dummio-demo" --file_type="pandas_df"
python demo/cloud.py --directory="s3://dummio-demo" --file_type="pandas_df"
python demo/cloud.py --directory="gcs://dummio-demo" --file_type="numpy"
python demo/cloud.py --directory="az://dummio/demo" --file_type="pandas_df"
```
"""

import click
import pandas as pd
from upath import UPath
from upath.implementations.cloud import AzurePath

import dummio
from dummio.pandas import df_csv, df_feather, df_parquet

USE_DICT = [
    "json",
    "orjson",
    "yaml",
    "dill",
    "pickle",
]


def as_upath(directory: str) -> UPath:
    """Convert a string path to a UPath."""
    path = UPath(directory)

    # set up is more complex for azure, requiring explicit credential passing:
    if isinstance(path, AzurePath):
        from adlfs import AzureBlobFileSystem
        from azure.identity import DefaultAzureCredential

        azure_creds = DefaultAzureCredential()
        token = azure_creds.get_token("https://storage.azure.com/.default").token
        abfs = AzureBlobFileSystem(account_name="dummio", credential=token)
        path = UPath(path, fs=abfs)
    return path


def _text(directory: UPath) -> None:
    """Do IO of text against a cloud location."""
    text = "Hello, world!"
    text_path = directory / "text.txt"

    print("You don't need dummio for text!")
    text_path.write_text(text)
    assert text_path.read_text() == text
    text_path.unlink()

    print("But can use dummio if you want to.")
    dummio.text.save(data=text, filepath=text_path)
    assert dummio.text.load(filepath=text_path) == text
    text_path.unlink()

    print("Dummio also supports append mode (while native pathlib write_text does not).")
    dummio.text.save(text, filepath=text_path)
    dummio.text.save(text, filepath=text_path, mode="a")
    loaded_text = dummio.text.load(text_path)
    assert loaded_text == text + text


def _dict_io(directory: UPath, file_type: str) -> None:
    """Do IO of a dictionary against a cloud location."""
    data = {"a": 1, "b": 2}
    data_path = directory / f"{file_type}/data.{file_type}"

    print(f"Doing IO of a dictionary-as-{file_type} against {data_path}.")
    module = getattr(dummio, file_type)
    module.save(data=data, filepath=data_path)
    assert module.load(filepath=data_path) == data


def _pandas_df(directory: UPath) -> None:
    """Do IO of pandas data frames against a cloud location."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    csv_path = directory / "dataframes" / "data.csv"
    parquet_path = directory / "dataframes" / "data.parquet"
    feather_path = directory / "dataframes" / "data.feather"

    print(f"Doing IO of df against {csv_path}")
    df_csv.save(data=df, filepath=csv_path)
    assert df_csv.load(filepath=csv_path).equals(df)

    print(f"Doing IO of df against {parquet_path}")
    df_parquet.save(data=df, filepath=parquet_path)
    assert df_parquet.load(filepath=parquet_path).equals(df)

    print(f"Doing IO of df against {feather_path}")
    df_feather.save(data=df, filepath=feather_path)
    assert df_feather.load(filepath=feather_path).equals(df)


@click.command()
@click.option(
    "--directory",
    type=str,
    required=True,
    help="Cloud directory path parsable by universal_pathlib.",
)
@click.option(
    "--file_type",
    type=str,
    default="pandas_df",
    help="Type of data to use for the demo: text, dict, pandas_df",
)
def example(directory: str, file_type: str) -> None:
    """Show how to use dummio for IO of a pandas data frame vs a cloud location."""
    _directory = as_upath(directory)
    if file_type in USE_DICT:
        _dict_io(directory=_directory, file_type=file_type)
    elif file_type == "text":
        _text(_directory)
    elif file_type == "onnx":
        from dummio import onnx

        onnx.example(filepath=_directory / "onnx" / "model.onnx")
    elif file_type == "pydantic":
        from dummio import pydantic

        pydantic.example(filepath=_directory / "pydantic" / "data.json")
    elif file_type == "pandas_df":
        _pandas_df(_directory)
    elif file_type == "numpy":
        from dummio.numpy import ndarray_io

        ndarray_io.example(filepath=_directory / "numpy" / "data.npy")
        ndarray_io.example(filepath=_directory / "numpy" / "weirdfilename")
    else:
        raise ValueError(f"Unrecognized file_type: {file_type}")


if __name__ == "__main__":
    example()
