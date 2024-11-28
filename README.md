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
- text
- simple dictionaries:
    - json
    - yaml
- pandas dataframes:
    - csv
    - parquet
- onnx.ModelProto instances

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

## Development

```
git clone git@github.com:zkurtz/dummio.git
cd dummio
pip install uv
uv sync --group extras
source .venv/bin/activate
pre-commit install
```
