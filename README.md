---
title: Chainlit Bot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# Chainlit Bot

A versatile chatbot powered by Chainlit and OpenAI's GPT-4 Turbo, featuring multiple conversation aspects and a clean, maintainable codebase.

## Features

- 🤖 Powered by OpenAI's GPT-4 Turbo
- 🎯 Multiple conversation aspects:
  - Concept Simplification
  - Summarization
  - Creativity
  - Narrative Structure
  - Arithmetic Reasoning
  - Conversational Tone
- 🔄 Default template for general conversations
- 📝 Comprehensive logging system
- 🎨 Clean, modular codebase

## Usage

1. Select a conversation aspect using the buttons at the top
2. Start chatting with the bot
3. The bot will respond according to the selected aspect's style

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your OpenAI API key
4. Run the app: `chainlit run app.py`

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key

## License

MIT