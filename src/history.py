import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from .config import Config


class History:
    
    def __init__(self):
        self.history_file = Config.CONFIG_DIR / "history.json"
        self._ensure_history_exists()
    
    def _ensure_history_exists(self) -> None:
        if not self.history_file.exists():
            self.history_file.write_text(json.dumps([], indent=2))
    
    def _load_history(self) -> list:
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_history(self, history: list) -> None:
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def add(self, query: str, command: str, 
            explanation: bool = False) -> None:
        
        shell = Config().get("SHELL")
        history = self._load_history()
        
        entry: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "command": command,
            "shell": shell,
            "is_explanation": explanation
        }
        
        history.insert(0, entry)
        self._save_history(history)
    
    def get_last(self) -> Optional[Dict[str, Any]]:
        history = self._load_history()
        
        for entry in history:
            if not entry.get("is_explanation", False):
                return entry
        
        return None
    
    def get_last_command(self) -> Optional[str]:
        entry = self.get_last()
        return entry.get("command") if entry else None
    
    def get_all(self, limit: int = 20) -> list:
        history = self._load_history()
        return history[-limit:]
    
    def clear(self) -> None:
        self._save_history([])


history = History()
