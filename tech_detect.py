import subprocess
import logging

logger = logging.getLogger(__name__)

class TechnologyDetector:
    """Detects web technologies using WhatWeb."""
    
    def __init__(self):
        self.whatweb_path = "whatweb"
        
    def check_whatweb_installed(self) -> bool:
        """Check if WhatWeb is installed and accessible."""
        try:
            subprocess.run([self.whatweb_path, "--version"], 
                         capture_output=True, 
                         check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
            
    def detect_technologies(self, url: str) -> str:
        """
        Detect technologies used by the target website.
        
        Args:
            url (str): Target website URL
            
        Returns:
            str: Raw WhatWeb output
        """
        if not self.check_whatweb_installed():
            raise RuntimeError(
                "WhatWeb is not installed. Please install it first: "
                "https://github.com/urbanadventurer/WhatWeb"
            )
            
        try:
            # Run WhatWeb with verbose output
            result = subprocess.run(
                [self.whatweb_path, url, "-v"],
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout.strip()
            
        except subprocess.SubprocessError as e:
            logger.error(f"WhatWeb execution failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in technology detection: {str(e)}")
            raise 