import pytest
from playwright.sync_api import Page, expect

# Import configuration and Page Objects
from helpers import config
from pages.ehr_2fa_page import Ehr2faPage
from pages.ehr_landing_page import EhrLandingPage
from pages.ehr_login_popup_page import EhrLoginPopupPage


def test_ehr_login_reaches_2fa(page: Page):
    """Test that the login flow reaches the 2FA page."""
    
    # --- Landing Page --- 
    landing_page = EhrLandingPage(page)
    landing_page.goto_landing_page(config.EHR_URL)
    print(f"Navigated to {config.EHR_URL}")
    expect(landing_page.login_link).to_be_visible()

    # --- Open Login Popup --- 
    print("Opening login popup...")
    # Use synchronous context manager
    with page.context.expect_page() as new_tab:
        landing_page.login_link.click()
    new_tab_login_context = new_tab.value
    # Wait for the new tab to load - we need a custom load here 
    new_tab_login_context.wait_for_load_state()
    print("Login popup opened.")

    # --- Handle Login Form --- 
    login_page = EhrLoginPopupPage(new_tab_login_context)
    print(f"Attempting login as {config.EHR_USERNAME}...")
    login_page.login(config.EHR_USERNAME, config.EHR_PASSWORD)
    print("Login form submitted.")

    # --- Handle 2FA Page --- 
    two_fa_page = Ehr2faPage(new_tab_login_context)
    print("Checking for 2FA page elements...")
    expect(two_fa_page.phone_input).to_be_visible()
    expect(two_fa_page.voice_option).to_be_visible()
    expect(two_fa_page.continue_button).to_be_visible()
    print("2FA page elements verified successfully.")
        