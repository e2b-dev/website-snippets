// npm install @e2b/code-interpreter
import { CodeInterpreter } from '@e2b/code-interpreter'

// Create a E2B Code Interpreter with JavaScript kernel
const sandbox = await CodeInterpreter.create()
await sandbox.notebook.createKernel({ kernelName: 'javascript' })

// Execute JavaScript cells
await sandbox.notebook.execCell('x = 1')
const execution = await sandbox.notebook.execCell('x+=1; x')

// Outputs 2
console.log(execution.text)

// Close the sandbox
await sandbox.close()
