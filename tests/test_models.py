"""Unit tests for Pydantic data models."""

from tsv_to_yaml_converter.models import Project, Shot


class TestModels:
    """Test cases for Pydantic models."""

    def test_shot_creation(self):
        """Test Shot model creation."""
        shot = Shot(
            shot_number=1,
            shot_timecode={"in_time": "00:00:00:00", "out_time": "00:00:05:00"},
            specific_area="Wide shot",
            camera_movement={"speed": "Slow", "type": "Pan"},
            camera_angle="Medium",
            description="Test shot",
        )

        assert shot.shot_number == 1
        assert shot.shot_timecode.in_time == "00:00:00:00"
        assert shot.shot_timecode.out_time == "00:00:05:00"
        assert shot.specific_area == "Wide shot"
        assert shot.camera_movement.speed == "Slow"
        assert shot.camera_movement.type == "Pan"

    def test_project_creation(self):
        """Test Project model creation."""
        project = Project(title="Test Project", total_shots=5, phases=[])

        assert project.title == "Test Project"
        assert project.total_shots == 5
        assert len(project.phases) == 0
