# load_tester.py
# Load Testing for Nova Applications

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict

class LoadTestResult:
    """Load test results"""
    
    def __init__(self):
        self.successful = 0
        self.failed = 0
        self.responses = []
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def add_response(self, status: int, duration: float):
        """Add a response"""
        if 200 <= status < 300:
            self.successful += 1
        else:
            self.failed += 1
        self.responses.append(duration)
    
    def add_error(self, error: str):
        """Add an error"""
        self.failed += 1
        self.errors.append(error)
    
    def get_stats(self) -> Dict:
        """Get statistics"""
        if not self.responses:
            return {'error': 'No responses'}
        
        return {
            'total_requests': len(self.responses),
            'successful': self.successful,
            'failed': self.failed,
            'success_rate': self.successful / len(self.responses) if self.responses else 0,
            'response_times': {
                'min': min(self.responses),
                'max': max(self.responses),
                'avg': statistics.mean(self.responses),
                'median': statistics.median(self.responses),
                'p95': statistics.quantiles(self.responses, n=20)[18] if len(self.responses) >= 20 else None,
                'p99': statistics.quantiles(self.responses, n=100)[98] if len(self.responses) >= 100 else None,
            }
        }

class LoadTester:
    """Load testing tool"""
    
    def __init__(self, base_url: str, concurrent_users: int = 10):
        self.base_url = base_url
        self.concurrent_users = concurrent_users
        self.results = LoadTestResult()
    
    async def run_test(self, endpoints: List[str], requests_per_user: int = 100):
        """Run load test"""
        self.results.start_time = time.time()
        
        async def test_user(session, endpoints):
            for _ in range(requests_per_user):
                endpoint = endpoints[_ % len(endpoints)]
                start = time.time()
                try:
                    async with session.get(f"{self.base_url}{endpoint}") as response:
                        duration = time.time() - start
                        self.results.add_response(response.status, duration)
                except Exception as e:
                    duration = time.time() - start
                    self.results.add_error(str(e))
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(self.concurrent_users):
                task = asyncio.create_task(test_user(session, endpoints))
                tasks.append(task)
            await asyncio.gather(*tasks)
        
        self.results.end_time = time.time()
        return self.results.get_stats()
    
    def run_sync(self, endpoints: List[str], requests_per_user: int = 100):
        """Run load test synchronously"""
        return asyncio.run(self.run_test(endpoints, requests_per_user))