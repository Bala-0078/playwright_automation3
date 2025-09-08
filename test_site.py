# test_site.py
# Playwright regression testing script for www.google.com
# Captures screenshots and logs, runs in headless mode

import os
import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def setup_logging(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'test_logs.txt')
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return log_path

def test_google():
    screenshots_dir = 'screenshots'
    os.makedirs(screenshots_dir, exist_ok=True)
    log_dir = 'logs'
    log_path = setup_logging(log_dir)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # 1. Navigate to Google
            logging.info('Navigating to https://www.google.com')
            page.goto('https://www.google.com', timeout=15000)
            page.screenshot(path=os.path.join(screenshots_dir, 'google_home.png'))
            logging.info('Google home page loaded and screenshot taken.')

            # 2. Accept cookies if prompted
            try:
                if page.is_visible("button:has-text('I agree')"):
                    page.click("button:has-text('I agree')")
                    logging.info('Accepted cookies.')
            except Exception:
                pass  # Cookie prompt may not appear in all regions

            # 3. Perform a search
            search_query = 'Playwright Python'
            logging.info(f'Entering search query: {search_query}')
            page.fill("input[name='q']", search_query)
            page.press("input[name='q']", "Enter")
            page.wait_for_selector('h3', timeout=10000)
            page.screenshot(path=os.path.join(screenshots_dir, 'search_results.png'))
            logging.info('Search results page loaded and screenshot taken.')

            # 4. Click the first search result link
            first_result_selector = 'h3'
            try:
                first_result = page.query_selector(first_result_selector)
                if first_result:
                    first_result.click()
                    page.wait_for_load_state('load', timeout=10000)
                    page.screenshot(path=os.path.join(screenshots_dir, 'first_result.png'))
                    logging.info('Clicked first search result and took screenshot.')
                else:
                    logging.warning('First search result not found.')
            except PlaywrightTimeoutError:
                logging.error('Timeout while waiting for first search result to load.')

            browser.close()
            logging.info('Test completed successfully.')

    except Exception as e:
        logging.exception(f'Test failed: {e}')
        print(f"Test failed. See logs at {log_path}")

if __name__ == "__main__":
    test_google()
