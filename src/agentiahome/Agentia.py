import os
from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents.run import RunConfig
import asyncio
from openai import OpenAI

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

# Running the main Function 
async def main():
    agent = Agent(
        name="Linksy",
        instructions="You are helpful Home Assistant, who can control Home Appliances",
        model=model
    )

    result = await Runner.run(agent, "Turn of the lights of my room", run_config=config)
    print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())