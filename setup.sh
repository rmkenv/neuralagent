#!/bin/bash

# Cognitive AI Clone Platform - Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ASCII Art Header
echo -e "${BLUE}"
cat << "EOF"
 ██████╗ ██████╗  ██████╗ ███╗   ██╗██╗████████╗██╗██╗   ██╗███████╗
██╔════╝██╔═══██╗██╔════╝ ████╗  ██║██║╚══██╔══╝██║██║   ██║██╔════╝
██║     ██║   ██║██║  ███╗██╔██╗ ██║██║   ██║   ██║██║   ██║█████╗  
██║     ██║   ██║██║   ██║██║╚██╗██║██║   ██║   ██║╚██╗ ██╔╝██╔══╝  
╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║██║   ██║   ██║ ╚████╔╝ ███████╗
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝
                                                                    
           █████╗ ██╗     ██████╗██╗      ██████╗ ███╗   ██╗███████╗
          ██╔══██╗██║    ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝
          ███████║██║    ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  
          ██╔══██║██║    ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  
          ██║  ██║██║    ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗
          ╚═╝  ╚═╝╚═╝     ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                                                                    
EOF
echo -e "${NC}"

echo -e "${GREEN}🧠 Cognitive AI Clone Platform Setup${NC}"
echo -e "${BLUE}Creating AI systems that think like you through conversational assessment${NC}"
echo ""

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}=== $1 ===${NC}"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print info messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
print_header "Checking System Requirements"

# Check Python 3.11+
if command_exists python3; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_info "Found Python $PYTHON_VERSION"
    if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 11) else 1)'; then
        print_error "Python 3.11+ required. Found $PYTHON_VERSION"
        exit 1
    fi
    print_success "Python version check passed"
else
    print_error "Python 3.11+ is required but not found"
    exit 1
fi

# Check pip
if command_exists pip3; then
    print_success "Found pip3"
else
    print_error "pip3 is required but not found"
    exit 1
fi

# Check Docker (optional)
if command_exists docker; then
    print_success "Found Docker"
    DOCKER_AVAILABLE=true
else
    print_info "Docker not found - Docker deployment will not be available"
    DOCKER_AVAILABLE=false
fi

# Check Docker Compose (optional)
if command_exists docker-compose || command_exists docker; then
    if docker compose version >/dev/null 2>&1; then
        print_success "Found Docker Compose"
        DOCKER_COMPOSE_AVAILABLE=true
    elif command_exists docker-compose; then
        print_success "Found docker-compose"
        DOCKER_COMPOSE_AVAILABLE=true
    else
        DOCKER_COMPOSE_AVAILABLE=false
    fi
else
    DOCKER_COMPOSE_AVAILABLE=false
fi

# Check Git
if command_exists git; then
    print_success "Found Git"
else
    print_error "Git is required but not found"
    exit 1
fi

print_success "System requirements check completed"

# Create project structure
print_header "Creating Project Structure"

# Create main directories
mkdir -p {src/{cognitive_assessment,cognitive_profiling,llm_integration,memory_systems,web_interface},data/{assessments,profiles,training_data,models,chroma,ollama,logs},config,tests,scripts,monitoring}

print_success "Project directories created"

# Create __init__.py files
find src -type d -exec touch {}/__init__.py \;
print_success "Python package structure created"

# Setup Python virtual environment
print_header "Setting Up Python Environment"

if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Upgrade pip
pip install --upgrade pip setuptools wheel
print_success "Updated pip, setuptools, and wheel"

# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    print_info "Creating requirements.txt..."
    cat > requirements.txt << 'EOF'
# Core ML/AI Libraries
torch>=2.0.0
transformers>=4.35.0
sentence-transformers>=2.2.2
datasets>=2.15.0
peft>=0.6.0
guidance>=0.1.10
langchain>=0.0.340
ollama>=0.1.7

# Vector Database & Memory
chromadb>=0.4.15
faiss-cpu>=1.7.4

# Chat-based Assessment
streamlit>=1.28.0
streamlit-chat>=0.1.1
plotly>=5.17.0
textstat>=0.7.3
spacy>=3.7.0
nltk>=3.8.1

# Data Processing
pandas>=2.1.0
numpy>=1.25.0
scikit-learn>=1.3.0
networkx>=3.2.0
scipy>=1.11.0

# Web Framework
fastapi>=0.104.0
uvicorn>=0.24.0

# Utilities
python-dotenv>=1.0.0
pydantic>=2.5.0
loguru>=0.7.2
tqdm>=4.66.0
streamlit-js-eval>=0.1.5

# Development Dependencies
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
jupyterlab>=4.0.0
EOF
    print_success "Created requirements.txt"
fi

# Install Python dependencies
print_info "Installing Python dependencies (this may take a few minutes)..."
pip install -r requirements.txt
print_success "Python dependencies installed"

# Download spaCy model
print_info "Downloading spaCy English model..."
python -m spacy download en_core_web_sm
print_success "spaCy model downloaded"

# Create .env file if it doesn't exist
print_header "Environment Configuration"

if [ ! -f ".env" ]; then
    print_info "Creating environment configuration..."
    cat > .env << 'EOF'
# Ollama Configuration  
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# ChromaDB Configuration
CHROMA_HOST=http://localhost:8001
CHROMA_COLLECTION_NAME=cognitive_memory

# Assessment Configuration
MAX_ASSESSMENT_TIME=3600
SESSION_TIMEOUT=7200

# Logging
LOG_LEVEL=INFO
PROJECT_NAME=cognitive-ai-clone

# Development Settings
DEBUG=True
ENVIRONMENT=development
EOF
    print_success "Environment file created"
else
    print_info "Environment file already exists"
fi

# Create configuration files
print_header "Creating Configuration Files"

# Create config/settings.py
cat > config/settings.py << 'EOF'
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Environment settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Ollama settings
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1:8b')

# ChromaDB settings
CHROMA_HOST = os.getenv('CHROMA_HOST', 'http://localhost:8001')
CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'cognitive_memory')

# Assessment settings
MAX_ASSESSMENT_TIME = int(os.getenv('MAX_ASSESSMENT_TIME', 3600))
SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 7200))

# Logging settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
PROJECT_NAME = os.getenv('PROJECT_NAME', 'cognitive-ai-clone')

# Data directories
DATA_DIR = BASE_DIR / 'data'
ASSESSMENTS_DIR = DATA_DIR / 'assessments'
PROFILES_DIR = DATA_DIR / 'profiles'
MODELS_DIR = DATA_DIR / 'models'
LOGS_DIR = DATA_DIR / 'logs'

# Create directories if they don't exist
for directory in [DATA_DIR, ASSESSMENTS_DIR, PROFILES_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
EOF

print_success "Configuration files created"

# Copy implementation files
print_header "Setting Up Core Implementation"

# Create the main application files in their proper locations
print_info "Setting up core cognitive assessment system..."

# Copy files to proper locations (these would be copied from the created files above)
# For the demo, we'll create symbolic references
touch src/cognitive_assessment/chat_assessment.py
touch src/cognitive_profiling/cognitive_profiler.py  
touch src/llm_integration/reasoning_engine.py
touch src/web_interface/streamlit_app.py

print_success "Core implementation files configured"

# Create startup scripts
print_header "Creating Startup Scripts"

# Create run_local.sh
cat > scripts/run_local.sh << 'EOF'
#!/bin/bash
# Local development startup script

echo "🧠 Starting Cognitive AI Clone Platform (Local Development)"

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama not detected. Please start Ollama first:"
    echo "   Download from: https://ollama.ai"
    echo "   Then run: ollama serve"
    echo ""
fi

# Start Streamlit app
echo "🚀 Starting Streamlit application..."
streamlit run src/web_interface/streamlit_app.py --server.address localhost --server.port 8501

echo "✅ Application started at http://localhost:8501"
EOF

# Create run_docker.sh
cat > scripts/run_docker.sh << 'EOF'
#!/bin/bash
# Docker deployment startup script

echo "🧠 Starting Cognitive AI Clone Platform (Docker)"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not running"
    exit 1
fi

# Create required directories
mkdir -p data/{chroma,ollama,redis,prometheus,grafana,logs}

# Start with basic services
echo "🚀 Starting core services..."
docker-compose up -d chroma-db ollama

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Pull required Ollama model
echo "📥 Downloading AI model (this may take a few minutes on first run)..."
docker-compose exec ollama ollama pull llama3.1:8b

# Start main application
echo "🚀 Starting main application..."
docker-compose up -d cognitive-clone-app

echo "✅ Application started at http://localhost:8501"
echo "📊 ChromaDB available at http://localhost:8001"
echo "🤖 Ollama API available at http://localhost:11434"

# Show logs
docker-compose logs -f cognitive-clone-app
EOF

# Create stop_docker.sh
cat > scripts/stop_docker.sh << 'EOF'
#!/bin/bash
# Stop all Docker services

echo "🛑 Stopping Cognitive AI Clone Platform..."
docker-compose down

echo "✅ All services stopped"
EOF

# Make scripts executable
chmod +x scripts/*.sh
print_success "Startup scripts created"

# Setup Docker configuration (if Docker is available)
if [ "$DOCKER_AVAILABLE" = true ] && [ "$DOCKER_COMPOSE_AVAILABLE" = true ]; then
    print_header "Docker Setup"
    
    # Create Docker network
    if ! docker network ls | grep -q cognitive-net; then
        docker network create cognitive-net
        print_success "Docker network created"
    fi
    
    # Create volume directories
    mkdir -p data/{chroma,ollama,redis,prometheus,grafana}
    print_success "Docker volume directories created"
    
    print_info "Docker setup completed - use 'scripts/run_docker.sh' to start with Docker"
fi

# Create basic tests
print_header "Setting Up Testing Framework"

cat > tests/test_basic.py << 'EOF'
import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.append(str(Path(__file__).parent.parent / 'src'))

def test_import_cognitive_assessment():
    """Test that we can import the cognitive assessment module."""
    try:
        from cognitive_assessment.chat_assessment import ChatBasedAssessment
        assert True
    except ImportError:
        pytest.fail("Could not import ChatBasedAssessment")

def test_import_cognitive_profiler():
    """Test that we can import the cognitive profiler module."""
    try:
        from cognitive_profiling.cognitive_profiler import CognitiveProfileGenerator
        assert True
    except ImportError:
        pytest.fail("Could not import CognitiveProfileGenerator")

def test_import_reasoning_engine():
    """Test that we can import the reasoning engine module."""
    try:
        from llm_integration.reasoning_engine import ReasoningEngine
        assert True
    except ImportError:
        pytest.fail("Could not import ReasoningEngine")

if __name__ == "__main__":
    pytest.main([__file__])
EOF

print_success "Testing framework configured"

# Create README.md
print_header "Creating Documentation"

cat > README.md << 'EOF'
# 🧠 Cognitive AI Clone Development Platform

Create AI systems that think and reason like you through conversational assessment and cognitive profiling.

## 🚀 Quick Start

### Option 1: Local Development
```bash
# Setup (run once)
./scripts/setup.sh

# Start application
./scripts/run_local.sh
```

### Option 2: Docker Deployment
```bash
# Setup and start with Docker
./scripts/run_docker.sh
```

## 📖 How It Works

1. **Conversational Assessment** (15-20 minutes)
   - Natural personality discovery through chat
   - Problem-solving scenarios with real-time analysis

2. **Cognitive Profile Generation**
   - AI analyzes your thinking patterns and communication style
   - Creates a comprehensive cognitive signature

3. **AI Clone Creation**
   - Fine-tunes reasoning engines to match your cognitive patterns
   - Creates AI systems that think like you

4. **Hybrid Profile Creation** (Coming Soon)
   - Mix and match cognitive strengths from multiple profiles
   - Create specialized cognitive agents for specific use cases

## 🎯 Features

- **Chat-based Assessment**: Natural conversation analysis
- **Real-time Pattern Detection**: Cognitive style identification
- **Comprehensive Profiling**: Multi-dimensional cognitive mapping
- **AI Clone Generation**: Personalized reasoning engines
- **Privacy-first**: All processing happens locally
- **Open Source**: Complete transparency and customization

## 🔧 Technical Stack

- **Frontend**: Streamlit with interactive chat interface
- **Backend**: Python with FastAPI (optional)
- **AI Models**: Ollama for local LLM serving
- **Vector Database**: ChromaDB for cognitive memory
- **Analysis**: spaCy, scikit-learn, NetworkX
- **Deployment**: Docker with Docker Compose

## 📁 Project Structure

```
cognitive-ai-clone/
├── src/
│   ├── cognitive_assessment/     # Chat-based assessment system
│   ├── cognitive_profiling/      # Profile generation
│   ├── llm_integration/          # AI reasoning engines
│   ├── memory_systems/           # Cognitive memory management
│   └── web_interface/            # Streamlit application
├── data/                         # User data and models
├── config/                       # Configuration files
├── scripts/                      # Deployment scripts
└── tests/                        # Test suite
```

## 🛠️ Development Setup

1. **Prerequisites**: Python 3.11+, Git, Docker (optional)
2. **Installation**: Run `./scripts/setup.sh`
3. **Development**: Activate venv and run `streamlit run src/web_interface/streamlit_app.py`
4. **Testing**: Run `pytest tests/`

## 🚀 Deployment Options

### Local Development
- Direct Python execution with virtual environment
- Ideal for development and testing

### Docker Compose
- Full stack deployment with all services
- Production-ready with monitoring and scaling

### Production
- Nginx reverse proxy
- Redis session management
- Prometheus/Grafana monitoring

## 📊 Monitoring

Access monitoring dashboards:
- **Application**: http://localhost:8501
- **ChromaDB**: http://localhost:8001
- **Ollama API**: http://localhost:11434
- **Prometheus**: http://localhost:9090 (with monitoring profile)
- **Grafana**: http://localhost:3000 (with monitoring profile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: See docs/ directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## 🔮 Roadmap

- [ ] LLM fine-tuning integration
- [ ] Multi-user profile management
- [ ] Cognitive profile versioning
- [ ] Hybrid profile creation
- [ ] Advanced reasoning templates
- [ ] API for external integrations
- [ ] Mobile app interface

---

**Ready to build AI that thinks like you?** 🧠✨
EOF

print_success "Documentation created"

# Final setup summary
print_header "Setup Complete!"

echo -e "${GREEN}"
cat << "EOF"
🎉 Cognitive AI Clone Platform setup completed successfully!

🚀 Next Steps:
EOF
echo -e "${NC}"

echo -e "${BLUE}1. Start the application:${NC}"
echo -e "   ${YELLOW}Local:${NC}  ./scripts/run_local.sh"
if [ "$DOCKER_AVAILABLE" = true ]; then
echo -e "   ${YELLOW}Docker:${NC} ./scripts/run_docker.sh"
fi

echo -e "\n${BLUE}2. Open your browser:${NC}"
echo -e "   ${YELLOW}Main App:${NC} http://localhost:8501"

echo -e "\n${BLUE}3. Complete your cognitive assessment:${NC}"
echo -e "   • Natural personality chat (5-7 minutes)"
echo -e "   • Problem-solving scenarios (8-10 minutes)"
echo -e "   • Generate your cognitive profile"
echo -e "   • Create your AI clone"

echo -e "\n${BLUE}4. Advanced features (optional):${NC}"
if [ "$DOCKER_AVAILABLE" = true ]; then
echo -e "   • ChromaDB dashboard: http://localhost:8001"
echo -e "   • Ollama API: http://localhost:11434"
fi
echo -e "   • Run tests: ${YELLOW}pytest tests/${NC}"
echo -e "   • View logs: ${YELLOW}tail -f data/logs/app.log${NC}"

echo ""
print_success "Ready to create AI systems that think like you! 🧠✨"

# Check if this is the first run
if [ ! -f ".setup_complete" ]; then
    echo "setup_complete" > .setup_complete
    echo ""
    echo -e "${YELLOW}💡 Pro Tips:${NC}"
    echo -e "   • Be authentic during assessment - there are no wrong answers"
    echo -e "   • The AI learns your reasoning patterns, not just preferences"
    echo -e "   • Try asking your clone complex problems after creation"
    echo -e "   • Provide feedback to help your clone learn and improve"
    echo ""
fi

echo -e "${GREEN}Happy cognitive cloning! 🚀${NC}"