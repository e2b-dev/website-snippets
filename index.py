# pip install e2b-code-interpreter
from e2b_code_interpreter import Sandbox

# Create a E2B Sandbox
with Sandbox() as sandbox:
    # Run code
    sandbox.run_code("x = 1")
    execution = sandbox.run_code("x+=1; x")

    print(execution.text) # outputs 2
