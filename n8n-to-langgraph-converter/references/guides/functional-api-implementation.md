# Functional API Implementation Guide

## Implementation Requirements

### Mandatory Defaults
- Model: Use OpenAI "gpt-4o-mini" as the default LLM unless explicitly overridden
- Paradigm: See `guides/paradigm-selection.md` for selection criteria
- Execution Pattern: Default to Synchronous pattern (regular functions with `.invoke()`) for simplicity; use Asynchronous pattern (async functions with `await` and `.ainvoke()`) only when truly needed for concurrent operations
- Sync/Async Consistency: CRITICAL - Entrypoint and all tasks must match in sync/async pattern. Never mix synchronous entrypoint with async tasks or vice versa

## Core Pattern Overview

### Basic Structure
- Use `@entrypoint` decorator for main workflow
- Initialize non-serializable objects (credentials, API clients) globally
- Entrypoint receives only serializable inputs (strings, numbers, lists, dicts)
- Use standard Python control flow inside entrypoint

### Node Conversions
- Main workflow → `@entrypoint` function
- Long-running operations (API calls) → `@task` functions
- HTTP Request/Code/Function → helper functions or `@task`
- Conditionals → if/else inside `@entrypoint`
- Loops → for/while inside `@entrypoint`
- Human review → `interrupt()` calls
- Custom nodes → helper or `@task` functions

## Sync/Async Execution Patterns

### Synchronous Pattern (Default - Recommended)
- **Entrypoint**: Regular function (no async keyword)
- **Tasks**: Regular functions (no async keyword)
- **Method Calls**: Use synchronous methods (e.g., `llm.invoke()` not `await llm.ainvoke()`)
- **Invocation**: Use `.invoke()` method
- **Result Retrieval**: Call tasks and use `.result()` to get return value

### Asynchronous Pattern (Only if truly needed for concurrency)
- **Entrypoint**: Async function with async keyword
- **Tasks**: Async functions with async keyword
- **Method Calls**: Use await with async method calls (e.g., `await llm.ainvoke()`)
- **Invocation**: Use `.ainvoke()` method
- **Result Retrieval**: Call tasks and use `await` on `.result()` to get return value

### Critical Consistency Rules
- **CRITICAL**: Entrypoint and all tasks must match in sync/async pattern
- **ERROR TO AVOID**: Never mix synchronous entrypoint with async tasks or vice versa
- **Error Message**: "In a sync context async tasks cannot be called"
- **Default Choice**: Use synchronous pattern unless you specifically need async concurrency within tasks themselves

## Serialization Requirements

### What Can Be Serialized (Entrypoint Inputs)
- Strings, numbers, lists, dictionaries
- JSON/msgpack serializable data only

### What Cannot Be Serialized
- Credentials objects
- API client instances
- Database connections
- File handles

### Global Initialization Pattern
- Initialize non-serializable objects globally (outside entrypoint)
- Pass only serializable data to entrypoint
- Access global objects from within entrypoint and tasks

## State Management

### State Types
- **`previous`**: Short-term state (current execution context)
- **`store`**: Long-term state (persistent across executions)
- **`entrypoint.final()`**: Output that is not saved to state

### Task Execution
- Tasks return futures - call `.result()` to get value (or `await .result()` in async context)
- Use appropriate calling patterns (direct call, task decorator)

## Key Features

### Human-in-the-Loop
- Use `interrupt()` function to pause execution
- Resume with Command primitive
- Pass payload data to interrupt

### Streaming
- Use `writer` parameter with StreamWriter
- Built-in streaming support

### Persistence/Memory
- Checkpointer at entrypoint-level
- State management with function-scoped variables

## Common Implementation Errors

1. **Sync/Async Mismatch (CRITICAL)**: Never mix synchronous entrypoint with async tasks
2. **Wrong Method Calls**: Match sync/async pattern in method calls
3. **Wrong Invocation Method**: Use `.invoke()` for sync, `.ainvoke()` for async
4. **Missing LangGraph Decorators**: Always use `@entrypoint` and `@task` decorators
5. **Non-Serializable Inputs**: Never pass credentials or API clients as entrypoint inputs

## Implementation Pattern

### Conceptual Structure
1. Import LangGraph Functional API components (`entrypoint`, `task`) and memory checkpointer
2. Globally initialize non-serializable resources (credentials, API clients)
3. Choose sync or async pattern (default: synchronous)
4. Define `@task` functions for long-running operations, ensuring consistency with chosen pattern
5. Create main workflow function decorated with `@entrypoint`, specifying checkpointer
6. Use standard Python control flow inside entrypoint
7. Retrieve main list of items from serialized workflow input
8. Iterate over each item, calling task functions and collecting results
9. Return dictionary containing results
10. Invoke workflow with serialized input and configuration

### Error Handling
- Handle errors within chosen paradigm's error handling framework
- Ensure proper return values and state updates
- Maintain data connections between nodes

### Documentation References
- Functional API Overview: https://blog.langchain.com/introducing-the-langgraph-functional-api/
- Functional API Concepts: https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/functional_api.md
- Human-in-the-Loop Patterns: https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/human_in_the_loop.md
