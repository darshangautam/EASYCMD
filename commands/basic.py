from rich.console import Console
import os

console = Console()

def do_help(shell):
    """Show available commands"""
    console.print("\n[bold]EasyCMD Built-in Commands:[/bold]")
    commands = {
        "help": "Show this help message",
        "ls / dir": "List files and folders",
        "cd <path>": "Change directory",
        "pwd": "Print current working directory",
        "clear / cls": "Clear the screen",
        "exit / quit": "Exit EasyCMD"
    }
    for cmd, desc in commands.items():
        console.print(f"  [bold cyan]{cmd:<15}[/bold cyan] {desc}")
    console.print("\n[italic]Any other command will be passed to Windows cmd.[/italic]")

def do_ls(shell, args=""):
    """List files (easier version)"""
    target = os.path.join(shell.current_dir, args) if args else shell.current_dir
    try:
        items = os.listdir(target)
        for item in sorted(items):
            full_path = os.path.join(target, item)
            if os.path.isdir(full_path):
                console.print(f"[bold blue]{item}/[/bold blue]")
            else:
                console.print(item)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def do_cd(shell, args):
    """Change directory"""
    if not args:
        console.print("[yellow]Usage: cd <folder or ..>[/yellow]")
        return
    try:
        new_path = os.path.join(shell.current_dir, args)
        if os.path.isdir(new_path):
            os.chdir(new_path)
            shell.current_dir = os.getcwd()
        else:
            console.print(f"[red]Directory not found: {args}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def do_pwd(shell, args=""):
    """Print current directory"""
    console.print(f"[bold blue]Current directory:[/bold blue] {shell.current_dir}")

def do_clear(shell, args=""):
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def do_exit(shell, args=""):
    """Exit the shell"""
    console.print("[bold red]Goodbye! 👋[/bold red]")
    return True  # This will stop the loop