# pip install mistralai e2b-code-interpreter
import os
from mistralai import Mistral
from e2b_code_interpreter import CodeInterpreter

api_key = os.environ["MISTRAL_API_KEY"]

# Create Mistral client
client = Mistral(api_key=api_key)
system_prompt = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
prompt = "Calculate how many r's are in the word 'strawberry'"

# Send the prompt to the model
response = client.chat.complete(
    model="codestral-latest",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
)

# Extract the code from the response
code = response.choices[0].message.content

# Execute the code with E2B Code Interpreter
with CodeInterpreter() as sandbox:
    execution = sandbox.notebook.exec_cell(code)
    result = execution.text

print(result)
