from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from helpers.config import WEINFUSE_EMAIL, WEINFUSE_PASSWORD
from helpers.util import get_otp_code

def test_weinfuse_login_reaches_2fa(page: Page):
    """Test that the login flow reaches the 2FA page."""

    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login(WEINFUSE_EMAIL, WEINFUSE_PASSWORD)
    expect(login_page.otp_input).to_be_visible()
    expect(login_page.continue_button).to_be_visible() 

    # Add further test steps here after OTP
    print("Successfully logged in and waiting for OTP.")

def test_weinfuse_login_completes(page: Page):
    """Test the complete login flow including OTP."""

    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login(WEINFUSE_EMAIL, WEINFUSE_PASSWORD)

    otp_code = get_otp_code()
    
    # Wait for OTP field to be ready before handling OTP
    expect(login_page.otp_input).to_be_visible(timeout=15000)
    expect(login_page.continue_button).to_be_visible()

    login_page.otp_input.fill(otp_code)
    login_page.continue_button.click()
    
    print("Login and OTP verification successful!")
