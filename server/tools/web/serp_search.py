from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple, Literal, TypeAlias
from langchain.utilities import SerpAPIWrapper
from dotenv import load_dotenv
from pydantic import BaseModel, Extra, Field, root_validator

import tempfile
import asyncio

load_dotenv()


google_params: dict = Field(
    default={
        "engine": "google",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
    }
)

bing_params: dict = Field(
    default={
        "engine": "bing",
        "gl": "us",
        "hl": "en",
    }
)

SearchEngine: TypeAlias = Literal["google", "bing"]




class SerpSearch(ABC):
    
    def change_engine(self, engine: SearchEngine, force: bool = False):
        """Change the search engine."""
        if not engine is None or force:
            if engine == "google":
                self.engine = google_params
            elif engine == "bing":
                self.engine = bing_params
    
    def __init__(self, engine: SearchEngine = "google"):
        """Initialize a SerpSearch object."""
        # self.change_engine(engine)
        # self.serp = SerpAPIWrapper(params=self.engine)
        self.serp = SerpAPIWrapper()

    async def arun(self, query: str) -> str:
        """Run query through SerpAPI and parse result async."""
        # self.change_engine(engine)
        return await self.serp.arun(query)

    def run(self, query: str) -> str:
        """Run query through SerpAPI and parse result."""
        # self.change_engine(engine)
        return self.serp.run(query)

    def results(self, query: str) -> dict:
        """Run query through SerpAPI and return the raw result."""
        return self.serp.results(query)

    async def aresults(self, query: str) -> dict:
        """Use aiohttp to run query through SerpAPI and return the results async."""
        return await self.serp.aresults(query)

