# Contributing to TSV to YAML Converter

Thank you for your interest in contributing to the TSV to YAML converter! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- pip

### Local Development

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/tsv-to-yaml-converter.git
   cd tsv-to-yaml-converter
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

## Code Style and Quality

### Code Formatting

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run these tools before committing:

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

Pre-commit hooks automatically run quality checks on commit. Install them with:

```bash
pre-commit install
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

## Project Structure

```
tsv-to-yaml-converter/
├── src/
│   └── tsv_to_yaml_converter/
│       ├── __init__.py
│       ├── __main__.py          # CLI entry point
│       ├── converter.py         # Core conversion logic (orchestrator)
│       ├── cli_commands.py      # CLI command implementations
│       ├── data_processor.py    # Data transformation logic
│       ├── tsv_reader.py        # TSV file reading and validation
│       ├── yaml_writer.py       # YAML file writing and formatting
│       ├── file_manager.py      # File system operations
│       ├── error_handler.py     # Error handling and logging
│       ├── config.py            # Configuration management
│       └── models.py            # Pydantic data models
├── tests/
│   ├── conftest.py             # Shared test fixtures
│   ├── test_converter.py       # Core conversion tests
│   ├── test_config.py          # Configuration tests
│   └── test_models.py          # Model validation tests
├── docs/                        # Documentation
├── pyproject.toml               # Project configuration
├── README.md                    # Main documentation
└── USER-FILES/                  # User data (gitignored)
```

## Development Guidelines

### Code Organization

The project follows a modular architecture with clear separation of concerns:

- **`converter.py`**: Main orchestrator that coordinates the conversion process
- **`cli_commands.py`**: CLI command implementations and UI logic
- **`data_processor.py`**: Data transformation and model building logic
- **`tsv_reader.py`**: TSV file reading, validation, and data cleaning
- **`yaml_writer.py`**: YAML file writing and formatting
- **`file_manager.py`**: File system operations and directory management
- **`error_handler.py`**: Error handling, logging, and statistics
- **`config.py`**: Configuration management and validation
- **`models.py`**: Pydantic data models for type safety

### Refactoring Guidelines

When contributing, please follow these refactoring principles:

#### File Size Limits
- **Maximum file size**: 150 lines per file
- **Target file size**: 50-100 lines for optimal maintainability
- **Large files**: Split into smaller, focused components

#### Single Responsibility Principle
- Each class should have one clear responsibility
- Each method should do one thing well
- Extract complex logic into separate modules

#### Code Quality Standards
- **No unused imports**: All imports must be actively used
- **Type hints**: All functions should have complete type annotations
- **Docstrings**: All public methods should have clear docstrings
- **Test coverage**: New features must include comprehensive tests

### Current Refactoring Priorities

Based on the latest analysis (`temp/refactor.md`), the following refactoring is planned:

#### High Priority (Immediate)
1. **Split `cli_commands.py`** (231 lines)
   - Extract UI components to `cli/ui.py`
   - Extract error handling to `cli/error_handler.py`
   - Extract mappings logic to `cli/mappings.py`

2. **Split `data_processor.py`** (223 lines)
   - Extract field mapping to `processing/field_mapper.py`
   - Extract validation to `processing/validator.py`
   - Extract formatting to `processing/formatter.py`

#### Medium Priority (Next Sprint)
3. **Extract analysis logic** from `converter.py`
   - Create `analysis/validator.py`
   - Create `analysis/analyzer.py`

### Code Quality Issues to Address

The project currently has 117 flake8 violations that need to be addressed:

- **64 line length violations**: Break long lines, extract variables
- **53 whitespace issues**: Remove trailing whitespace, fix blank lines
- **3 missing newlines**: Add newlines at end of files

## Feature Development

### Adding New Features

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow the development workflow**:
   - Write tests first (TDD approach)
   - Implement the feature
   - Ensure all tests pass
   - Run code quality tools
   - Update documentation

3. **Update tests**: Add comprehensive tests for new functionality

4. **Update documentation**: Update README.md and other relevant docs

### Example: Adding a New CLI Flag

```python
# In __main__.py
@click.option(
    "--new-flag",
    is_flag=True,
    help="Description of the new flag"
)
def process(ctx, config, new_flag):
    """Process all TSV files in the input directory."""
    commands = CLICommands(project_root, verbose)
    commands.process_files(config, new_flag)

# In cli_commands.py
def process_files(self, config, new_flag=False):
    """Process all TSV files in the input directory."""
    # Implementation here
    pass

# Add tests in test_converter.py
def test_process_with_new_flag():
    """Test processing with the new flag."""
    # Test implementation
    pass
```

## Testing Guidelines

### Test Structure

- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows

### Test Naming

- Use descriptive test names that explain the expected behavior
- Follow the pattern: `test_<method_name>_<scenario>`

### Test Coverage

- Aim for 90%+ test coverage
- Test both success and failure scenarios
- Test edge cases and boundary conditions

### Example Test

```python
def test_data_processor_formats_values_correctly():
    """Test that value formatting works correctly."""
    processor = DataProcessor(mock_tsv_reader)
    
    # Test sentence case formatting
    assert processor._format_value("MEDIEVAL_PERIOD", "period") == "Medieval period"
    
    # Test underscore removal
    assert processor._format_value("CASTLE_HALL", "location_name") == "Castle hall"
```

## Documentation Guidelines

### Code Documentation

- **Docstrings**: Use Google-style docstrings for all public methods
- **Type hints**: Include complete type annotations
- **Comments**: Add comments for complex logic

### Example Docstring

```python
def process_tsv_data(self, df: pd.DataFrame) -> Dict[int, Dict]:
    """Process TSV data into hierarchical dictionary structure.
    
    Args:
        df: Pandas DataFrame containing TSV data
        
    Returns:
        Dictionary with phase numbers as keys and phase data as values
        
    Raises:
        ValueError: If DataFrame is empty or invalid
    """
```

### README Updates

When adding new features, update the README.md to include:

- Feature description
- Usage examples
- Configuration options
- Changelog entry

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the guidelines above
3. **Run all tests** and ensure they pass
4. **Run code quality tools** and fix any issues
5. **Update documentation** as needed
6. **Create a pull request** with a clear description

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Code coverage maintained or improved

## Code Quality
- [ ] Code follows style guidelines
- [ ] No flake8 violations
- [ ] Type hints added where appropriate

## Documentation
- [ ] README.md updated
- [ ] Docstrings added/updated
- [ ] Changelog updated
```

## Code Review Guidelines

### For Reviewers

- **Check functionality**: Ensure the code works as intended
- **Review test coverage**: Verify adequate test coverage
- **Check code quality**: Look for style and quality issues
- **Verify documentation**: Ensure documentation is updated
- **Consider performance**: Check for potential performance issues

### For Contributors

- **Respond promptly** to review comments
- **Make requested changes** or explain why they're not needed
- **Test changes** after addressing feedback
- **Update PR** with any additional changes

## Release Process

### Version Bumping

- **Patch version** (1.0.1): Bug fixes
- **Minor version** (1.1.0): New features
- **Major version** (2.0.0): Breaking changes

### Release Checklist

- [ ] All tests pass
- [ ] Code quality tools pass
- [ ] Documentation is up to date
- [ ] Changelog is updated
- [ ] Version is bumped in pyproject.toml
- [ ] Release notes are prepared

## Getting Help

If you need help with development:

1. **Check the documentation**: README.md and this file
2. **Review existing code**: Look at similar implementations
3. **Run tests**: Use tests as examples of expected behavior
4. **Ask questions**: Open an issue for clarification

## Code of Conduct

This project follows the Contributor Covenant Code of Conduct. Please be respectful and inclusive in all interactions.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.