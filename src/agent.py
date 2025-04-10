import time
import random
from .utils.logger import Logger
from .utils.llm_client import LLMClient
from .utils.config import Config
from .actions.browser import BrowserHandler
from .actions.desktop import DesktopHandler

class SlowAgent:
    """A slow, deliberate agent for interacting with various interfaces."""
    
    def __init__(self, name="SlowAgent"):
        """Initialize the slow agent."""
        self.name = name
        self.logger = Logger(name=f"agent_{name.lower()}")
        self.logger.info(f"Initializing {name}")
        
        # Initialize components
        self.llm = LLMClient()
        self.browser = None
        self.desktop = None
        
        # Agent state
        self.conversation_history = []
        self.task_queue = []
        self.current_task = None
        self.last_action_time = 0
        self.thinking = False
    
    def think(self, prompt, system_message=None):
        """Think about the given prompt - this is the main reasoning function."""
        self.thinking = True
        self.logger.info(f"Thinking about: {prompt[:50]}..." if len(prompt) > 50 else f"Thinking about: {prompt}")
        
        # Add pauses to simulate deep thinking
        thinking_duration = random.uniform(1.0, 3.0)
        time.sleep(thinking_duration)
        
        # Default system message if none provided
        if system_message is None:
            system_message = (
                "You are a slow, methodical agent designed to carefully analyze situations "
                "and take deliberate actions. Take your time to think through problems step by step."
            )
        
        # Update conversation history
        if not self.conversation_history:
            self.conversation_history.append({"role": "system", "content": system_message})
        
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Generate response
        response = self.llm.generate_with_history(self.conversation_history)
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Add another pause after thinking
        time.sleep(random.uniform(0.5, 1.5))
        self.thinking = False
        
        return response
    
    def init_browser(self, headless=False):
        """Initialize the browser handler."""
        self.logger.info("Initializing browser handler")
        self.browser = BrowserHandler(headless=headless)
        return self.browser.start_browser()
    
    def init_desktop(self):
        """Initialize the desktop handler."""
        self.logger.info("Initializing desktop handler")
        self.desktop = DesktopHandler()
        return True
    
    def add_task(self, task_description):
        """Add a task to the queue."""
        self.logger.info(f"Adding task: {task_description}")
        self.task_queue.append(task_description)
        return len(self.task_queue)
    
    def execute_next_task(self):
        """Execute the next task in the queue."""
        if not self.task_queue:
            self.logger.info("No tasks in queue")
            return False
        
        self.current_task = self.task_queue.pop(0)
        self.logger.info(f"Executing task: {self.current_task}")
        
        # Think about how to execute the task
        execution_plan = self.think(
            f"I need to execute the following task: {self.current_task}. "
            f"Please provide a step-by-step plan for executing this task."
        )
        
        self.logger.info(f"Execution plan generated")
        return execution_plan
    
    def wait(self, seconds):
        """Wait for the specified number of seconds."""
        self.logger.info(f"Waiting for {seconds} seconds")
        time.sleep(seconds)
    
    def dynamic_pause(self, min_seconds=0.5, max_seconds=2.0):
        """Pause for a random amount of time to simulate natural behavior."""
        pause_time = random.uniform(min_seconds, max_seconds)
        self.logger.debug(f"Pausing for {pause_time:.2f} seconds")
        time.sleep(pause_time)
    
    def observe_browser(self):
        """Observe the current state of the browser."""
        if not self.browser or not self.browser.page:
            self.logger.error("Browser not initialized")
            return None
        
        try:
            screenshot_path = self.browser.take_screenshot()
            page_content = self.browser.get_page_content()
            title = self.browser.page.title()
            url = self.browser.page.url
            
            observation = {
                "title": title,
                "url": url,
                "screenshot_path": screenshot_path,
                "content_length": len(page_content) if page_content else 0
            }
            
            self.logger.info(f"Observed browser state: {title} at {url}")
            return observation
        except Exception as e:
            self.logger.error(f"Error observing browser: {str(e)}")
            return None
    
    def observe_desktop(self):
        """Observe the current state of the desktop."""
        if not self.desktop:
            self.logger.error("Desktop handler not initialized")
            return None
        
        try:
            screenshot_path = self.desktop.take_screenshot()
            screen_size = self.desktop.get_screen_size()
            
            observation = {
                "screenshot_path": screenshot_path,
                "screen_size": screen_size
            }
            
            self.logger.info(f"Observed desktop state")
            return observation
        except Exception as e:
            self.logger.error(f"Error observing desktop: {str(e)}")
            return None
    
    def run_session(self, tasks=None):
        """Run a session with multiple tasks."""
        self.logger.info("Starting agent session")
        
        if tasks:
            for task in tasks:
                self.add_task(task)
        
        while self.task_queue:
            execution_plan = self.execute_next_task()
            self.logger.info(f"Completed task with plan: {execution_plan[:100]}...")
            self.dynamic_pause(1.0, 3.0)
        
        self.logger.info("Session completed")
        return True
