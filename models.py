from dataclasses import dataclass
from typing import List

@dataclass
class AspectInfo:
    description: str
    examples: List[str]
    system_template: str
    user_template: str 