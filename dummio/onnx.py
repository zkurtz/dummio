"""IO methods for sklearn models using ONNX serialization."""

import onnx

from dummio.constants import PathType


def save(data: onnx.ModelProto, *, filepath: PathType) -> None:
    """Saves a sklearn model to a file using ONNX serialization.

    Args:
        data: Data to save. This needs to be an sklearn model.
        filepath: Path to save the data.
    """
    byte_str = data.SerializeToString()
    with open(filepath, "wb") as file:
        file.write(byte_str)


def load(filepath: PathType) -> onnx.ModelProto:
    """Loads a sklearn model from a file using ONNX serialization.

    Args:
        filepath: Path to read the data.
    """
    with open(filepath, "rb") as file:
        byte_str = file.read()
    return onnx.load_model_from_string(byte_str)
