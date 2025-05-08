# AI-Fuzz

AI-Fuzz is an intelligent web path fuzzing tool that uses AI to generate relevant paths for security testing. It combines WhatWeb for technology detection and Google's Gemini AI for smart path generation.

## Features

- Technology detection using WhatWeb
- AI-powered path generation using Google's Gemini
- Concurrent URL fuzzing
- Detailed results with status codes
- JSON output for further analysis

## Prerequisites

- Python 3.8 or higher
- WhatWeb (for technology detection)
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-fuzz.git
cd ai-fuzz
```

2. Run the setup script:
```bash
./setup.sh
```

This will:
- Install required Python packages
- Check for WhatWeb installation
- Create a default configuration file

## Configuration

1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Update the configuration in `config.json`:
```json
{
    "api_keys": {
        "gemini": "YOUR_GEMINI_API_KEY"
    }
}
```

## Usage

Basic usage:
```bash
python main.py https://example.com
```

Save results to a specific directory:
```bash
python main.py https://example.com --output-dir custom_results
```

## Output

The tool generates:
- Console output with detected technologies and fuzzing results
- JSON file with detailed results in the specified output directory

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 