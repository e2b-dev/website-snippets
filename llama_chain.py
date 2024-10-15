# pip install ollama
import ollama
from e2b_code_interpreter import Sandbox

# Create Ollama client
system = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed in the cell and nothing else. Strip backticks in code blocks."
prompt = "Calculate how many r's are in the word 'strawberry'"

response = ollama.chat(model="llama3.2", messages=[
    {
        "role": "system",
        "content": system
    },
    {
        "role": "user",
        "content": prompt
    }
])

code = response['message']['content']

with Sandbox() as sandbox:
    execution = sandbox.run_code(code)
    result = execution.logs.stdout

summary = ollama.chat(model="llama3.2", messages=[
    {
        "role": "system",
        "content": system
    },
    {
        "role": "user",
        "content": prompt
    },
    {
        "role": "assistant",
        "content": code
    },
    {
        "role": "user",
        "content": "\n".join(result)
    },
    {
        "role": "user",
        "content": "Summarize the result in a single line."
    }
])

print(summary['message']['content'])
