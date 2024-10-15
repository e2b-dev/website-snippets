# pip install openai e2b-code-interpreter
from openai import OpenAI
from e2b_code_interpreter import Sandbox

# Create OpenAI client
client = OpenAI()
prompt = "Calculate how many r's are in the word 'strawberry'"

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
    messages=[{"role": "user", "content": prompt}],
    tools=tools,
)

# Execute the tool if it's called by the model
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    if tool_call.function.name == "execute_python":
        # Create a sandbox and execute the code
        with Sandbox() as sandbox:
            code = tool_call.function.arguments
            execution = sandbox.run_code(code)
            result = execution.text

        # Send the result back to the model
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt},
                {"role": "function", "name": "execute_python", "content": result}
            ]
        )

print(response.choices[0].message.content)
