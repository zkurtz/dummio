"""IO for yaml.

dummio.yaml requires ruamel.yaml (not pyyaml) because ruamel.yaml appears to be the way of the future.
"""

from upath import UPath

from dummio.constants import DEFAULT_ENCODING, DEFAULT_WRITE_MODE, AnyDict, PathType, TextMode

try:
    import ruamel.yaml as yaml
except ImportError:
    raise ImportError("Install ruamel.yaml to use dummio.yaml")


def save(
    data: AnyDict,
    *,
    filepath: PathType,
    typ: str = "rt",
    encoding: str = DEFAULT_ENCODING,
    mode: TextMode = DEFAULT_WRITE_MODE,
) -> None:
    """Save a yaml file.

    Args:
        data: The data to save.
        filepath: The file path.
        typ: The type of ruamel.yaml IO to use. "rt" for round-trip (default, a subclass of "safe").If you need faster
            IO, consider setting this to "safe" or "unsafe". See https://stackoverflow.com/a/51318354/2232265 for
            details.
        encoding: The encoding to use.
        mode: The write mode.
    """
    yaml_ = yaml.YAML(typ=typ)  # pyright: ignore
    dumper = yaml_.dump
    if isinstance(filepath, UPath):
        with filepath.open(mode, encoding=encoding) as stream:
            dumper(data, stream)
    else:
        with open(filepath, mode, encoding=encoding) as file:
            dumper(data, file)


def load(
    filepath: PathType,
    *,
    typ: str = "rt",
    encoding: str = DEFAULT_ENCODING,
) -> AnyDict:
    """Read a yaml file.

    Args:
        filepath: The file path.
        typ: The type of ruamel.yaml IO to use. "rt" for round-trip (default, a subclass of "safe").If you need faster
            IO, consider setting this to "safe" or "unsafe". See https://stackoverflow.com/a/51318354/2232265 for
            details.
        encoding: The encoding to use.
    """
    yaml_ = yaml.YAML(typ=typ)  # pyright: ignore
    loader = yaml_.load
    if isinstance(filepath, UPath):
        data_str = filepath.read_text(encoding=encoding)
        return loader(data_str)
    with open(filepath, "r", encoding=encoding) as file:
        return loader(file)
