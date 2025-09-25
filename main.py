# module main

# system
import os, sys
import traceback
from typing import Dict, Any, Callable

# libs
import ollama
import yfinance as yf


def get_stock_price(symbol: str) -> float:
    """Get the current stock price for a given symbol."""
    try:
        ticker = yf.Ticker(symbol)
        result = ticker.info.get('regularMarketPrice') or ticker.fast_info.last_price
    except Exception as e:
        result = str(e) # just return the error itself
    
    return result


"""
This is the official way to tell ollama about functions it can call.
"""
TOOLS_SCHEMA = [
    {
        'type': 'function',
        'function': {
            'name': 'get_stock_price',
            'description': 'Get the current stock price for a given symbol',
            'parameters': {
                'type': 'object',
                'properties': {
                    'symbol': {
                        'type': 'string',
                        'description': 'Stock symbol (e.g., AAPL, GOOGL)',
                    },
                },
                'required': ['symbol'],
            },
        },
    }
]

"""
This thing is just for convenience,
so we can check if the requested function is avaialable in our toolset. 
"""
TOOLS_LIST = {
    'get_stock_price': get_stock_price,
}

if __name__ == '__main__':
    model = 'qwen3:4b-instruct'
    history = []

    print(f'Running with model={model}. Type "/quit" to exit.')
    while True:
        try:
            # Get user input
            user_input = input('>> ').strip()
            if user_input.startswith('/'):
                break

            # Append history
            history.append({'role': 'user', 'content': user_input})

            # Generate response
            response = ollama.chat(model, messages=history, tools=TOOLS_SCHEMA)

            # Check if we need to make any functions calls.
            # Ollama does not run functions on its own.
            # We need to run the functions and then feed the results back to ollama.
            if response.message.tool_calls:
                for tool in response.message.tool_calls:
                    # find the function we need to call
                    func = TOOLS_LIST.get(tool.function.name, None)

                    # run this function if it is available
                    tool_result = func(**tool.function.arguments) if func else 'Tool not found'

                    # append the results to history as role:tool
                    history.append({
                        'role': 'tool',
                        'content': str(tool_result),
                        'name': tool.function.name,
                    })

                # run ollama again to get the final coherent response
                response = ollama.chat(model, messages=history, tools=TOOLS_SCHEMA)

            # append ollama response
            history.append({
                'role': 'assistant',
                'content': response.message.content,
            })
            print(response.message.content)            
        except:
            traceback.print_exc()
    
    print('Quit.')


