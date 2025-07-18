import datetime
import time
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, FunctionTool, function_tool, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, output_guardrail
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.run import RunConfig
import asyncio
from openai import OpenAI
from openai.types.responses import ResponseTextDeltaEvent
import requests
import chainlit as cl
import json
import time
import re
from Tools import lightState, FanState, RoomTemperature, RoomHumidity, TurnOnTheFan, TurnOffTheFan, TurnOffTheLight, TurnOnTheLight, ShedulerFunction

# Load environment variables from .env file
load_dotenv()
GEMINIKEY = "AIzaSyBLLjLgbNo3RtnwM3iP5Fs_OjeV7zUthzM" or os.getenv("GEMINI_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/" or os.getenv("BASE_URL")
MODAL = "gemini-2.5-flash-preview-05-20"
if not GEMINIKEY:    
    raise ValueError("GEMINI_KEY not found in environment variables")
if not BASE_URL:
    raise ValueError("BASE_URL not found in environment variables")

# Declaring Client, Modal, and Config 
client = AsyncOpenAI(
    api_key=GEMINIKEY,
    base_url=BASE_URL
)
model = OpenAIChatCompletionsModel(
    model=MODAL,
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

def parse_scheduling_request(user_input: str) -> tuple[str, int]:
    """
    Parse natural language scheduling requests to extract action and time.
    Returns: (action, time_in_seconds)
    """
    user_input = user_input.lower().strip()
    
    # Time patterns
    time_patterns = {
        r'(\d+)\s*minute': lambda x: int(x) * 60,
        r'(\d+)\s*min': lambda x: int(x) * 60,
        r'(\d+)\s*hour': lambda x: int(x) * 3600,
        r'(\d+)\s*hr': lambda x: int(x) * 3600,
        r'(\d+)\s*second': lambda x: int(x),
        r'(\d+)\s*sec': lambda x: int(x),
        r'(\d+)\s*day': lambda x: int(x) * 86400,
    }
    
    # Extract time
    time_seconds = 60  # default 1 minute
    for pattern, converter in time_patterns.items():
        match = re.search(pattern, user_input)
        if match:
            time_seconds = converter(match.group(1))
            break
    
    # Extract action (remove scheduling words and time references)
    action = user_input
    scheduling_words = ['schedule', 'scheduled', 'in', 'after', 'later', 'set', 'timer']
    for word in scheduling_words:
        action = action.replace(word, '').strip()
    
    # Remove time patterns from action
    for pattern in time_patterns.keys():
        action = re.sub(pattern, '', action).strip()
    
    # Clean up action
    action = re.sub(r'\s+', ' ', action).strip()
    
    return action, time_seconds

@cl.on_chat_start
async def main():
    # Initialize the agent first
    agent = Agent(
        name="Basheer",
        instructions="""You are Basheer, an intelligent and friendly Home Assistant Agent. You can control home appliances and provide real-time information about your smart home.

**Your Capabilities:**
🔆 **Light Control**: Turn lights on/off in any room
💨 **Fan Control**: Control room fans and ventilation  
🌡️ **Temperature Monitoring**: Check room temperature in real-time
⏰ **Task Scheduling**: Schedule any action to happen later (e.g., "turn off lights in 30 minutes")

**How to Help Users:**
1. **Direct Commands**: "Turn on the light", "Check temperature", "Turn off fan"
2. **Scheduling**: "Turn on light in 5 minutes", "Turn off fan in 1 hour"
3. **Status Checks**: "What's the temperature?", "Is the light on?"
4. **Natural Language**: Understand various ways users might phrase requests

**Important Guidelines:**
- Always use the appropriate tools to perform actions
- Be helpful, friendly, and confirm actions when completed
- If a user wants to schedule something, extract the action and time from their request
- Provide clear, concise responses with emojis for better user experience
- If you encounter an error, try to understand what the user wants and use the correct tool

**Available Tools:**
- TurnOnTheLight, TurnOffTheLight
- TurnOnTheFan, TurnOffTheFan  
- FanState, lightState, RoomTemperature
- ShedulerFunction (for delayed execution)

Remember: You're here to make home automation simple and enjoyable! 😊""",
        tools=[TurnOffTheFan, TurnOnTheLight, TurnOffTheLight, TurnOnTheFan, FanState, lightState, RoomTemperature, ShedulerFunction,RoomHumidity],
        model=model
    )
    
    # Store the agent in the session
    cl.user_session.set("agent", agent)
    cl.user_session.set("memory", [])  # Add memory list to session
    
    # Send welcome message after a small delay to ensure it appears after Chainlit's welcome
    await asyncio.sleep(1)
    await cl.Message(
        content="Hello! I am Basheer, your Home Assistant. How can I assist you today?"
    ).send()

# result = await Runner.run(agent, "Turn of the lights of my room", run_config=config)
    # print(result.final_output)
@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    memory = cl.user_session.get("memory")  # Get memory list

    # Optionally, pass memory to agent (if agent supports it)
    agent.memory = memory

    
    # Append user message and agent response to memory
    memory.append({"role": "user", "content": message.content})
    # Process the message with the agent
    result = await Runner.run_streamed(agent,memory, run_config=config)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
    memory.append({"role": "assistant", "content": result.final_output})

    cl.user_session.set("memory", memory)
    # Send the response back to the user
    await cl.Message(content=result.final_output).send()
