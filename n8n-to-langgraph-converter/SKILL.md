---
name: n8n-to-langgraph-converter
description: Convert n8n workflow automations to LangGraph AI-orchestrated workflows. Use when the user provides an n8n JSON export or requests conversion of n8n workflows to LangGraph Python code. Handles workflow analysis, custom logic extraction, and complete LangGraph implementation with best practices.
license: MIT
---

# n8n to LangGraph Converter

Convert n8n workflow automations into production-ready LangGraph AI-orchestrated Python workflows using a systematic 3-phase methodology.

## When to Use This Skill

Use this skill when:
- User provides an n8n workflow JSON export for conversion
- User requests conversion of n8n automation to LangGraph
- User asks about migrating from n8n to LangGraph
- User needs to understand how to translate n8n nodes to LangGraph patterns

## Overview

This skill transforms n8n workflows (no-code/low-code automation) into LangGraph implementations (AI-orchestrated Python workflows) while maintaining semantic equivalence and following production best practices.

## Conversion Methodology

Follow this systematic 3-phase approach:

### Phase 1: Production Requirements Analysis

**Objective**: Analyze the n8n workflow JSON and produce comprehensive technical specifications.

**Process**:
1. Request the n8n workflow JSON export from the user
2. Load and apply the Phase 1 orchestration prompt from `references/orchestration-prompts/Step1-ProductionRequirements.md`
3. Analyze the workflow to produce:
   - Global workflow summary (objectives, triggers, execution rules, security requirements, error handling)
   - Per-node specifications (functionality, parameters, data mapping, execution paths)
   - Custom node identification
   - Complete technical specification document

**Output**: Technical specification document detailing all workflow requirements

### Phase 2: Custom Logic Extraction (If Applicable)

**Objective**: Document custom code logic from n8n function nodes.

**Process**:
1. Identify any custom nodes from Phase 1 (Python/Node.js function nodes, code blocks, custom transformations)
2. If custom nodes exist:
   - Request the custom code from the user
   - Load and apply the Phase 2 orchestration prompt from `references/orchestration-prompts/Step2-CustomLogic.md`
   - Analyze each custom node to document:
     - Purpose and inputs
     - Processing logic step-by-step
     - Outputs and data structures
     - Dependencies and error handling
     - Translation strategy for LangGraph
3. If no custom nodes exist, skip this phase

**Output**: Custom logic documentation with translation strategies

### Phase 3: LangGraph Implementation

**Objective**: Generate complete, production-ready LangGraph Python code.

**Process**:
1. Load ALL implementation guides from `references/guides/` directory (mandatory first step):
   - `paradigm-selection.md` - Functional API vs Graph API decision criteria
   - `functional-api-implementation.md` - Functional API patterns and best practices
   - `graph-api-implementation.md` - Graph API patterns and best practices
   - `authentication-setup.md` - OAuth2, environment detection, credential handling
   - `api-integration.md` - Gmail, Google Sheets, HTTP requests, Hunter.io
   - `project-structure.md` - Code organization and file structure
   - `testing-and-troubleshooting.md` - Testing strategies and common issues
   - `output-requirements.md` - Code formatting and documentation standards

2. Load and apply the Phase 3 orchestration prompt from `references/orchestration-prompts/Step3-MainOrchestorPrompt.md`

3. Analyze specifications from Phase 1 and Phase 2 (if applicable)

4. Select implementation paradigm:
   - **Functional API** (`@entrypoint`): Default choice for sequential/moderate complexity
   - **Graph API** (`StateGraph`): For complex workflows with extensive parallelism
   - Use `paradigm-selection.md` criteria for decision

5. Generate complete LangGraph implementation including:
   - Environment validation and configuration
   - Authentication setup (environment-aware)
   - Task functions with proper decorators
   - Helper functions for API integrations
   - Main entrypoint with checkpointing
   - Error handling and logging
   - Requirements file
   - Environment template
   - Documentation

6. Perform final review cross-referencing ALL guides for compliance

**Output**: Complete LangGraph Python implementation ready for production use

## Critical Implementation Requirements

**ALWAYS enforce these requirements**:

### 1. Serialization Safety
```python
# ✅ CORRECT: Non-serializable objects initialized globally
google_creds = get_google_credentials()
sheets_service = build('sheets', 'v4', credentials=google_creds)
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

@entrypoint(checkpointer=checkpointer)
def workflow(company_urls: List[str]):  # Only JSON-serializable inputs
    # Access global objects from within
    return results
```

```python
# ❌ WRONG: Non-serializable objects as parameters
@entrypoint(checkpointer=checkpointer)
def workflow(llm: ChatOpenAI):  # Will fail checkpointing!
    return results
```

### 2. Sync/Async Consistency
```python
# ✅ CORRECT: All synchronous
@task
def fetch_data(url: str) -> str:
    return requests.get(url).text

@entrypoint(checkpointer=checkpointer)
def workflow(urls: List[str]):
    result = fetch_data(urls[0])
    return result.result()
```

```python
# ❌ WRONG: Mixing async and sync
@task
async def fetch_data(url: str) -> str:  # Async task
    return await aiohttp.get(url)

@entrypoint(checkpointer=checkpointer)
def workflow(urls: List[str]):  # Sync entrypoint - WILL FAIL!
    result = fetch_data(urls[0])
    return result.result()
```

### 3. Task Result Pattern
```python
# ✅ CORRECT: Get result with .result()
@task
def process_data(data: str) -> Dict:
    return {"processed": data}

@entrypoint
def workflow(data: str):
    task = process_data(data)  # Returns Command object
    result = task.result()  # Get actual result
    return result
```

### 4. Environment-Aware Authentication
```python
# ✅ CORRECT: Detect environment and adapt
def is_headless() -> bool:
    return not os.getenv('DISPLAY') or os.getenv('SSH_CONNECTION')

def get_google_credentials():
    SCOPES = [...]
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if is_headless():
                # Use --no-browser flag for headless environments
                flow.run_local_server(open_browser=False)
            else:
                flow.run_local_server(port=0)
```

## Node Mapping Patterns

Common n8n nodes map to LangGraph as follows:

| n8n Node Type | LangGraph Pattern | Notes |
|--------------|-------------------|-------|
| Manual Trigger | `if __name__ == "__main__"` | Script entry point |
| Webhook Trigger | Flask/FastAPI endpoint | Requires web framework |
| Cron Trigger | APScheduler + workflow invocation | Schedule management |
| HTTP Request | `@task` with requests library | Handle timeouts and errors |
| Function Node | `@task` or helper function | Complex logic as task |
| IF Node | Native Python `if/elif/else` | Conditional routing |
| Switch Node | Native Python `match/case` or dict dispatch | Multi-way branching |
| Set Node | Variable assignment | State management |
| Code Node | `@task` function | Custom Python logic |
| OpenAI/LLM Node | `@task` with LangChain LLM | Use langchain-openai |
| Google Sheets | Helper function with google-api-python-client | Handle auth properly |
| Gmail | Helper function with base64url encoding | RFC 2822 format |
| Loop Node | Python `for` loop within entrypoint | Iterate over items |
| Merge Node | Python list operations or conditional logic | Combine data streams |

## Helper Scripts

Use `scripts/setup-project.py` to initialize a new LangGraph project structure with proper configuration files and directory layout.

## References

All orchestration prompts and implementation guides are available in the `references/` directory:

- **Orchestration Prompts** (`references/orchestration-prompts/`):
  - Step 1: Production Requirements Analysis
  - Step 2: Custom Logic Extraction
  - Step 3: Main Orchestrator (LangGraph Implementation)

- **Implementation Guides** (`references/guides/`):
  - Paradigm Selection (Functional vs Graph API)
  - Functional API Implementation
  - Graph API Implementation
  - Authentication Setup
  - API Integration
  - Project Structure
  - Testing and Troubleshooting
  - Output Requirements

## Workflow

Execute the following steps in order:

1. **Request n8n JSON**: Ask user for n8n workflow JSON export
2. **Phase 1**: Apply production requirements analysis
3. **Phase 2**: If custom nodes detected, extract and document custom logic
4. **Phase 3**: Load ALL guides, then generate LangGraph implementation
5. **Review**: Cross-reference all guides to ensure compliance
6. **Deliver**: Provide complete implementation with setup instructions

## Success Criteria

A successful conversion includes:
- ✅ Complete Python implementation following chosen paradigm
- ✅ All n8n nodes mapped to LangGraph equivalents
- ✅ Proper serialization (global non-serializable objects)
- ✅ Consistent sync/async patterns (no mixing)
- ✅ Environment-aware authentication
- ✅ Error handling and logging
- ✅ `requirements.txt` with all dependencies
- ✅ Environment template (`.env.example` or `env_template.txt`)
- ✅ Setup and usage documentation
- ✅ Code follows all implementation guide requirements

## Common Pitfalls to Avoid

**CRITICAL ERRORS** documented in guides:

1. ❌ **Never pass non-serializable objects to @entrypoint** (causes checkpointing failures)
2. ❌ **Never mix async tasks with sync entrypoint** (causes invoke failures)
3. ❌ **Never forget .result() when using task returns** (gets Command object instead of actual result)
4. ❌ **Never hardcode credentials** (use environment variables)
5. ❌ **Never skip environment detection for auth** (causes failures in headless/WSL environments)
6. ❌ **Never use Gmail API without base64url encoding** (RFC 2822 requirement)

## Example Usage

User: "I have an n8n workflow that reads URLs from Google Sheets, scrapes content, summarizes it with OpenAI, finds email contacts, generates personalized emails, and creates Gmail drafts. Can you convert it to LangGraph?"

Response Process:
1. Request n8n JSON export
2. Apply Phase 1 to analyze workflow structure and requirements
3. Check for custom function nodes (Phase 2 if needed)
4. Load all implementation guides from `references/guides/`
5. Apply Phase 3 to generate LangGraph implementation using Functional API
6. Include complete setup: requirements.txt, .env template, auth setup
7. Provide usage instructions and execution example

The result is a production-ready Python script using LangGraph's `@entrypoint` and `@task` decorators with proper authentication, error handling, and best practices.
