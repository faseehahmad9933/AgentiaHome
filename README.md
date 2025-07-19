# Basheer: Your Smart Home Assistant 🚀🤖  [Opensourced]

Basheer is an intelligent, conversational home assistant that lets you control and monitor your smart home devices using natural language. Powered by modern LLMs (OpenAI/Gemini) and Chainlit, Basheer makes home automation simple, friendly, and fun!

---

## 🌟 Features

- **Conversational Home Automation:**
  - Control lights and fans, check their status, and monitor room temperature/humidity using natural language.
- **Task Scheduling:**
  - Schedule actions (e.g., "Turn off the fan in 10 minutes") with delayed execution.
- **Real-Time Feedback:**
  - Get instant confirmation and status updates for your commands.
- **Extensible Toolset:**
  - Easily add new device controls or sensors as Python async functions.
- **Modern LLM Integration:**
  - Uses OpenAI or Gemini models for natural language understanding.
- **Chainlit UI:**
  - Friendly web-based chat interface for user interaction.

---

## 🛠️ Available Commands/Tools

- **TurnOnTheLight / TurnOffTheLight:**  Switch lights on or off.
- **TurnOnTheFan / TurnOffTheFan:**  Switch fans on or off.
- **lightState / FanState:**  Query the current state (on/off) of lights or fans.
- **RoomTemperature / RoomHumidity:**  Get the latest temperature or humidity reading.
- **ShedulerFunction:**  Schedule any of the above actions to run after a specified delay.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd AgentiaHome
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
Or, if using PEP 621/pyproject.toml:
```bash
pip install .
```

### 3. Set up environment variables
Create a `.env` file in the project root with:
```
AGENTOPS_API_KEY=your_agentops_api_key
GEMINI_KEY=your_gemini_api_key
BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```
(You can get your Adafruit IO key from your Adafruit account.)

### 4. Run the app
```bash
chainlit run chatbot.py
```
Then open the provided local URL in your browser.

---

## 💬 Usage Examples

- `Turn on the light`
- `Turn off the fan in 10 minutes`
- `What's the temperature?`
- `Is the light on?`

Basheer will respond, execute the action, and confirm.

---

## 👨‍💻 Developer

- **Author:** Faseeh Ahmad  
- **Contact:** faseehkamboh9933@gmail.com

---

## ⚠️ License & Notice

- This project is entirely open-source and ready to be utilized as a foundational template for your next undertaking.
- We encourage you to credit the original developer when showcasing this code on social platforms. Your recognition helps foster our open-source community!- 
- 
---

Happy tinkering with Basheer Bhai! 💻😊
