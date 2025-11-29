# JHA - Just Help Assistant

For those - who still are not friend with CLI.

A powerful LLM-based CLI tool that helps you find and execute the right commands for your development workflows.


## Features

✨ **LLM-Powered Command Discovery**
- Query for suitable commands using natural language
- Get explanations for complex commands
- Support for multiple shells (bash, zsh, cmd, powershell)
- Command history tracking for quick re-execution

🔧 **Configuration Management**
- Simple config command to set OpenAI API key
- Choose your preferred LLM model
- Specify your shell
- Persistent configuration storage

📋 **Usage Examples**

```bash
# Check Installation
jha version
jha --help

# Setup your API key, MODEL & Shell
jha config set OPENAI_KEY=sk-xxx-yyy-zzz #Acquire & Set your OpenAI Key
jha config set MODEL=gpt-5-nano # Set your preferred model
jha config set SHELL=bash # Set the bash you are working on

# Find a command
jha "Move a folder with all its children to another location"

# Get explanation for last command
jhax

# Get explanation for any command
jha explain "<command-goes-here>"

# See all historical commands
jha history 
jha history clear

```

## Installation

### Prerequisites
- Python 3.8+
- pip or poetry

### Development Setup

1. Clone/Download the project

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

## Configuration

Configuration is stored in `~/.jha/config.json`


## Architecture

- **Typer**: CLI framework for argument parsing and command routing
- **OpenAI Python SDK**: LLM integration
- **Click**: Terminal formatting and colors
- **JSONSchema**: Configuration management

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
├── setup.py
├── requirements.txt
└── README.md
```

### Running locally
```bash
python -m jha "Your query here"
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT
