"""Unit tests for TSV to YAML converter core functionality."""

from tsv_to_yaml_converter.converter import TSVToYAMLConverter


class TestTSVToYAMLConverter:
    """Test cases for TSVToYAMLConverter class."""

    def test_initialization(self, temp_project_dir):
        """Test converter initialization."""
        converter = TSVToYAMLConverter(temp_project_dir)

        assert converter.project_root == temp_project_dir
        assert converter.input_dir.exists()
        assert converter.output_dir.exists()

    def test_clean_value(self, temp_project_dir):
        """Test value cleaning functionality."""
        converter = TSVToYAMLConverter(temp_project_dir)

        # Test None values
        assert converter.tsv_reader.clean_value(None) is None
        assert converter.tsv_reader.clean_value("") is None
        assert converter.tsv_reader.clean_value("   ") is None

        # Test string values
        assert converter.tsv_reader.clean_value("  test  ") == "test"
        assert converter.tsv_reader.clean_value("test") == "test"

    def test_convert_tsv_to_yaml(self, temp_project_dir, sample_tsv_file):
        """Test TSV to YAML conversion."""
        converter = TSVToYAMLConverter(temp_project_dir)

        output_file = temp_project_dir / "output.yaml"

        # Convert the file
        success = converter.convert_tsv_to_yaml(sample_tsv_file, output_file)

        assert success
        assert output_file.exists()

        # Check that the output file contains valid YAML
        import yaml

        with open(output_file, "r") as f:
            data = yaml.safe_load(f)

        assert "project" in data
        assert data["project"]["title"] == "Test Data"
        assert data["project"]["total_shots"] == 2
        assert len(data["project"]["phases"]) == 1

    def test_process_files(self, temp_project_dir, sample_tsv_file):
        """Test batch file processing."""
        converter = TSVToYAMLConverter(temp_project_dir)

        success = converter.process_files()

        assert success
        # Check that output files were created
        output_dir = converter.output_dir
        # Look in subdirectories for YAML files
        yaml_files = list(output_dir.rglob("*.yaml"))
        assert len(yaml_files) > 0

    def test_analyze_files(self, temp_project_dir, sample_tsv_file):
        """Test file analysis functionality."""
        converter = TSVToYAMLConverter(temp_project_dir)

        results = converter.analyze_files()

        assert "total_files" in results
        assert "valid_tsv_files" in results
        assert results["total_files"] >= 1
