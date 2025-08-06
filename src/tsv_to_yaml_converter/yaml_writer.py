"""YAML output formatting and writing functionality."""

import yaml
from pathlib import Path
from loguru import logger

from .models import Project


class YAMLWriter:
    """Handles YAML output formatting and writing."""

    def __init__(self, yaml_indent: int = 2, yaml_width: int = 120):
        """Initialize the YAML writer with formatting options."""
        self.yaml_indent = yaml_indent
        self.yaml_width = yaml_width

    def write_yaml_file(self, project: Project, output_file: Path) -> None:
        """Write project data to YAML file with custom formatting."""
        # First, get the YAML as a string
        yaml_content = yaml.dump(
            {'project': project.model_dump(exclude_none=True)},
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            indent=self.yaml_indent,
            width=self.yaml_width
        )

        # Add empty lines before epochs, scenes, and shots
        lines = yaml_content.split('\n')
        formatted_lines = []

        for _, line in enumerate(lines):
            # Add empty line before epoch_number
            if '- epoch_number:' in line:
                formatted_lines.append('')

            # Add double empty lines before scene_number
            elif '- scene_number:' in line:
                formatted_lines.append('')
                formatted_lines.append('')

            # Add empty line before shot_number
            elif '- shot_number:' in line:
                formatted_lines.append('')

            formatted_lines.append(line)

        # Write the formatted content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(formatted_lines))

    def finalize_and_write(self, project: Project, output_file: Path) -> None:
        """Write YAML output and log success."""
        # Write YAML file
        self.write_yaml_file(project, output_file)

        # Log success
        total_epochs = len(project.epochs)
        total_scenes = sum(len(epoch.scenes) for epoch in project.epochs)
        total_shots = sum(len(scene.shots) for epoch in project.epochs for scene in epoch.scenes)

        logger.info(f"Successfully wrote YAML to {output_file.name}")
        logger.info(f"  → {total_epochs} epochs, {total_scenes} scenes, {total_shots} shots")
