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

We're [on pypi](https://pypi.org/project/dummio/) so you can just `pip install dummio` or `poetry add dummio` etc.

## Development

1. Install poetry: `curl -sSL https://install.python-poetry.org | python3 -`
1. Install [pyenv and its virtualenv plugin](https://github.com/pyenv/pyenv-virtualenv).
1. Create a dev ops virtual environment:
```
PYTHON_VERSION=3.12.2
function makenv {
    # clean up any existing env
    source deactivate
    pyenv uninstall --force $1

    # build new venv
    pyenv install $PYTHON_VERSION --skip-existing
    pyenv global $PYTHON_VERSION
    pyenv virtualenv $PYTHON_VERSION $1
    pyenv activate $1
    poetry install --with extras --with dev
    pre-commit install
    poetry lock --no-update
}
makenv dummio
```
