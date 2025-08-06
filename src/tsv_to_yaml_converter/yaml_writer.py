"""YAML output formatting and writing functionality."""

from pathlib import Path

import yaml
from loguru import logger

from .models import Project


def represent_str(dumper, data):
    """Custom string representer that handles strings longer than 80 characters."""
    if len(data) > 80:  # If string is longer than 80 characters
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


class YAMLWriter:
    """Handles YAML output formatting and writing."""

    def __init__(self, yaml_indent: int = 2, yaml_width: int = 120):
        """Initialize the YAML writer with formatting options."""
        self.yaml_indent = yaml_indent
        self.yaml_width = yaml_width
        # Register custom representer for strings
        yaml.add_representer(str, represent_str)

    def write_yaml_file(self, project: Project, output_file: Path) -> None:
        """Write project data to YAML file with custom formatting."""
        # First, get the YAML as a string
        yaml_content = yaml.dump(
            {"project": project.model_dump(exclude_none=True)},
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            indent=self.yaml_indent,
            width=self.yaml_width,
        )

        # Add empty lines before epochs, scenes, and shots
        lines = yaml_content.split("\n")
        formatted_lines = []

        for _, line in enumerate(lines):
            # Add empty line before phase_number
            if "- phase_number:" in line:
                formatted_lines.append("")

            # Add double empty lines before scene_number
            elif "- scene_number:" in line:
                formatted_lines.append("")
                formatted_lines.append("")

            # Add empty line before shot_number
            elif "- shot_number:" in line:
                formatted_lines.append("")

            formatted_lines.append(line)

        # Write the formatted content
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_lines))

    def finalize_and_write(self, project: Project, output_file: Path) -> None:
        """Write YAML output and log success."""
        # Write YAML file
        self.write_yaml_file(project, output_file)

        # Log success with statistics
        total_phases = len(project.phases)
        total_scenes = sum(len(phase.scenes) for phase in project.phases)
        total_shots = sum(
            len(scene.shots) for phase in project.phases for scene in phase.scenes
        )

        logger.debug(f"Successfully wrote YAML to {output_file.name}")
        logger.debug(
            f"  → {total_phases} phases, {total_scenes} scenes, {total_shots} shots"
        )
