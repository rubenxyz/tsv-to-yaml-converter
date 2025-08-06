"""Rich UI rendering for CLI commands."""

import json
from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.table import Table

console = Console()


class CLIUI:
    """Handles Rich UI rendering for CLI commands."""

    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message."""
        console.print(f"✅ [green]{message}[/green]")

    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message."""
        console.print(f"❌ [red]{message}[/red]")

    @staticmethod
    def print_info(message: str) -> None:
        """Print an info message."""
        console.print(f"📋 [cyan]{message}[/cyan]")

    @staticmethod
    def print_warning(message: str) -> None:
        """Print a warning message."""
        console.print(f"⚠️  [yellow]{message}[/yellow]")

    @staticmethod
    def print_file_info(message: str) -> None:
        """Print file information."""
        console.print(f"📁 [cyan]{message}[/cyan]")

    @staticmethod
    def print_processing_info(message: str) -> None:
        """Print processing information."""
        console.print(f"🔄 [blue]{message}[/blue]")

    @staticmethod
    def display_analysis_results(
        results: Dict[str, Any], verbose: bool = False
    ) -> None:
        """Display analysis results in a formatted table."""
        # Create summary table
        table = Table(title="File Analysis Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Files", str(results["total_files"]))
        table.add_row("Valid TSV Files", str(results["valid_tsv_files"]))
        table.add_row("Invalid Files", str(len(results["invalid_files"])))

        console.print(table)

        # Display valid files
        if results["files_found"]:
            console.print("\n📁 [cyan]Valid TSV Files:[/cyan]")
            for file_name in results["files_found"]:
                console.print(f"  • {file_name}")

        # Display invalid files
        if results["invalid_files"]:
            console.print("\n⚠️  [yellow]Invalid Files:[/yellow]")
            for invalid_file in results["invalid_files"]:
                console.print(f"  • {invalid_file['file']}: {invalid_file['error']}")

        # Output JSON for programmatic use
        if verbose:
            console.print("\n📋 [cyan]Detailed Results (JSON):[/cyan]")
            console.print(json.dumps(results, indent=2))

    @staticmethod
    def display_project_status(
        input_files: int,
        output_dir: Path,
        verbose: bool = False,
    ) -> None:
        """Display current project status."""
        console.print("\n📊 [cyan]Project Status:[/cyan]")
        console.print(f"  • Input files found: {input_files}")
        console.print(f"  • Output directory: {output_dir}")

        if verbose:
            console.print("  • Verbose logging: enabled")
        else:
            console.print("  • Verbose logging: disabled")

    @staticmethod
    def display_config_created(output: Path) -> None:
        """Display configuration file creation success."""
        console.print(f"✅ [green]Configuration file created: {output}[/green]")
        console.print("📝 Edit the file to customize your settings.")

    @staticmethod
    def display_mappings_created(mappings_file: Path) -> None:
        """Display mappings file creation success."""
        console.print(f"✅ [green]Mappings file created: {mappings_file}[/green]")
        console.print("📝 Edit the file to customize your field mappings.")

    @staticmethod
    def display_processing_success(output_dir: Path) -> None:
        """Display processing success message."""
        console.print("✅ [green]Processing completed successfully![/green]")
        console.print(f"📁 Check output in: {output_dir}")

    @staticmethod
    def display_processing_error(output_dir: Path) -> None:
        """Display processing error message."""
        console.print("❌ [red]Processing completed with errors![/red]")
        console.print(f"📋 Check logs in: {output_dir}")
