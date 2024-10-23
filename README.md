# ezio

A lightweight collection of standardized wrappers for IO of common file types, including text, yaml, and json.

`ezio` replaces entire blocks of code like 
```
import json

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
```
with simply
```
import ezio

data = ezio.json.load(file_path)
```

Users should not need to worry about encodings or file open `mode` options for 99% of use cases. However, you may pass additional keyword arguments to the underlying IO methods.

## Examples

```
import ezio

text = "hello world"
data = {"key": text}
path = "io_example_file"

# Text
ezio.text.save(text, path=path)
assert text == ezio.text.load(path)

# JSON
ezio.json.save(data)
assert data == ezio.json.load(path)

# YAML
ezio.yaml.save(data)
assert data == ezio.yaml.load(path)
```

## Development

Install poetry:
```
curl -sSL https://install.python-poetry.org | python3 -
```

Install [pyenv and its virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv). Then:
```
pyenv install 3.12.2
pyenv global 3.12.2
pyenv virtualenv 3.12.2 ezio
pyenv activate ezio
```

Install this package and its dependencies in your virtual env:
```
poetry install --with io_modules --with dev
```

Set up git hooks:
```
pre-commit install
```
