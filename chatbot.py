import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, FunctionTool, function_tool
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.run import RunConfig
import asyncio
from openai import OpenAI
import requests
import chainlit as cl
import json
import time
import re

# Load environment variables from .env file
load_dotenv()
GEMINIKEY = "AIzaSyBLLjLgbNo3RtnwM3iP5Fs_OjeV7zUthzM" or os.getenv("GEMINI_KEY")
BASE_URL = os.getenv("BASE_URL")
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

# Tools
@function_tool  
async def lightState() -> str:
    """Tell the state of the light (is it ON or OFF).
    """
    url = f"https://io.adafruit.com/api/v2/Faseeh99/feeds/light/data/last"

    headers = {
    "X-AIO-Key": "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    }
    response = requests.get(url, headers=headers)
    jsonRespounse= response.json()
    value = jsonRespounse.get('value')
    print(value)
    if value == '1':
        return "The light is ON"
    elif value == '0':
        return "The light is OFF"
    else:
        return "Unknown state"
    
@function_tool  
async def FanState() -> str:
    """Tell the state of the Fan (is it ON or OFF).
    """
    url = f"https://io.adafruit.com/api/v2/Faseeh99/feeds/fan/data/last"

    headers = {
    "X-AIO-Key": "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    }
    response = requests.get(url, headers=headers)
    jsonRespounse= response.json()
    value = jsonRespounse.get('value')
    print(value)
    if value == '1':
        return "The Fan is ON"
    elif value == '0':
        return "The Fan is OFF"
    else:
        return "Unknown state"

@function_tool  
async def RoomTemperature() -> str:
    """Tell's the exact value of Temperature the Room Temperature.
    """
    url = f"https://io.adafruit.com/api/v2/Faseeh99/feeds/sensor/data/last"

    headers = {
    "X-AIO-Key": "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    }
    response = requests.get(url, headers=headers)
    jsonRespounse= response.json()
    value = jsonRespounse.get('value')
    print(value)
    if value != None:
        return f"The Temperature is {value}"
    else:
        return "Temperture: 37 Deg"

@function_tool  
async def TurnOnTheFan() -> str:
    """change the state of Fan to 1 (i.e ON).
    """
    USERNAME = "Faseeh99"
    AIO_KEY = "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    FEED_KEY = "fan"

    url = f"https://io.adafruit.com/api/v2/{USERNAME}/feeds/{FEED_KEY}/data"

    headers = {
        "Content-Type": "application/json",
        "X-AIO-Key": AIO_KEY
    }

    payload = {
        "value": "1"  # or "0", depending on what you want to send
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Handle the response
    if response.status_code in (200, 201):
        print("Feed updated successfully:")
        print(response.json())
        return "Fan turned ON successfully."
    else:
        print("Failed to update feed:")
        print(response.status_code, response.text)
        return "Failed to turn ON the Fan."
    
@function_tool
async def TurnOffTheFan() -> str:
    """change the state of Fan to 0 (i.e OFF).
    """
    USERNAME = "Faseeh99"
    AIO_KEY = "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    FEED_KEY = "fan"

    url = f"https://io.adafruit.com/api/v2/{USERNAME}/feeds/{FEED_KEY}/data"

    headers = {
        "Content-Type": "application/json",
        "X-AIO-Key": AIO_KEY
    }

    payload = {
        "value": "0"  # or "1", depending on what you want to send
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Handle the response
    if response.status_code in (200, 201):
        print("Feed updated successfully:")
        print(response.json())
        return "Fan turned OFF successfully."
    else:
        print("Failed to update feed:")
        print(response.status_code, response.text)
        return "Failed to turn OFF the Fan."
    

@function_tool  
async def TurnOffTheLight() -> str:
    """change the state of Light to 0 (i.e OFF).
    """
    USERNAME = "Faseeh99"
    AIO_KEY = "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    FEED_KEY = "light"

    url = f"https://io.adafruit.com/api/v2/{USERNAME}/feeds/{FEED_KEY}/data"

    headers = {
        "Content-Type": "application/json",
        "X-AIO-Key": AIO_KEY
    }

    payload = {
        "value": "0"  # or "0", depending on what you want to send
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Handle the response
    if response.status_code in (200, 201):
        print("Feed updated successfully:")
        print(response.json())
        return "Light turned OFF successfully."
    else:
        print("Failed to update feed:")
        print(response.status_code, response.text)
        return "Failed to turn OFF the Light."
    
@function_tool  
async def TurnOnTheLight() -> str:
    """change the state of Light to 1 (i.e ON).
    """
    USERNAME = "Faseeh99"
    AIO_KEY = "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    FEED_KEY = "light"

    url = f"https://io.adafruit.com/api/v2/{USERNAME}/feeds/{FEED_KEY}/data"

    headers = {
        "Content-Type": "application/json",
        "X-AIO-Key": AIO_KEY
    }

    payload = {
        "value": "1"  # or "0", depending on what you want to send
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Handle the response
    if response.status_code in (200, 201):
        print("Feed updated successfully:")
        print(response.json())
        return "Light turned ON successfully."
    else:
        print("Failed to update feed:")
        print(response.status_code, response.text)
        return "Failed to turn ON the Light."

@function_tool  
async def ShedulerFunction(FuncName: str, Tim: int) -> str:
    """
    Schedule a home automation task to be executed after a specified delay.
    Args:
        FuncName: Function name or natural language description (e.g., 'turn on light', 'TurnOnTheLight')
        Tim: Time in seconds to wait before execution
    """
    # Map natural language phrases to function names
    phrase_map = {
        # Light controls
        "turn on light": "TurnOnTheLight",
        "turn on the light": "TurnOnTheLight",
        "switch on light": "TurnOnTheLight",
        "light on": "TurnOnTheLight",
        "turn off light": "TurnOffTheLight", 
        "turn off the light": "TurnOffTheLight",
        "switch off light": "TurnOffTheLight",
        "light off": "TurnOffTheLight",
        # Fan controls
        "turn on fan": "TurnOnTheFan",
        "turn on the fan": "TurnOnTheFan", 
        "switch on fan": "TurnOnTheFan",
        "fan on": "TurnOnTheFan",
        "turn off fan": "TurnOffTheFan",
        "turn off the fan": "TurnOffTheFan",
        "switch off fan": "TurnOffTheFan", 
        "fan off": "TurnOffTheFan",
        # Status checks
        "check light": "lightState",
        "light status": "lightState",
        "check fan": "FanState",
        "fan status": "FanState",
        "temperature": "RoomTemperature",
        "room temperature": "RoomTemperature",
        "check temperature": "RoomTemperature"
    }
    
    # Normalize input and find the function
    normalized = FuncName.strip().lower()
    mapped_func_name = phrase_map.get(normalized, FuncName)
    
    # Map function names to function_tool objects
    function_map = {
        "TurnOnTheLight": TurnOnTheLight,
        "TurnOffTheLight": TurnOffTheLight,
        "TurnOnTheFan": TurnOnTheFan,
        "TurnOffTheFan": TurnOffTheFan,
        "FanState": FanState,
        "lightState": lightState,
        "RoomTemperature": RoomTemperature,
    }
    
    func = function_map.get(mapped_func_name)
    if not func:
        available_functions = ", ".join(list(phrase_map.keys())[:5]) + "..."
        return f"❌ Function '{FuncName}' not found. Available options: {available_functions}"
    
    # Convert time to human-readable format
    time_str = f"{Tim} seconds"
    if Tim >= 60:
        minutes = Tim // 60
        seconds = Tim % 60
        if seconds == 0:
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''}"
        else:
            time_str = f"{minutes} minute{'s' if minutes > 1 else ''} and {seconds} second{'s' if seconds > 1 else ''}"
    
    # Schedule the task
    await asyncio.sleep(Tim)
    result = await func()
    
    return f"✅ Scheduled task completed! {mapped_func_name} executed after {time_str}. Result: {result}"

@cl.on_chat_start
async def main():
    # Initialize the agent first
    agent = Agent(
        name="Linksy",
        instructions="""You are Linksy, an intelligent and friendly Home Assistant Agent. You can control home appliances and provide real-time information about your smart home.

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

**For Scheduling Requests:**
- When users want to schedule something, extract the action and time from their request
- Use ShedulerFunction with the extracted action and time in seconds
- Common scheduling phrases: "schedule to...", "in X minutes", "after X hours", "turn on/off in..."
- Examples:
  * "schedule to turn on the light in one minute" → ShedulerFunction("turn on light", 60)
  * "turn off fan in 30 minutes" → ShedulerFunction("turn off fan", 1800)
  * "check temperature in 5 minutes" → ShedulerFunction("check temperature", 300)

**Important Guidelines:**
- Always use the appropriate tools to perform actions
- For scheduling, use ShedulerFunction with natural language descriptions
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
        tools=[TurnOffTheFan, TurnOnTheLight, TurnOffTheLight, TurnOnTheFan, FanState, lightState, RoomTemperature, ShedulerFunction],
        model=model
    )
    
    # Store the agent in the session
    cl.user_session.set("agent", agent)
    
    # Send welcome message after a small delay to ensure it appears after Chainlit's welcome
    await asyncio.sleep(0.5)
    await cl.Message(
        content="Hello! I am your Home Assistant. How can I assist you today?"
    ).send()

# result = await Runner.run(agent, "Turn of the lights of my room", run_config=config)
    # print(result.final_output)
@cl.on_message
async def on_message(message: cl.Message):
    # Get the agent from the session
    agent = cl.user_session.get("agent")
    
    # Process the message with the agent
    result = await Runner.run(agent, message.content, run_config=config)
    
    # Send the response back to the user
    await cl.Message(content=result.final_output).send()

if __name__ == "__main__":
    asyncio.run(main())