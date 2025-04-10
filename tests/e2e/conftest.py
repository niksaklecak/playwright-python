"""
This module contains shared fixtures.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import os
import pytest
from playwright.sync_api import Page, expect
from pages.pom_manager import PomManager


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

@pytest.fixture
def auth_page(page: Page) -> Page:
    page.goto("/")
    perform_authentication(page)
    page.context().storage_state(path="tests/e2e/storage_state.json")
    return page

def perform_authentication(page: Page) -> None:
    page.get_by_role("link", name="Account").click()
    pom = PomManager(page)
    pom.loginPage.login("testniksa1@gmail.com", "sifra123")

