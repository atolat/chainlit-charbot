from dataclasses import dataclass
from typing import Dict, List
from logger_config import logger

@dataclass
class AspectInfo:
    description: str
    examples: List[str]
    system_template: str
    user_template: str

class PromptManager:
    def __init__(self):
        logger.info("Initializing PromptManager")
        # Default template for when no aspect is selected
        self.default_aspect = AspectInfo(
            description="General purpose AI assistant with balanced capabilities",
            examples=[
                "What can you help me with?",
                "How do you work?",
                "What are your capabilities?"
            ],
            system_template="""You are a helpful AI assistant with expertise in various domains.
Your goal is to provide clear, accurate, and helpful responses while maintaining a friendly tone.
Adapt your communication style based on the user's needs and the complexity of the topic.""",
            user_template="""{input}
Think through your response step by step."""
        )
        logger.debug("Default aspect template created")

        self.aspects = {
            "Concept Simplification": AspectInfo(
                description="Break down complex topics into simple, understandable terms",
                examples=[
                    "Explain quantum computing in simple terms",
                    "How does blockchain work?",
                    "What is machine learning?"
                ],
                system_template="""You are an expert at breaking down complex concepts into simple, understandable terms.
Your goal is to make difficult topics accessible while maintaining accuracy.
Always use clear examples and analogies to illustrate points.""",
                user_template="""Please help me understand this concept: {input}
- What are the key components?
- Can you provide a simple analogy?
- What are common misconceptions?"""
            ),
            "Summarization": AspectInfo(
                description="Extract and present key information concisely",
                examples=[
                    "Summarize the key points of climate change",
                    "Give me a brief overview of the internet's history",
                    "What are the main ideas in this article?"
                ],
                system_template="""You are a skilled summarizer who can extract key information and present it concisely.
Focus on the most important points while maintaining context.
Structure your summaries in a clear, logical manner.""",
                user_template="""Please summarize this information: {input}
- What are the main points?
- What's the key takeaway?
- What context is important to retain?"""
            ),
            "Creativity": AspectInfo(
                description="Generate innovative ideas and unique perspectives",
                examples=[
                    "Generate ideas for a sustainable city",
                    "How could we improve remote work?",
                    "What are some creative solutions to reduce plastic waste?"
                ],
                system_template="""You are a creative thinker who can generate innovative ideas and solutions.
Think outside the box while staying relevant to the topic.
Encourage creative exploration and unique perspectives.""",
                user_template="""Let's explore this creatively: {input}
- What are some unique perspectives?
- How can we approach this differently?
- What innovative solutions can we consider?"""
            ),
            "Narrative Structure": AspectInfo(
                description="Organize information into compelling stories",
                examples=[
                    "Help me structure a story about time travel",
                    "Organize the history of AI as a narrative",
                    "How can I make this presentation more engaging?"
                ],
                system_template="""You are an expert in storytelling and narrative organization.
Help structure information in a compelling, story-like format.
Focus on flow, progression, and engagement in your responses.""",
                user_template="""Help me structure this as a narrative: {input}
- What's the main story arc?
- How can we make it more engaging?
- What elements would enhance the flow?"""
            ),
            "Arithmetic Reasoning": AspectInfo(
                description="Solve mathematical problems step by step",
                examples=[
                    "Calculate compound interest on $1000 at 5% for 3 years",
                    "If a train travels at 60 mph for 2.5 hours, how far does it go?",
                    "What's the probability of getting three heads in a row?"
                ],
                system_template="""You are a mathematical reasoning expert who can solve problems step by step.
Break down complex calculations into manageable parts.
Explain your mathematical thinking clearly and thoroughly.""",
                user_template="""Let's solve this step by step: {input}
- What's the first step?
- What formulas or methods should we use?
- How can we verify the answer?"""
            ),
            "Conversational Tone": AspectInfo(
                description="Engage in natural, friendly discussions",
                examples=[
                    "Tell me about your favorite book",
                    "What's your opinion on artificial intelligence?",
                    "How do you feel about remote work?"
                ],
                system_template="""You are a friendly and engaging conversational partner.
Maintain a natural, warm tone while being informative.
Adapt your communication style to match the user's level of expertise.""",
                user_template="""Let's discuss this: {input}
- What's your perspective?
- Can you explain this in simple terms?
- How does this relate to everyday experience?"""
            )
        }
        logger.info(f"Initialized {len(self.aspects)} aspects")

    def get_aspect_names(self) -> List[str]:
        """Get list of available aspect names."""
        logger.debug("Getting aspect names")
        return list(self.aspects.keys())

    def get_aspect_info(self, aspect_name: str) -> AspectInfo:
        """Get information for a specific aspect."""
        logger.debug(f"Getting aspect info for: {aspect_name}")
        return self.aspects.get(aspect_name, self.default_aspect)

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

    def get_templates(self, aspect_name: str | None) -> tuple[str, str]:
        """Get system and user templates for an aspect."""
        if aspect_name is None:
            logger.info("No aspect selected, using default template")
            info = self.default_aspect
        else:
            logger.info(f"Using templates for aspect: {aspect_name}")
            info = self.aspects.get(aspect_name, self.default_aspect)
        return info.system_template, info.user_template 