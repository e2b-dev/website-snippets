# pip install mistralai e2b-code-interpreter
import os
import json
from mistralai import Mistral
from e2b_code_interpreter import Sandbox

api_key = os.environ["MISTRAL_API_KEY"]

# Create Mistral client
client = Mistral(api_key=api_key)
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

# Send the prompt to the model
response = client.chat.complete(
    model="mistral-large-latest",
    messages=messages,
    tools=tools
)

# Append the response message to the messages list
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
                "name": "execute_python",
                "content": result,
                "tool_call_id": tool_call.id,
            })

# Generate the final response
final_response = client.chat.complete(
    model="mistral-large-latest",
    messages=messages,
)

print(final_response.choices[0].message.content)
