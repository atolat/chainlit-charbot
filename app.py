# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion
import os
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from dotenv import load_dotenv

load_dotenv()

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
    # Create aspect selection buttons
    aspects = list(ASPECT_TEMPLATES.keys())
    actions = [
        cl.Action(name=aspect, value=aspect, label=aspect)
        for aspect in aspects
    ]
    
    # Send welcome message with aspect selection
    await cl.Message(
        content="Welcome! Please select an aspect for our conversation:",
        actions=actions
    ).send()

@cl.action_callback("Concept Simplification")
@cl.action_callback("Summarization")
@cl.action_callback("Creativity")
@cl.action_callback("Narrative Structure")
@cl.action_callback("Arithmetic Reasoning")
@cl.action_callback("Conversational Tone")
async def on_action(action):
    # Store the selected aspect in the user session
    cl.user_session.set("selected_aspect", action.value)
    
    # Send confirmation message
    await cl.Message(
        content=f"You've selected: {action.value}. How can I help you today?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    # Get the selected aspect from the session
    selected_aspect = cl.user_session.get("selected_aspect")
    
    if not selected_aspect:
        await cl.Message(
            content="Please select an aspect first using the buttons above."
        ).send()
        return

    settings = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,  # Slightly increased for more varied responses
        "max_tokens": 500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    client = AsyncOpenAI()

    # Get the appropriate templates for the selected aspect
    system_template = ASPECT_TEMPLATES[selected_aspect]
    user_template = USER_TEMPLATES[selected_aspect]

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

    msg = cl.Message(content="")

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