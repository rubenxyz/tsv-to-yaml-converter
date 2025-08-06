"""Unit tests for TSV to YAML converter."""

import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest
import pandas as pd

from tsv_to_yaml_converter.converter import TSVToYAMLConverter
from tsv_to_yaml_converter.config import Config
from tsv_to_yaml_converter.models import Project, Shot


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_dir = Path(temp_dir) / "test_project"
        project_dir.mkdir()
        yield project_dir


@pytest.fixture
def sample_tsv_data():
    """Sample TSV data for testing."""
    return [
        {
            'PHASE_NUM': '1',
            'PHASE_START': '1800',
            'PHASE_END': '1900',
            'SCENE_NUM': '1',
            'LOC_TYPE': 'Interior',
            'DIURNAL': 'Day',
            'LOCATION': 'Living Room',
            'SHOT_NUM': '1',
            'IN': '00:00:00:00',
            'OUT': '00:00:05:00',
            'SPECIFIC AREA': 'Wide shot',
            'MOVE_SPEED': 'Slow',
            'MOVE_TYPE': 'Pan',
            'ANGLE': 'Medium',
            'SHOT_DESCRIPTION': 'Establishing shot'
        },
        {
            'PHASE_NUM': '1',
            'PHASE_START': '1800',
            'PHASE_END': '1900',
            'SCENE_NUM': '1',
            'LOC_TYPE': 'Interior',
            'DIURNAL': 'Day',
            'LOCATION': 'Living Room',
            'SHOT_NUM': '2',
            'IN': '00:00:05:00',
            'OUT': '00:00:08:00',
            'SPECIFIC AREA': 'Close-up',
            'MOVE_SPEED': 'Static',
            'MOVE_TYPE': 'Static',
            'ANGLE': 'Close',
            'SHOT_DESCRIPTION': 'Close-up of character'
        }
    ]


@pytest.fixture
def sample_tsv_file(temp_project_dir, sample_tsv_data):
    """Create a sample TSV file for testing."""
    input_dir = temp_project_dir / "USER-FILES" / "01.INPUT"
    input_dir.mkdir(parents=True)
    
    tsv_file = input_dir / "test_data.tsv"
    df = pd.DataFrame(sample_tsv_data)
    df.to_csv(tsv_file, sep='\t', index=False)
    
    return tsv_file


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
        assert converter.clean_value(None) is None
        assert converter.clean_value('') is None
        assert converter.clean_value('   ') is None
        
        # Test string values
        assert converter.clean_value('  test  ') == 'test'
        assert converter.clean_value('test') == 'test'
        
        # Test numeric values
        assert converter.clean_value(123) == 123
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
        with open(output_file, 'r') as f:
            data = yaml.safe_load(f)
        
        assert 'project' in data
        assert data['project']['title'] == 'Test Data'
        assert data['project']['total_shots'] == 2
        assert len(data['project']['epochs']) == 1
        assert len(data['project']['epochs'][0]['scenes']) == 1
        assert len(data['project']['epochs'][0]['scenes'][0]['shots']) == 2
    
    def test_analyze_files(self, temp_project_dir, sample_tsv_file):
        """Test file analysis functionality."""
        converter = TSVToYAMLConverter(temp_project_dir)
        
        # Analyze files
        results = converter.analyze_files()
        
        assert results['total_files'] == 1
        assert results['valid_tsv_files'] == 1
        assert len(results['files_found']) == 1
        assert results['files_found'][0] == 'test_data.tsv'
        assert len(results['invalid_files']) == 0
    
    def test_process_files(self, temp_project_dir, sample_tsv_file):
        """Test batch file processing."""
        converter = TSVToYAMLConverter(temp_project_dir)
        
        # Process files
        success = converter.process_files()
        
        assert success
        assert converter.stats['total_files'] == 1
        assert converter.stats['processed_files'] == 1
        assert converter.stats['failed_files'] == 0
        
        # Check that output was created
        output_dirs = list(converter.output_dir.iterdir())
        assert len(output_dirs) == 1
        
        # Check that input file remains in place (no moving)
        input_files = list(converter.input_dir.rglob('*.tsv'))
        assert len(input_files) == 1


class TestConfig:
    """Test cases for Config class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = Config()
        
        assert config.project_title is None
        assert config.yaml_indent == 2
        assert config.yaml_width == 120
    
    def test_config_from_dict(self):
        """Test configuration from dictionary."""
        config_data = {
            'project_title': 'Test Project',
            'yaml_indent': 4
        }
        
        config = Config(**config_data)
        
        assert config.project_title == 'Test Project'
        assert config.yaml_indent == 4
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test invalid yaml_indent
        with pytest.raises(ValueError):
            Config(yaml_indent=0)
        
        with pytest.raises(ValueError):
            Config(yaml_indent=10)
        
        # Test invalid yaml_width
        with pytest.raises(ValueError):
            Config(yaml_width=50)
        
        with pytest.raises(ValueError):
            Config(yaml_width=300)


class TestModels:
    """Test cases for data models."""
    
    def test_shot_creation(self):
        """Test Shot model creation."""
        shot = Shot(
            shot_number=1,
            shot_timecode={'in': '00:00:00:00', 'out': '00:00:05:00'},
            specific_area='Wide shot',
            camera_movement={'speed': 'Slow', 'type': 'Pan'},
            angle='Medium',
            description='Test shot'
        )
        
        assert shot.shot_number == 1
        assert shot.shot_timecode.in_time == '00:00:00:00'
        assert shot.shot_timecode.out_time == '00:00:05:00'
        assert shot.specific_area == 'Wide shot'
        assert shot.camera_movement.speed == 'Slow'
        assert shot.camera_movement.movement_type == 'Pan'
        assert shot.angle == 'Medium'
        assert shot.description == 'Test shot'
    
    def test_project_creation(self):
        """Test Project model creation."""
        project = Project(
            title='Test Project',
            total_shots=5,
            epochs=[]
        )
        
        assert project.title == 'Test Project'
        assert project.total_shots == 5
        assert len(project.epochs) == 0