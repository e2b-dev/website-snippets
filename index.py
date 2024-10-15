# pip install e2b-code-interpreter
from e2b_code_interpreter import CodeInterpreter

# Create a E2B Code Interpreter
with CodeInterpreter() as sandbox:
    # Execute cells
    sandbox.notebook.exec_cell("x = 1")
    execution = sandbox.notebook.exec_cell("x+=1; x")

    print(execution.text) # outputs 2
