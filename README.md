# jha-cli : a CLI tool for just-in-time shell command discovery.

If you prefer working in the terminal but sometimes fall short on remembering commands, this CLI tool can help.
It’s also useful for anyone still getting comfortable with the command line.

It uses OpenAI models to interpret natural-language queries and suggest relevant shell commands.

## Features

- Query for suitable commands using natural language
- Support for multiple shells (bash, zsh, cmd, PowerShell)
- Get explanations for commands
- Command history tracking for quick re-execution and recall
- Option to jump to the last command from history
- Simple config commands to set OPENAI_KEY, MODEL, and SHELL
- Persistent configuration storage
- Searched command stored in clipboard for quick execution

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from PyPI
```bash
pip install jha-cli
```

### Alternative Installation (Windows)
```bash
pip install pipx
python -m pipx ensurepath
# Restart command prompt
pipx install jha-cli
```

## Usage

### Check Installation
```bash
jha
jha version
jha --help
```

### Initial Setup
```bash
# Set your OpenAI API key
jha config set OPENAI_KEY=sk-your-api-key-here

# Set preferred model (optional)
jha config set MODEL=gpt-4o-mini

# Set your shell (optional)
jha config set SHELL=bash
```

### Basic Commands
```bash
# Generate a command from natural language
jha "Move a folder with all its children to another location"

# Explain what a command does
jha explain "mv source_folder/ destination_folder/"

# Get explanation for the last generated command
jhax

# View command history
jha history

# Show the last query and command
jha last

# Check version
jha version
```

## Configuration
The configuration file is stored at `~/.jha/config.json` and all historical command stored at `~/.jha/history.json`


## Development Setup

1. Clone/Download the project: [https://github.com/jhaspider/jha-cli](https://github.com/jhaspider/jha-cli)

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install as CLI command:
```bash
pip install -e .
```

## Architecture

The project uses the following key dependencies:
- **Typer**: CLI framework for command parsing and routing
- **OpenAI Python SDK**: Integration with OpenAI's API
- **Click & Rich**: Terminal formatting and enhanced output
- **Pydantic**: Data validation and settings management

## Project Structure

```
jha-cli/
├── src/
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── cli.py                # Main CLI commands
│   ├── config.py             # Configuration management
│   ├── llm.py                # LLM integration
│   ├── history.py            # Command history tracking
│   └── utils.py              # Utility functions
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests on the [GitHub repository](https://github.com/jhaspider/jha-cli).

## License

MIT
