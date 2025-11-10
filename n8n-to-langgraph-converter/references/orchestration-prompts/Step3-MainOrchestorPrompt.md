# n8n to LangGraph Conversion Prompt

## Task Overview
Convert the provided n8n JSON workflow into a LangGraph implementation. **All implementations must use LangGraph** - analyze workflow complexity to determine whether to use Functional API (`@entrypoint`) or Graph API (`StateGraph`). Maintain original workflow logic, data flow, and functionality.

**CRITICAL FIRST STEP: Before analyzing the workflow, you MUST read ALL guide files in the `guides/` directory to understand implementation patterns, authentication requirements, API integration approaches, project structure standards, and testing methodologies.**

## Execution Process (Follow These Steps)

### Phase 1: Guide Review (MANDATORY FIRST STEP)
1. Read ALL guide files in the `guides/` directory:
   - `guides/paradigm-selection.md`
   - `guides/functional-api-implementation.md`
   - `guides/graph-api-implementation.md`
   - `guides/authentication-setup.md`
   - `guides/api-integration.md`
   - `guides/project-structure.md`
   - `guides/testing-and-troubleshooting.md`
   - `guides/output-requirements.md`
2. Understand paradigm selection criteria, implementation patterns, authentication requirements, API integration patterns, project structure standards, and testing approaches from the guides

### Phase 2: Workflow Analysis
3.Read and analyze the n8n JSON workflow
4. Scan n8n JSON for custom node placeholders pointing to `/req-for-custom-nodes/<node-name>.md`
5.  Read all referenced custom node requirement files completely
6. Analyze workflow complexity using decision framework from guides

### Phase 3: Implementation Planning
7. Select implementation paradigm (default to Functional API with `@entrypoint` unless complexity requires Graph API with `StateGraph`)
8. Select execution pattern (default to Synchronous for simplicity unless async concurrency truly needed)
9. Plan custom node translations to Python functions appropriate for chosen paradigm and execution pattern

### Phase 4: Implementation
10. Create complete LangGraph implementation using proper decorators (`@entrypoint`/`@task` or `StateGraph`), parameters, and patterns from guides
11. Ensure sync/async consistency - if entrypoint is synchronous, all tasks must be synchronous with synchronous method calls; if entrypoint is async, all tasks must be async with await statements
12. Document all conversions with custom node traceability and documentation references

### Phase 5: Final Review
13. **MANDATORY FINAL GUIDE REVIEW** - Cross-reference implementation against all guides:
    - Paradigm selection guide
    - Implementation guide for chosen paradigm
    - Authentication setup guide
    - API integration guide
    - Project structure guide
    - Testing and troubleshooting guide
    - Output requirements guide
14. **CRITICAL**: Verify LangGraph decorators present and sync/async pattern consistent - NEVER plain Python without `@entrypoint` or `StateGraph`, NEVER mix sync entrypoint with async tasks

## Input Materials
- **n8n JSON Workflow**: [Paste your n8n JSON workflow here]
- **Project Requirements**: [Paste your project requirements here]