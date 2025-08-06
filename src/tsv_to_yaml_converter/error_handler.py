"""Error handling functionality for consistent error management."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from loguru import logger


class ErrorHandler:
    """Provides consistent error handling and logging."""

    def __init__(self):
        """Initialize the error handler."""
        self.errors: List[Dict[str, Any]] = []
        self.stats = {
            "total_files": 0,
            "processed_files": 0,
            "failed_files": 0,
            "start_time": None,
            "end_time": None,
        }

    def start_processing(self) -> None:
        """Mark the start of processing."""
        self.stats["start_time"] = datetime.now()
        self.errors.clear()

    def end_processing(self) -> None:
        """Mark the end of processing."""
        self.stats["end_time"] = datetime.now()

    def log_error(
        self, file_path: Path, error: Exception, error_type: str = None
    ) -> None:
        """Log an error with consistent formatting."""
        error_info = {
            "file": str(file_path),
            "error": str(error),
            "type": error_type or type(error).__name__,
            "timestamp": datetime.now().isoformat(),
        }

        self.errors.append(error_info)
        self.stats["failed_files"] += 1

        logger.error(f"Error processing {file_path.name}: {str(error)}")

    def log_success(self, file_path: Path) -> None:
        """Log a successful processing."""
        self.stats["processed_files"] += 1
        logger.info(f"Successfully processed {file_path.name}")

    def log_summary(self) -> None:
        """Log a summary of processing results."""
        logger.info("Batch processing complete!")
        logger.info(f"  → Total files: {self.stats['total_files']}")
        logger.info(f"  → Processed: {self.stats['processed_files']}")
        logger.info(f"  → Failed: {self.stats['failed_files']}")

        if self.errors:
            logger.warning("Errors encountered:")
            for error in self.errors:
                logger.warning(f"  • {error['file']}: {error['error']}")

    def has_errors(self) -> bool:
        """Check if any errors occurred."""
        return len(self.errors) > 0
