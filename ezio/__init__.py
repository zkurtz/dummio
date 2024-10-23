"""ezio initialization."""

from importlib.metadata import version

__version__ = version("ezio")


from ezio import json as json
from ezio import text as text

try:
    from ezio import yaml as yaml
except ImportError:
    # yaml is an optional dependency
    pass
