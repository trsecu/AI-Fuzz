import json
import logging
from typing import List, Dict
from google import genai

logger = logging.getLogger(__name__)

class AIFuzz:
    """AI-Fuzz tool using Gemini API for path generation."""
    
    def __init__(self, api_key: str):
        """Initialize the AI-Fuzz tool with Gemini API key."""
        self.client = genai.Client(api_key=api_key)
        
    def generate_paths(self, url: str, tech_data: str) -> List[str]:
        """
        Generate potential fuzzing paths for a given URL.
        
        Args:
            url: The target URL to generate paths for
            tech_data: Raw WhatWeb output containing detected technologies
            
        Returns:
            List of potential paths to fuzz
        """
        try:
            # Construct the prompt
            prompt = self._construct_prompt(url, tech_data)
            
            # Generate paths using Gemini
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            # Parse and return the paths
            return self._parse_response(response.text)
            
        except Exception as e:
            logger.error(f"Failed to generate paths: {str(e)}")
            raise
            
    def _construct_prompt(self, url: str, tech_data: str) -> str:
        """Construct the prompt for Gemini."""
        return f"""Given the website URL: {url}

WhatWeb scan results:
{tech_data}

Based on the WhatWeb scan results above, generate a list of 20 possible URL paths that might be worth fuzzing for security testing.
Focus on:
1. Common administrative interfaces
2. API endpoints
3. Configuration files
4. Backup directories
5. Sensitive data storage locations
6. Common CMS paths
7. Development and testing endpoints

Return only the paths, one per line, without any explanations or additional text.
Each path should start with a forward slash (/).

Example format:
/admin
/api/v1/users
/config.php
/backup.zip
/wp-admin
/phpinfo.php
"""
        
    def _parse_response(self, response: str) -> List[str]:
        """Parse the Gemini response into a list of paths."""
        # Split by newlines and clean up
        paths = [line.strip() for line in response.split('\n')]
        # Filter out empty lines and ensure paths start with /
        paths = [path for path in paths if path and path.startswith('/')]
        return paths

def load_config() -> Dict:
    """Load configuration from config.json."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {str(e)}")
        raise 