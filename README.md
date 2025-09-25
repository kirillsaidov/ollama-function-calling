# Ollama Function Calling for Dummies

This is a simple, beginner-friendly example showing how to use **function calling** with Ollama.

## What this example does

This project demonstrates the complete workflow for function calling with Ollama:

1. **Create a custom function** (`get_stock_price`) that fetches real stock prices
2. **Register the function** with Ollama so the LLM knows it exists
3. **Handle tool calls** when the LLM decides it needs to use your function
4. **Feed results back** to the LLM so it can generate a natural, coherent response
5. **Avoid raw output** – the LLM explains the results instead of just dumping numbers

Instead of getting a raw response like `175.42`, you get a helpful answer like *"Apple's current stock price is $175.42 per share."*

## Quick start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- The `qwen3:4b-instruct` model (or modify the code for your preferred model)

### Installation
#### Clone repo
```sh
git clone https://github.com/kirillsaidov/ollama-function-calling.git
cd ollama-function-calling
```
#### Install dependencies
```sh
python3 -m venv venv
./venv/bin/pip install ollama yfinance
```

### Run the example
```sh
./venv/bin/python main.py
```

#### Try It Out
```sh
>> What's Apple's stock price?
Apple's current stock price is $252.13 per share.

>> How much is Google trading for?
Alphabet Inc. (GOOGL) is currently trading at 247.14 per share.
```

## How It Works

The magic happens in **three steps**:

### Step 1: First LLM Call
- User asks a question
- LLM analyzes if it needs external data
- If yes, LLM returns a **tool call** instead of a final answer

### Step 2: Execute Your Function
- Your code receives the tool call
- Executes your custom function (`get_stock_price`)
- Captures the real-world result

### Step 3: Second LLM Call
- Tool result is added to the conversation history
- LLM gets the complete context (original question + tool result)
- LLM generates a **natural, coherent response** using the data

This ensures users get helpful explanations, not just raw data dumps!

## This project structure

```sh
ollama-function-calling/
├── main.py             # Main example code
├── README.md           # This file
└── requirements.txt    # Dependencies
```

## Customizing for your own functions

Want to add your own functions? Follow this procedure:

1. **Create your function**:
```py
def get_weather(city: str) -> str:
    # Your implementation here
    return f"Sunny, 75°F in {city}"
```

2. **Add it to the TOOLS dictionary**:
```py
TOOLS_LIST = {
    'get_stock_price': get_stock_price,
    'get_weather': get_weather, # Add your function
}
```

3. **Define the tool schema**:
```py
TOOL_SCHEMA = [
    # ... existing stock price schema
    {
        'type': 'function',
        'function': {
            'name': 'get_weather',
            'description': 'Get current weather for a city',
            'parameters': {
                'type': 'object',
                'properties': {
                    'city': {'type': 'string', 'description': 'City name'}
                },
                'required': ['city'],
            },
        },
    }
]
```

Now you can test it by running the script.

## 📄 License
Unlicense.
