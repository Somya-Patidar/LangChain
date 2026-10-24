# LangChain Tools and Tool Calling --- Short Notes

## 1. What Is a Tool?

A **tool** is a Python function or API wrapped in a format that an LLM
can understand and request when it needs to perform an action.

LLMs are good at reasoning and language generation. By themselves, they
generally cannot directly access live external data, call your APIs, run
your application code, or read/update your database. Tools connect an
LLM to these external capabilities.

## 2. How Tools Fit into an Agent

An **AI agent** uses an LLM for reasoning and decision-making, and tools
for taking actions.

``` mermaid
flowchart TD
    U[User request] --> L[LLM: reason and decide]
    L -->|Tool call request| T[Tool]
    T -->|Result| L
    L --> A[Final answer]
```

The model chooses a tool and provides its arguments. The application or
framework executes the tool, returns the result to the model, and the
model can then answer or request another tool.

## 3. Built-in Tools vs. Custom Tools

### Built-in tools

Tools already provided by a framework or integration. You import and use
them rather than writing their implementation yourself.

Examples from the notes: - `DuckDuckGoSearchRun` --- search the web
through DuckDuckGo. - `WikipediaQueryRun` --- retrieve Wikipedia
information. - `PythonREPLTool` --- run Python code. - `ShellTool` ---
run shell commands. - `RequestsGetTool` --- make HTTP GET requests. -
`GmailSendMessageTool` --- send email through Gmail. -
`SlackSendMessageTool` --- post a message to Slack. -
`SQLDatabaseQueryTool` --- run SQL queries.

**Note:** Availability and exact class names depend on the LangChain
package or integration version. Tools that execute code, shell commands,
send messages, or modify databases should be used with appropriate
permissions and safeguards.

### Custom tools

Tools you define yourself when you want the LLM to use your own API,
business logic, database, product, or application.

Use custom tools when: - You need to call your own API. - You want to
encapsulate business logic. - You want the LLM to interact with your app
or database through controlled functions.

## 4. Ways to Create Custom Tools

LangChain supports several approaches:

1.  **`@tool` decorator** --- the simple way to turn a Python function
    into a tool. The function name, docstring, and type hints help
    describe the tool and its inputs.
2.  **`StructuredTool`** --- define a tool with a structured input
    schema, often using Pydantic. Useful when the tool accepts multiple
    named arguments and you want validation.
3.  **`BaseTool`** --- a base class for more customized tools. You
    implement the tool's input schema and execution behavior.

### Example: `@tool`

``` python
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b
```

The type hints describe the expected inputs, and the docstring tells the
model what the tool does.

## 5. Structured Tools and BaseTool

-   **Structured tool:** A tool whose arguments follow a defined schema,
    such as `{"a": 2, "b": 7}`. This makes multi-argument inputs clear
    and validates their shape.
-   **`BaseTool`:** The base class underlying LangChain tool
    implementations. It provides a common tool interface and lets you
    customize input validation and execution. `@tool` and
    `StructuredTool` are convenient higher-level ways to define tools.

## 6. Toolkits

A **toolkit** is a collection of related tools bundled for one purpose.

Example: a Google Drive toolkit might include: -
`GoogleDriveCreateFileTool` --- create or upload a file. -
`GoogleDriveSearchTool` --- search for files. -
`GoogleDriveReadFileTool` --- read file contents.

A toolkit groups tools for convenience and reuse; an agent can choose
the individual tool it needs.

## 7. Tool Binding vs. Tool Calling

### Tool binding

**Tool binding** registers or provides tool definitions to the model so
it knows: - Which tools are available. - What each tool does
(description). - Which arguments it expects (input schema).

Binding usually makes tools available; it does **not** mean the tools
have already run.

### Tool calling

**Tool calling** is when the model decides a tool is useful and emits a
structured request containing: - The tool name. - The arguments to pass.

The model typically **does not execute the tool itself**. LangChain or
your application executes it, sends the result back to the model, and
the model uses that result to continue.

## 8. Short Tool-Calling Example

User asks: "What is 8 multiplied by 7?"

The model may request:

``` json
{
  "name": "multiply",
  "args": {
    "a": 8,
    "b": 7
  }
}
```

The application executes `multiply(8, 7)`, gets `56`, and returns that
result to the model. The model then responds: "8 × 7 = 56."

## 9. Key Difference

-   **LLM:** Thinks, interprets the request, and decides whether a tool
    is needed.
-   **Tool:** Performs a specific action or computation.
-   **Tool binding:** Makes tool descriptions and schemas available to
    the model.
-   **Tool calling:** The model requests a tool with arguments.
-   **Tool execution:** The framework/application actually runs the
    function and returns its result.
-   **Agent:** Coordinates reasoning, tool calls, results, and the final
    response.
