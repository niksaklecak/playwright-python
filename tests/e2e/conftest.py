"""
This module contains shared fixtures.
"""

# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------

import os
import pytest
from playwright.sync_api import Page


# ------------------------------------------------------------
# Browser / General Fixtures
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
@pytest.fixture(scope="function", autouse=True)
def increase_default_timeout(page: Page):
    # Add back the intended body with correct indentation
    # Set timeout to 60 seconds (adjust as needed)
    page.set_default_timeout(30 * 1000)



