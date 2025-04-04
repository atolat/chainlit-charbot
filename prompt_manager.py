import json
from typing import Dict, List, Optional, Tuple
from logger_config import logger
from models import AspectInfo
from config_manager import ConfigManager

class PromptManager:
    def __init__(self):
        logger.info("Initializing PromptManager")
        self.config = ConfigManager()
        self.aspects = self._load_aspects()
        logger.info(f"Initialized {len(self.aspects)} aspects")

    def _load_aspects(self) -> Dict[str, AspectInfo]:
        """Load aspects from JSON file."""
        try:
            with open('aspects.json', 'r') as f:
                aspects_data = json.load(f)
            
            aspects = {}
            for name, data in aspects_data.items():
                aspects[name] = AspectInfo(
                    description=data['description'],
                    examples=data['examples'],
                    system_template=data['system_template'],
                    user_template=data['user_template']
                )
            return aspects
        except Exception as e:
            logger.error(f"Error loading aspects: {e}")
            return {}

    def get_aspect_names(self) -> List[str]:
        """Get list of available aspect names."""
        logger.debug("Getting aspect names")
        return [name for name in self.aspects.keys() if name != 'default']

    def get_aspect_info(self, aspect_name: str) -> AspectInfo:
        """Get information for a specific aspect."""
        logger.debug(f"Getting aspect info for: {aspect_name}")
        return self.aspects.get(aspect_name, self.aspects[self.config.get_default_aspect()])

    def get_action_description(self, aspect_name: str) -> str:
        """Get formatted description for action button."""
        logger.debug(f"Getting action description for: {aspect_name}")
        info = self.aspects[aspect_name]
        return f"{info.description}\n\nExample tasks:\n" + "\n".join(f"• {example}" for example in info.examples)

    def get_confirmation_message(self, aspect_name: str) -> str:
        """Get formatted confirmation message for selected aspect."""
        logger.debug(f"Getting confirmation message for: {aspect_name}")
        info = self.aspects[aspect_name]
        examples = "\n".join(f"• {example}" for example in info.examples[:2])
        return f"""You've selected: {aspect_name}
        
{info.description}

Try asking something like:
{examples}"""

    def get_templates(self, aspect_name: Optional[str]) -> Tuple[str, str]:
        """Get system and user templates for the specified aspect."""
        logger.debug(f"Getting templates for aspect: {aspect_name}")
        if aspect_name is None:
            logger.info("No aspect selected, using default template")
            info = self.aspects[self.config.get_default_aspect()]
        else:
            logger.info(f"Using templates for aspect: {aspect_name}")
            info = self.aspects.get(aspect_name, self.aspects[self.config.get_default_aspect()])
        return info.system_template, info.user_template 