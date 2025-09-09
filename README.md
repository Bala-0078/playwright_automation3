# Playwright Regression Testing

This repository contains a scalable Playwright automation script for regression testing of websites. The script can run in headless mode, capture screenshots, save logs, and is integrated with GitHub Actions for CI/CD.

## Features

- Headless browser testing using Playwright
- Screenshot capture during test execution
- Detailed logging for analysis
- Configurable test scenarios
- GitHub Actions integration for automated testing

## Folder Structure

```
|----.github/workflows/playwright.yaml
|----requirements.txt
|----test_site.py
|----logs/           (created during execution)
|----screenshots/    (created during execution)
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Bala-0078/playwright_automation3.git
cd playwright_automation3

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

## Usage

### Running Tests Locally

```bash
# Run with default configuration
python test_site.py

# Run with custom domain
python test_site.py --domain https://www.example.com

# Run with custom configuration file
python test_site.py --config my_config.json
```

### Configuration File Format

Create a JSON file with the following structure:

```json
{
  "domain": "https://www.example.com",
  "functionalities": [
    {
      "type": "search",
      "selector": "input[name=\"q\"]",
      "value": "Playwright Python",
      "result_selector": "h3"
    },
    {
      "type": "click",
      "selector": "a[href=\"/about\"]",
      "result_selector": ".about-page"
    },
    {
      "type": "form",
      "form_selector": "form#contact",
      "fields": [
        {"selector": "input[name=\"name\"]", "value": "Test User"},
        {"selector": "input[name=\"email\"]", "value": "test@example.com"},
        {"selector": "textarea[name=\"message\"]", "value": "This is a test message"}
      ],
      "submit_selector": "button[type=\"submit\"]",
      "result_selector": ".success-message"
    }
  ]
}
```

## GitHub Actions

The repository is configured with GitHub Actions to run tests automatically:

- On push to the main branch
- On pull requests to the main branch
- Manually via workflow dispatch (with optional domain parameter)

### Artifacts

After each test run, GitHub Actions will upload the following artifacts:

- Screenshots captured during testing
- Log files for detailed analysis

## Extending the Tests

To add new test functionalities, extend the configuration file with additional test scenarios. The script currently supports the following test types:

- `search`: Fill a search field and submit
- `click`: Click on an element and verify a result appears
- `form`: Fill and submit a form

## License

MIT
