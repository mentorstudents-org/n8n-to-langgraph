# n8n to LangGraph Conversion - Implementation Documentation

## Executive Summary

This document provides comprehensive details of the conversion from an n8n workflow to LangGraph implementation for an automated outbound sales email campaign.

## Table of Contents

1. [Implementation Paradigm Decision](#implementation-paradigm-decision)
2. [Workflow Analysis](#workflow-analysis)
3. [Complete Node Conversion Table](#complete-node-conversion-table)
4. [Architecture Details](#architecture-details)
5. [Dependencies](#dependencies)
6. [Configuration and Setup](#configuration-and-setup)
7. [Testing Instructions](#testing-instructions)
8. [API Integration Details](#api-integration-details)

---

## Implementation Paradigm Decision

### Selected Paradigm

**Functional API with `@entrypoint` decorator**

**Execution Pattern**: Synchronous (regular functions with `.invoke()`)

### Justification

**Workflow Complexity Analysis**:
- The workflow follows a sequential, linear processing model
- Contains only simple conditional branching (If node checks email availability)
- No parallel execution paths requiring explicit orchestration
- No complex state management or reducer logic needed
- No requirement for workflow visualization or time-travel debugging

**Features Required**:
- Basic checkpointing for state persistence ✓
- Task execution for long-running API calls ✓
- Simple conditional routing (if/else sufficient) ✓
- Standard Python control flow adequate ✓

**Conclusion**: The workflow matches the "Simple to Moderate" complexity profile described in the Paradigm Selection Guide, making Functional API the optimal choice.

**Why Not Graph API**:
- No need for granular node-level checkpointing
- No complex conditional routing between nodes
- No parallel execution requiring explicit orchestration
- Graph structure would add unnecessary complexity

**Execution Pattern Justification**:
- Sequential processing is sufficient (one company at a time)
- No concurrent operations needed within tasks
- Synchronous pattern provides simpler implementation and debugging
- Matches workflow's linear processing model

---

## Workflow Analysis

### Original n8n Workflow Summary

**Objective**: Automated outbound sales email campaign that scrapes company websites, finds contact information, generates personalized emails using AI, and sends them via Gmail while tracking successes and failures in Google Sheets.

**Workflow Settings**:
- Execution Order: v1
- Active Status: Disabled (manual trigger only)
- Sequential processing (one item at a time)

**Flow Structure**:
1. Manual trigger initiates workflow
2. Read company URLs from Google Sheets (column A)
3. For each URL:
   - Fetch website HTML content
   - Extract text from HTML body
   - Generate company summary using OpenAI
   - Find contact emails using Hunter.io
   - **Conditional Branch**:
     - **If emails found**: Generate personalized email → Create Gmail draft → Log success
     - **If no emails**: Log failure
4. Continue to next company

**Custom Nodes**: None detected (all standard n8n nodes)

### Data Flow Analysis

```
Manual Trigger
    ↓
Google Sheets (Read URLs)
    ↓
[FOR EACH URL]
    ↓
HTTP Request (Fetch HTML)
    ↓
HTML Extractor (Extract Text)
    ↓
OpenAI Summarizer
    ↓
Hunter.io (Find Emails)
    ↓
If Node (Check emails.length != 0)
    ↓
  ├─[TRUE: Emails Found]─────────────┐
  │   ↓                               │
  │   Edit Fields (Prepare Data)      │
  │   ↓                               │
  │   OpenAI Email Body Generator     │
  │   ↓                               │
  │   OpenAI Subject Generator        │
  │   ↓                               │
  │   Gmail (Create Draft)            │
  │   ↓                               │
  │   Google Sheets (Log Success)     │
  │                                   │
  └─[FALSE: No Emails]────────────────┤
      ↓                               │
      Google Sheets (Log Failure)     │
                                      │
[CONTINUE TO NEXT URL]<───────────────┘
```

---

## Complete Node Conversion Table

| n8n Node Name | n8n Node Type | Custom Req File | Functionality | LangGraph Implementation | Dependencies | Notes |
|---------------|---------------|----------------|---------------|-------------------------|--------------|-------|
| When clicking 'Execute workflow' | n8n-nodes-base.manualTrigger | - | Manual workflow trigger | Main execution block (`if __name__ == "__main__"`) | - | Converted to Python script entry point |
| Google Sheets | n8n-nodes-base.googleSheets | - | Read company URLs from Sheet1, column A | `read_company_urls_from_sheets()` helper function | google-api-python-client, google-auth | OAuth2 authentication required |
| HTTP Request | n8n-nodes-base.httpRequest | - | Fetch HTML content from company website | `@task fetch_website_content(url)` | requests | Includes timeout, redirects, user-agent header |
| HTML | n8n-nodes-base.html | - | Extract text content from HTML body using CSS selector | `@task extract_text_from_html(html)` | beautifulsoup4 | Removes scripts, styles, nav, footer elements |
| OpenAI- Summarizer | @n8n/n8n-nodes-langchain.openAi | - | Generate concise company summary (gpt-4-turbo → gpt-4o-mini) | `@task summarize_company(text)` | langchain-openai | Model changed to gpt-4o-mini per guide requirements |
| Hunter | n8n-nodes-base.hunter | - | Find email addresses and contacts for domain | `@task find_contacts_hunter(url)` | requests | API key authentication, domain extraction from URL |
| If | n8n-nodes-base.if | - | Conditional routing based on email availability | `if emails and len(emails) > 0:` / `else:` | - | Native Python if/else in entrypoint |
| Edit Fields-Prepare Update Data | n8n-nodes-base.set | - | Prepare company URL for success logging | Inline variable assignment | - | Simplified to direct variable usage |
| OpenAI1- email body | @n8n/n8n-nodes-langchain.openAi | - | Generate personalized cold email body | `@task generate_email_body(summary, first_name, last_name)` | langchain-openai | Includes full prompt template with examples |
| OpenAI- subject | @n8n/n8n-nodes-langchain.openAi | - | Generate 3-4 word subject line | `@task generate_email_subject(summary, org, first_name, last_name)` | langchain-openai | Context-aware subject generation |
| Gmail | n8n-nodes-base.gmail | - | Create draft email in Gmail | `create_gmail_draft(to, subject, body)` helper function | google-api-python-client | RFC 2822 format, base64url encoding required |
| Google Sheets - Update Success Log | n8n-nodes-base.googleSheets | - | Log successful contacts to Success sheet | `update_success_log(url, email, name)` helper function | google-api-python-client | Appends to Success sheet |
| Google Sheets- Log Failed Lookups | n8n-nodes-base.googleSheets | - | Log failed lookups to Failures sheet | `log_failed_lookup(domain)` helper function | google-api-python-client | Appends to Failures sheet |

### Custom Node Implementation Details

**No custom nodes detected in this workflow.** All nodes are standard n8n built-in nodes and have been converted to appropriate Python functions.

---

## Architecture Details

### Code Organization Structure

The implementation follows the structure defined in `guides/project-structure.md`:

1. **Imports and Dependencies**
   - LangGraph and LangChain components
   - Google API libraries
   - HTTP and HTML parsing libraries
   - Standard library modules (base64, logging, etc.)

2. **Configuration Variables**
   - Google API scopes
   - OpenAI model configuration
   - Logging setup

3. **Environment Validation**
   - `validate_environment()` - Checks all required env vars

4. **Authentication Helper Functions**
   - `is_wsl()` - Detect WSL environment
   - `is_headless()` - Detect headless environment
   - `get_google_credentials()` - Handle OAuth2 with environment detection

5. **Global Initialization**
   - Non-serializable objects initialized globally:
     - `google_creds` - Google OAuth2 credentials
     - `sheets_service` - Google Sheets API client
     - `gmail_service` - Gmail API client
     - `llm` - OpenAI ChatOpenAI instance
     - `checkpointer` - MemorySaver for state persistence

6. **Task Functions** (Long-running operations)
   - `@task fetch_website_content(url)` - HTTP request
   - `@task extract_text_from_html(html)` - HTML parsing
   - `@task summarize_company(text)` - OpenAI summarization
   - `@task find_contacts_hunter(url)` - Hunter.io API call
   - `@task generate_email_body(...)` - Email body generation
   - `@task generate_email_subject(...)` - Subject generation

7. **Helper Functions** (Synchronous operations)
   - `read_company_urls_from_sheets()` - Google Sheets read
   - `create_gmail_draft(...)` - Gmail draft creation
   - `update_success_log(...)` - Success logging
   - `log_failed_lookup(...)` - Failure logging

8. **Main Workflow Entrypoint**
   - `@entrypoint(checkpointer=checkpointer)`
   - `outbound_sales_workflow(company_urls)` - Main workflow logic
   - Receives only serializable inputs (list of URLs)

9. **Execution Entry Point**
   - `if __name__ == "__main__":` - Script execution
   - Reads URLs from Sheets
   - Invokes workflow with `.invoke()`

### Key Implementation Principles

#### 1. Serialization Requirements

**Entrypoint Inputs**: Must be JSON/msgpack serializable
- ✓ Correct: `List[str]` of company URLs
- ✗ Incorrect: API client objects, credentials

**Global Initialization**: Non-serializable objects
- Google API credentials and service clients
- OpenAI LLM instance
- Database connections (if any)

#### 2. Sync/Async Consistency

**Pattern**: Synchronous throughout
- Entrypoint: Regular function (no `async` keyword)
- Tasks: Regular functions (no `async` keyword)
- Method calls: Synchronous (e.g., `llm.invoke()` not `await llm.ainvoke()`)
- Task result retrieval: `task.result()` not `await task.result()`
- Workflow invocation: `.invoke()` not `.ainvoke()`

**Why Synchronous**:
- Sequential processing (one company at a time)
- No concurrent operations needed
- Simpler implementation and debugging

#### 3. Error Handling Strategy

- Try-except blocks in all task functions
- Detailed logging at each step
- Graceful degradation (continue processing other companies on error)
- Clear error messages with actionable guidance
- Exit codes indicating success/failure

#### 4. State Management

- **Checkpointer**: MemorySaver for entrypoint-level persistence
- **State Passing**: Function return values and variables
- **Thread ID**: Configurable for workflow tracking
- **No Complex State**: Simple variables sufficient for this workflow

---

## Dependencies

### Core Dependencies

```python
# LangGraph and LangChain
langgraph>=0.2.0                 # Core framework with Functional API
langgraph-checkpoint>=1.0.0      # State persistence and checkpointing
langchain-openai>=0.2.0          # OpenAI integration
langchain-core>=0.3.0            # Core LangChain functionality
```

### Google API Dependencies

```python
google-auth>=2.34.0              # Google authentication
google-auth-oauthlib>=1.2.0      # OAuth2 flow for user consent
google-auth-httplib2>=0.2.0      # HTTP library for Google APIs
google-api-python-client>=2.147.0 # Google Sheets and Gmail APIs
```

### HTTP and Web Scraping

```python
requests>=2.32.0                 # HTTP requests for websites and Hunter.io
beautifulsoup4>=4.12.0           # HTML parsing and text extraction
```

### Environment and Configuration

```python
python-dotenv>=1.0.0             # Load environment variables from .env
```

### Standard Library (No Installation Needed)

- `base64` - Base64url encoding for Gmail API
- `logging` - Workflow execution logging
- `urllib.parse` - URL parsing for domain extraction
- `json` - JSON processing (if needed)
- `os` - Environment variable access
- `sys` - Exit codes and system operations

---

## Configuration and Setup

### Environment Variables

Required environment variables (see `env_template.txt`):

```bash
# OpenAI
OPENAI_API_KEY=sk-...           # From https://platform.openai.com/api-keys

# Hunter.io
HUNTER_API_KEY=...              # From https://hunter.io/api_keys

# Google Sheets
GOOGLE_SPREADSHEET_ID=...       # From spreadsheet URL
```

### Google Cloud Setup

1. **Create Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing

2. **Enable APIs**:
   - Google Sheets API
   - Gmail API

3. **Create OAuth Credentials**:
   - Go to APIs & Services → Credentials
   - Create Credentials → OAuth 2.0 Client ID
   - Application type: Desktop application
   - Download credentials as `credentials.json`

4. **OAuth Scopes Required**:
   - `https://www.googleapis.com/auth/spreadsheets`
   - `https://www.googleapis.com/auth/gmail.compose`

### Google Sheets Structure

**Sheet1** (Input):
```
| Column A       |
|----------------|
| companyUrl     |
| https://...    |
| https://...    |
```

**Success** sheet (Output):
```
| Column A    | Column B       | Column C     |
|-------------|----------------|--------------|
| companyUrl  | contactEmail   | contactName  |
```

**Failures** sheet (Output):
```
| Column A           |
|--------------------|
| failedCompanyUrl   |
```

### Authentication Flow

**First Run**:
1. Script detects missing `token.json`
2. Reads `credentials.json`
3. Initiates OAuth2 flow based on environment:
   - **Interactive**: Opens browser automatically
   - **WSL**: Provides `wslview`/`explorer.exe` instructions
   - **Headless**: Displays URL for manual authorization
4. User authorizes application
5. Token saved to `token.json`

**Subsequent Runs**:
1. Load `token.json`
2. Automatically refresh if expired
3. Continue workflow execution

---

## Testing Instructions

### Pre-Implementation Testing

1. **Environment Validation**:
   ```bash
   # Check Python version
   python --version  # Should be 3.9+
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **API Credentials**:
   - Verify OpenAI API key works
   - Test Hunter.io API key
   - Confirm Google credentials valid

3. **Google Sheets Access**:
   - Create test spreadsheet
   - Add test company URLs
   - Create Success and Failures sheets

### Environment-Specific Setup

| Environment | Setup Steps | Authentication Method | Notes |
|-------------|-------------|----------------------|-------|
| Local (Interactive) | Install deps, create .env, download credentials.json, run script | Automatic browser OAuth | Browser opens automatically |
| SSH/Remote (Headless) | Install deps, create .env, download credentials.json, run script | Manual OAuth with URL | Follow terminal instructions |
| WSL | Install deps, create .env, download credentials.json, run script | Hybrid OAuth | Use `wslview <url>` or `explorer.exe <url>` |
| Docker | Build image, mount credentials volume, set env vars | Service Account or manual OAuth | Don't copy credentials into image |
| CI/CD | Set secrets in CI config | Service Account or env vars | Use secrets management |

### Test Execution

1. **Minimal Test**:
   ```bash
   # Add 1-2 test URLs to spreadsheet
   python workflow.py
   ```

2. **Verify**:
   - Check console output for progress
   - Verify Gmail drafts created
   - Check Success/Failures sheets updated

3. **Error Scenarios**:
   - Test with invalid URL (should log error and continue)
   - Test with domain without emails (should log to Failures)
   - Test with API rate limits

### Troubleshooting

See `guides/testing-and-troubleshooting.md` for comprehensive troubleshooting guide.

**Common Issues**:

1. **Authentication Errors**:
   - Delete `token.json` and re-authenticate
   - Verify APIs enabled in Google Cloud Console
   - Check OAuth consent screen configured

2. **API Errors**:
   - Verify API keys in `.env`
   - Check rate limits not exceeded
   - Ensure proper encoding for Gmail API

3. **Environment Issues**:
   - WSL: Install `wslu` package for `wslview`
   - Headless: Use manual authorization flow
   - Docker: Mount credentials as volumes

---

## API Integration Details

### OpenAI Integration

**Model**: `gpt-4o-mini` (per guide requirements)

**Usage**:
- Company summarization
- Email body generation
- Email subject generation

**Implementation**:
```python
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
response = llm.invoke(prompt)
content = response.content.strip()
```

**Error Handling**:
- Catch API exceptions
- Log errors with context
- Return empty string on failure
- Continue processing other companies

### Hunter.io Integration

**Endpoint**: Domain Search API

**Authentication**: API key in query params

**Implementation**:
```python
response = requests.get(
    'https://api.hunter.io/v2/domain-search',
    params={'domain': domain, 'api_key': HUNTER_API_KEY},
    timeout=10
)
```

**Domain Extraction**:
- Parse URL to extract domain
- Remove `www.` prefix
- Handle various URL formats

**Response Handling**:
- Extract email array
- Get organization name
- Handle empty results gracefully

### Gmail API Integration

**Critical Requirement**: RFC 2822 format with base64url encoding

**Message Format**:
```
To: recipient@example.com
Subject: Email Subject

Email body content
```

**Encoding Process**:
1. Create RFC 2822 formatted message (headers + blank line + body)
2. Encode to UTF-8 bytes
3. Apply base64url encoding (URL-safe base64)
4. Send as `raw` field in Gmail API

**Implementation**:
```python
# Create RFC 2822 message
message_text = f"To: {to_email}\r\nSubject: {subject}\r\n\r\n{body}"

# Encode to UTF-8, then base64url
message_bytes = message_text.encode('utf-8')
encoded_message = base64.urlsafe_b64encode(message_bytes).decode('utf-8')

# Send to Gmail API
draft_body = {'message': {'raw': encoded_message}}
gmail_service.users().drafts().create(userId='me', body=draft_body).execute()
```

**Why base64url**:
- Gmail API requires TYPE_BYTES for `raw` field
- Standard base64 may contain `+` and `/` (problematic in URLs)
- base64url replaces `+` with `-`, `/` with `_`
- Removes padding `=` characters

### Google Sheets API Integration

**Operations**:
- Read: Get values from range
- Write: Append values to sheet

**Read Implementation**:
```python
result = sheets_service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range='Sheet1!A:A'
).execute()
values = result.get('values', [])
```

**Write Implementation**:
```python
values = [[url, email, name]]
body = {'values': values}
sheets_service.spreadsheets().values().append(
    spreadsheetId=SPREADSHEET_ID,
    range='Success!A:C',
    valueInputOption='RAW',
    body=body
).execute()
```

**Authentication**: OAuth2 with user consent

**Scopes**: `https://www.googleapis.com/auth/spreadsheets`

---

## Conclusion

This implementation successfully converts the n8n workflow to LangGraph using the Functional API with synchronous execution pattern. All nodes have been properly converted, authentication is handled with environment detection, and API integrations follow best practices including proper encoding for Gmail API.

The implementation is production-ready with comprehensive error handling, logging, and documentation.

### Key Success Factors

✓ Proper paradigm selection (Functional API for sequential workflow)  
✓ Synchronous execution pattern (matches workflow requirements)  
✓ Correct serialization (global initialization of non-serializable objects)  
✓ Environment-aware authentication (WSL, headless, interactive)  
✓ Proper API integration (base64url encoding for Gmail)  
✓ Comprehensive error handling and logging  
✓ Complete documentation and setup instructions  

### Documentation References

- [LangGraph Functional API Overview](https://blog.langchain.com/introducing-the-langgraph-functional-api/)
- [LangGraph Functional API Concepts](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/functional_api.md)
- [Human-in-the-Loop Patterns](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/human_in_the_loop.md)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Hunter.io API Documentation](https://hunter.io/api-documentation)

