# Output Requirements Guide

## Implementation Paradigm Decision

Reference `guides/paradigm-selection.md` for selection criteria.

```
Selected Paradigm: [Functional API with @entrypoint / Graph API with StateGraph]
Execution Pattern: [Synchronous / Asynchronous] (Default: Synchronous)

Justification:
- Workflow complexity analysis
- Required features analysis
- Rationale for selection
```

## Complete Implementation
Provide full, runnable LangGraph code with custom nodes integrated. Initialize non-serializable objects globally (Functional API).

## Comprehensive Node Analysis Documentation

### A. Complete Node Conversion Table
| n8n Node Name | n8n Node Type | Custom Req File | Functionality | Implementation | Dependencies | Notes |
|---------------|---------------|----------------|---------------|----------------|--------------|-------|
| EmailProcessor | HTTP Request | - | API call | requests.get() | requests | Standard |
| BusinessLogic | Function | `/req-for-custom-nodes/logic.md` | Validation rules | custom function | pandas | custom |

### B. Custom Node Implementation Details
For each custom node:
- Source: Which requirement file
- Translation: How original code converted to Python
- Integration: How it connects to workflow
- Dependencies: External packages required

## Dependencies List
**Core:** `python-dotenv`, `langgraph`, `langgraph-checkpoint`, `langchain-openai`
**Additional (as needed):** `requests`/`httpx`, `pandas`, `google-auth*`, `googleapiclient`, workflow-specific packages
**Standard Library (import as needed):** `base64` (for encoding), `email.mime` (for email formatting), `json`, `urllib`, `datetime`, etc.

## Configuration
Refer to `guides/project-structure.md` and `guides/authentication-setup.md` for complete setup details.

## Testing Instructions
Refer to `guides/testing-and-troubleshooting.md` for comprehensive testing approach.

## Graph Flow Analysis (Only for Graph API Implementation)
Refer to `guides/graph-api-implementation.md` for graph analysis patterns.

## Expected Deliverables
1. Pre-conversion Analysis: List custom node requirement files and purposes
2. Implementation Paradigm Decision: Explicit choice (Functional API with `@entrypoint` OR Graph API with `StateGraph`) with justification
3. **Complete, runnable LangGraph code** in chosen paradigm with all custom nodes integrated
   - **MANDATORY**: Must use `@entrypoint` decorator (Functional API) OR `StateGraph` (Graph API)
   - **NEVER deliver plain Python without LangGraph decorators**
4. Enhanced workflow documentation showing all node conversions
5. Custom node implementation details with source traceability
6. Dependencies list including `langgraph`, `langgraph-checkpoint`, and packages for custom nodes
7. Configuration and setup instructions
8. .env template file with all required variables
9. .gitignore file with .env entry
10. Authentication documentation with environment-specific setup
11. Troubleshooting guide for authentication issues
12. Graph flow analysis (only if Graph API used)
13. Reference to relevant documentation for implementation patterns used

## Implementation Guidelines

### Key Implementation Principles
- **ALWAYS use LangGraph** - never plain Python without decorators
- **Serialization**: Entrypoint inputs must be JSON/msgpack serializable; initialize non-serializable objects globally
- **Import**: `from langgraph.func import entrypoint, task` (Functional API) or `from langgraph.graph import StateGraph` (Graph API)
- **Paradigm Selection**: See `guides/paradigm-selection.md` for criteria

### Additional Considerations
- Maintain error handling from original workflow
- Preserve retry logic or timeout settings
- Keep authentication and security configurations
- Ensure scalability and performance characteristics
- Add comments explaining complex conversions
- Include necessary data validation

