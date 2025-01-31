"""Constants for dummio."""

from pathlib import Path
from typing import Any, Literal, TypeAlias

from upath import UPath

PathType: TypeAlias = str | Path | UPath
AnyDict: TypeAlias = dict[Any, Any]
TextMode: TypeAlias = Literal["r", "w", "a"]

DEFAULT_ENCODING = "utf-8"
DEFAULT_WRITE_MODE = "w"
