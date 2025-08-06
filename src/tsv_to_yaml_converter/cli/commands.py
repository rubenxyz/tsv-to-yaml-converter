"""Core CLI command implementations."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..converter import TSVToYAMLConverter
from ..config import Config
from .ui import CLIUI
from .error_handler import CLIErrorHandler
from .mappings import CLIMappings


class CLICommands:
    """Handles core CLI command implementations."""

    def __init__(self, project_root: Path, verbose: bool):
        """Initialize CLI commands with context."""
        self.project_root = project_root
        self.verbose = verbose
        self.ui = CLIUI()
        self.error_handler = CLIErrorHandler(self.ui)
        self.mappings = CLIMappings()
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Setup logging based on verbose flag."""
        level = "DEBUG" if self.verbose else "INFO"
        logger.add(sys.stdout, level=level, colorize=True)

    def _create_converter(self) -> TSVToYAMLConverter:
        """Create and return a converter instance."""
        try:
            return TSVToYAMLConverter(self.project_root)
        except Exception as e:
            self.error_handler.handle_converter_error(e)

    def process_files(
        self,
        config: Optional[Path],
        no_camera_movement: bool = False,
        no_shot_timecode: bool = False,
    ) -> None:
        """Process all TSV files in the input directory."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.ui.console,
            transient=True,
        ) as progress:
            task = progress.add_task("Initializing converter...", total=None)

            try:
                # Initialize converter
                converter = self._create_converter()
                progress.update(task, description="Processing TSV files...")

                # Process files
                success = converter.process_files(
                    config, no_camera_movement, no_shot_timecode
                )

                if success:
                    self.ui.display_processing_success(converter.output_dir)
                else:
                    self.ui.display_processing_error(converter.output_dir)
                    sys.exit(1)

            except Exception as e:
                self.error_handler.handle_processing_error(e)

    def analyze_files(self) -> None:
        """Analyze files without processing them."""
        try:
            converter = self._create_converter()
            results = converter.analyze_files()

            self.ui.display_analysis_results(results, self.verbose)

        except Exception as e:
            self.error_handler.handle_analysis_error(e)

    def init_config(self, output: Path) -> None:
        """Initialize a new configuration file."""
        try:
            config = Config()
            config.save_to_file(output)

            self.ui.display_config_created(output)

        except Exception as e:
            self.error_handler.handle_config_error(e)

    def init_mappings(self, mappings_file: Path) -> None:
        """Initialize a new mappings configuration file."""
        try:
            default_mappings = self.mappings.get_default_mappings()
            config = Config()
            config.save_mappings(default_mappings, mappings_file)

            self.ui.display_mappings_created(mappings_file)

        except Exception as e:
            self.error_handler.handle_mappings_error(e)

    def status(self) -> None:
        """Show current project status."""
        try:
            converter = self._create_converter()
            self._display_project_status(converter)

        except Exception as e:
            self.error_handler.handle_general_error(e)

    def _display_project_status(self, converter: TSVToYAMLConverter) -> None:
        """Display current project status."""
        input_files = len(list(converter.input_dir.glob("*.tsv")))

        self.ui.display_project_status(
            input_files=input_files,
            output_dir=converter.output_dir,
            verbose=self.verbose,
        )
