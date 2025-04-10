from base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email = page.get_by_role("textbox", name="Email").click()
        self.password = page.get_by_placeholder("Password")
        self.submitButton = page.get_by_role("button", name="Login")
        

    def login(self, email: str, password: str) -> None:   
        self.email.fill(email)
        self.password.fill(password)
        self.submitButton.click()
        