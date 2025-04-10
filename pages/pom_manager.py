from playwright.async_api import Page, expect
from .login_page import LoginPage

class PomManager:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.loginPage = LoginPage(page)
