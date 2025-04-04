# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion
import os
from openai import AsyncOpenAI, OpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from dotenv import load_dotenv
from prompt_manager import PromptManager
from logger_config import logger

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize PromptManager
prompt_manager = PromptManager()

@cl.on_chat_start
async def start():
    logger.info("Starting new chat session")
    await cl.Message(
        content="Welcome! I'm your AI assistant. How can I help you today?",
    ).send()

@cl.on_message
async def main(message: cl.Message):
    logger.info(f"Received message: {message.content}")
    
    # Get the current aspect from the session
    current_aspect = cl.user_session.get("current_aspect")
    logger.debug(f"Current aspect: {current_aspect}")
    
    # Get templates based on the current aspect
    system_template, user_template = prompt_manager.get_templates(current_aspect)
    logger.debug("Retrieved templates from PromptManager")
    
    # Format the user message with the template
    formatted_message = user_template.format(input=message.content)
    logger.debug("Formatted user message with template")
    
    # Create messages for the API call
    messages = [
        {"role": "system", "content": system_template},
        {"role": "user", "content": formatted_message}
    ]
    logger.debug("Created messages for API call")
    
    # Send message to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    logger.info("Received response from OpenAI")
    
    # Send response back to user
    await cl.Message(
        content=response.choices[0].message.content
    ).send()
    logger.debug("Sent response to user")

@cl.action_callback("select_aspect")
async def on_action(action):
    logger.info(f"Action selected: {action.value}")
    
    # Store the selected aspect in the session
    cl.user_session.set("current_aspect", action.value)
    logger.debug(f"Stored aspect in session: {action.value}")
    
    # Get confirmation message
    confirmation = prompt_manager.get_confirmation_message(action.value)
    logger.debug("Generated confirmation message")
    
    # Send confirmation message
    await cl.Message(
        content=confirmation
    ).send()
    logger.debug("Sent confirmation message")
    
    # Remove the action buttons
    await action.remove()
    logger.debug("Removed action buttons")

@cl.on_chat_start
async def show_aspect_buttons():
    logger.info("Showing aspect selection buttons")
    
    # Create action buttons for each aspect
    actions = [
        cl.Action(
            name=f"select_aspect",
            value=aspect_name,
            label=aspect_name,
            description=prompt_manager.get_action_description(aspect_name)
        )
        for aspect_name in prompt_manager.get_aspect_names()
    ]
    logger.debug(f"Created {len(actions)} action buttons")
    
    # Send message with action buttons
    await cl.Message(
        content="Select an aspect to customize my behavior:",
        actions=actions
    ).send()
    logger.debug("Sent message with action buttons")