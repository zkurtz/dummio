"""IO for pydantic models."""

from typing import Type

import pydantic
from upath import UPath

from dummio.constants import PathType


def save(
    data: pydantic.BaseModel,
    *,
    filepath: PathType,
) -> None:
    """Save a pydantic model instance to a json text file."""
    data_json_str = data.model_dump_json()
    UPath(filepath).write_text(data_json_str)


def load(
    filepath: PathType,
    *,
    model: Type[pydantic.BaseModel],
) -> pydantic.BaseModel:
    """Load a pydantic model instance from a json text file."""
    data_json_str = UPath(filepath).read_text()
    return model.model_validate_json(data_json_str)


def example(filepath: PathType) -> None:
    """Example of using the pydantic IO."""
    from datetime import datetime, timezone
    from uuid import UUID, uuid4

    class Data(pydantic.BaseModel):
        id: UUID
        documentation: str
        config: dict
        rmse: float
        trained_at: datetime

    data = Data(
        id=uuid4(),
        documentation="This is a test data instance.",
        config={"n_estimators": 100, "learning_rate": 0.01},
        rmse=0.1,
        trained_at=datetime.now(timezone.utc),
    )
    save(data, filepath=filepath)
    loaded_data = load(filepath=filepath, model=Data)
    assert data == loaded_data
