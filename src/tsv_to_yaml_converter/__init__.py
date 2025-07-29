"""TSV to YAML Shot List Converter.

A batch processing tool for converting film/video shot lists from TSV format
to hierarchical YAML format following standardized input/output patterns.
"""

__version__ = "1.0.0"
__author__ = "Claude"
__email__ = "claude@example.com"

from .converter import TSVToYAMLConverter
from .config import Config

__all__ = [
    "TSVToYAMLConverter",
    "Config",
]