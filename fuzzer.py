import asyncio
import httpx
from typing import List, Dict, Optional
import logging
from rich.progress import Progress
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class Fuzzer:
    """Handles HTTP fuzzing operations."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.timeout = config["fuzzing"]["timeout"]
        self.max_retries = config["fuzzing"]["max_retries"]
        self.concurrent_requests = config["fuzzing"]["concurrent_requests"]
        
    async def fuzz_urls(self, base_url: str, paths: List[str]) -> List[Dict]:
        """
        Fuzz multiple URLs concurrently.
        
        Args:
            base_url (str): Base URL to fuzz against
            paths (List[str]): List of paths to test
            
        Returns:
            List[Dict]: List of results with status codes and paths
        """
        results = []
        semaphore = asyncio.Semaphore(self.concurrent_requests)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            with Progress() as progress:
                task = progress.add_task("[cyan]Fuzzing...", total=len(paths))
                
                async def fuzz_single_url(path: str) -> Optional[Dict]:
                    url = urljoin(base_url, path)
                    async with semaphore:
                        for attempt in range(self.max_retries):
                            try:
                                response = await client.get(url)
                                return {
                                    "path": path,
                                    "status_code": response.status_code,
                                    "url": url
                                }
                            except httpx.RequestError as e:
                                logger.warning(f"Request failed for {url}: {str(e)}")
                                if attempt == self.max_retries - 1:
                                    return {
                                        "path": path,
                                        "status_code": None,
                                        "error": str(e),
                                        "url": url
                                    }
                        return None
                        
                tasks = [fuzz_single_url(path) for path in paths]
                for coro in asyncio.as_completed(tasks):
                    result = await coro
                    if result:
                        results.append(result)
                    progress.update(task, advance=1)
                    
        return results
        
    def format_results(self, results: List[Dict]) -> str:
        """Format fuzzing results for display."""
        formatted = []
        for result in results:
            status = result["status_code"]
            path = result["path"]
            url = result["url"]
            
            if status is None:
                formatted.append(f"[red]ERROR[/red] {path} ({url}) - {result['error']}")
            elif 200 <= status < 300:
                formatted.append(f"[green]FOUND[/green] {path} ({url}) - Status: {status}")
            elif status == 403:
                formatted.append(f"[yellow]FORBIDDEN[/yellow] {path} ({url}) - Status: {status}")
            elif status == 404:
                formatted.append(f"[dim]NOT FOUND[/dim] {path} ({url}) - Status: {status}")
            else:
                formatted.append(f"[blue]OTHER[/blue] {path} ({url}) - Status: {status}")
                
        return "\n".join(formatted)
        
    def save_results(self, results: List[Dict], output_file: str):
        """Save fuzzing results to a file."""
        import json
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2) 
