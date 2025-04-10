"""
These tests cover space x login 
"""

import pytest

from playwright.sync_api import expect, Page


def test_space_x(auth_page: Page) -> None:
    # Now 'setup' is the page object returned from the setup fixture
    # You can directly use 'setup' as your page object
    auth_page.goto("/some-other-page")  # Example usage
    # Add assertions or other test steps here

