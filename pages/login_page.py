from playwright.sync_api import Page, expect
from helpers.config import WEINFUSE_BASE_URL
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_path = '/login'
        self.email_input = page.get_by_label("Email address")
        self.password_input = page.get_by_label("Password")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.otp_input = page.get_by_label("Enter your one-time code")

    def navigate(self):
        """Navigates to the login page and waits for the email input."""
        self.page.goto(WEINFUSE_BASE_URL)

    def login(self, email: str, password: str):
        """Performs the login steps up to the OTP entry with waits."""
        self.email_input.fill(email)
        self.continue_button.click()
        self.password_input.fill(password)
        self.continue_button.click()