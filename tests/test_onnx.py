from pathlib import Path

from dummio import onnx as onnx_io


def test_onnx_io_cycle(tmp_path: Path) -> None:
    _ = onnx_io.example(tmp_path / "model.onnx")
