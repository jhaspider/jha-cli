# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-30

### Added
- Initial release of JHA CLI
- LLM-powered command discovery using natural language queries
- Configuration management for OpenAI API keys and models
- Command history tracking and replay functionality
- Support for multiple shells (bash, zsh, cmd, powershell)
- CLI commands: query, explain, config, history, last
- Two entry points: `jha` (main tool) and `jhax` (last command explanation)

### Features
- Natural language to shell command translation
- Command explanation capabilities
- Persistent configuration storage in `~/.jha/config.json`
- Command history storage and management
- Cross-platform clipboard integration
- Rich terminal output formatting

### Dependencies
- OpenAI Python SDK for LLM integration
- Typer for CLI framework
- Click for terminal formatting
- Rich for enhanced output
- Pydantic for data validation