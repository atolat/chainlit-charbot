import json
from typing import Dict, Any
from logger_config import logger

class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open('config.json', 'r') as f:
                self._config = json.load(f)
            logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Set default configuration
            self._config = {
                "model": {
                    "name": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "top_p": 1.0,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0
                },
                "default_aspect": "default"
            }

    def get_model_config(self) -> Dict[str, Any]:
        """Get model configuration settings."""
        return self._config.get("model", {})

    def get_default_aspect(self) -> str:
        """Get default aspect name."""
        return self._config.get("default_aspect", "default") 