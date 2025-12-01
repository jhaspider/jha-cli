import json
from pathlib import Path
from typing import Optional
import click
from .utils import (display_warning, display_success, display_error)


class Config:
    
    CONFIG_DIR = Path.home() / ".jha"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    HISTORY_FILE = CONFIG_DIR / "history.json"
    
    # Default values
    DEFAULTS = {
        "OPENAI_KEY": "",
        "MODEL": "gpt-4o-mini",
        "SHELL": "bash",
    }
    
    def __init__(self):
        self.CONFIG_DIR.mkdir(exist_ok=True)
        self._ensure_config_exists()
    
    def _ensure_config_exists(self) -> None:
        if not self.CONFIG_FILE.exists():
            self.CONFIG_FILE.write_text(
                json.dumps(self.DEFAULTS, indent=2)
            )
    
    def load(self) -> dict:
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._ensure_config_exists()
            return self.DEFAULTS.copy()
    
    def save(self, config: dict) -> None:
        self.CONFIG_DIR.mkdir(exist_ok=True)
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        config = self.load()
        return config.get(key, default or self.DEFAULTS.get(key))
    
    def set(self, key: str, value: str) -> None:
        config = self.load()
        
        # Validation
        if key == "OPENAI_KEY" and not value.startswith("sk-"):
            click.echo(display_warning("Warning: OpenAI API keys typically start with 'sk-'"))
        
        config[key] = value
        self.save(config)
        click.echo(display_success(f"{key} set successfully"))
    
    def clear(self) -> None:
        self.save(self.DEFAULTS.copy())
        click.echo(display_success("Configuration cleared"))
    
    def show(self) -> None:
        config = self.load()
        
        for key, value in config.items():
            if key == "OPENAI_KEY" and value:
                # Mask API key
                masked_key = value[:7] + "*" * (len(value) - 11) + value[-4:]
                click.echo(f"{key:<15}: {masked_key}")
            else:
                click.echo(f"{key:<15}: {value if value else '(not set)'}")
        



config = Config()
