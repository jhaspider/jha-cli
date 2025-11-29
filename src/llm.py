import click
from openai import OpenAI, APIConnectionError, AuthenticationError
from typing import Optional

class LLMProvider:
    
    SHELL_DESCRIPTIONS = {
        "bash": "GNU Bash",
        "zsh": "Zsh shell",
        "fish": "Fish shell",
        "cmd": "Windows Command Prompt",
        "powershell": "Windows PowerShell",
        "sh": "POSIX shell",
    }
    
    def __init__(self, api_key: str, model: str, shell: str = "bash"):
        self.api_key = api_key
        self.model = model
        self.shell = shell
        self.client = None
        self._connect()
    
    def _connect(self) -> None:
        try:
            self.client = OpenAI(api_key=self.api_key)
            # Test connection
            # self.client.models.retrieve(self.model)
        except AuthenticationError:
            raise ValueError("Invalid OpenAI API key. Please check your configuration.")
        except APIConnectionError:
            raise ConnectionError("Failed to connect to OpenAI API.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {str(e)}")
    
    def generate_command(self, query: str) -> str:
        
        if not self.client:
            self._connect()
        
        shell_name = self.SHELL_DESCRIPTIONS.get(self.shell, self.shell)
        
        developer_message = """
        You are an expert command-line assistant helping developers find the right commands for their development tasks.

        When a user asks for a command:
        1. Provide the most appropriate command for their operating system/shell
        2. Be concise, just the command only, no additional details.
        3. For example : mv source_folder/ destination_folder/
        4. For example : rm -rf folder_name/

        Always respond with only the command - no extra commentary."""
        
        user_message = f"For {shell_name}, provide a command to: {query}"
        
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "developer", "content": developer_message},
                    {"role": "user", "content": user_message}
                ],
                text={
                    "format": {
                        "type": "text"
                    },
                    "verbosity": "low"
                },
                reasoning={
                    "effort": "low"
                },
                store=False
            )
            
            return response.output_text.strip()
        
        except AuthenticationError:
            raise ValueError("OpenAI API authentication failed. Check your API key.")
        except APIConnectionError:
            raise ConnectionError("Failed to connect to OpenAI API.")
        except Exception as e:
            raise RuntimeError(f"LLM error: {str(e)}")
    
    def explain_command(self, command: str) -> str:
        if not self.client:
            self._connect()
        
        developer_message = """
        You are an expert command-line assistant helping developers find the right commands for their development tasks.
        
        When explaining a command:
        1. Break down what each part does
        2. Explain important flags
        3. Provide context about when to use it

        Only the explanation with respect to the command - no extra commentary."""
        
        user_message = f"Explain this command in detail: {command}"
        
        try:
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "developer", "content": developer_message},
                    {"role": "user", "content": user_message}
                ],
                text={
                    "format": {
                        "type": "text"
                    },
                    "verbosity": "low"
                },
                reasoning={
                    "effort": "low"
                },
                store=False
            )
            
            return response.output_text.strip()
        
        
        
        except AuthenticationError:
            raise ValueError("OpenAI API authentication failed. Check your API key.")
        except APIConnectionError:
            raise ConnectionError("Failed to connect to OpenAI API.")
        except Exception as e:
            raise RuntimeError(f"LLM error: {str(e)}")


def get_llm(config) -> LLMProvider:
    """Get LLM provider instance with validation."""
    api_key = config.get("OPENAI_KEY")
    
    if not api_key:
        click.echo(click.style(
            "❌ OpenAI API key not configured.\n"
            "Set it using: jha config set OPENAI_KEY=your-key",
            fg="red"
        ))
        raise SystemExit(1)
    
    model = config.get("MODEL")
    shell = config.get("SHELL")
    
    try:
        return LLMProvider(api_key, model, shell)
    except ValueError as e:
        click.echo(click.style(f"❌ {str(e)}", fg="red"))
        raise SystemExit(1)
    except ConnectionError as e:
        click.echo(click.style(f"❌ {str(e)}", fg="red"))
        raise SystemExit(1)
    except RuntimeError as e:
        click.echo(click.style(f"❌ {str(e)}", fg="red"))
        raise SystemExit(1)
