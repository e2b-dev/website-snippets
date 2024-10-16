# pip install anthropic e2b-code-interpreter
from anthropic import Anthropic
from e2b_code_interpreter import Sandbox

# Create Anthropic client
client = Anthropic()
model = "claude-3-5-sonnet-20240620"

# Define the messages
messages = [
    {
        "role": "user",
        "content": "Calculate how many r's are in the word 'strawberry'"
    }
]

# Define the tools
tools = [{
    "name": "execute_python",
    "description": "Execute python code in a Jupyter notebook cell and return (not print) the result",
    "input_schema": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The python code to execute in a single cell"
            }
        },
        "required": ["code"]
    }
}]

# Generate text with Anthropic
message = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=messages,
    tools=tools
)

# Append the response message to the messages list
messages.append({
    "role": "assistant",
    "content": message.content
})

# Execute the tool if it's called by the model
if message.stop_reason == "tool_use":
    tool_use = next(block for block in message.content if block.type == "tool_use")
    tool_name = tool_use.name
    tool_input = tool_use.input

    if tool_name == "execute_python":
        with Sandbox() as sandbox:
            code = tool_input['code']
            execution = sandbox.run_code(code)
            result = execution.text

        # Append the tool result to the messages list
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                }
            ],
        })

# Generate the final response
final_response = client.messages.create(
    model=model,
    max_tokens=1024,
    messages=messages,
    tools=tools
)

print(final_response.content[0].text)
