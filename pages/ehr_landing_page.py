from playwright.sync_api import Page, Locator
from .base_page import BasePage

class EhrLandingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Locator for the main login link
        self.login_link: Locator = page.get_by_role("link", name="Log In")

    def goto_landing_page(self, url: str):
        """Navigates to the EHR landing page."""
        self.page.goto(url)

    def open_login_popup(self) -> Page:
        """Clicks the login link and returns the new popup page."""
        with self.page.expect_popup() as popup_info:
            self.login_link.click()
        return popup_info.value 