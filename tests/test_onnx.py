import onnx
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

from dummio import onnx as onnx_io


def test_onnx_io_cycle(tmp_path) -> None:
    # Empty model:
    model = onnx.ModelProto()
    filepath = tmp_path / "model.onnx"
    onnx_io.save(model, filepath=filepath)
    loaded_model = onnx_io.load(filepath=filepath)
    assert model.SerializeToString() == loaded_model.SerializeToString()

    # Minimal sklearn model:
    iris = load_iris()
    clr = LogisticRegression(solver="saga", max_iter=10000)
    clr.fit(iris.data, iris.target)  # pyright: ignore[reportAttributeAccessIssue]
    initial_type = [("float_input", FloatTensorType([None, 4]))]
    onx = convert_sklearn(clr, initial_types=initial_type)
    assert isinstance(onx, onnx.ModelProto)  # pyright wasn't sure
    filepath = tmp_path / "model.onnx"
    onnx_io.save(onx, filepath=filepath)
    loaded_onx = onnx_io.load(filepath=filepath)
    assert onx.SerializeToString() == loaded_onx.SerializeToString()
