"""Load versioned prompts for the agent.

Prompts live in <project_root>/prompts/*.md with YAML frontmatter.
The frontmatter is loader metadata; the body is the system prompt text
passed to the LLM verbatim.
"""

from pathlib import Path

import frontmatter
from pydantic import BaseModel

# prompts live at <project_root>/prompts/*.md
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class RecipeMetadata(BaseModel):
    version: str


def load_recipe(name: str = "research_recipe") -> tuple[RecipeMetadata, str]:
    """Load a versioned prompt by name. Returns (metadata, body).

    The body is markdown with frontmatter stripped, ready to pass as the system prompt to the LLM.
    """
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Recipe not found: {path}")
    parsed = frontmatter.load(path)
    return RecipeMetadata(**parsed.metadata), parsed.content


if __name__ == "__main__":
    # Smoke test: `uv run python -m app.prompts`
    metadata, body = load_recipe()
    print(f"Loaded recipe v{metadata.version} ({len(body)} chars)")
    print("---")
    print(body[:500] + "...")