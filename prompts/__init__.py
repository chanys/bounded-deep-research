"""Single source of truth for prompt versions used in production runs."""
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

CLEANUP_VERSION = "cleanup_v1"
RESEARCH_RECIPE_VERSION = "research_recipe_v1"  # Phase 2
JUDGE_VERSION = "judge_v1"  # Phase 4


def load(version: str) -> str:
    """Load a prompt by version string."""
    return (PROMPTS_DIR / f"{version}.md").read_text()