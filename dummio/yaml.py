"""IO for yaml."""

try:
    import yaml
except ImportError:
    raise ImportError("Please install pyyaml to use dummio.yaml")

from dummio.constants import DEFAULT_ENCODING, DEFAULT_WRITE_MODE, AnyDict, PathType


def save(
    data: AnyDict,
    *,
    filepath: PathType,
    encoding: str = DEFAULT_ENCODING,
    mode: str = DEFAULT_WRITE_MODE,
) -> None:
    """Save a yaml file."""
    with open(filepath, mode, encoding=encoding) as file:
        yaml.dump(data, file)


def load(filepath: PathType, encoding: str = DEFAULT_ENCODING) -> AnyDict:
    """Read a yaml file."""
    with open(filepath, "r", encoding=encoding) as file:
        return yaml.load(file, Loader=yaml.FullLoader)
