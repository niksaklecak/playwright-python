from .base_page import BasePage
from playwright.async_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_placeholder("Password")
        self.submitButton = page.get_by_role("button", name="Login")
        

    async def login(self, email: str, password: str) -> None:   
        await self.email_input.fill(email)
        await self.password_input.fill(password)
        await self.submitButton.click()
        