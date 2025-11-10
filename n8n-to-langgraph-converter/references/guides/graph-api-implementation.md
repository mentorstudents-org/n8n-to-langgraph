# Graph API Implementation Guide

See `guides/paradigm-selection.md` for when to use Graph API vs Functional API.

## Core Pattern Overview

### Basic Structure
- Define state schema (TypedDict/Pydantic)
- Create StateGraph
- Add nodes as functions
- Define edges (regular/conditional)
- Compile with checkpointer
- Invoke with recursion limit

### Node Conversions
- n8n nodes → LangGraph node functions accepting state
- HTTP/Database → tool nodes or custom functions
- Conditionals → conditional edges with routing functions
- Loops → graph loop structures
- Custom nodes → node functions

## State Schema Definition

### TypedDict Approach
- Define using TypedDict with all field types
- Explicit type definitions for all state fields

### Pydantic Approach
- Use Pydantic models for state validation
- Automatic type checking and validation

## Graph Construction

### Node Functions
- Accept state as parameter
- Return updated state or state updates
- Handle business logic within nodes

### Edge Types
- **Regular Edges**: Direct connections between nodes
- **Conditional Edges**: Dynamic routing based on state conditions
- **Loop Edges**: Return to previous nodes for iteration

### Routing Functions
- Define conditional logic for edge routing
- Return next node name based on state
- Handle complex decision trees

## State Management

### Reducers
- Define merge logic for state updates
- Handle state conflicts and merging
- Specify how to combine state from different nodes

### State Updates
- Return partial state updates from nodes
- Automatic merging based on reducer logic
- Preserve state across node executions

## Execution

### Compilation
- Compile graph with checkpointer
- Set up persistence and memory
- Configure execution parameters

### Invocation
- Invoke with recursion_limit in config
- Handle graph execution flow
- Manage state transitions

## Key Features

### Granular Checkpointing
- Node-level checkpointing and time-travel debugging
- Individual node state preservation
- Step-by-step replay capabilities

### Visualization
- Full graph visualization support
- Workflow understanding and documentation
- Visual representation of node connections

### Parallel Execution
- Multiple parallel execution paths
- Explicit orchestration of concurrent operations
- Complex state dependencies

## Graph Flow Analysis

### Loop Structure Identification
- **Controller Node**: Name of node managing iteration
- **Conditional Exit**: Edge and condition routing to END
- **Processing Entry Point**: First node for item processing

### Path Tracing
- **Success Path**: Document node sequence from processing to completion
- **Failure Paths**: Document each failure branch
- **Loop Verification**: Confirm loops back to controller

### Final Verdict
- Confirm all branches route correctly
- No dead-ends or recursion traps
- Complete workflow coverage

## Implementation Considerations

### Complexity
- Moderate to Complex implementation
- Requires explicit graph structure
- More setup than Functional API

### State Management
- Explicit State with reducers
- Complex state merging logic
- Node-level state preservation

### Control Flow
- Explicit edges/conditionals
- Graph loop structures
- Complex routing logic
