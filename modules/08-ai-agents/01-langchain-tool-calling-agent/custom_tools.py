"""
Custom tool adapters for the LangChain agent executor example.
These tools are safe, local placeholders and must be replaced with secure implementations in production.
"""
from typing import Dict

class SQLRunner:
    def __init__(self):
        self.name = 'sql_runner'
        self.schema = {'required': ['query']}

    def __call__(self, query: str) -> Dict:
        # In real world execute against a read-only replica and sanitize queries
        return {'rows': [], 'query': query}

class HTTPFetcher:
    def __init__(self):
        self.name = 'http_fetcher'
        self.schema = {'required': ['url']}

    def __call__(self, url: str) -> Dict:
        # Example placeholder: do not perform real requests in this example
        return {'status': 200, 'url': url}

sql_runner = SQLRunner()
http_fetcher = HTTPFetcher()
