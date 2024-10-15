# pip install anthropic e2b-code-interpreter
from anthropic import Anthropic
from e2b_code_interpreter import Sandbox

# Create Anthropic client
anthropic = Anthropic()
system_prompt = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
prompt = "Calculate how many r's are in the word 'strawberry'"

# Send messages to Anthropic API
response = anthropic.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {"role": "assistant", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)

# Extract code from response
code = response.content[0].text

# Execute code in E2B Sandbox
with Sandbox() as sandbox:
    execution = sandbox.run_code(code)
    result = execution.logs.stdout

print(result)
