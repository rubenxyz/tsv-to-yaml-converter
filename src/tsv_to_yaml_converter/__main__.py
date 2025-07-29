"""CLI entry point for TSV to YAML converter."""

import json
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from .converter import TSVToYAMLConverter
from .config import Config
from loguru import logger

console = Console()
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
    
    # Setup logging
    if verbose:
        logger.add(sys.stdout, level="DEBUG", colorize=True)
    else:
        logger.add(sys.stdout, level="INFO", colorize=True)


@cli.command()
@click.option(
    "--config",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    help="Configuration file path (YAML format)"
)
@click.pass_context
def process(ctx: click.Context, config: Optional[Path]) -> None:
    """Process all TSV files in the input directory."""
    project_root = ctx.obj['project_root']
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Initializing converter...", total=None)
        
        try:
            # Initialize converter
            converter = TSVToYAMLConverter(project_root)
            progress.update(task, description="Processing TSV files...")
            
            # Process files
            success = converter.process_files(config)
            
            if success:
                console.print("✅ [green]Processing completed successfully![/green]")
                console.print(f"📁 Check output in: {converter.output_dir}")
            else:
                console.print("❌ [red]Processing completed with errors![/red]")
                console.print(f"📋 Check logs in: {converter.output_dir}")
                sys.exit(1)
                
        except Exception as e:
            console.print(f"❌ [red]Error: {e}[/red]")
            sys.exit(1)


@cli.command()
@click.pass_context
def analyze(ctx: click.Context) -> None:
    """Analyze files without processing them."""
    project_root = ctx.obj['project_root']
    
    try:
        # Initialize converter
        converter = TSVToYAMLConverter(project_root)
        
        # Analyze files
        results = converter.analyze_files()
        
        # Display results in a nice table
        table = Table(title="File Analysis Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Files", str(results['total_files']))
        table.add_row("Valid TSV Files", str(results['valid_tsv_files']))
        table.add_row("Invalid Files", str(len(results['invalid_files'])))
        
        console.print(table)
        
        if results['files_found']:
            console.print("\n📁 [cyan]Valid TSV Files:[/cyan]")
            for file_name in results['files_found']:
                console.print(f"  • {file_name}")
        
        if results['invalid_files']:
            console.print("\n⚠️  [yellow]Invalid Files:[/yellow]")
            for invalid_file in results['invalid_files']:
                console.print(f"  • {invalid_file['file']}: {invalid_file['error']}")
        
        # Output JSON for programmatic use
        if ctx.obj.get('verbose'):
            console.print("\n📋 [cyan]Detailed Results (JSON):[/cyan]")
            console.print(json.dumps(results, indent=2))
            
    except Exception as e:
        console.print(f"❌ [red]Error: {e}[/red]")
        sys.exit(1)


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
    try:
        # Create default configuration
        config = Config()
        
        # Save to file
        config.save_to_file(output)
        
        console.print(f"✅ [green]Configuration file created: {output}[/green]")
        console.print("📝 Edit the file to customize your settings.")
        
    except Exception as e:
        console.print(f"❌ [red]Error creating configuration: {e}[/red]")
        sys.exit(1)


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
    try:
        # Create default mappings
        default_mappings = {
            "TIME": {
                "GH": "Golden Hour",
                "MH": "Magic Hour", 
                "BH": "Blue Hour",
                "DAY": "Day",
                "NIGHT": "Night",
                "DAWN": "Dawn",
                "DUSK": "Dusk"
            },
            "LOC_TYPE": {
                "EXT": "Exterior",
                "INT": "Interior",
                "EXT/INT": "Exterior/Interior"
            },
            "MOVE_TYPE": {
                "STATIC": "Static",
                "PAN": "Pan",
                "TILT": "Tilt",
                "DOLLY": "Dolly",
                "CRANE": "Crane",
                "HANDHELD": "Handheld",
                "STEADICAM": "Steadicam"
            },
            "MOVE_SPEED": {
                "SLOW": "Slow",
                "MEDIUM": "Medium", 
                "FAST": "Fast",
                "VERY_SLOW": "Very Slow",
                "VERY_FAST": "Very Fast"
            },
            "ANGLE": {
                "LOW": "Low Angle",
                "HIGH": "High Angle",
                "EYE_LEVEL": "Eye Level",
                "DUTCH": "Dutch Angle",
                "BIRDS_EYE": "Bird's Eye",
                "WORM_EYE": "Worm's Eye"
            }
        }
        
        # Create config and save mappings
        config = Config()
        config.save_mappings(default_mappings, mappings_file)
        
        console.print(f"✅ [green]Mappings file created: {mappings_file}[/green]")
        console.print("📝 Edit the file to customize your field mappings.")
        
    except Exception as e:
        console.print(f"❌ [red]Error creating mappings: {e}[/red]")
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """Show current project status."""
    project_root = ctx.obj['project_root']
    
    try:
        # Initialize converter
        converter = TSVToYAMLConverter(project_root)
        
        # Check directory status
        table = Table(title="Project Status")
        table.add_column("Directory", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Files", style="yellow")
        
        # Input directory
        input_files = list(converter.input_dir.rglob('*.tsv'))
        table.add_row(
            "01.INPUT",
            "✅ Ready" if input_files else "⚠️  Empty",
            str(len(input_files))
        )
        
        # Output directory
        output_dirs = list(converter.output_dir.iterdir())
        table.add_row(
            "02.OUTPUT",
            "📁 Has Output" if output_dirs else "📂 Empty",
            str(len(output_dirs))
        )
        
        # Output directory status
        output_files = list(converter.output_dir.rglob('*.yaml'))
        table.add_row(
            "02.OUTPUT",
            "✅ Has Output" if output_files else "📂 Empty",
            str(len(output_files))
        )
        
        console.print(table)
        
        if input_files:
            console.print(f"\n📁 [cyan]Ready to process {len(input_files)} TSV file(s):[/cyan]")
            for file_path in input_files:
                console.print(f"  • {file_path.name}")
        
    except Exception as e:
        console.print(f"❌ [red]Error checking status: {e}[/red]")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()