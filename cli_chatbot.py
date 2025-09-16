#!/usr/bin/env python3
"""
Neural Agent CLI Chatbot
A command-line interface for chatting with AI models using multiple providers.
Supports OpenAI, Anthropic, DeepSeek, and free APIs.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import configparser
from dataclasses import dataclass
import requests
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

@dataclass
class ChatConfig:
    """Configuration for the chatbot"""
    provider: str = "openrouter"  # Default to free OpenRouter
    model: str = "deepseek/deepseek-r1:free"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2000
    system_prompt: str = "You are a helpful AI assistant."

class APIClient:
    """Generic API client for different providers"""
    
    def __init__(self, config: ChatConfig):
        self.config = config
        self.session = requests.Session()
        self.setup_provider()
    
    def setup_provider(self):
        """Setup provider-specific configurations"""
        if self.config.provider == "openai":
            self.config.base_url = self.config.base_url or "https://api.openai.com/v1"
            self.config.model = self.config.model or "gpt-3.5-turbo"
            
        elif self.config.provider == "anthropic":
            self.config.base_url = self.config.base_url or "https://api.anthropic.com/v1"
            self.config.model = self.config.model or "claude-3-haiku-20240307"
            
        elif self.config.provider == "deepseek":
            self.config.base_url = self.config.base_url or "https://api.deepseek.com/v1"
            self.config.model = self.config.model or "deepseek-chat"
            
        elif self.config.provider == "openrouter":
            self.config.base_url = self.config.base_url or "https://openrouter.ai/api/v1"
            self.config.model = self.config.model or "deepseek/deepseek-r1:free"
            
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    def chat_completion(self, messages: list) -> Dict[str, Any]:
        """Send chat completion request"""
        headers = self._get_headers()
        
        if self.config.provider == "anthropic":
            return self._anthropic_request(messages, headers)
        else:
            return self._openai_compatible_request(messages, headers)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {"Content-Type": "application/json"}
        
        if self.config.provider == "anthropic":
            headers["x-api-key"] = self.config.api_key or ""
            headers["anthropic-version"] = "2023-06-01"
        elif self.config.provider == "openrouter":
            headers["Authorization"] = f"Bearer {self.config.api_key or ''}"
            headers["HTTP-Referer"] = "https://github.com/rmkenv/neuralagent"
            headers["X-Title"] = "Neural Agent CLI"
        else:
            headers["Authorization"] = f"Bearer {self.config.api_key or ''}"
        
        return headers
    
    def _anthropic_request(self, messages: list, headers: Dict[str, str]) -> Dict[str, Any]:
        """Handle Anthropic-specific request format"""
        # Convert messages format for Anthropic
        system_msg = None
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                user_messages.append(msg)
        
        payload = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": user_messages
        }
        
        if system_msg:
            payload["system"] = system_msg
        
        response = self.session.post(
            f"{self.config.base_url}/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")
        
        return response.json()
    
    def _openai_compatible_request(self, messages: list, headers: Dict[str, str]) -> Dict[str, Any]:
        """Handle OpenAI-compatible request format"""
        payload = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        response = self.session.post(
            f"{self.config.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")
        
        return response.json()

class ConfigManager:
    """Manage configuration from files and environment variables"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.neuralagent/config.ini")
        self.config_dir = Path(self.config_path).parent
        
    def load_config(self) -> ChatConfig:
        """Load configuration from file and environment variables"""
        config = ChatConfig()
        
        # Load from config file if it exists
        if os.path.exists(self.config_path):
            file_config = configparser.ConfigParser()
            file_config.read(self.config_path)
            
            if 'DEFAULT' in file_config:
                section = file_config['DEFAULT']
                config.provider = section.get('provider', config.provider)
                config.model = section.get('model', config.model)
                config.api_key = section.get('api_key', config.api_key)
                config.base_url = section.get('base_url', config.base_url)
                config.temperature = section.getfloat('temperature', config.temperature)
                config.max_tokens = section.getint('max_tokens', config.max_tokens)
                config.system_prompt = section.get('system_prompt', config.system_prompt)
        
        # Override with environment variables
        config.provider = os.getenv('NEURALAGENT_PROVIDER', config.provider)
        config.model = os.getenv('NEURALAGENT_MODEL', config.model)
        config.api_key = os.getenv('NEURALAGENT_API_KEY', config.api_key)
        config.base_url = os.getenv('NEURALAGENT_BASE_URL', config.base_url)
        
        if os.getenv('NEURALAGENT_TEMPERATURE'):
            config.temperature = float(os.getenv('NEURALAGENT_TEMPERATURE'))
        if os.getenv('NEURALAGENT_MAX_TOKENS'):
            config.max_tokens = int(os.getenv('NEURALAGENT_MAX_TOKENS'))
        if os.getenv('NEURALAGENT_SYSTEM_PROMPT'):
            config.system_prompt = os.getenv('NEURALAGENT_SYSTEM_PROMPT')
        
        # Provider-specific API key environment variables
        if not config.api_key:
            if config.provider == "openai":
                config.api_key = os.getenv('OPENAI_API_KEY')
            elif config.provider == "anthropic":
                config.api_key = os.getenv('ANTHROPIC_API_KEY')
            elif config.provider == "deepseek":
                config.api_key = os.getenv('DEEPSEEK_API_KEY')
            elif config.provider == "openrouter":
                config.api_key = os.getenv('OPENROUTER_API_KEY')
        
        return config
    
    def save_config(self, config: ChatConfig):
        """Save configuration to file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        file_config = configparser.ConfigParser()
        file_config['DEFAULT'] = {
            'provider': config.provider,
            'model': config.model,
            'temperature': str(config.temperature),
            'max_tokens': str(config.max_tokens),
            'system_prompt': config.system_prompt
        }
        
        if config.api_key:
            file_config['DEFAULT']['api_key'] = config.api_key
        if config.base_url:
            file_config['DEFAULT']['base_url'] = config.base_url
        
        with open(self.config_path, 'w') as f:
            file_config.write(f)
        
        print(f"Configuration saved to {self.config_path}")

class ChatBot:
    """Main chatbot class"""
    
    def __init__(self, config: ChatConfig):
        self.config = config
        self.client = APIClient(config)
        self.conversation_history = []
        
        # Add system message
        if config.system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": config.system_prompt
            })
    
    def chat(self, user_input: str) -> str:
        """Send a message and get response"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        try:
            # Get response from API
            response = self.client.chat_completion(self.conversation_history)
            
            # Extract assistant message
            if self.config.provider == "anthropic":
                assistant_message = response["content"][0]["text"]
            else:
                assistant_message = response["choices"][0]["message"]["content"]
            
            # Add assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history but keep system prompt"""
        system_messages = [msg for msg in self.conversation_history if msg["role"] == "system"]
        self.conversation_history = system_messages
    
    def save_conversation(self, filename: str):
        """Save conversation to file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"Conversation saved to {filename}")
    
    def load_conversation(self, filename: str):
        """Load conversation from file"""
        with open(filename, 'r') as f:
            self.conversation_history = json.load(f)
        print(f"Conversation loaded from {filename}")

def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🧠 Neural Agent CLI Chatbot")
    print("=" * 60)
    print("Type 'help' for commands, 'quit' or 'exit' to leave")
    print("=" * 60)

def print_help():
    """Print help message"""
    help_text = """
Available commands:
  help              - Show this help message
  clear             - Clear conversation history
  save <filename>   - Save conversation to file
  load <filename>   - Load conversation from file
  config            - Show current configuration
  set <key> <value> - Set configuration value
  quit/exit         - Exit the chatbot

Configuration keys:
  provider          - API provider (openai, anthropic, deepseek, openrouter)
  model             - Model name
  temperature       - Response randomness (0.0-2.0)
  max_tokens        - Maximum response length
  system_prompt     - System prompt for the AI

Examples:
  set provider openai
  set model gpt-4
  set temperature 0.5
  save my_conversation.json
"""
    print(help_text)

def interactive_mode(config: ChatConfig):
    """Run interactive chat mode"""
    chatbot = ChatBot(config)
    print_welcome()
    print(f"Using {config.provider} with model: {config.model}")
    
    if config.provider == "openrouter" and not config.api_key:
        print("💡 Using free OpenRouter API (no key required)")
        print("   For better rate limits, get a free API key at: https://openrouter.ai/")
    elif not config.api_key:
        print(f"⚠️  No API key found for {config.provider}")
        print("   Set your API key with environment variables or config file")
    
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye! 👋")
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'clear':
                chatbot.clear_history()
                print("Conversation history cleared.")
                continue
            
            elif user_input.lower() == 'config':
                print(f"Current configuration:")
                print(f"  Provider: {config.provider}")
                print(f"  Model: {config.model}")
                print(f"  Temperature: {config.temperature}")
                print(f"  Max tokens: {config.max_tokens}")
                print(f"  API key: {'Set' if config.api_key else 'Not set'}")
                continue
            
            elif user_input.lower().startswith('save '):
                filename = user_input[5:].strip()
                if filename:
                    chatbot.save_conversation(filename)
                else:
                    print("Please specify a filename")
                continue
            
            elif user_input.lower().startswith('load '):
                filename = user_input[5:].strip()
                if filename and os.path.exists(filename):
                    chatbot.load_conversation(filename)
                else:
                    print("File not found or no filename specified")
                continue
            
            elif user_input.lower().startswith('set '):
                parts = user_input[4:].strip().split(' ', 1)
                if len(parts) == 2:
                    key, value = parts
                    if key == 'provider':
                        config.provider = value
                        chatbot = ChatBot(config)  # Recreate with new provider
                        print(f"Provider set to: {value}")
                    elif key == 'model':
                        config.model = value
                        chatbot.config.model = value
                        print(f"Model set to: {value}")
                    elif key == 'temperature':
                        try:
                            config.temperature = float(value)
                            chatbot.config.temperature = config.temperature
                            print(f"Temperature set to: {value}")
                        except ValueError:
                            print("Temperature must be a number")
                    elif key == 'max_tokens':
                        try:
                            config.max_tokens = int(value)
                            chatbot.config.max_tokens = config.max_tokens
                            print(f"Max tokens set to: {value}")
                        except ValueError:
                            print("Max tokens must be an integer")
                    elif key == 'system_prompt':
                        config.system_prompt = value
                        chatbot = ChatBot(config)  # Recreate with new system prompt
                        print(f"System prompt updated")
                    else:
                        print(f"Unknown configuration key: {key}")
                else:
                    print("Usage: set <key> <value>")
                continue
            
            # Regular chat message
            print("AI: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Neural Agent CLI Chatbot - Chat with AI models via multiple providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Interactive mode with default settings
  %(prog)s --provider openai --model gpt-4   # Use OpenAI GPT-4
  %(prog)s --provider anthropic              # Use Anthropic Claude
  %(prog)s --config ~/.my_config.ini         # Use custom config file
  %(prog)s --setup                           # Setup configuration interactively

Environment Variables:
  NEURALAGENT_PROVIDER     # Default provider
  NEURALAGENT_MODEL        # Default model
  NEURALAGENT_API_KEY      # API key for any provider
  OPENAI_API_KEY           # OpenAI API key
  ANTHROPIC_API_KEY        # Anthropic API key
  DEEPSEEK_API_KEY         # DeepSeek API key
  OPENROUTER_API_KEY       # OpenRouter API key

Supported Providers:
  openrouter (default)     # Free tier available, multiple models
  openai                   # GPT models (requires API key)
  anthropic                # Claude models (requires API key)
  deepseek                 # DeepSeek models (requires API key)
        """
    )
    
    parser.add_argument('--provider', '-p', 
                       choices=['openai', 'anthropic', 'deepseek', 'openrouter'],
                       help='AI provider to use')
    parser.add_argument('--model', '-m', help='Model name to use')
    parser.add_argument('--api-key', '-k', help='API key')
    parser.add_argument('--temperature', '-t', type=float, help='Temperature (0.0-2.0)')
    parser.add_argument('--max-tokens', type=int, help='Maximum tokens in response')
    parser.add_argument('--system-prompt', '-s', help='System prompt')
    parser.add_argument('--config', '-c', help='Config file path')
    parser.add_argument('--setup', action='store_true', help='Setup configuration interactively')
    parser.add_argument('--version', action='version', version='Neural Agent CLI 1.0.0')
    
    args = parser.parse_args()
    
    # Load configuration
    config_manager = ConfigManager(args.config)
    config = config_manager.load_config()
    
    # Override with command line arguments
    if args.provider:
        config.provider = args.provider
    if args.model:
        config.model = args.model
    if args.api_key:
        config.api_key = args.api_key
    if args.temperature is not None:
        config.temperature = args.temperature
    if args.max_tokens:
        config.max_tokens = args.max_tokens
    if args.system_prompt:
        config.system_prompt = args.system_prompt
    
    # Setup mode
    if args.setup:
        print("🔧 Neural Agent CLI Setup")
        print("=" * 30)
        
        provider = input(f"Provider [{config.provider}]: ").strip() or config.provider
        model = input(f"Model [{config.model}]: ").strip() or config.model
        api_key = input(f"API Key [{'***' if config.api_key else 'none'}]: ").strip()
        if api_key:
            config.api_key = api_key
        
        temp_input = input(f"Temperature [{config.temperature}]: ").strip()
        if temp_input:
            try:
                config.temperature = float(temp_input)
            except ValueError:
                print("Invalid temperature, keeping current value")
        
        tokens_input = input(f"Max tokens [{config.max_tokens}]: ").strip()
        if tokens_input:
            try:
                config.max_tokens = int(tokens_input)
            except ValueError:
                print("Invalid max tokens, keeping current value")
        
        system_input = input(f"System prompt [{config.system_prompt[:50]}...]: ").strip()
        if system_input:
            config.system_prompt = system_input
        
        config.provider = provider
        config.model = model
        
        config_manager.save_config(config)
        print("\n✅ Configuration saved!")
        return
    
    # Start interactive mode
    try:
        interactive_mode(config)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
