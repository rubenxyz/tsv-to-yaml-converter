"""CLI command implementations for TSV to YAML converter."""

import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from loguru import logger

from .converter import TSVToYAMLConverter
from .config import Config

console = Console()


class CLICommands:
    """Handles CLI command implementations."""
    
    def __init__(self, project_root: Path, verbose: bool):
        """Initialize CLI commands with context."""
        self.project_root = project_root
        self.verbose = verbose
        self._setup_logging()
    
    def _setup_logging(self) -> None:
        """Setup logging based on verbose flag."""
        level = "DEBUG" if self.verbose else "INFO"
        logger.add(sys.stdout, level=level, colorize=True)
    
    def _handle_error(self, error: Exception, message: str = "Error") -> None:
        """Handle errors consistently across commands."""
        console.print(f"❌ [red]{message}: {error}[/red]")
        sys.exit(1)
    
    def _create_converter(self) -> TSVToYAMLConverter:
        """Create and return a converter instance."""
        try:
            return TSVToYAMLConverter(self.project_root)
        except Exception as e:
            self._handle_error(e, "Failed to initialize converter")
    
    def process_files(self, config: Optional[Path]) -> None:
        """Process all TSV files in the input directory."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Initializing converter...", total=None)
            
            try:
                # Initialize converter
                converter = self._create_converter()
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
                self._handle_error(e)
    
    def analyze_files(self) -> None:
        """Analyze files without processing them."""
        try:
            converter = self._create_converter()
            results = converter.analyze_files()
            
            self._display_analysis_results(results)
            
        except Exception as e:
            self._handle_error(e, "Error during analysis")
    
    def _display_analysis_results(self, results: Dict[str, Any]) -> None:
        """Display analysis results in a formatted table."""
        # Create summary table
        table = Table(title="File Analysis Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Files", str(results['total_files']))
        table.add_row("Valid TSV Files", str(results['valid_tsv_files']))
        table.add_row("Invalid Files", str(len(results['invalid_files'])))
        
        console.print(table)
        
        # Display valid files
        if results['files_found']:
            console.print("\n📁 [cyan]Valid TSV Files:[/cyan]")
            for file_name in results['files_found']:
                console.print(f"  • {file_name}")
        
        # Display invalid files
        if results['invalid_files']:
            console.print("\n⚠️  [yellow]Invalid Files:[/yellow]")
            for invalid_file in results['invalid_files']:
                console.print(f"  • {invalid_file['file']}: {invalid_file['error']}")
        
        # Output JSON for programmatic use
        if self.verbose:
            console.print("\n📋 [cyan]Detailed Results (JSON):[/cyan]")
            console.print(json.dumps(results, indent=2))
    
    def init_config(self, output: Path) -> None:
        """Initialize a new configuration file."""
        try:
            config = Config()
            config.save_to_file(output)
            
            console.print(f"✅ [green]Configuration file created: {output}[/green]")
            console.print("📝 Edit the file to customize your settings.")
            
        except Exception as e:
            self._handle_error(e, "Error creating configuration")
    
    def init_mappings(self, mappings_file: Path) -> None:
        """Initialize a new mappings configuration file."""
        try:
            default_mappings = self._get_default_mappings()
            config = Config()
            config.save_mappings(default_mappings, mappings_file)
            
            console.print(f"✅ [green]Mappings file created: {mappings_file}[/green]")
            console.print("📝 Edit the file to customize your field mappings.")
            
        except Exception as e:
            self._handle_error(e, "Error creating mappings")
    
    def _get_default_mappings(self) -> Dict[str, Dict[str, str]]:
        """Get default field mappings."""
        return {
            "DIURNAL": {
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
    
    def status(self) -> None:
        """Show current project status."""
        try:
            converter = self._create_converter()
            self._display_project_status(converter)
            
        except Exception as e:
            self._handle_error(e, "Error checking status")
    
    def _display_project_status(self, converter: TSVToYAMLConverter) -> None:
        """Display project status in a formatted table."""
        table = Table(title="Project Status")
        table.add_column("Directory", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Files", style="yellow")
        
        # Input directory status
        input_files = list(converter.input_dir.rglob('*.tsv'))
        table.add_row(
            "01.INPUT",
            "✅ Ready" if input_files else "⚠️  Empty",
            str(len(input_files))
        )
        
        # Output directory status
        output_dirs = list(converter.output_dir.iterdir())
        table.add_row(
            "02.OUTPUT",
            "📁 Has Output" if output_dirs else "📂 Empty",
            str(len(output_dirs))
        )
        
        # Output files status
        output_files = list(converter.output_dir.rglob('*.yaml'))
        table.add_row(
            "02.OUTPUT",
            "✅ Has Output" if output_files else "📂 Empty",
            str(len(output_files))
        )
        
        console.print(table)
        
        # Display input files
        if input_files:
            console.print(f"\n📁 [cyan]Ready to process {len(input_files)} TSV file(s):[/cyan]")
            for file_path in input_files:
                console.print(f"  • {file_path.name}") 