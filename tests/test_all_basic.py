"""Test IO methods for basic data types."""

from pathlib import Path
from types import ModuleType
from typing import Any

from upath import UPath

import dummio


def dictionary() -> dict[str, int]:
    return {"a": 1, "b": 2}


def _assert_cycle(*, data: Any, path: Path, module: ModuleType) -> None:
    """Apply the module save/load cycle on the data and assert that the reloaded data matches the input data."""

    module.save(data, filepath=path)
    loaded_data = module.load(path)
    assert data == loaded_data

    # The same cycle should work in case path is specified as a str
    str_path = str(path)
    module.save(data, filepath=str_path)
    loaded_data = module.load(str_path)
    assert data == loaded_data

    # The same cycle should work in case path is specified as a UPath
    upath_ = UPath(path)
    module.save(data, filepath=upath_)
    loaded_data = module.load(upath_)
    assert data == loaded_data


def test_json(tmp_path: Path) -> None:
    _assert_cycle(
        path=tmp_path / "data.json",
        data=dictionary(),
        module=dummio.json,
    )


def test_orjson(tmp_path: Path) -> None:
    _assert_cycle(
        path=tmp_path / "data.json",
        data=dictionary(),
        module=dummio.orjson,
    )


def test_text(tmp_path: Path) -> None:
    _assert_cycle(
        path=tmp_path / "data.json",
        data="Hello world!",
        module=dummio.text,
    )


def test_yaml(tmp_path: Path) -> None:
    _assert_cycle(
        path=tmp_path / "data.json",
        data=dictionary(),
        module=dummio.yaml,
    )


def test_pickle(tmp_path: Path) -> None:
    _assert_cycle(
        path=tmp_path / "data.pkl",
        data=dictionary(),
        module=dummio.pickle,
    )


def test_dill(tmp_path: Path) -> None:
    _assert_cycle(
        path=tmp_path / "data.pkl",
        data=dictionary(),
        module=dummio.dill,
    )
