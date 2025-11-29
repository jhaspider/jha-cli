# AI Coding Agent Instructions for JHA CLI

Welcome to the JHA CLI codebase! This document provides essential guidance for AI coding agents to be productive in this project. Follow these instructions to understand the architecture, workflows, and conventions specific to this repository.

## Project Overview
JHA (Just Help Assistant) is an LLM-powered CLI tool designed to simplify development workflows by:
- Discovering and explaining shell commands using natural language queries.
- Managing configurations for OpenAI API keys and preferred LLM models.
- Tracking and re-executing command history.

### Key Features
- **LLM Integration**: Uses OpenAI Python SDK for natural language processing.
- **CLI Framework**: Built with Typer for argument parsing and command routing.
- **Configuration Management**: Persistent storage using JSON files.
- **Command History**: Tracks and replays commands via `jhax`.

## Codebase Architecture
The project is structured as follows:

```
src/
├── __main__.py           # Entry point for the CLI
├── cli.py                # Defines main CLI commands
├── config.py             # Handles configuration logic
├── llm.py                # Manages interactions with the LLM
├── history.py            # Tracks and replays command history
├── utils.py              # Shared utility functions
```

### Key Components
1. **CLI Commands** (`cli.py`):
   - Implements the primary interface for users.
   - Routes commands to appropriate handlers.
   - Includes commands like `query`, `explain`, `config`, `history`, and `last`.
2. **Configuration Management** (`config.py`):
   - Stores user preferences in `~/.jha/config.json`.
   - Supports setting, viewing, and clearing configurations.
   - Validates OpenAI API keys and provides default values for settings.
3. **LLM Integration** (`llm.py`):
   - Interfaces with OpenAI's API to process user queries.
   - Supports multiple models (e.g., `gpt-5-nano`).
   - Provides methods for generating and explaining commands.
4. **Command History** (`history.py`):
   - Tracks executed commands in `~/.jha/history.json`.
   - Provides methods to add, retrieve, and clear history.
5. **Utility Functions** (`utils.py`):
   - Handles terminal interactions, such as displaying messages and copying commands to the clipboard.

## Developer Workflows

### Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install the CLI locally:
   ```bash
   pip install -e .
   ```

### Running the CLI
Execute the CLI locally for testing:
```bash
python -m jha "Your query here"
```

### Testing
Run the test suite using:
```bash
pytest tests/
```

## Project-Specific Conventions
- **Configuration File**: All user settings are stored in `~/.jha/config.json`. Use `config.py` for any changes to configuration logic.
- **Command History**: Use `history.py` to modify how commands are tracked or replayed.
- **Error Handling**: Follow existing patterns in `utils.py` for consistent error messages and logging.
- **Clipboard Integration**: Use `utils.py` for copying commands to the clipboard, ensuring cross-platform compatibility.

## External Dependencies
- **Typer**: CLI framework for argument parsing.
- **OpenAI Python SDK**: For LLM queries.
- **Click**: For terminal formatting.
- **Rich**: For enhanced terminal output.
- **Python-Dotenv**: For managing environment variables.

## Examples
### Adding a New Command
1. Define the command in `cli.py` using Typer's `@app.command` decorator.
2. Implement the logic in a separate module if it involves significant functionality.
3. Update the README with usage examples.

### Modifying Configuration
1. Update `config.py` to handle new settings.
2. Ensure changes are reflected in `~/.jha/config.json`.
3. Add tests for the new configuration logic.

### Debugging LLM Integration
1. Check the API key and model configuration in `~/.jha/config.json`.
2. Use the `get_llm` function in `llm.py` to validate the connection.
3. Handle exceptions using the patterns in `llm.py`.

---

For any questions or clarifications, refer to the `README.md` or the respective module docstrings.