# API Documentation

## Overview

The TSV to YAML converter provides a comprehensive API for batch processing TSV shot list files. The package is organized into several modules, each with specific responsibilities.

## Core Modules

### `tsv_to_yaml_converter.converter`

The main conversion logic module.

#### `TSVToYAMLConverter`

The primary class for batch processing TSV files.

```python
class TSVToYAMLConverter:
    def __init__(self, project_root: Path, config: Optional[Config] = None)
```

**Parameters:**
- `project_root`: Root directory for the project
- `config`: Optional configuration object

**Methods:**

- `convert_tsv_to_yaml(tsv_file: Path, output_file: Path, project_title: Optional[str] = None) -> bool`
  - Convert a single TSV file to YAML format
  - Returns `True` if successful, `False` otherwise

- `process_files(config_file: Optional[Path] = None) -> bool`
  - Process all TSV files in the input directory
  - Returns `True` if all files processed successfully

- `analyze_files() -> Dict[str, Any]`
  - Analyze all files in the input directory without processing
  - Returns detailed analysis results

### `tsv_to_yaml_converter.config`

Configuration management using Pydantic models.

#### `Config`

Configuration class with validation.

```python
class Config(BaseModel):
    project_title: Optional[str] = None
    verbose_logging: bool = False
    preserve_directory_structure: bool = True
    yaml_indent: int = 2
    yaml_width: int = 120
```

**Methods:**

- `from_file(config_path: Path) -> Config`
  - Load configuration from YAML file

- `save_to_file(config_path: Path) -> None`
  - Save configuration to YAML file

### `tsv_to_yaml_converter.models`

Pydantic models for data validation and serialization.

#### Data Models

- `ShotList`: Complete shot list structure
- `Project`: Project information
- `Epoch`: Epoch containing multiple scenes
- `Scene`: Scene containing multiple shots
- `Shot`: Individual shot information
- `Timecode`: Timecode information
- `CameraMovement`: Camera movement details
- `TimePeriod`: Time period for epochs
- `Statistics`: Processing statistics

### `tsv_to_yaml_converter.logging`

Logging utilities and log generation.

#### `LogManager`

Manages logging configuration and log generation.

```python
class LogManager:
    def __init__(self, verbose: bool = False)
```

**Methods:**

- `save_logs(stats: Dict, output_dir: Path, input_dir: Path) -> None`
  - Generate and save XML and Markdown logs

## Usage Examples

### Basic Usage

```python
from pathlib import Path
from tsv_to_yaml_converter import TSVToYAMLConverter

# Initialize converter
converter = TSVToYAMLConverter(Path("./project"))

# Process all files
success = converter.process_files()
```

### With Configuration

```python
from tsv_to_yaml_converter import TSVToYAMLConverter, Config

# Create custom configuration
config = Config(
    project_title="My Film Project",
    verbose_logging=True,
    yaml_indent=4
)

# Initialize converter with config
converter = TSVToYAMLConverter(Path("./project"), config)

# Process files
success = converter.process_files()
```

### File Analysis

```python
from tsv_to_yaml_converter import TSVToYAMLConverter

converter = TSVToYAMLConverter(Path("./project"))

# Analyze files without processing
results = converter.analyze_files()

print(f"Found {results['valid_tsv_files']} valid TSV files")
```

### Single File Conversion

```python
from pathlib import Path
from tsv_to_yaml_converter import TSVToYAMLConverter

converter = TSVToYAMLConverter(Path("./project"))

# Convert single file
success = converter.convert_tsv_to_yaml(
    Path("input.tsv"),
    Path("output.yaml"),
    "My Project"
)
```

## Error Handling

The converter provides comprehensive error handling:

- Individual file failures don't stop batch processing
- Detailed error information is logged
- Error statistics are tracked in the `stats` attribute

```python
converter = TSVToYAMLConverter(Path("./project"))
success = converter.process_files()

# Check for errors
if converter.stats['errors']:
    for error in converter.stats['errors']:
        print(f"Error in {error['file']}: {error['error']}")
```

## Statistics

The converter tracks processing statistics:

```python
converter = TSVToYAMLConverter(Path("./project"))
converter.process_files()

stats = converter.stats
print(f"Processed: {stats['processed_files']}")
print(f"Failed: {stats['failed_files']}")
print(f"Total: {stats['total_files']}")
```

## Logging

The package uses Loguru for structured logging:

```python
from tsv_to_yaml_converter.logging import get_logger

logger = get_logger()
logger.info("Processing started")
logger.error("An error occurred")
```

## Type Hints

All functions and methods include comprehensive type hints for better IDE support and static analysis:

```python
from typing import Optional, Dict, Any
from pathlib import Path

def convert_tsv_to_yaml(
    tsv_file: Path,
    output_file: Path,
    project_title: Optional[str] = None
) -> bool:
    ...
```