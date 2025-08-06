"""Data processing functionality for TSV to YAML converter."""

from typing import Any, Dict

from .models import (
    CameraMovement,
    Location,
    Phase,
    Project,
    Scene,
    Shot,
    ShotTimecode,
    TimePeriod,
)
from .tsv_reader import TSVReader


class DataProcessor:
    """Handles the transformation of TSV data into hierarchical structures and Pydantic models."""

    def __init__(self, tsv_reader: TSVReader):
        """Initialize the data processor with a TSV reader."""
        self.tsv_reader = tsv_reader

    def _format_value(self, value: str, field_name: str) -> str:
        """Format values based on field type."""
        if not value:
            return value

        # Apply sentence case and remove underscores for specific fields
        if field_name in [
            "location_name",
            "specific_area",
            "period",
            "season",
            "weather",
            "speed",
            "type",
        ]:
            # Remove underscores and apply sentence case
            formatted = value.replace("_", " ").lower()
            return formatted.capitalize()

        return value

    def process_tsv_data(self, df) -> Dict[int, Dict]:
        """Process TSV data into hierarchical dictionary structure."""
        phases_dict = {}
        current_phase = None
        current_scene = None

        for _, row in df.iterrows():
            row_data = self.tsv_reader.clean_row_data(row, df.columns)

            if not self.tsv_reader.is_valid_row(row_data):
                continue

            # Carry forward phase and scene numbers from previous rows
            if row_data.get("PHASE_NUM"):
                current_phase = int(row_data["PHASE_NUM"])
            if row_data.get("SCENE_NUM"):
                try:
                    current_scene = int(float(row_data["SCENE_NUM"]))
                except (ValueError, TypeError):
                    # Skip rows with invalid scene numbers
                    continue

            if current_phase is None or current_scene is None:
                continue

            shot_num = int(str(row_data["SHOT_NUM"]).replace("\ufeff", ""))
            self._process_row_data(
                phases_dict, row_data, current_phase, current_scene, shot_num
            )

        return phases_dict

    def _process_row_data(
        self,
        phases_dict: Dict,
        row_data: Dict[str, Any],
        phase_num: int,
        scene_num: int,
        shot_num: int,
    ) -> None:
        """Process a single row of data into the hierarchical structure."""
        self._ensure_phase_exists(phases_dict, phase_num, row_data)
        self._ensure_scene_exists(phases_dict, phase_num, scene_num, row_data)
        self._add_shot_to_scene(phases_dict, phase_num, scene_num, shot_num, row_data)

    def _ensure_phase_exists(
        self, phases_dict: Dict, phase_num: int, row_data: Dict[str, Any]
    ) -> None:
        """Create phase if it doesn't exist."""
        if phase_num not in phases_dict:
            phases_dict[phase_num] = {
                "phase_number": phase_num,
                "time_period": {
                    "start": (
                        int(row_data["PHASE_START"])
                        if row_data.get("PHASE_START")
                        else None
                    ),
                    "end": (
                        int(row_data["PHASE_END"])
                        if row_data.get("PHASE_END")
                        else None
                    ),
                },
                "scenes": {},
            }

    def _ensure_scene_exists(
        self,
        phases_dict: Dict,
        phase_num: int,
        scene_num: int,
        row_data: Dict[str, Any],
    ) -> None:
        """Create scene if it doesn't exist."""
        if scene_num not in phases_dict[phase_num]["scenes"]:
            phases_dict[phase_num]["scenes"][scene_num] = {
                "scene_number": scene_num,
                "comment": row_data.get("SCENE_CONTEXT_COMMENT"),
                "period": self._format_value(row_data.get("PERIOD"), "period"),
                "season": self._format_value(row_data.get("SEASON"), "season"),
                "weather": self._format_value(row_data.get("WEATHER"), "weather"),
                "location": {
                    "type": row_data.get("LOC_TYPE"),
                    "location_name": self._format_value(
                        row_data.get("LOCATION"), "location_name"
                    ),
                },
                "diurnal": row_data.get("DIURNAL"),
                "light_source": row_data.get("LIGHT_SOURCE(S)"),
                "shots": [],
            }

    def _add_shot_to_scene(
        self,
        phases_dict: Dict,
        phase_num: int,
        scene_num: int,
        shot_num: int,
        row_data: Dict[str, Any],
    ) -> None:
        """Create and add shot to the appropriate scene."""
        shot = self._create_shot_data(shot_num, row_data)
        phases_dict[phase_num]["scenes"][scene_num]["shots"].append(shot)

    def _create_shot_data(
        self, shot_num: int, row_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create shot data dictionary from row data."""
        shot_data = {
            "shot_number": shot_num,
            "camera_angle": row_data.get("ANGLE"),
            "specific_area": self._format_value(
                row_data.get("SPECIFIC AREA"), "specific_area"
            ),
            "description": row_data.get("SHOT_DESCRIPTION"),
            "camera_movement": {
                "speed": self._format_value(row_data.get("MOVE_SPEED"), "speed"),
                "type": self._format_value(row_data.get("MOVE_TYPE"), "type"),
                "video_prompt": row_data.get("VIDEO_PROMPT"),
            },
            "shot_timecode": {
                "in_time": row_data.get("IN"),
                "out_time": row_data.get("OUT"),
            },
            "image_prompt": row_data.get("IMAGE_PROMPT"),
        }

        # Only include oref if the value is "TRUE"
        oref_value = row_data.get("OREF")
        if oref_value == "TRUE":
            shot_data["oref"] = oref_value

        return shot_data

    def build_project_structure(
        self,
        project: Project,
        phases_dict: Dict[int, Dict],
        no_camera_movement: bool = False,
        no_shot_timecode: bool = False,
    ) -> Project:
        """Convert dictionary structure to Pydantic models."""
        for phase_num in sorted(phases_dict.keys()):
            phase_data = phases_dict[phase_num]
            phase = self._create_phase_model(
                phase_data, no_camera_movement, no_shot_timecode
            )
            project.phases.append(phase)

        return project

    def _create_phase_model(
        self,
        phase_data: Dict,
        no_camera_movement: bool = False,
        no_shot_timecode: bool = False,
    ) -> Phase:
        """Create Phase model from dictionary data."""
        phase = Phase(
            phase_number=phase_data["phase_number"],
            time_period=TimePeriod(**phase_data["time_period"]),
            scenes=[],
        )

        # Convert scenes dictionary to list
        for scene_num in sorted(phase_data["scenes"].keys()):
            scene_data = phase_data["scenes"][scene_num]
            scene = self._create_scene_model(
                scene_data, no_camera_movement, no_shot_timecode
            )
            phase.scenes.append(scene)

        return phase

    def _create_scene_model(
        self,
        scene_data: Dict,
        no_camera_movement: bool = False,
        no_shot_timecode: bool = False,
    ) -> Scene:
        """Create Scene model from dictionary data."""
        scene = Scene(
            scene_number=scene_data["scene_number"],
            comment=scene_data["comment"],
            period=scene_data["period"],
            season=scene_data["season"],
            weather=scene_data["weather"],
            location=Location(**scene_data["location"]),
            diurnal=scene_data["diurnal"],
            light_source=scene_data["light_source"],
            shots=[],
        )

        # Convert shots to Shot objects
        for shot_data in scene_data["shots"]:
            shot = self._create_shot_model(
                shot_data, no_camera_movement, no_shot_timecode
            )
            scene.shots.append(shot)

        return scene

    def _create_shot_model(
        self,
        shot_data: Dict,
        no_camera_movement: bool = False,
        no_shot_timecode: bool = False,
    ) -> Shot:
        """Create Shot model from dictionary data."""
        shot_kwargs = {
            "shot_number": shot_data["shot_number"],
            "camera_angle": shot_data["camera_angle"],
            "specific_area": shot_data["specific_area"],
            "description": shot_data["description"],
            "image_prompt": shot_data["image_prompt"],
        }

        # Only include oref if it exists in the shot data (i.e., was "TRUE")
        if "oref" in shot_data:
            shot_kwargs["oref"] = shot_data["oref"]

        # Add camera_movement only if not excluded
        if not no_camera_movement:
            shot_kwargs["camera_movement"] = CameraMovement(
                **shot_data["camera_movement"]
            )

        # Add shot_timecode only if not excluded
        if not no_shot_timecode:
            shot_kwargs["shot_timecode"] = ShotTimecode(**shot_data["shot_timecode"])

        return Shot(**shot_kwargs)

    def get_project_title(self, tsv_file, project_title: str = "") -> str:
        """Infer project title from filename if not provided."""
        if not project_title:
            project_title = tsv_file.stem.replace("_", " ").replace("-", " ").title()
        return project_title

    def initialize_project(self, project_title: str, total_shots: int) -> Project:
        """Initialize the project structure."""
        return Project(title=project_title, total_shots=total_shots, phases=[])
