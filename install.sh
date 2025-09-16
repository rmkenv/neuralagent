#!/bin/bash

# Neural Agent CLI Installation Script
# This script installs the Neural Agent CLI chatbot

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧠 Neural Agent CLI Installation${NC}"
echo "=================================="

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python not found. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

# Check if pip is available
echo -e "\n${YELLOW}Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo -e "${RED}❌ pip not found. Please install pip.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip found${NC}"

# Install core dependencies only
echo -e "\n${YELLOW}Installing core dependencies...${NC}"
$PIP_CMD install requests python-dotenv configparser

echo -e "${GREEN}✅ Core dependencies installed${NC}"

# Make CLI executable
echo -e "\n${YELLOW}Setting up CLI...${NC}"
chmod +x cli_chatbot.py
echo -e "${GREEN}✅ CLI script made executable${NC}"

# Test installation
echo -e "\n${YELLOW}Testing installation...${NC}"
if $PYTHON_CMD cli_chatbot.py --version &> /dev/null; then
    echo -e "${GREEN}✅ Installation successful!${NC}"
else
    echo -e "${RED}❌ Installation test failed${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 Neural Agent CLI is ready to use!${NC}"
echo -e "\n${BLUE}Quick start:${NC}"
echo -e "  ${PYTHON_CMD} cli_chatbot.py                    # Start chatting (free)"
echo -e "  ${PYTHON_CMD} cli_chatbot.py --setup           # Configure settings"
echo -e "  ${PYTHON_CMD} cli_chatbot.py --help            # Show all options"
echo -e "\n${BLUE}For full features, install all dependencies:${NC}"
echo -e "  ${PIP_CMD} install -r requirements.txt"
echo -e "\n${YELLOW}Note: The chatbot uses free OpenRouter API by default.${NC}"
echo -e "${YELLOW}No API key required to get started!${NC}"
