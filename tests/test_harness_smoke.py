"""Smoke tests for the test harness itself, not for any application behaviour.

These exist to prove three things about the setup: pytest collects from `tests/`,
`asyncio_mode = "auto"` actually runs an async test body rather than erroring on it,
and the root conftest makes the settings import work without a `.env`.
"""
import asyncio

from core.config import settings


def test_pytest_runs_a_sync_test():
    assert True


async def test_pytest_runs_an_async_test():
    await asyncio.sleep(0)
    assert True


def test_settings_import_without_dotenv():
    assert settings.openai_api_key
