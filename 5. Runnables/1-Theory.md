# LangChain Runnables

## 1. Definition

A **Runnable** is a standardized interface in LangChain that allows
different components to accept inputs, perform operations, and return
outputs. Components such as prompts, language models, retrievers, and
Python functions can all be represented as Runnables.

Basically Runnable provides a common interface for executing different components and to create different workflows like serial, pareallel or any other

## 2. Why were Runnables needed?

Before the Runnable interface, different LangChain components had
different methods for performing their operations. For example:

-   Prompts used `.format()` to format input variables.
-   Language models used methods such as `.predict()` to generate
    responses.
-   Chains could use methods such as `.run()` to execute a workflow.

This created inconsistency because developers had to remember different
methods for different components. Connecting components into a pipeline
also required additional code to pass outputs from one component to
another.

### Solution: Runnable interface

Runnable provides a common interface for executing different components:

-   `.invoke()` --- executes a component with a single input.
-   `.batch()` --- executes a component on multiple inputs.
-   `.stream()` --- streams output as it becomes available.

Since components follow a common interface, they can be easily connected
and composed into chains using the pipe (`|`) operator.

Runnable acts as an abstraction: basically it is an abstraction class & it hides the internal implementation of each component and provides a consistent way to execute it.

## 3. Types of Runnables

1. Task-Specific Runnables
- Definition: Core LangChain components that have been converted into Runnables so they can be used in pipelines.
- Purpose: Perform task-specific operations such as LLM calls, prompting, and retrieval.
- Examples:
  - ChatOpenAI — Runs an LLM model.
  - PromptTemplate — Formats prompts dynamically.
  - Retriever — Retrieves relevant documents.

2. Runnable Primitives
- Definition: Fundamental building blocks for structuring execution.
- Purpose: Orchestrate execution by defining how different functions run sequentially, in parallel, or conditionally.

  -----------------------------------------------------------------------
  Runnable                            Definition / Property
  ----------------------------------- -----------------------------------
  `RunnableSequence`                  Executes components sequentially;
                                      the output of one becomes the input
                                      of the next.

  `RunnableParallel`                  Executes multiple components with
                                      the same input and combines their
                                      outputs into a dictionary.

  `RunnableLambda`                    Converts a normal Python function
                                      into a Runnable.

  `RunnablePassthrough`               Passes the input unchanged to the
                                      next component.

  `RunnableBranch`                    Selects and executes a Runnable
                                      based on specified conditions.
  -----------------------------------------------------------------------

## 4. Example

``` python
chain = prompt | model | parser

result = chain.invoke({"topic": "AI"})
```

Here, the prompt, model, and parser are connected into a
`RunnableSequence`. The output of each component is automatically passed
to the next component.

**Key takeaway:** Runnable provides a common execution interface and
makes LangChain components modular, reusable, and easy to compose into
sequential or parallel workflows.
