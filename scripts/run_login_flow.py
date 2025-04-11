import sys
import time # Import time for sleep
from playwright.sync_api import sync_playwright, Playwright, Page

# Import configuration and Page Objects
from helpers import config
from pages.ehr_landing_page import EhrLandingPage
from pages.ehr_login_popup_page import EhrLoginPopupPage
from pages.ehr_2fa_page import Ehr2faPage

def run_login(playwright: Playwright):
    """Orchestrates the login flow using Page Objects."""
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        ignore_https_errors=True, 
        locale="en-GB", 
        timezone_id="Europe/Berlin", 
        viewport={"width": 1280, "height": 720}
    )
    main_page: Page = context.new_page()
    login_popup_page: Page = None

    try:
        # --- Landing Page --- 
        landing_page = EhrLandingPage(main_page)
        landing_page.goto_landing_page(config.EHR_URL)
        print(f"Navigated to {config.EHR_URL}")

        # --- Open Login Popup --- 
        print("Opening login popup...")
        login_popup_page = landing_page.open_login_popup()
        login_popup_page.wait_for_load_state()
        print("Login popup opened.")

        # --- Handle Login Form --- 
        login_page = EhrLoginPopupPage(login_popup_page)
        print(f"Attempting login as {config.EHR_USERNAME}...")
        login_page.login(config.EHR_USERNAME, config.EHR_PASSWORD)
        print("Login form submitted.")

        # --- Handle 2FA Page --- 
        two_fa_page = Ehr2faPage(login_popup_page)
        print("Checking for 2FA page elements...")
        two_fa_page.verify_2fa_elements_visible()
        print("2FA page elements verified. Manual 2FA needed or implement automation.")

        # === Placeholder for next steps ===
        print("Reached end of placeholder script. Add next steps.")
        # Example: Keep browser open for inspection
        print("Keeping browser open for 30 seconds...")
        time.sleep(30)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
    finally:
        # --- Cleanup --- 
        print("Closing browser context...")
        context.close()
        print("Browser closed.")

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run_login(playwright) 