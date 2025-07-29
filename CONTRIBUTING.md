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
│       ├── converter.py         # Core conversion logic
│       ├── config.py            # Configuration management
│       ├── models.py            # Data models
│       └── logging.py           # Logging utilities
├── tests/
│   ├── __init__.py
│   └── test_converter.py        # Unit tests
├── docs/                        # Documentation
├── pyproject.toml               # Project configuration
└── README.md                    # Main documentation
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write code following the style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run quality checks
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

### 4. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat: add new configuration option"
git commit -m "fix: resolve issue with file processing"
git commit -m "docs: update API documentation"
```

### 5. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat: add support for custom output formats
fix: resolve issue with empty TSV files
docs: update installation instructions
test: add unit tests for configuration validation
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)
- Use fixtures for common setup

Example:
```python
def test_convert_tsv_to_yaml_success(temp_project_dir, sample_tsv_file):
    """Test successful TSV to YAML conversion."""
    # Arrange
    converter = TSVToYAMLConverter(temp_project_dir)
    output_file = temp_project_dir / "output.yaml"
    
    # Act
    success = converter.convert_tsv_to_yaml(sample_tsv_file, output_file)
    
    # Assert
    assert success
    assert output_file.exists()
```

### Test Coverage

- Aim for high test coverage (80%+)
- Focus on critical paths and edge cases
- Test both success and failure scenarios

## Documentation Guidelines

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google docstring format
- Include type hints for all parameters and return values

Example:
```python
def convert_tsv_to_yaml(
    tsv_file: Path,
    output_file: Path,
    project_title: Optional[str] = None
) -> bool:
    """Convert TSV shot list to hierarchical YAML format.
    
    Args:
        tsv_file: Path to input TSV file
        output_file: Path to output YAML file
        project_title: Optional project title (inferred from filename if not provided)
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
```

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Keep documentation clear and concise

## Pull Request Guidelines

### Before Submitting

1. **Ensure all tests pass**:
   ```bash
   pytest
   ```

2. **Run quality checks**:
   ```bash
   black src/ tests/
   isort src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

3. **Update documentation** if needed

4. **Add tests** for new functionality

### Pull Request Description

Include:
- Description of changes
- Motivation for changes
- Any breaking changes
- Screenshots (if UI changes)
- Test results

## Issue Reporting

When reporting issues:

1. Use the issue template
2. Provide clear steps to reproduce
3. Include error messages and stack traces
4. Specify your environment (OS, Python version, etc.)

## Code Review

All contributions require code review. Reviewers will check:

- Code quality and style
- Test coverage
- Documentation updates
- Performance implications
- Security considerations

## Getting Help

If you need help:

1. Check the documentation
2. Search existing issues
3. Create a new issue with the "question" label
4. Join our community discussions

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.