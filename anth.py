# pip install anthropic e2b-code-interpreter
from anthropic import Anthropic
from e2b_code_interpreter import CodeInterpreter

# Create Anthropic client
anthropic = Anthropic()
system_prompt = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
prompt = "Calculate how many r's are in the word 'strawberry'"

response = anthropic.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {"role": "assistant", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)

code = response.content[0].text

with CodeInterpreter() as sandbox:
    execution = sandbox.notebook.exec_cell(code)
    result = execution.logs.stdout

print(result)
