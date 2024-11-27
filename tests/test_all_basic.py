"""Test IO methods for basic data types."""

from pathlib import Path
from types import ModuleType
from typing import Any

import dummio


def dictionary() -> dict[str, int]:
    return {"a": 1, "b": 2}


def _assert_cycle(*, data: Any, path: Path, module: ModuleType) -> None:
    """Apply the module save/load cycle on the data and assert that the reloaded data matches the input data."""

    module.save(data, filepath=path)
    loaded_data = module.load(path)
    assert data == loaded_data

    # The same cycle should work in case path is specified as a str instead of a pathlib.Path
    str_path = str(path)
    module.save(data, filepath=str_path)
    loaded_data = module.load(str_path)
    assert data == loaded_data


def test_json(tmp_path: Path) -> None:
    """Test the packio package."""
    _assert_cycle(
        path=tmp_path / "data.json",
        data=dictionary(),
        module=dummio.json,
    )


def test_text(tmp_path: Path) -> None:
    """Test the packio package."""
    _assert_cycle(
        path=tmp_path / "data.json",
        data="Hello world!",
        module=dummio.text,
    )


def test_yaml(tmp_path: Path) -> None:
    """Test the packio package."""
    _assert_cycle(
        path=tmp_path / "data.json",
        data=dictionary(),
        module=dummio.yaml,
    )
