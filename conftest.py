"""Root conftest, loaded by pytest before any test module is imported.

It does two jobs, and both are needed for `uv run pytest` to work in CI.

Existing at the repository root makes pytest prepend that root to `sys.path`, so
test modules under `tests/` can `import app`, `core`, and `eval`. Without this file
the only paths prepended are the test directories themselves, and collection fails
with `ModuleNotFoundError: No module named 'core'`.

Seeding a dummy key handles the second blocker: `core/config.py` builds a
module-level `Settings()` whose `openai_api_key` field is required and has no
default, so importing it raises a pydantic ValidationError wherever there is no
`.env` and no key in the environment. That is exactly the CI case, since `.env` is
not checked in. `setdefault` means a real key already in the environment wins, so
this never masks local configuration and never hands the suite a real credential.
"""
import os

os.environ.setdefault("OPENAI_API_KEY", "test")
