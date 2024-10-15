# pip install openai e2b-code-interpreter
from openai import OpenAI
from e2b_code_interpreter import CodeInterpreter

# Create OpenAI client
client = OpenAI()
system = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
prompt = "Calculate how many r's are in the word 'strawberry'"

# Send the prompt to the model
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
)

# Extract the code from the response
code = response.choices[0].message.content

# Execute the code with E2B Code Interpreter
if code:
    with CodeInterpreter() as sandbox:
        execution = sandbox.notebook.exec_cell(code)
        result = execution.text

    print(result)
