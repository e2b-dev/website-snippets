# pip install openai e2b-code-interpreter
import json
from openai import OpenAI
from e2b_code_interpreter import Sandbox

# Create OpenAI client
client = OpenAI()
messages = [
    {
        "role": "user",
        "content": "Calculate how many r's are in the word 'strawberry'"
    }
]

# Define the tools
tools = [{
    "type": "function",
    "function": {
        "name": "execute_python",
        "description": "Execute python code in a Jupyter notebook cell and return result",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The python code to execute in a single cell"
                }
            },
            "required": ["code"]
        }
    }
}]

# Generate text with OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

response_message = response.choices[0].message
messages.append(response_message)

# Execute the tool if it's called by the model
if response_message.tool_calls:
    for tool_call in response_message.tool_calls:
        if tool_call.function.name == "execute_python":
            # Create a sandbox and execute the code
            with Sandbox() as sandbox:
                code = json.loads(tool_call.function.arguments)['code']
                execution = sandbox.run_code(code)
                result = execution.text

            # Send the result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "execute_python",
                "content": result
            })

final_response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages
)

print(final_response.choices[0].message.content)
