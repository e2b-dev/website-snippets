# pip install ollama
import ollama
from e2b_code_interpreter import CodeInterpreter

# Send the prompt to the model
response = ollama.chat(model="llama3.2", messages=[
    {
        "role": "system",
        "content": "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
    },
    {
        "role": "user",
        "content": "Calculate how many r's are in the word 'strawberry'"
    }
])

# Extract the code from the response
code = response['message']['content']

# Execute the code with E2B Code Interpreter
with CodeInterpreter() as sandbox:
    execution = sandbox.notebook.exec_cell(code)
    result = execution.logs.stdout

print(result)
