"""Shared test fixtures."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest


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
            "PHASE_NUM": "1",
            "PHASE_START": "1800",
            "PHASE_END": "1900",
            "SCENE_NUM": "1",
            "LOC_TYPE": "Interior",
            "DIURNAL": "Day",
            "LOCATION": "Living Room",
            "SHOT_NUM": "1",
            "IN": "00:00:00:00",
            "OUT": "00:00:05:00",
            "SPECIFIC AREA": "Wide shot",
            "MOVE_SPEED": "Slow",
            "MOVE_TYPE": "Pan",
            "ANGLE": "Medium",
            "SHOT_DESCRIPTION": "Establishing shot",
        },
        {
            "PHASE_NUM": "1",
            "PHASE_START": "1800",
            "PHASE_END": "1900",
            "SCENE_NUM": "1",
            "LOC_TYPE": "Interior",
            "DIURNAL": "Day",
            "LOCATION": "Living Room",
            "SHOT_NUM": "2",
            "IN": "00:00:05:00",
            "OUT": "00:00:08:00",
            "SPECIFIC AREA": "Close-up",
            "MOVE_SPEED": "Static",
            "MOVE_TYPE": "Static",
            "ANGLE": "Close",
            "SHOT_DESCRIPTION": "Close-up of character",
        },
    ]


@pytest.fixture
def sample_tsv_file(temp_project_dir, sample_tsv_data):
    """Create a sample TSV file for testing."""
    input_dir = temp_project_dir / "USER-FILES" / "01.INPUT"
    input_dir.mkdir(parents=True)

    tsv_file = input_dir / "test_data.tsv"
    df = pd.DataFrame(sample_tsv_data)
    df.to_csv(tsv_file, sep="\t", index=False)

    return tsv_file
