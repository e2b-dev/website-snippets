// npm install ai @ai-sdk/openai @e2b/code-interpreter
import { openai } from '@ai-sdk/openai'
import { generateText } from 'ai'
import { Sandbox } from '@e2b/code-interpreter'

// Create OpenAI client
const model = openai('gpt-4o')
const system = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
const prompt = "Calculate how many r's are in the word 'strawberry'"

// Generate code with OpenAI
const { text: code } = await generateText({
  model,
  system,
  prompt
})

// Run the code in E2B Sandbox
const sandbox = await Sandbox.create()
const { text, results, logs, error } = await sandbox.runCode(code)

console.log(text)
