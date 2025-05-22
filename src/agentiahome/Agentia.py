import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, FunctionTool, function_tool
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.run import RunConfig
import asyncio
from openai import OpenAI
import requests


# Load environment variables from .env file
load_dotenv()
GEMINIKEY = os.getenv("GEMINI_KEY")
BASE_URL = os.getenv("BASE_URL")
MODAL = "gemini-2.0-flash"
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
# Tools
@function_tool  
async def lightState() -> str:
    """Tell the state of the light (is it ON or OFF).
    """
    response = requests.get('https://io.adafruit.com/api/v2/Faseeh99/feeds/light/data/last').json()
    if response['value'] == 'ON':
        return "The light is ON"
    elif response['value'] == 'OFF':
        return "The light is OFF"
    else:
        return "Unknown state"
    
@function_tool  
async def FanState() -> str:
    """Tell the state of the Fan (is it ON or OFF).
    """
    response = requests.get('https://io.adafruit.com/api/v2/Faseeh99/feeds/light/data/last').json()
    if response['value'] == 'ON':
        return "The light is ON"
    elif response['value'] == 'OFF':
        return "The light is OFF"
    else:
        return "Unknown state"


# Running the main Function 
async def main():
    agent = Agent(
        name="Linksy",
        instructions="You are helpful Home Assistant, who can control Home Appliances",
        tools=[lightState, read_file],
        model=model
    )

    result = await Runner.run(agent, "Turn of the lights of my room", run_config=config)
    print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())