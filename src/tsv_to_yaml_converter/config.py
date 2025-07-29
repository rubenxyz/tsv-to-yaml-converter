"""Configuration management for TSV to YAML converter."""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class Config(BaseModel):
    """Configuration for TSV to YAML conversion."""
    
    project_title: Optional[str] = Field(
        default=None,
        description="Project title (inferred from filename if not provided)"
    )

    yaml_indent: int = Field(
        default=2,
        ge=1,
        le=8,
        description="YAML indentation level"
    )
    yaml_width: int = Field(
        default=120,
        ge=80,
        le=200,
        description="YAML line width"
    )
    
    @classmethod
    def from_file(cls, config_path: Path) -> "Config":
        """Load configuration from YAML file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f) or {}
            return cls(**config_data)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return self.model_dump(exclude_none=True)
    
    def save_to_file(self, config_path: Path) -> None:
        """Save configuration to YAML file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)