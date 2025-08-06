"""Core TSV to YAML conversion logic."""

from pathlib import Path
from typing import Optional

from loguru import logger

from .config import Config
from .data_processor import DataProcessor
from .error_handler import ErrorHandler
from .file_manager import FileManager
from .tsv_reader import TSVReader
from .yaml_writer import YAMLWriter


class TSVToYAMLConverter:
    """Batch processor for converting TSV shot lists to YAML format."""

    def __init__(self, project_root: Path, config: Optional[Config] = None):
        """Initialize the converter with project structure."""
        self.config = config or Config()
        self.project_root = Path(project_root)

        # Initialize components
        self.file_manager = FileManager(project_root)
        self.error_handler = ErrorHandler()

        # Load field mappings
        field_mappings = self.config.load_mappings()
        self.tsv_reader = TSVReader(field_mappings)
        self.data_processor = DataProcessor(self.tsv_reader)
        self.yaml_writer = YAMLWriter(
            yaml_indent=self.config.yaml_indent, yaml_width=self.config.yaml_width
        )

    @property
    def input_dir(self) -> Path:
        """Get input directory."""
        return self.file_manager.input_dir

    @property
    def output_dir(self) -> Path:
        """Get output directory."""
        return self.file_manager.output_dir

    @property
    def stats(self):
        """Get processing statistics."""
        return self.error_handler.stats

    def convert_tsv_to_yaml(
        self,
        tsv_file: Path,
        output_file: Path,
        project_title: Optional[str] = None,
        no_camera_movement: bool = False,
        no_shot_timecode: bool = False,
    ) -> bool:
        """
        Convert TSV shot list to hierarchical YAML format.

        Args:
            tsv_file: Path to input TSV file
            output_file: Path to output YAML file
            project_title: Optional project title (inferred from filename if not provided)
            no_camera_movement: Exclude camera_movement section from output
            no_shot_timecode: Exclude shot_timecode section from output

        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Read and process TSV data
            df = self.tsv_reader.read_tsv_file(tsv_file)
            project_title = self.data_processor.get_project_title(
                tsv_file, project_title
            )

            # Initialize project structure
            project = self.data_processor.initialize_project(project_title, len(df))

            # Process data into hierarchical structure
            phases_dict = self.data_processor.process_tsv_data(df)

            # Convert to Pydantic models
            project = self.data_processor.build_project_structure(
                project, phases_dict, no_camera_movement, no_shot_timecode
            )

            # Generate statistics and write output
            self.yaml_writer.finalize_and_write(project, output_file)

            return True

        except Exception as e:
            self.error_handler.log_error(tsv_file, e)
            return False

    def analyze_files(self) -> dict:
        """Analyze all TSV files in the input directory without processing them."""
        analysis_results = self.file_manager.analyze_files()

        # Enhance analysis with TSV validation
        for file_info in analysis_results["file_details"]:
            if file_info["is_valid_tsv"]:
                file_path = self.input_dir / file_info["path"]
                validation_result = self.tsv_reader.validate_tsv_file(file_path)

                if validation_result["is_valid"]:
                    file_info["rows"] = validation_result["rows"]
                    file_info["columns"] = validation_result["columns"]
                else:
                    file_info["is_valid_tsv"] = False
                    file_info["error"] = validation_result["error"]
                    analysis_results["valid_tsv_files"] -= 1
                    analysis_results["invalid_files"].append(
                        {"file": file_path.name, "error": validation_result["error"]}
                    )

        return analysis_results

    def process_files(
        self,
        config_file: Optional[Path] = None,
        no_camera_movement: bool = False,
        no_shot_timecode: bool = False,
    ) -> bool:
        """Process all TSV files in the input directory."""
        self.error_handler.start_processing()

        # Load configuration if provided
        if config_file and config_file.exists():
            try:
                self.config = Config.from_file(config_file)
                logger.debug(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.warning(f"Failed to load configuration: {e}")

        # Get timestamped output directory
        output_dir = self.file_manager.get_timestamped_output_dir()
        logger.debug(f"Output directory: {output_dir}")

        # Find all TSV files in input directory
        tsv_files = self.file_manager.find_tsv_files()
        self.error_handler.stats["total_files"] = len(tsv_files)

        if not tsv_files:
            logger.warning("No TSV files found in input directory")
            return True

        logger.info(f"Found {len(tsv_files)} TSV files to process")

        # Process each file
        for tsv_file in tsv_files:
            logger.debug(f"Processing {tsv_file.name}...")

            # Determine output path
            output_path = self.file_manager.get_output_path(tsv_file, output_dir)

            # Get project title from config or infer from filename
            project_title = self.config.project_title

            # Convert the file
            success = self.convert_tsv_to_yaml(
                tsv_file,
                output_path,
                project_title,
                no_camera_movement,
                no_shot_timecode,
            )

            if success:
                self.error_handler.log_success(tsv_file)

        self.error_handler.end_processing()
        self.error_handler.log_summary()

        return not self.error_handler.has_errors()
