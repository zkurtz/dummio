# dummio

IO for dummies! We make IO as easy as possible by providing a unified `save`/`load` interface, using the most common and recommendable default options for IO between various object types and file types. (Users may pass additional keyword arguments to the underlying IO methods.)

## Simple IO calls

dummio simplifies IO calls for some file types. For example, instead of
```
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
```
you can simply
```
data = dummio.json.load(file_path)
```

## Standardized IO interface

In some coding applications it is desirable to pass an IO module as an argument to a function. Here it is convenient to pass a dummio submodule, since all dummio submodules have the same `save` and `load` interface, having equivalent signatures (except for differences hidden in `**kwargs`).

## Supported object and file types

So far we support:
- text, pickle, and dill
- simple dictionaries:
    - json
    - yaml
- pandas dataframes:
    - csv
    - feather
    - parquet
- onnx.ModelProto instances
- pydantic models (relying on the built-in json serialization methods)

Filepaths passed to `save` and `load` methods can be of type `str`, `pathlib.Path`, or `universal_pathlib.UPath` such that many of these methods will "just work" against cloud paths like `UPath("s3://bucket/key")`, `UPath("gs://bucket/key")`, or `UPath("az://container/key")`.

## Dependencies

dummio has no required dependencies. For example, calling `from dummio.pandas import df_parquet` will raise a helpful message to install pandas if you have not already done so.

## Examples

Basic IO methods can be accessed directly as `dummio.text`, `dummio.json`, etc:.
```
import dummio

text = "hello world"
data = {"key": text}
path = "io_example_file"

# Text
dummio.text.save(text, path=path)
assert text == dummio.text.load(path)

# YAML
dummio.yaml.save(data)
assert data == dummio.yaml.load(path)
```

## Installation

We're [on pypi](https://pypi.org/project/dummio/), so `pip install dummio`.

If working directly on this repo, consider using the [simplest-possible virtual environment](https://gist.github.com/zkurtz/4c61572b03e667a7596a607706463543).
