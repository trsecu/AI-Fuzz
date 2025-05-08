#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up AI-Fuzz...${NC}"

# Check Python version
python3 --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Check WhatWeb installation
echo -e "${YELLOW}Checking WhatWeb installation...${NC}"
if ! command -v whatweb &> /dev/null; then
    echo -e "${RED}WhatWeb is not installed.${NC}"
    echo -e "${YELLOW}Please install WhatWeb:${NC}"
    echo "Ubuntu/Debian: sudo apt-get install whatweb"
    echo "Fedora: sudo dnf install whatweb"
    echo "macOS: brew install whatweb"
    exit 1
fi

# Create default config if it doesn't exist
if [ ! -f config.json ]; then
    echo -e "${YELLOW}Creating default configuration...${NC}"
    cat > config.json << EOL
{
    "llm_provider": "gemini",
    "api_keys": {
        "gemini": "YOUR_GEMINI_API_KEY"
    },
    "fuzzing": {
        "max_paths": 20,
        "timeout": 5,
        "max_retries": 3,
        "concurrent_requests": 10,
        "user_agent": "AI-Fuzz/1.0"
    },
    "logging": {
        "level": "INFO",
        "file": "ai_fuzz.log"
    }
}
EOL
    echo -e "${YELLOW}Please update config.json with your Gemini API key${NC}"
fi

# Create results directory
mkdir -p results

echo -e "${GREEN}Setup completed!${NC}"
echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
echo "source venv/bin/activate"
echo -e "${YELLOW}To run the tool:${NC}"
echo "python main.py https://example.com"

git init
git add . 