from importlib.metadata import version

__version__ = version("dummio")


from dummio import json as json
from dummio import text as text
from dummio.constants import ModuleProtocol as ModuleProtocol

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
