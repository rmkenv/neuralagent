
# 🧠 Neural Agent CLI Chatbot

A powerful command-line interface for chatting with AI models from multiple providers including OpenAI, Anthropic, DeepSeek, and free APIs. Now featuring advanced **cognitive profiling** and **hybrid profile** functionality for personalized AI interactions.

## ✨ Features

### Core Chat Features
- **Multiple AI Providers**: Support for OpenAI, Anthropic, DeepSeek, and OpenRouter
- **Free AI Access**: Uses OpenRouter's free tier by default (no API key required)
- **Flexible Configuration**: Support for both config files and environment variables
- **Interactive Chat**: Full-featured CLI with conversation history
- **Conversation Management**: Save and load chat sessions
- **Real-time Configuration**: Change settings during chat sessions

### 🧠 Cognitive Profiling Features
- **Personality Assessment**: Interactive chat-based personality discovery
- **Problem-Solving Analysis**: Scenario-based cognitive assessment
- **Comprehensive Profiles**: Generate detailed cognitive profiles with traits, strengths, and biases
- **Hybrid Profiles**: Combine multiple profiles for specific use cases
- **Profile Management**: Save, load, and organize cognitive profiles
- **Personalized Chat**: Adapt AI responses based on your cognitive profile
- **Profile Analytics**: Track and analyze your cognitive patterns over time

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

3. Install additional dependencies for cognitive profiling:
```bash
pip install spacy textstat scikit-learn networkx
python -m spacy download en_core_web_sm
```

4. Run the chatbot:
```bash
python cli_chatbot.py
```

That's it! The chatbot will start using the free OpenRouter API by default.

## 🧠 Cognitive Profiling Quick Start

### Run Your First Assessment
```bash
# Start interactive assessment
python cli_chatbot.py --assess

# Or within the chat interface
You: assess
```

### Create a Hybrid Profile
```bash
# Create hybrid from two profiles
python cli_chatbot.py --create-hybrid PROFILE_001,PROFILE_002 0.6,0.4 leadership

# Or within chat
You: hybrid PROFILE_001,PROFILE_002 0.6,0.4 innovation
```

### Load a Profile for Personalized Chat
```bash
# Start chat with a specific profile
python cli_chatbot.py --load-profile PROFILE_20240916_143022

# Or within chat
You: load-profile PROFILE_20240916_143022
```

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

### Basic Chat Usage

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

### Cognitive Profiling Usage

```bash
# Run cognitive assessment
python cli_chatbot.py --assess

# List all profiles
python cli_chatbot.py --list-profiles

# Load specific profile for chat
python cli_chatbot.py --load-profile PROFILE_20240916_143022

# Create hybrid profile
python cli_chatbot.py --create-hybrid PROFILE_001,PROFILE_002 0.7,0.3 problem_solving

# Save assessment results
python cli_chatbot.py --assess --save-profile my_profile.json
```

### Interactive Commands

Once in the chat interface, you can use these commands:

#### Basic Commands
- `help` - Show available commands
- `clear` - Clear conversation history
- `save filename.json` - Save conversation to file
- `load filename.json` - Load conversation from file
- `config` - Show current configuration
- `set provider openai` - Change provider
- `set model gpt-4` - Change model
- `set temperature 0.5` - Change temperature
- `quit` or `exit` - Exit the chatbot

#### Cognitive Profiling Commands
- `assess` or `profile` - Run cognitive assessment
- `list-profiles` - List all saved profiles
- `load-profile <id>` - Load profile and adapt chat behavior
- `hybrid <ids> <weights> <use_case>` - Create hybrid profile
- `profile-stats` - Show profile statistics

#### Example Interactive Session
```
You: assess
[Runs cognitive assessment...]

You: list-profiles
[Shows available profiles...]

You: load-profile PROFILE_20240916_143022
✅ Chat adapted for profile: PROFILE_20240916_143022
Communication style: detailed_inquisitive
Learning preference: comprehensive

You: hybrid PROFILE_001,PROFILE_002 0.6,0.4 leadership
✅ Hybrid profile created: PROFILE_20240916_144530
🎯 Hybrid Signature: AN-HMH-LE

You: Tell me about machine learning
AI: [Provides response adapted to your cognitive profile...]
```

## 🧠 Understanding Cognitive Profiles

### Profile Components

Each cognitive profile includes:

- **Cognitive Traits**: Analytical, intuitive, creative, and systematic tendencies
- **Thinking Architecture**: How you process information and solve problems
- **Communication Style**: Your preferred interaction patterns
- **Decision-Making Profile**: How you approach decisions and risk
- **Strengths & Biases**: Your cognitive strengths and potential blind spots
- **Learning Preferences**: How you best absorb and process information

### Cognitive Signatures

Each profile gets a unique signature like `AN-HMH-LE`:
- **AN**: Primary thinking style (Analytical)
- **HMH**: Trait levels (High analytical, Medium intuitive, High creative)
- **LE**: Problem-solving approach (Leadership-oriented)

### Hybrid Profiles

Combine multiple profiles for specific use cases:
- **Leadership**: Balance analytical and interpersonal skills
- **Innovation**: Merge creative and systematic approaches
- **Problem-Solving**: Combine different thinking styles
- **Learning**: Adapt to different learning contexts

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
                      [--assess] [--save-profile SAVE_PROFILE] [--load-profile LOAD_PROFILE]
                      [--create-hybrid PROFILES WEIGHTS USE_CASE] [--list-profiles]

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

Cognitive Profiling Options:
  --assess              Run cognitive assessment
  --save-profile SAVE_PROFILE
                        Save current profile to file
  --load-profile LOAD_PROFILE
                        Load profile by ID
  --create-hybrid PROFILES WEIGHTS USE_CASE
                        Create hybrid profile: profile_ids weights use_case
  --list-profiles       List all profiles
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
- Try the cognitive assessment with `--assess`
- Experiment with different models to see which works best

### For Cognitive Profiling
- Take the assessment in a quiet environment for best results
- Be honest and detailed in your responses
- Try creating hybrid profiles for different contexts (work, learning, creativity)
- Load profiles before important conversations to get personalized responses
- Review your profile statistics periodically to track changes

### For Power Users
- Set up environment variables for seamless switching between providers
- Use config files for different use cases (coding, writing, analysis)
- Save important conversations with the `save` command
- Create specialized hybrid profiles for different domains
- Use profile backups for important cognitive data

### Rate Limiting
- Free tiers have rate limits - be patient between requests
- Consider upgrading to paid tiers for production use
- Use caching strategies for repeated queries

## 🛠️ Development

### Project Structure
```
neuralagent/
├── cli_chatbot.py                    # Main CLI application with profiling
├── src/                              # Cognitive profiling modules
│   ├── cognitive_assessment/
│   │   ├── __init__.py
│   │   └── chat_assessment.py        # Interactive assessment system
│   ├── cognitive_profiling/
│   │   ├── __init__.py
│   │   ├── cognitive_profiler.py     # Profile generation and hybridization
│   │   └── profile_manager.py        # Profile storage and management
│   ├── llm_integration/
│   └── cli_interface/
├── requirements.txt                  # Dependencies
├── README.md                        # This file
└── LICENSE                          # License file
```

### Key Components

#### Cognitive Assessment (`chat_assessment.py`)
- Interactive personality discovery through natural conversation
- Problem-solving scenario analysis
- Real-time response analysis using NLP
- Generates personality and problem-solving profiles

#### Cognitive Profiler (`cognitive_profiler.py`)
- Comprehensive profile generation from assessment data
- Hybrid profile creation and optimization
- Cognitive trait analysis and signature generation
- Compatibility assessment for profile mixing

#### Profile Manager (`profile_manager.py`)
- Profile storage and organization
- Profile search and compatibility matching
- Backup and restore functionality
- Export to multiple formats

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly (especially cognitive profiling features)
5. Submit a pull request

## 📊 Profile Data Storage

Profiles are stored in `~/.neuralagent/profiles/` with the following structure:

```
~/.neuralagent/
├── config.ini                       # Main configuration
└── profiles/
    ├── individual/                   # Individual cognitive profiles
    │   ├── PROFILE_20240916_143022.json
    │   └── PROFILE_20240916_144530.json
    ├── hybrid/                       # Hybrid profiles
    │   └── PROFILE_20240916_145030.json
    └── assessments/                  # Raw assessment data
        └── assessment_results_1726502400.json
```

## 🔒 Privacy and Data

- All cognitive profiles are stored locally on your machine
- No profile data is sent to external servers
- Assessment conversations are only used for profile generation
- You have full control over your cognitive data
- Profiles can be exported, backed up, and deleted at any time

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/rmkenv/neuralagent/issues)
- **Discussions**: Join discussions on [GitHub Discussions](https://github.com/rmkenv/neuralagent/discussions)

## 🔄 Migration from Streamlit

This project has been converted from a Streamlit web application to a CLI-only chatbot with enhanced cognitive profiling capabilities.

### Key Changes
- ✅ Removed all Streamlit dependencies
- ✅ Added CLI interface with argparse
- ✅ Added support for multiple AI providers
- ✅ Added configuration management
- ✅ Added conversation persistence
- ✅ Added free AI API as default
- ✅ **Enhanced cognitive profiling system**
- ✅ **Added hybrid profile functionality**
- ✅ **Added profile management and storage**
- ✅ **Added personalized AI interactions**

---

**Happy Chatting with Cognitive Intelligence! 🧠🚀**
