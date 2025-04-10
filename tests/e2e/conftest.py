"""
This module contains shared fixtures.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import os
import pytest
from playwright.async_api import Page, expect
from pages.pom_manager import PomManager
from dotenv import load_dotenv


# ------------------------------------------------------------
# Space x UI fixtures
# ------------------------------------------------------------

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "timezone_id": "Europe/Berlin",
        "locale": "en-GB",
        "ignore_https_errors": True,
        "viewport": {
                "width": 1280,
                "height": 720,
            }        
    }

# Increase default timeout for slow startups
@pytest.fixture(scope="session", autouse=True)
async def increase_default_timeout(page: Page):

@pytest.fixture
async def auth_page(page: Page) -> Page:
    await page.goto("/", timeout=60000)
    await perform_authentication(page)
    await page.context.storage_state(path="tests/e2e/storage_state.json")
    return page

async def perform_authentication(page: Page) -> None:
    # Load environment variables
    load_dotenv()
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    if not email or not password:
        raise ValueError("TEST_USER_EMAIL and TEST_USER_PASSWORD must be set in .env file")

    await page.get_by_role("link", name="Account").click()
    pom = PomManager(page)
    await pom.loginPage.login(email, password)

