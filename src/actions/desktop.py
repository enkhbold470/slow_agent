import pyautogui
import time
import os
from PIL import Image
from ..utils.logger import Logger

class DesktopHandler:
    """Handler for desktop interactions using PyAutoGUI."""
    
    def __init__(self, screenshot_dir="screenshots"):
        """Initialize the desktop handler."""
        self.logger = Logger(name="desktop_handler")
        pyautogui.PAUSE = 1.0  # Default pause between actions
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)
    
    def move_mouse(self, x, y, duration=0.5):
        """Move the mouse to the specified coordinates."""
        try:
            self.logger.info(f"Moving mouse to ({x}, {y})")
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            self.logger.error(f"Error moving mouse: {str(e)}")
            return False
    
    def click(self, x=None, y=None, button="left"):
        """Click at the specified coordinates or current position."""
        try:
            if x is not None and y is not None:
                self.logger.info(f"Clicking at ({x}, {y}) with {button} button")
                pyautogui.click(x, y, button=button)
            else:
                self.logger.info(f"Clicking at current position with {button} button")
                pyautogui.click(button=button)
            return True
        except Exception as e:
            self.logger.error(f"Error clicking: {str(e)}")
            return False
    
    def double_click(self, x=None, y=None):
        """Double-click at the specified coordinates or current position."""
        try:
            if x is not None and y is not None:
                self.logger.info(f"Double-clicking at ({x}, {y})")
                pyautogui.doubleClick(x, y)
            else:
                self.logger.info("Double-clicking at current position")
                pyautogui.doubleClick()
            return True
        except Exception as e:
            self.logger.error(f"Error double-clicking: {str(e)}")
            return False
    
    def type_text(self, text, interval=0.1):
        """Type the specified text."""
        try:
            self.logger.info(f"Typing text: {text[:20]}..." if len(text) > 20 else f"Typing text: {text}")
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            self.logger.error(f"Error typing text: {str(e)}")
            return False
    
    def press_key(self, key):
        """Press the specified key."""
        try:
            self.logger.info(f"Pressing key: {key}")
            pyautogui.press(key)
            return True
        except Exception as e:
            self.logger.error(f"Error pressing key: {str(e)}")
            return False
    
    def hotkey(self, *keys):
        """Press the specified hotkey combination."""
        try:
            self.logger.info(f"Pressing hotkey: {'+'.join(keys)}")
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            self.logger.error(f"Error pressing hotkey: {str(e)}")
            return False
    
    def take_screenshot(self, name=None, region=None):
        """Take a screenshot of the specified region or entire screen."""
        try:
            if not name:
                name = f"desktop_screenshot_{int(time.time())}"
            
            file_path = os.path.join(self.screenshot_dir, f"{name}.png")
            
            if region:
                self.logger.info(f"Taking screenshot of region {region} to {file_path}")
                screenshot = pyautogui.screenshot(region=region)
            else:
                self.logger.info(f"Taking full screenshot to {file_path}")
                screenshot = pyautogui.screenshot()
            
            screenshot.save(file_path)
            return file_path
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return None
    
    def find_image_on_screen(self, image_path, confidence=0.9):
        """Find the specified image on screen."""
        try:
            self.logger.info(f"Looking for image {image_path} on screen")
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                self.logger.info(f"Found image at {location}")
                return location
            else:
                self.logger.info(f"Image not found on screen")
                return None
        except Exception as e:
            self.logger.error(f"Error finding image: {str(e)}")
            return None
    
    def click_image(self, image_path, confidence=0.9):
        """Click on the specified image if found on screen."""
        try:
            location = self.find_image_on_screen(image_path, confidence)
            if location:
                center = pyautogui.center(location)
                return self.click(center.x, center.y)
            return False
        except Exception as e:
            self.logger.error(f"Error clicking image: {str(e)}")
            return False
    
    def get_screen_size(self):
        """Get the screen size."""
        try:
            size = pyautogui.size()
            self.logger.info(f"Screen size: {size}")
            return size
        except Exception as e:
            self.logger.error(f"Error getting screen size: {str(e)}")
            return None
    
    def scroll(self, clicks, x=None, y=None):
        """Scroll the specified number of clicks."""
        try:
            if x is not None and y is not None:
                self.logger.info(f"Scrolling {clicks} clicks at position ({x}, {y})")
                pyautogui.scroll(clicks, x, y)
            else:
                self.logger.info(f"Scrolling {clicks} clicks at current position")
                pyautogui.scroll(clicks)
            return True
        except Exception as e:
            self.logger.error(f"Error scrolling: {str(e)}")
            return False
