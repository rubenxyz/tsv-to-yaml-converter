"""TSV to YAML Shot List Converter.

A batch processing tool for converting film/video shot lists from TSV format
to hierarchical YAML format following standardized input/output patterns.
"""

__version__ = "1.0.0"
__author__ = "Claude"
__email__ = "claude@example.com"

from .cli_commands import CLICommands
from .config import Config
from .converter import TSVToYAMLConverter
from .data_processor import DataProcessor
from .error_handler import ErrorHandler
from .file_manager import FileManager
from .tsv_reader import TSVReader
from .yaml_writer import YAMLWriter

__all__ = [
    "TSVToYAMLConverter",
    "Config",
    "TSVReader",
    "DataProcessor",
    "YAMLWriter",
    "FileManager",
    "ErrorHandler",
    "CLICommands",
]
