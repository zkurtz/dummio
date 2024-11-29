"""IO for pydantic models."""

from pathlib import Path
from typing import Type

import pydantic

from dummio.constants import PathType


def save(
    data: pydantic.BaseModel,
    *,
    filepath: PathType,
) -> None:
    """Save a pydantic model instance to a json text file."""
    data_json_str = data.model_dump_json()
    Path(filepath).write_text(data_json_str)


def load(
    filepath: PathType,
    *,
    model: Type[pydantic.BaseModel],
) -> pydantic.BaseModel:
    """Load a pydantic model instance from a json text file."""
    data_json_str = Path(filepath).read_text()
    return model.model_validate_json(data_json_str)
