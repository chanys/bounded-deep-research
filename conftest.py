"""Root conftest, loaded by pytest before any test module is imported.

`core/config.py` builds a module-level `Settings()` whose `openai_api_key` field is
required and has no default, so importing almost anything under `app/`, `core/`, or
`eval/` raises a pydantic ValidationError when there is no `.env` and no key in the
environment. That is exactly the situation in CI, where `.env` is not checked in.

Seeding a dummy key here makes collection possible without handing the test run a
real credential. `setdefault` means a real key already in the environment wins, so
this never masks local configuration.
"""
import os

os.environ.setdefault("OPENAI_API_KEY", "test")
