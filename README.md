# TSV to YAML Shot List Converter

A professional batch processing tool for converting film/video shot lists from TSV format to hierarchical YAML format. Follows standardized input/output patterns and modern Python development practices.

## Features

- **Batch Processing**: Process multiple TSV files at once
- **Standardized Structure**: Uses the USER-FILES directory pattern
- **Timestamped Outputs**: Each run creates a new timestamped output folder
- **Comprehensive Logging**: Both XML (machine-readable) and Markdown (human-readable) logs
- **Analysis Mode**: Analyze files without processing them
- **Configuration Support**: Use YAML configuration files for custom settings
- **Error Recovery**: Continues processing even when individual files fail
- **Modern CLI**: Rich terminal interface with progress bars and colored output
- **Type Safety**: Full type hints and Pydantic validation
- **Professional Testing**: Comprehensive test suite with pytest

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Install from Source

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd tsv-to-yaml-converter
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

4. **Install development dependencies** (optional):
   ```bash
   pip install -e ".[dev]"
   ```

## Usage

### Basic Usage

1. **Prepare your files**: Place TSV files in the `USER-FILES/01.INPUT/` directory
2. **Run the converter**: 
   ```bash
   tsv-to-yaml process
   ```
3. **Find results**: Check the `USER-FILES/02.OUTPUT/` directory for timestamped output folders

### CLI Commands

The converter provides several commands for different operations:

#### Process Files
```bash
# Process all TSV files
tsv-to-yaml process

# Process with custom configuration
tsv-to-yaml process --config config.yaml

# Process with verbose output
tsv-to-yaml process --verbose
```

#### Analyze Files
```bash
# Analyze files without processing
tsv-to-yaml analyze

# Analyze with detailed output
tsv-to-yaml analyze --verbose
```

#### Initialize Configuration
```bash
# Create default configuration file
tsv-to-yaml init-config

# Create configuration in custom location
tsv-to-yaml init-config --output my-config.yaml
```

#### Check Status
```bash
# Show current project status
tsv-to-yaml status
```

#### Global Options
```bash
# Use custom project root
tsv-to-yaml --project-root /path/to/project process

# Enable verbose output
tsv-to-yaml --verbose process

# Show version
tsv-to-yaml --version
```

## Directory Structure

```
project_root/
└── USER-FILES/
    ├── 00.READY/          # Files ready for processing (ignored by script)
    ├── 01.INPUT/          # Active input folder (script processes this)
    ├── 02.OUTPUT/         # Generated output files and folders
    │   └── {YYMMDD}_{HHMMSS}/  # Folder created for each script run
    └── 03.DONE/           # Processed input files (ignored by script)
```

## Input Format

The converter expects TSV files with the following columns:
- `EPOCH_NUM`: Epoch number
- `EPOCH_START`: Epoch start time
- `EPOCH_END`: Epoch end time
- `SCENE_NUM`: Scene number
- `LOC_TYPE`: Location type
- `TIME`: Time of day
- `LOCATION`: Location description
- `SHOT_NUM`: Shot number
- `IN`: Timecode in
- `OUT`: Timecode out
- `SPECIFIC AREA`: Specific area description
- `MOVE_SPEED`: Camera movement speed
- `MOVE_TYPE`: Camera movement type
- `ANGLE`: Shot angle
- `SHOT_DESCRIPTION`: Shot description

## Output Format

The converter generates hierarchical YAML files with the following structure:

```yaml
project:
  title: "Project Title"
  total_shots: 150
  epochs:
    - epoch_number: 1
      time_period:
        start: 1800
        end: 1900
      scenes:
        - scene_number: 1
          location_type: "Interior"
          time: "Day"
          location: "Living Room"
          shots:
            - shot_number: 1
              timecode:
                in: "00:00:00:00"
                out: "00:00:05:00"
              specific_area: "Wide shot"
              camera_movement:
                speed: "Slow"
                type: "Pan"
              angle: "Medium"
              description: "Establishing shot"
  statistics:
    total_epochs: 3
    total_scenes: 15
    total_shots: 150
    total_duration: "00:00:00:00 - 00:15:30:00"
    time_span: "1800-1900"
    shot_type_distribution:
      Medium: 75
      Wide: 45
      Close: 30
    camera_movement_distribution:
      Static: 90
      Pan: 35
      Dolly: 25
```

## Configuration

Create a configuration file to customize processing behavior:

```yaml
# config.yaml
project_title: "My Film Project"
verbose_logging: true
preserve_directory_structure: true
yaml_indent: 2
yaml_width: 120
```

### Configuration Options

- `project_title`: Override the project title (default: inferred from filename)
- `verbose_logging`: Enable detailed logging output
- `preserve_directory_structure`: Maintain input directory structure in output
- `yaml_indent`: YAML indentation level (1-8)
- `yaml_width`: YAML line width (80-200)

## Development

### Project Structure

```
tsv-to-yaml-converter/
├── src/
│   └── tsv_to_yaml_converter/
│       ├── __init__.py
│       ├── __main__.py          # CLI entry point
│       ├── converter.py         # Core conversion logic
│       ├── config.py            # Configuration management
│       ├── models.py            # Data models
│       └── logging.py           # Logging utilities
├── tests/
│   ├── __init__.py
│   └── test_converter.py        # Unit tests
├── docs/                        # Documentation
├── pyproject.toml               # Project configuration
├── README.md                    # This file
└── USER-FILES/                  # User data (gitignored)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/tsv_to_yaml_converter

# Run specific test file
pytest tests/test_converter.py

# Run with verbose output
pytest -v
```

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## Logging

Each processing run generates two log files in the output directory:

- `processing_log.xml`: Machine-readable log with detailed metadata
- `processing_log.md`: Human-readable log with summary and status

## Error Handling

The converter continues processing even when individual files fail. Failed files are logged with detailed error information, and the overall process continues to completion.

## File Management

- **Input files**: Place TSV files in `USER-FILES/01.INPUT/`
- **Processed files**: Automatically moved to `USER-FILES/03.DONE/` after successful processing
- **Output files**: Generated in timestamped folders in `USER-FILES/02.OUTPUT/`

## Version Control

The `USER-FILES/` directory is excluded from version control to prevent committing user data and generated output files.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Clone the repository
2. Install in development mode: `pip install -e ".[dev]"`
3. Install pre-commit hooks: `pre-commit install`
4. Run tests: `pytest`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- Batch processing with standardized directory structure
- Comprehensive logging (XML and Markdown)
- Type-safe configuration with Pydantic
- Modern CLI with Click and Rich
- Full test coverage
- Professional project structure