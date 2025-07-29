"""Core TSV to YAML conversion logic."""

import pandas as pd
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import Config
from .models import Project, Epoch, Scene, Shot, ShotTimecode, CameraMovement, TimePeriod
from loguru import logger




class TSVToYAMLConverter:
    """Batch processor for converting TSV shot lists to YAML format."""
    
    def __init__(self, project_root: Path, config: Optional[Config] = None):
        """Initialize the converter with project structure."""
        self.project_root = Path(project_root)
        self.config = config or Config()
        self.user_files = self.project_root / "USER-FILES"
        self.input_dir = self.user_files / "01.INPUT"
        self.output_dir = self.user_files / "02.OUTPUT"
        
        # Create directories if they don't exist
        for directory in [self.user_files, self.input_dir, self.output_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Load field mappings
        self.field_mappings = self.config.load_mappings()
        
        # Processing statistics
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'errors': [],
            'start_time': None,
            'end_time': None
        }
    
    def get_timestamped_output_dir(self) -> Path:
        """Create and return timestamped output directory."""
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
        output_dir = self.output_dir / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir
    
    def clean_value(self, value: Any, field_name: Optional[str] = None) -> Any:
        """Clean and normalize values, handling NaN/null values and BOM characters."""
        if pd.isna(value) or value == '' or str(value).strip() == '':
            return None
        if isinstance(value, str):
            # Remove BOM characters and strip whitespace
            cleaned = value.strip().replace('\ufeff', '')
            if not cleaned:
                return None
            
            # Apply field mappings if available
            if field_name and hasattr(self, 'field_mappings'):
                mapped_value = self._apply_field_mapping(field_name, cleaned)
                if mapped_value:
                    return mapped_value
            
            return cleaned
        return value
    
    def _apply_field_mapping(self, field_name: str, value: str) -> Optional[str]:
        """Apply field mapping if available."""
        if not hasattr(self, 'field_mappings') or not self.field_mappings:
            return None
        
        field_mappings = self.field_mappings.get(field_name, {})
        return field_mappings.get(value, None)
    def convert_tsv_to_yaml(self, tsv_file: Path, output_file: Path, project_title: Optional[str] = None) -> bool:
        """
        Convert TSV shot list to hierarchical YAML format.
        
        Args:
            tsv_file: Path to input TSV file
            output_file: Path to output YAML file
            project_title: Optional project title (inferred from filename if not provided)
        
        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Read and process TSV data
            df = self._read_tsv_file(tsv_file)
            project_title = self._get_project_title(tsv_file, project_title)
            
            # Initialize project structure
            project = self._initialize_project(project_title, len(df))
            
            # Process data into hierarchical structure
            epochs_dict = self._process_tsv_data(df)
            
            # Convert to Pydantic models
            project = self._build_project_structure(project, epochs_dict)
            
            # Generate statistics and write output
            self._finalize_and_write(project, output_file)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing {tsv_file.name}: {str(e)}")
            self.stats['errors'].append({
                'file': str(tsv_file),
                'error': str(e),
                'type': type(e).__name__
            })
            return False

    def _read_tsv_file(self, tsv_file: Path) -> pd.DataFrame:
        """Read TSV file and handle BOM characters."""
        df = pd.read_csv(tsv_file, sep='\t', dtype=str, encoding='utf-8-sig')
        logger.info(f"Successfully read {len(df)} rows from {tsv_file.name}")
        return df

    def _get_project_title(self, tsv_file: Path, project_title: Optional[str]) -> str:
        """Infer project title from filename if not provided."""
        if not project_title:
            project_title = tsv_file.stem.replace('_', ' ').replace('-', ' ').title()
        return project_title

    def _initialize_project(self, project_title: str, total_shots: int) -> Project:
        """Initialize the project structure."""
        return Project(
            title=project_title,
            total_shots=total_shots,
            epochs=[]
        )

    def _process_tsv_data(self, df: pd.DataFrame) -> Dict[int, Dict]:
        """Process TSV data into hierarchical dictionary structure."""
        epochs_dict = {}
        current_epoch = None
        current_scene = None
        
        for _, row in df.iterrows():
            row_data = self._clean_row_data(row, df.columns)
            
            if not self._is_valid_row(row_data):
                continue
            
            # Carry forward epoch and scene numbers from previous rows
            if row_data.get('EPOCH_NUM'):
                current_epoch = int(row_data['EPOCH_NUM'])
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

    def _clean_row_data(self, row: pd.Series, columns: List[str]) -> Dict[str, Any]:
        """Clean all values in a row."""
        return {col: self.clean_value(row[col], col) for col in columns}

    def _is_valid_row(self, row_data: Dict[str, Any]) -> bool:
        """Check if row has essential data for processing."""
        return bool(row_data.get('SHOT_NUM'))



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
                    'start': int(row_data['EPOCH_START']) if row_data.get('EPOCH_START') else None,
                    'end': int(row_data['EPOCH_END']) if row_data.get('EPOCH_END') else None
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
                'time': row_data.get('TIME'),
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

    def _build_project_structure(self, project: Project, epochs_dict: Dict[int, Dict]) -> Project:
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

    def _finalize_and_write(self, project: Project, output_file: Path) -> None:
        """Write YAML output."""
        # Write YAML file
        self._write_yaml_file(project, output_file)
        
        # Log success
        total_epochs = len(project.epochs)
        total_scenes = sum(len(epoch.scenes) for epoch in project.epochs)
        total_shots = sum(len(scene.shots) for epoch in project.epochs for scene in epoch.scenes)
        
        logger.info(f"Successfully wrote YAML to {output_file.name}")
        logger.info(f"  → {total_epochs} epochs, {total_scenes} scenes, {total_shots} shots")

    def _write_yaml_file(self, project: Project, output_file: Path) -> None:
        """Write project data to YAML file with custom formatting."""
        # First, get the YAML as a string
        yaml_content = yaml.dump(
            {'project': project.model_dump(exclude_none=True)},
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            indent=self.config.yaml_indent,
            width=self.config.yaml_width
        )
        
        # Add empty lines before epochs and shots
        lines = yaml_content.split('\n')
        formatted_lines = []
        
        for _, line in enumerate(lines):
            # Add empty line before epoch_number
            if '- epoch_number:' in line:
                formatted_lines.append('')
            
            # Add empty line before scene_number
            elif '- scene_number:' in line:
                formatted_lines.append('')
            
            # Add empty line before shot_number
            elif '- shot_number:' in line:
                formatted_lines.append('')
            
            formatted_lines.append(line)
        
        # Write the formatted content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(formatted_lines))
    
    def analyze_files(self) -> Dict[str, Any]:
        """Analyze all TSV files in the input directory without processing them."""
        logger.info("Starting analysis mode...")
        
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'input_directory': str(self.input_dir),
            'files_found': [],
            'total_files': 0,
            'valid_tsv_files': 0,
            'invalid_files': [],
            'file_details': []
        }
        
        # Find all files in input directory
        for file_path in self.input_dir.rglob('*'):
            if file_path.is_file():
                analysis_results['total_files'] += 1
                file_info = {
                    'path': str(file_path.relative_to(self.input_dir)),
                    'size_bytes': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'extension': file_path.suffix.lower()
                }
                
                # Check if it's a TSV file
                if file_path.suffix.lower() == '.tsv':
                    try:
                        # Try to read the TSV file to validate it
                        df = pd.read_csv(file_path, sep='\t', dtype=str)
                        file_info['is_valid_tsv'] = True
                        file_info['rows'] = len(df)
                        file_info['columns'] = list(df.columns)
                        analysis_results['valid_tsv_files'] += 1
                        analysis_results['files_found'].append(file_path.name)
                    except Exception as e:
                        file_info['is_valid_tsv'] = False
                        file_info['error'] = str(e)
                        analysis_results['invalid_files'].append({
                            'file': file_path.name,
                            'error': str(e)
                        })
                else:
                    file_info['is_valid_tsv'] = False
                    file_info['error'] = 'Not a TSV file'
                    analysis_results['invalid_files'].append({
                        'file': file_path.name,
                        'error': 'Not a TSV file'
                    })
                
                analysis_results['file_details'].append(file_info)
        
        logger.info(f"Analysis complete: {analysis_results['total_files']} total files, {analysis_results['valid_tsv_files']} valid TSV files")
        
        return analysis_results
    
    def process_files(self, config_file: Optional[Path] = None) -> bool:
        """Process all TSV files in the input directory."""
        logger.info("Starting batch processing...")
        self.stats['start_time'] = datetime.now()
        
        # Load configuration if provided
        if config_file and config_file.exists():
            try:
                self.config = Config.from_file(config_file)
                logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.warning(f"Failed to load configuration: {e}")
        
        # Get timestamped output directory
        output_dir = self.get_timestamped_output_dir()
        logger.info(f"Output directory: {output_dir}")
        
        # Find all TSV files in input directory
        tsv_files = list(self.input_dir.rglob('*.tsv'))
        self.stats['total_files'] = len(tsv_files)
        
        if not tsv_files:
            logger.warning("No TSV files found in input directory")
            return True
        
        logger.info(f"Found {len(tsv_files)} TSV files to process")
        
        # Process each file
        for tsv_file in tsv_files:
            logger.info(f"Processing {tsv_file.name}...")
            
            # Determine output path (preserve directory structure)
            relative_path = tsv_file.relative_to(self.input_dir)
            output_path = output_dir / relative_path.with_suffix('.yaml')
            
            # Create output subdirectory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get project title from config or infer from filename
            project_title = self.config.project_title
            
            # Convert the file
            success = self.convert_tsv_to_yaml(tsv_file, output_path, project_title)
            
            if success:
                self.stats['processed_files'] += 1
                logger.info(f"Successfully processed {tsv_file.name}")
            else:
                self.stats['failed_files'] += 1
        
        self.stats['end_time'] = datetime.now()
        
        # Log summary
        logger.info("Batch processing complete!")
        logger.info(f"  → Total files: {self.stats['total_files']}")
        logger.info(f"  → Processed: {self.stats['processed_files']}")
        logger.info(f"  → Failed: {self.stats['failed_files']}")
        
        return self.stats['failed_files'] == 0