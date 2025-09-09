#!/usr/bin/env python3

import os
import json
import logging
import argparse
from datetime import datetime
from playwright.sync_api import sync_playwright

# Configure logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Create screenshots directory
screenshot_dir = 'screenshots'
os.makedirs(screenshot_dir, exist_ok=True)

def take_screenshot(page, name):
    """Take a screenshot and save it with a timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{screenshot_dir}/{name}_{timestamp}.png"
    page.screenshot(path=filename)
    logging.info(f"Screenshot saved: {filename}")
    return filename

def test_website(domain, functionalities):
    """Run tests on the specified website with given functionalities"""
    logging.info(f"Starting test for domain: {domain}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Navigate to the target website
            logging.info(f"Navigating to {domain}")
            page.goto(domain)
            take_screenshot(page, "homepage")
            
            # Perform specified actions
            for idx, functionality in enumerate(functionalities, 1):
                logging.info(f"Testing functionality {idx}: {functionality.get('type', 'unknown')}")
                
                if functionality["type"] == "search":
                    logging.info(f"Performing search with selector: {functionality['selector']}")
                    page.fill(functionality["selector"], functionality["value"])
                    page.press(functionality["selector"], "Enter")
                    page.wait_for_selector(functionality["result_selector"])
                    take_screenshot(page, f"search_results_{idx}")
                    logging.info("Search completed successfully")
                    
                elif functionality["type"] == "click":
                    logging.info(f"Clicking element with selector: {functionality['selector']}")
                    page.click(functionality["selector"])
                    page.wait_for_selector(functionality["result_selector"])
                    take_screenshot(page, f"navigation_result_{idx}")
                    logging.info("Click action completed successfully")
                    
                elif functionality["type"] == "form":
                    logging.info(f"Filling form with selector: {functionality['form_selector']}")
                    for field in functionality["fields"]:
                        page.fill(field["selector"], field["value"])
                    
                    page.click(functionality["submit_selector"])
                    page.wait_for_selector(functionality["result_selector"])
                    take_screenshot(page, f"form_submission_{idx}")
                    logging.info("Form submission completed successfully")
            
            logging.info("All tests completed successfully")
            
        except Exception as e:
            error_msg = f"Test failed: {str(e)}"
            logging.error(error_msg)
            take_screenshot(page, "error")
            raise
        
        finally:
            browser.close()

def load_config(config_file=None):
    """Load test configuration from file or use default"""
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config
    
    # Default configuration
    return {
        "domain": "https://www.google.com",
        "functionalities": [
            {
                "type": "search",
                "selector": "input[name=\"q\"]",
                "value": "Playwright Python",
                "result_selector": "h3"
            },
            {
                "type": "click",
                "selector": "a[href*=\"tbm=isch\"]",
                "result_selector": "img"
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser(description='Run Playwright regression tests on a website')
    parser.add_argument('--config', help='Path to test configuration JSON file')
    parser.add_argument('--domain', help='Website domain to test')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override domain if provided via command line
    if args.domain:
        config["domain"] = args.domain
    
    # Run tests
    test_website(config["domain"], config["functionalities"])

if __name__ == "__main__":
    main()
