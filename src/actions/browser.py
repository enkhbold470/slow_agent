from playwright.sync_api import sync_playwright
from ..utils.logger import Logger
import time
import os

class BrowserHandler:
    """Handler for browser interactions using Playwright."""
    
    def __init__(self, headless=False):
        """Initialize the browser handler."""
        self.logger = Logger(name="browser_handler")
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def __enter__(self):
        """Start the browser when entering the context."""
        self.start_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the browser when exiting the context."""
        self.close_browser()
    
    def start_browser(self):
        """Start the browser."""
        try:
            self.logger.info("Starting browser")
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            return True
        except Exception as e:
            self.logger.error(f"Error starting browser: {str(e)}")
            return False
    
    def close_browser(self):
        """Close the browser."""
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            
            self.page = None
            self.browser = None
            self.playwright = None
            
            self.logger.info("Browser closed")
            return True
        except Exception as e:
            self.logger.error(f"Error closing browser: {str(e)}")
            return False
    
    def navigate_to(self, url):
        """Navigate to the specified URL."""
        try:
            self.logger.info(f"Navigating to {url}")
            self.page.goto(url)
            return True
        except Exception as e:
            self.logger.error(f"Error navigating to {url}: {str(e)}")
            return False
    
    def take_screenshot(self, name=None):
        """Take a screenshot of the current page."""
        try:
            if not name:
                name = f"screenshot_{int(time.time())}"
            
            file_path = os.path.join(self.screenshot_dir, f"{name}.png")
            self.page.screenshot(path=file_path)
            self.logger.info(f"Screenshot saved to {file_path}")
            return file_path
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return None
    
    def find_element(self, selector):
        """Find an element by selector."""
        try:
            return self.page.query_selector(selector)
        except Exception as e:
            self.logger.error(f"Error finding element {selector}: {str(e)}")
            return None
    
    def click_element(self, selector):
        """Click an element by selector."""
        try:
            self.logger.info(f"Clicking element {selector}")
            self.page.click(selector)
            return True
        except Exception as e:
            self.logger.error(f"Error clicking element {selector}: {str(e)}")
            return False
    
    def type_text(self, selector, text):
        """Type text into an element by selector."""
        try:
            self.logger.info(f"Typing text into element {selector}")
            self.page.fill(selector, text)
            return True
        except Exception as e:
            self.logger.error(f"Error typing text into element {selector}: {str(e)}")
            return False
    
    def get_page_content(self):
        """Get the content of the current page."""
        try:
            return self.page.content()
        except Exception as e:
            self.logger.error(f"Error getting page content: {str(e)}")
            return None
    
    def extract_text(self, selector="body"):
        """Extract text from the specified element."""
        try:
            element = self.page.query_selector(selector)
            if element:
                return element.inner_text()
            return None
        except Exception as e:
            self.logger.error(f"Error extracting text from {selector}: {str(e)}")
            return None
