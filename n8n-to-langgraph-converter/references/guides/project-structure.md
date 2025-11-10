# Project Structure Guide

## Custom Node Handling

### 1. Read Custom Node Requirements FIRST
BEFORE generating any code:
- Scan n8n workflow JSON for nodes marked as custom with placeholders pointing to `/req-for-custom-nodes/<node-name>.md`
- Read each referenced requirement file completely
- These files contain actual implementation requirements for custom business logic
- Do NOT proceed until all custom node requirement files are analyzed

### 2. Custom Node Translation Process
For each custom node:
1. Read requirement file: `/req-for-custom-nodes/<node-name>.md`
2. Translate implementation to Python functions suitable for chosen paradigm
3. Preserve functionality to ensure inputs/outputs match for seamless integration
4. Expand specification with full details (Functionality, Parameters, Data Mapping, Success/Error Paths)
5. Mark as custom for traceability

### 3. Integration Strategy
- Custom nodes become Python functions in chosen paradigm
- Use appropriate calling patterns (direct call, task decorator, graph node)
- Ensure proper return values and state updates
- Handle errors within chosen paradigm's error handling framework

## Universal Requirements (Both Paradigms)

### Environment Setup
- **MANDATORY**: Include .env file loading and environment variable validation
- **MANDATORY**: Include headless environment detection and authentication fallbacks
- **MANDATORY**: Implement authentication mode detection with proper fallback chain

### Code Quality Standards
- Proper type hints and documentation
- Configuration variables at the top
- Clear imports and dependencies
- Helper functions for complex logic
- Logical code organization with clear sections
- Standard error handling with try/except
- Proper logging for debugging and monitoring

## Code Organization Structure

### Section Breakdown
1. **Imports and dependencies**
2. **Configuration variables**
3. **Environment validation function**
4. **Authentication helper functions** (headless detection, mode detection, credential management)
5. **Global initialization** of non-serializable objects (credentials, API clients, database connections)
6. **Workflow functions/nodes** (paradigm-appropriate)
7. **Main workflow entrypoint** (receives only serializable inputs)
8. **Execution entry point**

## Dependencies Management

### Core Dependencies
- `python-dotenv` - Environment variable management
- `langgraph` - Core LangGraph framework
- `langgraph-checkpoint` - Persistence and memory
- `langchain-openai` - OpenAI integration

### Additional Dependencies (as needed)
- `requests`/`httpx` - HTTP API calls
- `pandas` - Data processing
- `google-auth*` - Google authentication
- `googleapiclient` - Google API clients
- Workflow-specific packages

### Standard Library (import as needed)
- `base64` - For encoding operations
- `email.mime` - For email formatting
- `json` - JSON processing
- `urllib` - URL handling
- `datetime` - Date/time operations

## Environment Configuration

### Environment Variables Template
- Provide environment template file containing all required API keys, credentials, and configuration values
- Include descriptive comments for each variable explaining where to obtain the value and what it is used for
- Format as key-value pairs following standard dotenv convention

### Environment Variable Validation
- Implement validation function checking all required variables
- Clear error messages for missing variables
- List which specific variables missing
- Suggest how to fix issues

### .gitignore Entry
- Add `.env` to prevent committing secrets
- Include other sensitive files as needed

## Authentication Configuration

### Google Authentication Setup
- OAuth2 Flow: Interactive authentication with user consent
- Credentials: `credentials.json` from Google Cloud Console (OAuth 2.0 Client ID)
- Setup Process: Download credentials, enable APIs, first run authentication
- Environment Detection: Interactive, WSL, Headless with appropriate fallbacks
- Token Management: Automatic refresh on expiration

### GCP Services Setup
- Service Account Flow: Server-to-server without user interaction
- Credentials: Service account JSON key from GCP Console
- Setup: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

## Execution Status and User Messaging

### Success Criteria
- Never print success message if configuration/authentication fails
- If preflight/configuration fails: Set clear failure status and exit non-zero
- Log actionable error explaining what failed and how to fix it
- Avoid misleading summaries like "Workflow Completed Successfully" with zero items

### Success Summary Conditions
- All required configuration completed, AND
- Either at least one item processed, or workflow deterministically completed with zero items by design
- Include final summary reflecting true outcome: counts, errors, next steps

## Error Handling Patterns

### Configuration Errors
- Clear error messages for missing environment variables
- Specific guidance on how to fix configuration issues
- Validation of all required settings before execution

### Authentication Errors
- Detect when browser cannot be launched (WSL, headless) and fall back to manual authorization code flow
- For WSL: print instructions to open URL via `wslview <url>` or `explorer.exe <url>`, then paste code
- If `wslview` not found, prompt user with installation instructions
- If interactive auth fails, surface specific error with recovery guidance
- Handle token expiration and refresh automatically

### API Integration Errors
- Handle external API failures gracefully
- Provide meaningful error messages for debugging
- Implement retry logic where appropriate
- Manage rate limiting and quota issues
