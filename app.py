# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion
import os
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from dotenv import load_dotenv
from prompt_manager import PromptManager
from logger_config import logger

load_dotenv()
logger.info("Environment variables loaded")

# Initialize prompt manager
prompt_manager = PromptManager()

# Aspect descriptions and examples
ASPECT_INFO = {
    "Concept Simplification": {
        "description": "Break down complex topics into simple, understandable terms",
        "examples": [
            "Explain quantum computing in simple terms",
            "How does blockchain work?",
            "What is machine learning?"
        ]
    },
    "Summarization": {
        "description": "Extract and present key information concisely",
        "examples": [
            "Summarize the key points of climate change",
            "Give me a brief overview of the internet's history",
            "What are the main ideas in this article?"
        ]
    },
    "Creativity": {
        "description": "Generate innovative ideas and unique perspectives",
        "examples": [
            "Generate ideas for a sustainable city",
            "How could we improve remote work?",
            "What are some creative solutions to reduce plastic waste?"
        ]
    },
    "Narrative Structure": {
        "description": "Organize information into compelling stories",
        "examples": [
            "Help me structure a story about time travel",
            "Organize the history of AI as a narrative",
            "How can I make this presentation more engaging?"
        ]
    },
    "Arithmetic Reasoning": {
        "description": "Solve mathematical problems step by step",
        "examples": [
            "Calculate compound interest on $1000 at 5% for 3 years",
            "If a train travels at 60 mph for 2.5 hours, how far does it go?",
            "What's the probability of getting three heads in a row?"
        ]
    },
    "Conversational Tone": {
        "description": "Engage in natural, friendly discussions",
        "examples": [
            "Tell me about your favorite book",
            "What's your opinion on artificial intelligence?",
            "How do you feel about remote work?"
        ]
    }
}

# Aspect-specific system templates
ASPECT_TEMPLATES = {
    "Concept Simplification": """You are an expert at breaking down complex concepts into simple, understandable terms.
Your goal is to make difficult topics accessible while maintaining accuracy.
Always use clear examples and analogies to illustrate points.""",
    
    "Summarization": """You are a skilled summarizer who can extract key information and present it concisely.
Focus on the most important points while maintaining context.
Structure your summaries in a clear, logical manner.""",
    
    "Creativity": """You are a creative thinker who can generate innovative ideas and solutions.
Think outside the box while staying relevant to the topic.
Encourage creative exploration and unique perspectives.""",
    
    "Narrative Structure": """You are an expert in storytelling and narrative organization.
Help structure information in a compelling, story-like format.
Focus on flow, progression, and engagement in your responses.""",
    
    "Arithmetic Reasoning": """You are a mathematical reasoning expert who can solve problems step by step.
Break down complex calculations into manageable parts.
Explain your mathematical thinking clearly and thoroughly.""",
    
    "Conversational Tone": """You are a friendly and engaging conversational partner.
Maintain a natural, warm tone while being informative.
Adapt your communication style to match the user's level of expertise."""
}

# Aspect-specific user templates
USER_TEMPLATES = {
    "Concept Simplification": """Please help me understand this concept: {input}
- What are the key components?
- Can you provide a simple analogy?
- What are common misconceptions?""",
    
    "Summarization": """Please summarize this information: {input}
- What are the main points?
- What's the key takeaway?
- What context is important to retain?""",
    
    "Creativity": """Let's explore this creatively: {input}
- What are some unique perspectives?
- How can we approach this differently?
- What innovative solutions can we consider?""",
    
    "Narrative Structure": """Help me structure this as a narrative: {input}
- What's the main story arc?
- How can we make it more engaging?
- What elements would enhance the flow?""",
    
    "Arithmetic Reasoning": """Let's solve this step by step: {input}
- What's the first step?
- What formulas or methods should we use?
- How can we verify the answer?""",
    
    "Conversational Tone": """Let's discuss this: {input}
- What's your perspective?
- Can you explain this in simple terms?
- How does this relate to everyday experience?"""
}

@cl.on_chat_start
async def start_chat():
    logger.info("Starting new chat session")
    # Create aspect selection buttons with descriptions
    aspects = prompt_manager.get_aspect_names()
    actions = []
    
    for aspect in aspects:
        actions.append(
            cl.Action(
                name=aspect,
                value=aspect,
                label=aspect,
                description=prompt_manager.get_action_description(aspect)
            )
        )
    
    # Send welcome message with aspect selection
    await cl.Message(
        content="Welcome! Please select an aspect for our conversation. Hover over each option to see examples and descriptions:",
        actions=actions
    ).send()
    logger.info("Welcome message sent with aspect selection buttons")

@cl.action_callback("Concept Simplification")
@cl.action_callback("Summarization")
@cl.action_callback("Creativity")
@cl.action_callback("Narrative Structure")
@cl.action_callback("Arithmetic Reasoning")
@cl.action_callback("Conversational Tone")
async def on_action(action):
    # Store the selected aspect in the user session
    cl.user_session.set("selected_aspect", action.value)
    logger.info(f"User selected aspect: {action.value}")
    
    # Send confirmation message with examples
    await cl.Message(
        content=prompt_manager.get_confirmation_message(action.value)
    ).send()
    logger.debug(f"Confirmation message sent for aspect: {action.value}")

@cl.on_message
async def main(message: cl.Message):
    # Get the selected aspect from the session
    selected_aspect = cl.user_session.get("selected_aspect")
    logger.info(f"Processing message with aspect: {selected_aspect}")
    logger.debug(f"User message: {message.content}")
    
    settings = {
        "model": "gpt-4-turbo-preview",  # Upgraded to GPT-4 Turbo
        "temperature": 0.7,  # Balanced between creativity and consistency
        "max_tokens": 1000,  # Increased for more detailed responses
        "top_p": 0.9,  # Slightly reduced for more focused responses
        "frequency_penalty": 0.3,  # Added to reduce repetition
        "presence_penalty": 0.3,  # Added to encourage diverse topics
    }
    logger.debug(f"OpenAI settings: {settings}")

    client = AsyncOpenAI()

    # Get the appropriate templates for the selected aspect
    system_template, user_template = prompt_manager.get_templates(selected_aspect)
    logger.debug("Templates retrieved for message processing")

    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="system",
                template=system_template,
                formatted=system_template,
            ),
            PromptMessage(
                role="user",
                template=user_template,
                formatted=user_template.format(input=message.content),
            ),
        ],
        inputs={"input": message.content},
        settings=settings,
    )
    logger.debug("Prompt created for OpenAI API call")

    msg = cl.Message(content="")
    logger.info("Starting OpenAI API call")

    try:
        # Call OpenAI
        async for stream_resp in await client.chat.completions.create(
            messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
        ):
            token = stream_resp.choices[0].delta.content
            if not token:
                token = ""
            await msg.stream_token(token)
        
        # Update the prompt object with the completion
        prompt.completion = msg.content
        msg.prompt = prompt

        # Send and close the message stream
        await msg.send()
        logger.info("Response successfully sent to user")
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {str(e)}")
        await cl.Message(
            content="I apologize, but I encountered an error processing your request. Please try again."
        ).send()