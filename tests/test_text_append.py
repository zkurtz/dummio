"""Ensure we can write to text with append mode."""

from pathlib import Path

import dummio


def test_text_append(tmp_path: Path) -> None:
    data = "Hello world!"
    path = tmp_path / "data.txt"
    dummio.text.save(data, filepath=path)
    dummio.text.save(data, filepath=path, mode="a")
    loaded_data = dummio.text.load(path)
    assert data + data == loaded_data
