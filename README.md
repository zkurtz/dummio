# dummio

Standardized wrappers for IO of various file types. The goal is to make IO as easy as possible by implementing the most common and recommendable default options. Of course users may pass additional keyword arguments to the underlying IO methods.

`dummio` replaces entire blocks of code like
```
import json

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
```
with simply
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

## Development

Install poetry:
```
curl -sSL https://install.python-poetry.org | python3 -
```

Install [pyenv and its virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv). Then:
```
pyenv install 3.12.2
pyenv global 3.12.2
pyenv virtualenv 3.12.2 dummio
pyenv activate dummio
```

Install this package and its dependencies in your virtual env:
```
poetry install --with extras --with dev
```

Set up git hooks:
```
pre-commit install
```
