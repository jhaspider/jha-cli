"""Utility functions for JHA CLI."""

import click
import subprocess
import sys
from typing import Optional


def copy_to_clipboard(text: str) -> bool:
    try:
        if sys.platform == "darwin":  # macOS
            process = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            process.communicate(input=text.encode("utf-8"))
            return process.returncode == 0
        
        elif sys.platform == "linux":
            # Try xclip first, then xsel
            for cmd in ["xclip", "xsel"]:
                try:
                    process = subprocess.Popen(
                        [cmd],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    process.communicate(input=text.encode("utf-8"))
                    if process.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
            return False
        
        elif sys.platform == "win32":  # Windows
            process = subprocess.Popen(
                ["clip"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            process.communicate(input=text.encode("utf-8"))
            return process.returncode == 0
    
    except Exception:
        return False
    
    return False




def display_command(command: str) -> str:
    return click.style(command, fg="cyan")

def display_success(message: str) -> str:
    return click.style(f"✓ {message}", fg="green")

def display_error(message: str) -> str:
    return click.style(f"✗ {message}", fg="red")

def display_warning(message: str) -> str:
    return click.style(f"✗ {message}", fg="yellow")

def prompt_yes_no(message: str, default: bool = True) -> bool:
    default_str = "[Y/n]" if default else "[y/N]"
    prompt_text = f"{message} {default_str}: "
    
    user_input = click.prompt(prompt_text, default="").lower()
    
    if user_input == "":
        return default
    
    return user_input in ["y", "yes"]


def truncate_text(text: str, length: int = 50) -> str:
    return text[:length] + "..." if len(text) > length else text
