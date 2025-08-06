"""CLI entry point for TSV to YAML converter."""

from pathlib import Path
from typing import Optional

import click

from .cli_commands import CLICommands


@click.group()
@click.version_option(version="1.0.0", prog_name="tsv-to-yaml-converter")
@click.option(
    "--project-root",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path.cwd(),
    help="Project root directory (default: current directory)"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.pass_context
def cli(ctx: click.Context, project_root: Path, verbose: bool) -> None:
    """TSV to YAML Shot List Converter.
    
    A batch processing tool for converting film/video shot lists from TSV format
    to hierarchical YAML format following standardized input/output patterns.
    """
    ctx.ensure_object(dict)
    ctx.obj['project_root'] = project_root
    ctx.obj['verbose'] = verbose


@cli.command()
@click.option(
    "--config",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Configuration file path (YAML format)"
)
@click.pass_context
def process(ctx: click.Context, config: Optional[Path]) -> None:
    """Process all TSV files in the input directory."""
    commands = CLICommands(ctx.obj['project_root'], ctx.obj['verbose'])
    commands.process_files(config)


@cli.command()
@click.pass_context
def analyze(ctx: click.Context) -> None:
    """Analyze files without processing them."""
    commands = CLICommands(ctx.obj['project_root'], ctx.obj['verbose'])
    commands.analyze_files()


@cli.command()
@click.option(
    "--output",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    default=Path("config.yaml"),
    help="Output configuration file path"
)
@click.pass_context
def init_config(ctx: click.Context, output: Path) -> None:
    """Initialize a new configuration file."""
    commands = CLICommands(ctx.obj['project_root'], ctx.obj['verbose'])
    commands.init_config(output)


@cli.command()
@click.option(
    "--mappings-file",
    type=click.Path(file_okay=True, dir_okay=False, path_type=Path),
    default=Path("mappings.json"),
    help="Path to mappings configuration file"
)
@click.pass_context
def init_mappings(ctx: click.Context, mappings_file: Path) -> None:
    """Initialize a new mappings configuration file."""
    commands = CLICommands(ctx.obj['project_root'], ctx.obj['verbose'])
    commands.init_mappings(mappings_file)


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show current project status."""
    commands = CLICommands(ctx.obj['project_root'], ctx.obj['verbose'])
    commands.status()


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()