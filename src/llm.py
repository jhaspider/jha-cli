import click
from openai import OpenAI, APIConnectionError, AuthenticationError, RateLimitError, APIStatusError
from typing import Optional
from .utils import display_error, display_command, display_success

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
            self.client.models.retrieve(self.model)
        except AuthenticationError:
            raise ValueError("Invalid OpenAI API key. Please check your configuration.")
        except APIConnectionError:
            raise ConnectionError("Failed to connect to OpenAI API.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LLM: {str(e)}")
    
    def generate_command(self, query: str) -> str:
        
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
        
        openai_response = self.openai_response(developer_message, user_message)
        return openai_response
    
    def explain_command(self, command: str) -> str:
        
        developer_message = """
        You are an expert command-line assistant helping developers find the right commands for their development tasks.
        
        When explaining a command:
        1. Break down what each part does
        2. Explain important flags
        3. Provide context about when to use it

        Only the explanation with respect to the command - no extra commentary."""
        
        user_message = f"Explain this command in detail: {command}"
        
        openai_response = self.openai_response(developer_message, user_message)
        return openai_response
        
    def openai_response(self, developer_message: str, user_message: str, **options) -> str:
        if not self.client:
            self._connect()
        
        messages = [
            {"role": "developer", "content": developer_message},
            {"role": "user", "content": user_message},
        ]

        args = {
            "model": self.model,
            "input": messages,
            "store": options.pop("store", False),
            "max_output_tokens": options.pop("max_output_tokens", 300),
            "text": {"format": {"type": "text"}},
        }

        args.update(options)

        try:
            response = self.client.responses.create(**args)
            # print(f"Total tokens used: {response.usage.total_tokens}")
            return response.output_text.strip()

        except AuthenticationError as e:
            raise ValueError("OpenAI API authentication failed. Check your API key.") from e
        except RateLimitError as e:
            raise RuntimeError("OpenAI rate limit hit. Slow down or upgrade your plan.") from e
        except APIConnectionError as e:
            raise ConnectionError("Failed to connect to OpenAI API.") from e
        except APIStatusError as e:
            raise RuntimeError(f"OpenAI API error {e.status_code}: {e.message}") from e
        except Exception as e:
            raise RuntimeError(f"LLM error: {str(e)}") from e

def get_llm(config) -> LLMProvider:
    api_key = config.get("OPENAI_KEY")
    if not api_key:
        click.echo(display_error(
            "OpenAI API key not configured.\n"
            "Set it using: jha config set OPENAI_KEY=your-key"
        ))
        raise SystemExit(1)
    
    model = config.get("MODEL")
    shell = config.get("SHELL")
    
    try:
        return LLMProvider(api_key, model, shell)
    except ValueError as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        raise SystemExit(1)
    except ConnectionError as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        raise SystemExit(1)
    except RuntimeError as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        raise SystemExit(1)
