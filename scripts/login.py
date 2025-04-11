"""
WeInFuse login automation script using Playwright directly.
"""
from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
import logging
import time
import pyotp
import json
from playwright.async_api import Page
from pydantic import SecretStr

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get credentials for WeInFuse login
weinfuse_username = SecretStr(os.getenv('WEINFUSE_USERNAME', ''))
weinfuse_password = SecretStr(os.getenv('WEINFUSE_PASSWORD', ''))
otp_secret = SecretStr(os.getenv('WEINFUSE_OTP_SECRET', ''))

async def login(page: Page):
    """Login to WeInFuse with username and password."""
    logger.info("Starting login process...")
    
    # Navigate to login page
    await page.goto('https://app.weinfuse.com/login')
    
    # The app redirects to Auth0 login page
    # Wait for the email input which might be on Auth0 domain
    logger.info("Waiting for login form to load...")
    await page.wait_for_selector('#username', timeout=10000)
    logger.info("Login form loaded, entering email")
    
    # Enter email - using the specific ID from the form
    await page.fill('#username', weinfuse_username.get_secret_value())
    await page.click('button[data-action-button-primary="true"]')
    logger.info("Email entered, waiting for password field")
    
    # Enter password - ensure we wait for the field to appear after email submission
    await page.wait_for_selector('input[type="password"]', timeout=10000)
    logger.info("Password field found, entering password")
    await page.fill('input[type="password"]', weinfuse_password.get_secret_value())
    await page.click('button[data-action-button-primary="true"], button[type="submit"]')
    logger.info("Password entered")
    
    # The system might redirect multiple times during authentication
    # Wait for redirection to complete
    await page.wait_for_load_state('networkidle', timeout=10000)
    logger.info("Authentication redirects completed")

async def handle_otp(page: Page):
    """Handle OTP entry with retries."""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"OTP attempt {attempt}/{max_attempts}")
            
            # Generate a fresh OTP
            totp = pyotp.TOTP(otp_secret.get_secret_value())
            current_otp = totp.now()
            
            # Check how much time left for this OTP
            remaining_seconds = 30 - (int(time.time()) % 30)
            logger.info(f"Current OTP: {current_otp}, valid for {remaining_seconds} seconds")
            
            # If less than 5 seconds left, wait for next OTP
            if remaining_seconds < 5:
                logger.info("Less than 5 seconds left for current OTP, waiting for next one...")
                await asyncio.sleep(remaining_seconds + 1)
                totp = pyotp.TOTP(otp_secret.get_secret_value())
                current_otp = totp.now()
                logger.info(f"New OTP: {current_otp}")
            
            # Wait for OTP input field - using exact ID from OTP form
            await page.wait_for_selector('#code', timeout=10000)
            logger.info("OTP field found, entering code")
            await page.fill('#code', current_otp)
            
            # Click the continue button - using the exact button from the OTP form
            logger.info("Locating continue button...")
            await page.click('button[data-action-button-primary="true"]')
            logger.info("OTP submitted")
            
            # Check if OTP was accepted by looking for WeInFuse dashboard elements
            try:
                # Wait for dashboard-specific elements from the WeInFuse UI
                # These are based on the actual HTML structure of the dashboard
                logger.info("Waiting for dashboard elements...")
                
                # List of dashboard selectors - we'll check for any of these
                dashboard_selectors = [
                    'md-toolbar.app-toolbar',                  # Main toolbar
                    'input[placeholder="Patients"]',           # Search box
                    '.app-nav-link',                          # Nav menu items
                    'md-icon.material-icons:has-text("menu")', # Menu icon
                    '.MuiAvatar-root',                         # User avatar
                    'md-sidenav',                             # Side navigation
                    'img[src="/app/assets/images/default.svg"]' # Logo
                ]
                
                # Wait for any of these dashboard elements
                for selector in dashboard_selectors:
                    try:
                        await page.wait_for_selector(selector, timeout=5000)
                        logger.info(f"Found dashboard element: {selector}")
                        return True
                    except Exception:
                        continue
                
                # If we get here, none of the specific selectors were found
                # As a fallback, check for the URL pattern
                current_url = page.url
                if "/app.weinfuse.com/" in current_url or current_url.endswith("weinfuse.com"):
                    logger.info(f"Detected WeInFuse URL: {current_url}")
                    return True
                
                # No success indicators found, check for errors
                raise Exception("No dashboard elements detected")
                
            except Exception as e:
                # Look for error message with appropriate selectors from Auth0
                error_visible = await page.is_visible('.ulp-server-error, div[aria-live="assertive"], div[role="alert"]')
                if error_visible:
                    error_text = await page.text_content('.ulp-server-error, div[aria-live="assertive"], div[role="alert"]')
                    logger.error(f"OTP error: {error_text}")
                    logger.error("Invalid OTP. Retrying...")
                    continue
                else:
                    # No error message and no dashboard - might be processing
                    logger.info("OTP submitted, checking status with longer timeout...")
                    try:
                        # Wait longer in case of slow redirect, checking for any dashboard element
                        await page.wait_for_selector('md-toolbar, .app-nav-link, .MuiAvatar-root', timeout=30000)
                        logger.info("Dashboard detected after extended wait")
                        return True
                    except Exception:
                        logger.error("Could not verify OTP success")
                        continue
                        
        except Exception as e:
            logger.error(f"Error during OTP attempt {attempt}: {str(e)}")
            
        # Wait before next attempt
        if attempt < max_attempts:
            await asyncio.sleep(2)
    
    logger.error("Failed to complete OTP verification after maximum attempts")
    return False

# Standalone entry point for running the script directly (for testing)
async def main():
    """Main function to run the login automation standalone for testing."""
    try:
        from utils.browser_setup import initialize_playwright_browser
        from playwright.async_api import async_playwright
        
        logger.info("Starting standalone login test...")
        browser_options = initialize_playwright_browser(headless=False, slow_mo=10)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(**browser_options)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800},
                ignore_https_errors=True
            )
            page = await context.new_page()
            
            # Execute login process
            await login(page)
            
            # Handle OTP verification
            otp_success = await handle_otp(page)
            
            if otp_success:
                logger.info("Login completed successfully")
            else:
                logger.error("Login failed")
                
            # Wait for user input before closing
            input("Press Enter to close the browser...")
            await browser.close()
            
    except Exception as e:
        logger.error(f"Error in standalone login test: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
