"""Public methods and classes for packio package."""

from importlib.metadata import version

from packio.io import Reader as Reader
from packio.io import Writer as Writer

__version__ = version("packio")
