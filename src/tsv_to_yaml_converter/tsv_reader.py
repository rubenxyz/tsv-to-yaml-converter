"""TSV file reading and data cleaning functionality."""

from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from loguru import logger


class TSVReader:
    """Handles TSV file reading, validation, and data cleaning."""

    def __init__(self, field_mappings: Optional[Dict[str, Dict[str, str]]] = None):
        """Initialize the TSV reader with optional field mappings."""
        self.field_mappings = field_mappings or {}

    def read_tsv_file(self, tsv_file: Path) -> pd.DataFrame:
        """Read TSV file and handle BOM characters."""
        df = pd.read_csv(tsv_file, sep="\t", dtype=str, encoding="utf-8-sig")
        logger.info(f"Successfully read {len(df)} rows from {tsv_file.name}")
        return df

    def clean_value(self, value: Any, field_name: Optional[str] = None) -> Any:
        """Clean and normalize values, handling NaN/null values and BOM characters."""
        if pd.isna(value) or value == "" or str(value).strip() == "":
            return None

        if isinstance(value, str):
            # Remove BOM characters and strip whitespace
            cleaned = value.strip().replace("\ufeff", "").replace("\u200b", "")
            if not cleaned:
                return None

            # Apply field mappings if available
            if field_name and self.field_mappings:
                mapped_value = self._apply_field_mapping(field_name, cleaned)
                if mapped_value:
                    return mapped_value

            return cleaned

        return value

    def _apply_field_mapping(self, field_name: str, value: str) -> Optional[str]:
        """Apply field mapping if available."""
        if not self.field_mappings:
            return None

        field_mappings = self.field_mappings.get(field_name, {})
        return field_mappings.get(value, None)

    def clean_row_data(self, row: pd.Series, columns: List[str]) -> Dict[str, Any]:
        """Clean all values in a row."""
        return {col: self.clean_value(row[col], col) for col in columns}

    def is_valid_row(self, row_data: Dict[str, Any]) -> bool:
        """Check if row has essential data for processing."""
        return bool(row_data.get("SHOT_NUM"))

    def validate_tsv_file(self, tsv_file: Path) -> Dict[str, Any]:
        """Validate a TSV file and return analysis results."""
        try:
            df = self.read_tsv_file(tsv_file)
            return {
                "is_valid": True,
                "rows": len(df),
                "columns": list(df.columns),
                "error": None,
            }
        except Exception as e:
            return {"is_valid": False, "rows": 0, "columns": [], "error": str(e)}
