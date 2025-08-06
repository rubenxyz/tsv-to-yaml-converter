"""CLI entry point for TSV to YAML converter."""

from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from .cli_commands import CLICommands

console = Console()


@click.group()
@click.option(
    "--project-root",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Enable verbose logging"
)
@click.pass_context
def cli(ctx, project_root: Path, verbose: bool):
    """TSV to YAML Shot List Converter."""
    ctx.ensure_object(dict)
    ctx.obj["project_root"] = project_root
    ctx.obj["verbose"] = verbose


@cli.command()
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="Configuration file path",
)
@click.pass_context
def process(ctx, config: Optional[Path]):
    """Process all TSV files in the input directory."""
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj["verbose"]
    
    commands = CLICommands(project_root, verbose)
    commands.process_files(config)


@cli.command()
@click.pass_context
def analyze(ctx):
    """Analyze files without processing them."""
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj["verbose"]
    
    commands = CLICommands(project_root, verbose)
    commands.analyze_files()


@cli.command()
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=Path("config.yaml"),
    help="Output configuration file path",
)
@click.pass_context
def init_config(ctx, output: Path):
    """Initialize configuration file."""
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj["verbose"]
    
    commands = CLICommands(project_root, verbose)
    commands.init_config(output)


@cli.command()
@click.option(
    "--mappings-file",
    type=click.Path(path_type=Path),
    default=Path("mappings.json"),
    help="Output mappings file path",
)
@click.pass_context
def init_mappings(ctx, mappings_file: Path):
    """Initialize field mappings file."""
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj["verbose"]
    
    commands = CLICommands(project_root, verbose)
    commands.init_mappings(mappings_file)


@cli.command()
@click.pass_context
def status(ctx):
    """Show project status."""
    project_root = ctx.obj["project_root"]
    verbose = ctx.obj["verbose"]
    
    commands = CLICommands(project_root, verbose)
    commands.status()


if __name__ == "__main__":
    cli()
