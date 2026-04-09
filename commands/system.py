import subprocess
from rich.console import Console

console = Console()

def run_system_command(shell, command):
    """Run any unknown command using Windows cmd"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=shell.current_dir
        )
        if result.stdout.strip():
            console.print(result.stdout.strip())
        if result.stderr.strip():
            console.print(f"[red]{result.stderr.strip()}[/red]")
    except Exception as e:
        console.print(f"[red]Command failed: {e}[/red]")