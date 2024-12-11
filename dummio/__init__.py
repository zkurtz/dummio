from importlib.metadata import version

__version__ = version("dummio")


from dummio import json as json
from dummio import pickle as pickle
from dummio import text as text

try:
    from dummio import yaml as yaml
except ImportError:
    # this would require an optional yaml dependency such as pyyaml
    pass

try:
    from dummio import onnx as onnx
except ImportError:
    # this would require the optional dependency onnx
    pass

try:
    from dummio import pydantic as pydantic
except ImportError:
    # this would require the optional dependency pydantic
    pass

try:
    from dummio import dill as dill
except ImportError:
    # this would require the optional dependency dill
    pass
