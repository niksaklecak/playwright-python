"""
This module contains shared api fixtures.
"""
import pytest
from typing import AsyncGenerator
from helpers.api_client import ApiClient



# ------------------------------------------------------------
# SpaceX api project fixtures
# ------------------------------------------------------------

@pytest.fixture(scope='session')
async def api_client() -> AsyncGenerator[ApiClient, None]:
    async with ApiClient() as client:
        yield client

    
