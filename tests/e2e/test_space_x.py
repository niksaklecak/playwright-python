"""
These tests cover space x login 
"""

import pytest

# Import async Page and expect
from playwright.async_api import expect, Page

# Mark test as async
@pytest.mark.asyncio
async def test_space_x(auth_page: Page) -> None:
    # Now 'setup' is the page object returned from the setup fixture
    # You can directly use 'setup' as your page object
    # Use await for Playwright operations
    await auth_page.goto("/some-other-page")  # Example usage
    # Add assertions or other test steps here
    # Example assertion (needs await if it's a Playwright assertion)
    await expect(auth_page).to_have_title("Expected Title") # Replace with actual expected title

