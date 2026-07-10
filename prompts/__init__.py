"""Version + loader for the ingest ASR-cleanup prompt.

(The agent's research recipe is loaded separately by app/prompts.py, which
reads frontmatter-versioned markdown; this module serves the cleanup prompt.)
"""
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

CLEANUP_VERSION = "cleanup_v1"


def load(version: str) -> str:
    """Load a prompt by version string."""
    return (PROMPTS_DIR / f"{version}.md").read_text()