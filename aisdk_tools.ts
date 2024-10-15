// npm install ai @ai-sdk/openai zod @e2b/code-interpreter
import { openai } from '@ai-sdk/openai'
import { generateText } from 'ai'
import z from 'zod'
import { Sandbox } from '@e2b/code-interpreter'

// Create OpenAI client
const model = openai('gpt-4o')

const prompt = "Calculate how many r's are in the word 'strawberry'"

// Generate text with OpenAI
const { text } = await generateText({
  model,
  prompt,
  tools: {
    // Define a tool that runs code in a sandbox
    codeInterpreter: {
      description: 'Execute python code in a Jupyter notebook cell and return result',
      parameters: z.object({
        code: z.string().describe('The python code to execute in a single cell'),
      }),
      execute: async ({ code }) => {
        // Create a sandbox, execute LLM-generated code, and return the result
        const sandbox = await Sandbox.create()
        const { text, results, logs, error } = await sandbox.runCode(code)
        return results
      },
    },
  },
  // This is required to feed the tool call result back to the LLM
  maxSteps: 2
})

console.log(text)
