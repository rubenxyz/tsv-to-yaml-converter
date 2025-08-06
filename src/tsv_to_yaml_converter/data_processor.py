"""Data processing functionality for converting TSV data to hierarchical structure."""

from typing import Dict, Any
from loguru import logger

from .models import Project, Epoch, Scene, Shot, ShotTimecode, CameraMovement, TimePeriod
from .tsv_reader import TSVReader


class DataProcessor:
    """Processes TSV data into hierarchical structure."""

    def __init__(self, tsv_reader: TSVReader):
        """Initialize the data processor with a TSV reader."""
        self.tsv_reader = tsv_reader

    def process_tsv_data(self, df) -> Dict[int, Dict]:
        """Process TSV data into hierarchical dictionary structure."""
        epochs_dict = {}
        current_epoch = None
        current_scene = None

        for _, row in df.iterrows():
            row_data = self.tsv_reader.clean_row_data(row, df.columns)

            if not self.tsv_reader.is_valid_row(row_data):
                continue

            # Carry forward phase and scene numbers from previous rows
            if row_data.get('PHASE_NUM'):
                current_epoch = int(row_data['PHASE_NUM'])
            if row_data.get('SCENE_NUM'):
                try:
                    current_scene = int(float(row_data['SCENE_NUM']))
                except (ValueError, TypeError):
                    # Skip rows with invalid scene numbers
                    continue

            if current_epoch is None or current_scene is None:
                continue

            shot_num = int(row_data['SHOT_NUM'])
            self._process_row_data(epochs_dict, row_data, current_epoch, current_scene, shot_num)

        return epochs_dict

    def _process_row_data(self, epochs_dict: Dict, row_data: Dict[str, Any],
                         epoch_num: int, scene_num: int, shot_num: int) -> None:
        """Process a single row of data into the hierarchical structure."""
        self._ensure_epoch_exists(epochs_dict, epoch_num, row_data)
        self._ensure_scene_exists(epochs_dict, epoch_num, scene_num, row_data)
        self._add_shot_to_scene(epochs_dict, epoch_num, scene_num, shot_num, row_data)

    def _ensure_epoch_exists(self, epochs_dict: Dict, epoch_num: int, row_data: Dict[str, Any]) -> None:
        """Create epoch if it doesn't exist."""
        if epoch_num not in epochs_dict:
            epochs_dict[epoch_num] = {
                'epoch_number': epoch_num,
                'time_period': {
                    'start': int(row_data['PHASE_START']) if row_data.get('PHASE_START') else None,
                    'end': int(row_data['PHASE_END']) if row_data.get('PHASE_END') else None
                },
                'scenes': {}
            }

    def _ensure_scene_exists(self, epochs_dict: Dict, epoch_num: int, scene_num: int,
                           row_data: Dict[str, Any]) -> None:
        """Create scene if it doesn't exist."""
        if scene_num not in epochs_dict[epoch_num]['scenes']:
            epochs_dict[epoch_num]['scenes'][scene_num] = {
                'scene_number': scene_num,
                'location_type': row_data.get('LOC_TYPE'),
                'time': row_data.get('DIURNAL'),
                'location': row_data.get('LOCATION'),
                'shots': []
            }

    def _add_shot_to_scene(self, epochs_dict: Dict, epoch_num: int, scene_num: int,
                          shot_num: int, row_data: Dict[str, Any]) -> None:
        """Create and add shot to the appropriate scene."""
        shot = self._create_shot_data(shot_num, row_data)
        epochs_dict[epoch_num]['scenes'][scene_num]['shots'].append(shot)

    def _create_shot_data(self, shot_num: int, row_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create shot data dictionary from row data."""
        return {
            'shot_number': shot_num,
            'shot_timecode': {
                'in_time': row_data.get('IN'),
                'out_time': row_data.get('OUT')
            },
            'specific_area': row_data.get('SPECIFIC AREA'),
            'camera_movement': {
                'speed': row_data.get('MOVE_SPEED'),
                'type': row_data.get('MOVE_TYPE')
            },
            'angle': row_data.get('ANGLE'),
            'description': row_data.get('SHOT_DESCRIPTION')
        }

    def build_project_structure(self, project: Project, epochs_dict: Dict[int, Dict]) -> Project:
        """Convert dictionary structure to Pydantic models."""
        for epoch_num in sorted(epochs_dict.keys()):
            epoch_data = epochs_dict[epoch_num]
            epoch = self._create_epoch_model(epoch_data)
            project.epochs.append(epoch)
            logger.debug(f"Added Epoch {epoch.epoch_number} with {len(epoch.scenes)} scenes")

        return project

    def _create_epoch_model(self, epoch_data: Dict) -> Epoch:
        """Create Epoch model from dictionary data."""
        epoch = Epoch(
            epoch_number=epoch_data['epoch_number'],
            time_period=TimePeriod(**epoch_data['time_period']),
            scenes=[]
        )

        # Convert scenes dictionary to list
        for scene_num in sorted(epoch_data['scenes'].keys()):
            scene_data = epoch_data['scenes'][scene_num]
            scene = self._create_scene_model(scene_data)
            epoch.scenes.append(scene)

        return epoch

    def _create_scene_model(self, scene_data: Dict) -> Scene:
        """Create Scene model from dictionary data."""
        scene = Scene(
            scene_number=scene_data['scene_number'],
            location_type=scene_data['location_type'],
            time=scene_data['time'],
            location=scene_data['location'],
            shots=[]
        )

        # Convert shots to Shot objects
        for shot_data in scene_data['shots']:
            shot = self._create_shot_model(shot_data)
            scene.shots.append(shot)

        return scene

    def _create_shot_model(self, shot_data: Dict) -> Shot:
        """Create Shot model from dictionary data."""
        return Shot(
            shot_number=shot_data['shot_number'],
            shot_timecode=ShotTimecode(**shot_data['shot_timecode']),
            specific_area=shot_data['specific_area'],
            camera_movement=CameraMovement(**shot_data['camera_movement']),
            angle=shot_data['angle'],
            description=shot_data['description']
        )

    def get_project_title(self, tsv_file, project_title: str = None) -> str:
        """Infer project title from filename if not provided."""
        if not project_title:
            project_title = tsv_file.stem.replace('_', ' ').replace('-', ' ').title()
        return project_title

    def initialize_project(self, project_title: str, total_shots: int) -> Project:
        """Initialize the project structure."""
        return Project(
            title=project_title,
            total_shots=total_shots,
            epochs=[]
        )
