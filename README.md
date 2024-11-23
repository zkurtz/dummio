# dummio

IO for dummies! We make IO as easy as possible by implementing the most common and recommendable default options. (Users may pass additional keyword arguments to the underlying IO methods.) For example, instead of
```
import json

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
```
you can simply
```
import dummio

data = dummio.json.load(file_path)
```

So far we support:
- text
- json
- yaml

Note that `yaml` is not a required dependency; you may install `dummio` and use it for `json` without bothering with `yaml` installation. Any other IO modules to be added will similarly be optional.

## Examples

```
import dummio

text = "hello world"
data = {"key": text}
path = "io_example_file"

# Text
dummio.text.save(text, path=path)
assert text == dummio.text.load(path)

# JSON
dummio.json.save(data)
assert data == dummio.json.load(path)

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
uv sync
source .venv/bin/activate
pre-commit install
```
