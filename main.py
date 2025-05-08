import argparse
import asyncio
import logging
from rich.console import Console
from rich.panel import Panel
from typing import List
import os
from datetime import datetime
import json

from tech_detect import TechnologyDetector
from ai_engine import AIFuzz, load_config
from fuzzer import Fuzzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI-Fuzz: AI-powered web path fuzzer')
    parser.add_argument('url', help='Target URL to fuzz')
    parser.add_argument('--output-dir', default='results', help='Directory to save results')
    args = parser.parse_args()

    # Load configuration
    config = load_config()
    
    # Initialize components
    tech_detector = TechnologyDetector()
    ai_fuzz = AIFuzz(api_key=config['api_keys']['gemini'])
    fuzzer = Fuzzer(config)
    
    try:
        # Step 1: Technology Detection
        console.print(Panel.fit(
            "[bold cyan]Step 1: Technology Detection[/bold cyan]",
            border_style="cyan"
        ))
        tech_data = tech_detector.detect_technologies(args.url)
        console.print(f"Detected technologies:\n{tech_data}")
        
        # Step 2: AI Path Generation
        console.print(Panel.fit(
            "[bold cyan]Step 2: AI Path Generation[/bold cyan]",
            border_style="cyan"
        ))
        paths = ai_fuzz.generate_paths(args.url, tech_data)
        console.print(f"Generated {len(paths)} paths to fuzz")
        
        # Step 3: Fuzzing
        console.print(Panel.fit(
            "[bold cyan]Step 3: Fuzzing URLs[/bold cyan]",
            border_style="cyan"
        ))
        results = asyncio.run(fuzzer.fuzz_urls(args.url, paths))
        
        # Step 4: Results
        console.print(Panel.fit(
            "[bold cyan]Step 4: Results[/bold cyan]",
            border_style="cyan"
        ))
        console.print(fuzzer.format_results(results))
        
        # Save results
        os.makedirs(args.output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(args.output_dir, f"results_{timestamp}.json")
        fuzzer.save_results(results, output_file)
        console.print(f"\nResults saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
        
    return 0

if __name__ == "__main__":
    main() 