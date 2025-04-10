import logging
import os
from datetime import datetime

class Logger:
    """Custom logger for the slow agent."""
    
    def __init__(self, name="slow_agent", log_level=logging.INFO):
        """Initialize the logger."""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Clear any existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create file handler with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler(f"logs/{name}_{timestamp}.log")
        file_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        """Log info message."""
        self.logger.info(message)
    
    def error(self, message):
        """Log error message."""
        self.logger.error(message)
    
    def warning(self, message):
        """Log warning message."""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)
