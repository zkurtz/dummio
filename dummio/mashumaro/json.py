"""IO for mashumaro dataclasses.

This module supports IO only for a particular simple case of mashumaro dataclasses, where the class inherits from
`DataClassJSONMixin`. This mixin provides serialization and deserialization methods to and from dictionaries.
"""

from typing import Type, TypeVar

from mashumaro.mixins.json import DataClassJSONMixin
from upath import UPath

from dummio.constants import PathType

T = TypeVar("T", bound=DataClassJSONMixin)


def save(
    data: DataClassJSONMixin,
    *,
    filepath: PathType,
) -> None:
    """Save a mashumaro dataclass instance to a json text file."""
    json_str = data.to_json()
    assert isinstance(json_str, str), "expected a string from to_json()"
    UPath(filepath).write_text(json_str)


def load(
    filepath: PathType,
    *,
    model: Type[T],
) -> T:
    """Load a mashumaro dataclass instance from a json text file."""
    json_str = UPath(filepath).read_text()
    return model.from_json(json_str)


def example(filepath: PathType) -> None:
    """Example of using the mashumaro IO."""
    from dataclasses import dataclass
    from datetime import datetime, timezone
    from uuid import UUID, uuid4

    @dataclass
    class Data(DataClassJSONMixin):
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
