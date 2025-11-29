import sys
import typer
import click
import readline 
import pyperclip
from typing import Optional
from .config import config
from .llm import get_llm
from .history import history
from .utils import (
    display_command, display_explanation, display_success,
    display_error, display_info, prompt_yes_no,
    copy_to_clipboard
)

app = typer.Typer(
    help="JHA - Just Help Assistant. LLM-powered CLI command discovery.",
    no_args_is_help=True
)

@app.command(name="query", help="Generate a command from natural language query")
def query(
    q: str = typer.Argument(..., help="Natural language query for a command")
):
    try:
        click.echo(click.style("Give me a second..."))
        
        llm = get_llm(config)
        
        # Generate command
        command = llm.generate_command(q)
        
        # Display the command
        click.echo("\033[F\033[K", nl=False)
        display_command(command)
        
        # Add to history
        history.add(q, command)
        
        # Copy to clipboard
        if copy_to_clipboard(str(command)):
            display_success("Command copied to clipboard. Press Ctrl+V to use it. jhax for detailed explanation.")
        else:
            display_error("Failed to copy to clipboard")
    
    except Exception as e:
        display_error(f"Error: {str(e)}")
        raise typer.Exit(1)


@app.command(name="explain", help="Explain what a command does in detail")
def explain(
    cmd: Optional[str] = typer.Argument(None, help="The command to explain")
):
    try:
        # Handle ArgumentInfo explicitly
        if isinstance(cmd, typer.models.ArgumentInfo):
            cmd = cmd.default  # Extract the default valu
            
        if not cmd:
            cmd = pyperclip.paste().strip()
            if not cmd:
                display_error("Clipboard is empty or does not contain a valid command.")
                raise typer.Exit(1)
            
        llm = get_llm(config)
        
        # Get explanation
        explanation = llm.explain_command(cmd)
        
        # Display explanation
        display_explanation(explanation)
    
    except Exception as e:
        display_error(f"Error: {str(e)}")
        raise typer.Exit(1)


@app.command(name="config", help="Manage JHA configuration")
def config_cmd(
    action: str = typer.Argument("show", help="Action: show, set, clear"),
    param: Optional[str] = typer.Argument(None, help="KEY=VALUE for set action")
):
    try:
        if action == "show":
            config.show()
        
        elif action == "set":
            if not param or "=" not in param:
                display_error("Use format: jha config set KEY=VALUE")
                raise typer.Exit(1)
            
            key, value = param.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            
            if key not in config.DEFAULTS:
                display_error(f"Unknown config key: {key}")
                click.echo(f"Available keys: {', '.join(config.DEFAULTS.keys())}")
                raise typer.Exit(1)
            
            config.set(key, value)
        
        elif action == "clear":
            if prompt_yes_no("Clear all configuration?", default=False):
                config.clear()
            else:
                click.echo("Cancelled.")
        
        else:
            display_error(f"Unknown action: {action}")
            click.echo("Available actions: show, set, clear")
            raise typer.Exit(1)
    
    except Exception as e:
        display_error(f"Error: {str(e)}")
        raise typer.Exit(1)


@app.command(name="history", help="Shows history of previous queries and commands")
def history_cmd(
    action: str = typer.Argument("show", help="Action: show, clear"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of entries to show")
):

    try:
        if action == "show":
            entries = history.get_all(limit)
            
            if not entries:
                display_info("No history yet.")
                return
            
            click.echo()
            
            for i, entry in enumerate(entries, 1):
                timestamp = entry.get("timestamp", "")[:16]
                query = entry.get("query", "")
                command = entry.get("command", "")
                
                click.echo(f"{i}. [{timestamp}] {query}")
                display_command(command)
                click.echo()
        
        elif action == "clear":
            if prompt_yes_no("Clear all history?", default=False):
                history.clear()
                display_success("History cleared")
            else:
                click.echo("Cancelled.")
        
        else:
            display_error(f"Unknown action: {action}")
            raise typer.Exit(1)
    
    except Exception as e:
        display_error(f"Error: {str(e)}")
        raise typer.Exit(1)


@app.command(name="last", help="Show the last query and command and copies the command to clipboard")
def last():
    try:
        last_entry = history.get_last()
        
        if not last_entry:
            display_error("No previous command found.")
            raise typer.Exit(1)
        
        command = last_entry.get("command")
        query = last_entry.get("query")
        click.echo(click.style(f"Query: {query}", fg="blue"))
        display_command(command)
        
        if copy_to_clipboard(command):
            display_success("Command copied to clipboard. Press Ctrl+V to use it. jhax for detailed explanation.")
        else:
            display_error("Failed to copy to clipboard")
    
    except Exception as e:
        display_error(f"Error: {str(e)}")
        raise typer.Exit(1)

@app.command(name="version", help="Show the version of JHA")
def version():
    click.echo(click.style("v1.0.0", fg="cyan", bold=True))
    click.echo("JHA - Just Help Assistant. LLM-powered CLI command discovery.")


def main():
    first_arg = sys.argv[1]
    if(first_arg == "--help"):
        app()
        return
    is_found = first_arg in [command.name for command in app.registered_commands]
    if is_found:
        app()
    else:
        query(" ".join(sys.argv[1:]))

if __name__ == "__main__":
    main()
