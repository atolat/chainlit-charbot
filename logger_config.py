import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
def setup_logger():
    # Create a logger
    logger = logging.getLogger("chainlit_chatbot")
    logger.setLevel(logging.INFO)
    
    # Create handlers
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler - log to file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(f"logs/chatbot_{timestamp}.log")
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatters and add it to handlers
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Create and export the logger
logger = setup_logger() 