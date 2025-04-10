from playwright.sync_api import sync_playwright

class BasePage:

    URL = "/"

    def __init__(self, page):
        self.page = page

    # this method should wait until the page URL is loaded 
    # and also it should wait until the specified network request is completed
    def load(self, url, page_network_request) -> None:
        self.page.goto(url, waitUntil="networkidle")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_request(page_network_request)


       