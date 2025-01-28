"""IO methods for sklearn models using ONNX serialization."""

import onnx
from upath import UPath

from dummio.constants import PathType


def save(data: onnx.ModelProto, *, filepath: PathType) -> None:
    """Saves a sklearn model to a file using ONNX serialization.

    Args:
        data: Data to save. This needs to be an sklearn model.
        filepath: Path to save the data.
    """
    byte_str = data.SerializeToString()
    if isinstance(filepath, UPath):
        filepath.write_bytes(byte_str)
    else:
        with open(filepath, "wb") as file:
            file.write(byte_str)


def load(filepath: PathType) -> onnx.ModelProto:
    """Loads a sklearn model from a file using ONNX serialization.

    Args:
        filepath: Path to read the data.
    """
    if isinstance(filepath, UPath):
        byte_str = filepath.read_bytes()
    else:
        with open(filepath, "rb") as file:
            byte_str = file.read()
    return onnx.load_model_from_string(byte_str)


def example(filepath: PathType) -> None:
    """Show how to use onnx IO methods."""

    from skl2onnx import convert_sklearn
    from skl2onnx.common.data_types import FloatTensorType
    from sklearn.datasets import load_iris
    from sklearn.linear_model import LogisticRegression

    # Empty model:
    model = onnx.ModelProto()
    save(model, filepath=filepath)
    loaded_model = load(filepath=filepath)
    assert model.SerializeToString() == loaded_model.SerializeToString()

    # Minimal sklearn model:
    iris = load_iris()
    clr = LogisticRegression(solver="saga", max_iter=10000)
    clr.fit(iris.data, iris.target)  # pyright: ignore[reportAttributeAccessIssue]
    initial_type = [("float_input", FloatTensorType([None, 4]))]
    onx = convert_sklearn(clr, initial_types=initial_type)
    assert isinstance(onx, onnx.ModelProto)  # pyright wasn't sure

    save(onx, filepath=filepath)
    loaded_onx = load(filepath=filepath)
    assert onx.SerializeToString() == loaded_onx.SerializeToString()
