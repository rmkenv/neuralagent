# 🧠 Neural Agent CLI Chatbot

A powerful command-line interface for chatting with AI models from multiple providers including OpenAI, Anthropic, DeepSeek, and free APIs.

## ✨ Features

- **Multiple AI Providers**: Support for OpenAI, Anthropic, DeepSeek, and OpenRouter
- **Free AI Access**: Uses OpenRouter's free tier by default (no API key required)
- **Flexible Configuration**: Support for both config files and environment variables
- **Interactive Chat**: Full-featured CLI with conversation history
- **Conversation Management**: Save and load chat sessions
- **Real-time Configuration**: Change settings during chat sessions
- **Error Handling**: Robust error handling with helpful messages

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rmkenv/neuralagent.git
cd neuralagent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the chatbot:
```bash
python cli_chatbot.py
```

That's it! The chatbot will start using the free OpenRouter API by default.

## 🔧 Configuration

### Environment Variables

Set these environment variables for easy configuration:

```bash
# General configuration
export NEURALAGENT_PROVIDER=openrouter
export NEURALAGENT_MODEL=deepseek/deepseek-r1:free
export NEURALAGENT_API_KEY=your_api_key_here

# Provider-specific API keys
export OPENAI_API_KEY=your_openai_key
export ANTHROPIC_API_KEY=your_anthropic_key
export DEEPSEEK_API_KEY=your_deepseek_key
export OPENROUTER_API_KEY=your_openrouter_key

# Optional settings
export NEURALAGENT_TEMPERATURE=0.7
export NEURALAGENT_MAX_TOKENS=2000
export NEURALAGENT_SYSTEM_PROMPT="You are a helpful AI assistant."
```

### Configuration File

Create a config file at `~/.neuralagent/config.ini`:

```ini
[DEFAULT]
provider = openrouter
model = deepseek/deepseek-r1:free
api_key = your_api_key_here
temperature = 0.7
max_tokens = 2000
system_prompt = You are a helpful AI assistant.
```

### Interactive Setup

Run the setup wizard:

```bash
python cli_chatbot.py --setup
```

## 🎯 Usage Examples

### Basic Usage

```bash
# Start with default settings (free OpenRouter)
python cli_chatbot.py

# Use OpenAI GPT-4
python cli_chatbot.py --provider openai --model gpt-4

# Use Anthropic Claude
python cli_chatbot.py --provider anthropic --model claude-3-haiku-20240307

# Use custom temperature
python cli_chatbot.py --temperature 0.3

# Use custom config file
python cli_chatbot.py --config /path/to/config.ini
```

### Interactive Commands

Once in the chat interface, you can use these commands:

- `help` - Show available commands
- `clear` - Clear conversation history
- `save filename.json` - Save conversation to file
- `load filename.json` - Load conversation from file
- `config` - Show current configuration
- `set provider openai` - Change provider
- `set model gpt-4` - Change model
- `set temperature 0.5` - Change temperature
- `quit` or `exit` - Exit the chatbot

## 🌐 Supported Providers

### OpenRouter (Default - Free)
- **Models**: DeepSeek R1, DeepSeek V3, Gemma, and more
- **Free Tier**: 20 requests/minute, 50 requests/day (no API key required)
- **Upgrade**: Get API key at [openrouter.ai](https://openrouter.ai) for higher limits
- **Best For**: Getting started, experimentation, cost-free usage

### OpenAI
- **Models**: GPT-4, GPT-3.5-turbo, GPT-4-turbo
- **API Key**: Required (get from [platform.openai.com](https://platform.openai.com))
- **Best For**: High-quality responses, production use

### Anthropic
- **Models**: Claude-3 Haiku, Claude-3 Sonnet, Claude-3 Opus
- **API Key**: Required (get from [console.anthropic.com](https://console.anthropic.com))
- **Best For**: Long conversations, analysis, safety-focused responses

### DeepSeek
- **Models**: DeepSeek Chat, DeepSeek Coder
- **API Key**: Required (get from [platform.deepseek.com](https://platform.deepseek.com))
- **Best For**: Coding assistance, technical discussions

## 📋 Command Line Options

```
usage: cli_chatbot.py [-h] [--provider {openai,anthropic,deepseek,openrouter}]
                      [--model MODEL] [--api-key API_KEY] [--temperature TEMPERATURE]
                      [--max-tokens MAX_TOKENS] [--system-prompt SYSTEM_PROMPT]
                      [--config CONFIG] [--setup] [--version]

Neural Agent CLI Chatbot - Chat with AI models via multiple providers

options:
  -h, --help            show this help message and exit
  --provider {openai,anthropic,deepseek,openrouter}, -p {openai,anthropic,deepseek,openrouter}
                        AI provider to use
  --model MODEL, -m MODEL
                        Model name to use
  --api-key API_KEY, -k API_KEY
                        API key
  --temperature TEMPERATURE, -t TEMPERATURE
                        Temperature (0.0-2.0)
  --max-tokens MAX_TOKENS
                        Maximum tokens in response
  --system-prompt SYSTEM_PROMPT, -s SYSTEM_PROMPT
                        System prompt
  --config CONFIG, -c CONFIG
                        Config file path
  --setup               Setup configuration interactively
  --version             show program's version number and exit
```

## 🔑 Getting API Keys

### Free Option (Recommended for beginners)
- **OpenRouter**: No API key required for free tier
- **Limits**: 20 requests/minute, 50 requests/day
- **Models**: DeepSeek R1, DeepSeek V3, and other free models

### Paid Options

#### OpenAI
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up and add billing information
3. Create an API key in the API section
4. Set `OPENAI_API_KEY` environment variable

#### Anthropic
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up and add billing information
3. Create an API key
4. Set `ANTHROPIC_API_KEY` environment variable

#### DeepSeek
1. Go to [platform.deepseek.com](https://platform.deepseek.com)
2. Sign up and add billing information
3. Create an API key
4. Set `DEEPSEEK_API_KEY` environment variable

#### OpenRouter (Paid Tier)
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up and add credits
3. Create an API key
4. Set `OPENROUTER_API_KEY` environment variable

## 💡 Tips and Best Practices

### For Beginners
- Start with the default OpenRouter free tier
- Use the `--setup` command to configure interactively
- Try different models to see which works best for your needs

### For Power Users
- Set up environment variables for seamless switching between providers
- Use config files for different use cases (coding, writing, analysis)
- Save important conversations with the `save` command

### Rate Limiting
- Free tiers have rate limits - be patient between requests
- Consider upgrading to paid tiers for production use
- Use caching strategies for repeated queries

## 🛠️ Development

### Project Structure
```
neuralagent/
├── cli_chatbot.py          # Main CLI application
├── src/                    # Original cognitive profiling modules
│   ├── cognitive_assessment/
│   ├── cognitive_profiling/
│   ├── llm_integration/
│   └── cli_interface/
├── requirements.txt        # Dependencies
├── README.md              # This file
└── LICENSE                # License file
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/rmkenv/neuralagent/issues)
- **Discussions**: Join discussions on [GitHub Discussions](https://github.com/rmkenv/neuralagent/discussions)

## 🔄 Migration from Streamlit

This project has been converted from a Streamlit web application to a CLI-only chatbot. The original cognitive profiling functionality is preserved in the `src/` directory and can still be used programmatically.

### Key Changes
- ✅ Removed all Streamlit dependencies
- ✅ Added CLI interface with argparse
- ✅ Added support for multiple AI providers
- ✅ Added configuration management
- ✅ Added conversation persistence
- ✅ Added free AI API as default

---

**Happy Chatting! 🚀**
