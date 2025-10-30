# Paradigm Selection Guide

## Default Choice

**Default to Functional API** for most workflows. Use Graph API only when workflow requires specific Graph API features.

## Selection Criteria

### Use Functional API When:
- Sequential or moderately complex workflows
- Simple conditional branching (if/else sufficient)
- Standard Python control flow adequate
- Entrypoint-level checkpointing sufficient
- No need for workflow visualization
- Simple to moderate complexity

### Use Graph API When:
- Multiple parallel execution paths with explicit orchestration
- Complex conditional routing between nodes
- Granular node-level checkpointing required
- Time-travel debugging needed
- Workflow visualization required for understanding/documentation
- Complex state management with reducers needed
- Multi-agent systems
- Step-by-step replay workflows

## Feature Comparison

| Feature | Functional API | Graph API |
|---------|----------------|-----------|
| Human-in-the-loop | `interrupt()` function with payload | Node-level interrupts |
| Persistence/Memory | Checkpointer (entrypoint-level) | Checkpointer (node-level) |
| Streaming | Built-in `StreamWriter` | Built-in streaming |
| Async Tasks | `@task` decorator with futures | Parallel node execution |
| Visualization | Not supported (runtime-dynamic) | Full graph visualization |
| Time-travel | Limited (entrypoint checkpoints) | Full (node checkpoints) |
| State Management | Function-scoped, `previous` param | Explicit State with reducers |
| Control Flow | Standard Python + decorators | Explicit edges/conditionals |
| Simple Iterations | Standard for/while loops | Graph loop structures |
| Complexity | Simple to Moderate | Moderate to Complex |

## Implementation Requirements

Both paradigms require:
- Never use plain Python without LangGraph decorators/classes
- Functional API: Use `@entrypoint` decorator with standard Python control flow
- Graph API: Use `StateGraph` with node functions and explicit edges

## Mixing Paradigms

Both APIs can be mixed:
- Call Graph API from `@entrypoint`
- Use `@task` within Graph nodes
