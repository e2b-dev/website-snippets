from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from e2b_code_interpreter import CodeInterpreter

# Define the tool
def execute_python(code: str):
    with CodeInterpreter() as sandbox:
        execution = sandbox.notebook.exec_cell(code)
        return execution.text

e2b_interpreter_tool = FunctionTool.from_defaults(
    name="execute_python",
    description="Execute python code in a Jupyter notebook cell and return result",
    fn=execute_python
)

# Initialize LLM
llm = OpenAI(model="gpt-4o")

# Initialize ReAct agent
agent = ReActAgent.from_tools([e2b_interpreter_tool], llm=llm, verbose=True)
agent.chat("Calculate how many r's are in the word 'strawberry'")
