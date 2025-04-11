from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage

class EhrLoginPopupPage(BasePage):
    def __init__(self, page: Page):
        # Note: This takes the POPUP page as input
        super().__init__(page)
        # Locators for the login form
        self.username_input: Locator = page.locator("#inputUsername")
        self.password_input: Locator = page.locator("#inputPswd")
        self.login_button: Locator = page.get_by_role("button", name="Log in")

    def login(self, username: str, password: str):
        """Fills the login form and clicks the login button."""
        self.username_input.click()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click() 