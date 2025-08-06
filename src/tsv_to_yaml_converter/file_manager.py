"""File management functionality for handling directories and file operations."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from loguru import logger


class FileManager:
    """Manages file operations and directory structure."""

    def __init__(self, project_root: Path):
        """Initialize the file manager with project root."""
        self.project_root = Path(project_root)
        self.user_files = self.project_root / "USER-FILES"
        self.input_dir = self.user_files / "01.INPUT"
        self.output_dir = self.user_files / "02.OUTPUT"

        # Create directories if they don't exist
        self._ensure_directories_exist()

    def _ensure_directories_exist(self) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [self.user_files, self.input_dir, self.output_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def get_timestamped_output_dir(self) -> Path:
        """Create and return timestamped output directory."""
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
        output_dir = self.output_dir / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    def find_tsv_files(self) -> List[Path]:
        """Find all TSV files in the input directory."""
        return list(self.input_dir.rglob("*.tsv"))

    def get_output_path(self, tsv_file: Path, output_dir: Path) -> Path:
        """Determine output path for a TSV file."""
        relative_path = tsv_file.relative_to(self.input_dir)
        output_path = output_dir / relative_path.with_suffix(".yaml")

        # Create output subdirectory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        return output_path

    def analyze_files(self) -> Dict[str, Any]:
        """Analyze all files in the input directory."""
        logger.info("Starting analysis mode...")

        analysis_results = {
            "timestamp": datetime.now().isoformat(),
            "input_directory": str(self.input_dir),
            "files_found": [],
            "total_files": 0,
            "valid_tsv_files": 0,
            "invalid_files": [],
            "file_details": [],
        }

        # Find all files in input directory
        for file_path in self.input_dir.rglob("*"):
            if file_path.is_file():
                analysis_results["total_files"] += 1
                file_info = {
                    "path": str(file_path.relative_to(self.input_dir)),
                    "size_bytes": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat(),
                    "extension": file_path.suffix.lower(),
                }

                # Check if it's a TSV file
                if file_path.suffix.lower() == ".tsv":
                    file_info["is_valid_tsv"] = True
                    file_info["rows"] = "Unknown"  # Will be filled by TSVReader
                    file_info["columns"] = "Unknown"  # Will be filled by TSVReader
                    analysis_results["valid_tsv_files"] += 1
                    analysis_results["files_found"].append(file_path.name)
                else:
                    file_info["is_valid_tsv"] = False
                    file_info["error"] = "Not a TSV file"
                    analysis_results["invalid_files"].append(
                        {"file": file_path.name, "error": "Not a TSV file"}
                    )

                analysis_results["file_details"].append(file_info)

        logger.info(
            f"Analysis complete: {analysis_results['total_files']} total files, {analysis_results['valid_tsv_files']} valid TSV files"
        )

        return analysis_results
