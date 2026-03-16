"""Deep Research Agent - Production-ready AI research system."""

__version__ = "1.0.0"

from .manager import ResearchManager
from .app import create_app

__all__ = ["ResearchManager", "create_app"]
