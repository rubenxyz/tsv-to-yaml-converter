"""CLI error handling utilities."""

import sys

from rich.console import Console

from .ui import CLIUI

console = Console()


class CLIErrorHandler:
    """Handles CLI error handling and user feedback."""

    def __init__(self, ui: CLIUI):
        """Initialize the error handler with UI component."""
        self.ui = ui

    def handle_error(
        self,
        error: Exception,
        message: str = "Error",
        exit_on_error: bool = True,
    ) -> None:
        """Handle errors consistently across commands."""
        error_message = f"{message}: {error}"
        self.ui.print_error(error_message)

        if exit_on_error:
            sys.exit(1)

    def handle_converter_error(self, error: Exception) -> None:
        """Handle converter initialization errors."""
        self.handle_error(error, "Failed to initialize converter")

    def handle_analysis_error(self, error: Exception) -> None:
        """Handle analysis errors."""
        self.handle_error(error, "Error during analysis", exit_on_error=False)

    def handle_config_error(self, error: Exception) -> None:
        """Handle configuration creation errors."""
        self.handle_error(error, "Error creating configuration")

    def handle_mappings_error(self, error: Exception) -> None:
        """Handle mappings creation errors."""
        self.handle_error(error, "Error creating mappings")

    def handle_processing_error(self, error: Exception) -> None:
        """Handle processing errors."""
        self.handle_error(error, "Error during processing")

    def handle_general_error(self, error: Exception) -> None:
        """Handle general errors."""
        self.handle_error(error, "Unexpected error occurred")

    def validate_project_root(self, project_root) -> bool:
        """Validate project root directory."""
        if not project_root.exists():
            self.ui.print_error(f"Project root does not exist: {project_root}")
            return False

        if not project_root.is_dir():
            self.ui.print_error(f"Project root is not a directory: {project_root}")
            return False

        return True

    def validate_input_directory(self, input_dir) -> bool:
        """Validate input directory."""
        if not input_dir.exists():
            self.ui.print_warning(f"Input directory does not exist: {input_dir}")
            return False

        if not input_dir.is_dir():
            self.ui.print_error(f"Input path is not a directory: {input_dir}")
            return False

        return True

    def validate_output_directory(self, output_dir) -> bool:
        """Validate output directory."""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.ui.print_error(f"Cannot create output directory: {e}")
            return False
