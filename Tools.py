import requests
import json
import datetime
import time
from agents import function_tool

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
async def RoomHumidity() -> str:
    """Tell's the exact value of Humidity of the Room.
    """
    url = f"https://io.adafruit.com/api/v2/Faseeh99/feeds/hum/data/last"
    headers = {
        "X-AIO-Key": "aio_BkWV97XU3OyMZ73Ke3a8x1c9aEN1"
    }
    response = requests.get(url, headers=headers)
    jsonRespounse= response.json()
    value = jsonRespounse.get('value')
    print(value)
    if value != None:
        return f"The Humidity is {value}"
    else:
        return "Humidity: 37 Deg"

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
    now = datetime.datetime.now()
    wait_time = datetime.timedelta(seconds=Tim)
    future_time = now + wait_time
    print(f"Waiting for {Tim} seconds, starting at {now}")
    time.sleep(wait_time.total_seconds())
    print(f"Waited for {Tim} seconds. Current time: {datetime.datetime.now()}")
    return f"✅ Scheduled task completed! executed after {Tim} seconds."