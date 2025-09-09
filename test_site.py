# test_site.py
# Playwright regression test for www.google.com
# Captures screenshots and logs, structured for CI/CD integration

import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Create output directories if they don't exist
def ensure_directories():
    os.makedirs('screenshots', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('logs/test_log.txt', 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def test_google():
    ensure_directories()
    try:
        log('Starting Playwright regression test for www.google.com')
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # 1. Test: Page load
            log('Navigating to Google homepage...')
            page.goto('https://www.google.com', timeout=15000)
            page.screenshot(path='screenshots/google_home.png')
            log('Google homepage loaded and screenshot captured.')

            # Accept cookies if the consent form appears
            try:
                consent_btn = page.locator("button:has-text('Accept all')")
                if consent_btn.is_visible():
                    consent_btn.click()
                    log('Accepted cookies consent.')
                    page.screenshot(path='screenshots/google_home_after_consent.png')
            except Exception:
                log('No consent dialog detected.')

            # 2. Test: Search functionality
            log('Testing search functionality...')
            page.fill("input[name='q']", "Playwright Python")
            page.screenshot(path='screenshots/search_filled.png')
            page.press("input[name='q']", "Enter")
            try:
                page.wait_for_selector('h3', timeout=10000)
                log('Search results loaded.')
                page.screenshot(path='screenshots/search_results.png')
            except PlaywrightTimeoutError:
                log('Timeout waiting for search results.')

            # 3. Test: Navigation element (clicking the 'Images' link)
            log("Testing navigation to 'Images'...")
            try:
                images_link = page.locator("a:has-text('Images')")
                if images_link.is_visible():
                    images_link.click()
                    page.wait_for_load_state('networkidle')
                    log("Navigated to 'Images' tab.")
                    page.screenshot(path='screenshots/images_tab.png')
                else:
                    log("'Images' link not found.")
            except Exception as e:
                log(f"Error navigating to 'Images': {e}")

            browser.close()
            log('Test completed successfully.')
    except Exception as e:
        log(f'Exception occurred: {e}')
        raise

if __name__ == '__main__':
    test_google()
