"""Unit tests for configuration management."""

import pytest

from tsv_to_yaml_converter.config import Config


class TestConfig:
    """Test cases for Config class."""

    def test_default_config(self):
        """Test default configuration."""
        config = Config()

        assert config.yaml_indent == 2
        assert config.yaml_width == 120  # Default is 120, not 80
        assert config.mappings_file == "mappings.json"

    def test_config_from_dict(self):
        """Test configuration from dictionary."""
        config_dict = {
            "yaml_indent": 4,
            "yaml_width": 120,
            "mappings_file": "custom_mappings.json",
        }

        config = Config(**config_dict)

        assert config.yaml_indent == 4
        assert config.yaml_width == 120
        assert config.mappings_file == "custom_mappings.json"

    def test_config_validation(self):
        """Test configuration validation."""
        # Test invalid yaml_indent
        with pytest.raises(ValueError):
            Config(yaml_indent=0)

        # Test invalid yaml_width
        with pytest.raises(ValueError):
            Config(yaml_width=0)
