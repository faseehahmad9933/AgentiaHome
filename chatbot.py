import datetime
import time
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel,trace, FunctionTool, function_tool, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, output_guardrail
from dotenv import load_dotenv
from openai import AsyncOpenAI
import agentops 
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
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY") or "7a3b48f7-ba78-47b5-b73b-57cf55d17525"
GEMINIKEY = "AIzaSyBLLjLgbNo3RtnwM3iP5Fs_OjeV7zUthzM" or os.getenv("GEMINI_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/" or os.getenv("BASE_URL")
MODAL = "gemini-2.5-flash-preview-05-20"
agentops.init(
    api_key=AGENTOPS_API_KEY,
    default_tags=['openai agents sdk']
)
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


@cl.on_chat_start
async def main():
    TaskSheduler = Agent(name = "TaskSheduler",
    instructions = """Give the name of the fuction tool and delaytime to the [ShedulerFunction] Tool,then call the specific tool as told by [ShedulerFunction]. 
    For Example: You gave these two arguments to the Sheduler Function [TurnOnTheLight,3] 
    Now, After the delaytime completed (After 3 Seconds), Sheduler Function returns:
    "Time to do Scheduled task! Call the Function Tool [TurnOffTheFan]"
    then call [TurnOffTheFan] tool from your toolset.

    Similarly Second Example: You gave these two arguments to the Sheduler Function [TurnOnTheLight,5]
    Now, After the delaytime completed (After 5 Seconds), Sheduler Function returns:
    "Time to do Scheduled task! Call the Function Tool [TurnOnTheLight]"
    then call [TurnOnTheLight] tool from your toolset.

    Understand the request and use the tools.""",
    tools=[ShedulerFunction, TurnOffTheFan, TurnOnTheLight, TurnOffTheLight, TurnOnTheFan, FanState, lightState, RoomTemperature,RoomHumidity],
        model=model)
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
        tools=[TaskSheduler.as_tool(
            tool_name="TaskSheduler",
            tool_description="Shedules a task, and ends up when the task is completed",
        ),TurnOffTheFan, TurnOnTheLight, TurnOffTheLight, TurnOnTheFan, FanState, lightState, RoomTemperature,RoomHumidity],
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
    # Create a trace for the code review workflow
    with trace("Assistant-workflow") as review_trace:
        # # Start monitoring the agent
        # with agentops.monitor():
        result = Runner.run_streamed(agent,memory, run_config=config)
        msg = cl.Message(content="")
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # print(event.data.delta, end="", flush=True) 
                await msg.stream_token(event.data.delta)
            # if token := event.choices[0].delta.content or "":
    memory.append({"role": "assistant", "content": result.final_output})

    cl.user_session.set("memory", memory)
    # Send the response back to the user
    # await cl.Message(content=result.final_output).send()
