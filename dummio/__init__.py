from importlib.metadata import version

__version__ = version("dummio")


from dummio import json as json
from dummio import text as text

try:
    from dummio import yaml as yaml
except ImportError:
    # yaml is an optional dependency
    pass
