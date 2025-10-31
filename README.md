# Automated Outbound Sales Email Campaign - LangGraph Implementation

This project converts an n8n workflow to LangGraph for automated outbound sales email generation.

## Overview

**Implementation**: Functional API with `@entrypoint` (Synchronous pattern)

**Workflow Process**:
1. Reads company URLs from Google Sheets
2. Fetches and extracts website content
3. Generates company summaries using OpenAI (gpt-4o-mini)
4. Finds contact emails via Hunter.io
5. Generates personalized cold emails
6. Creates Gmail drafts
7. Logs successes and failures back to Google Sheets

## Prerequisites

- Python 3.9 or higher
- Google Cloud Project with Gmail and Sheets APIs enabled
- OpenAI API key
- Hunter.io API key
- Google Spreadsheet with company URLs

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Google Sheets API
   - Gmail API
4. Create OAuth 2.0 credentials:
   - Go to **APIs & Services** → **Credentials**
   - Click **Create Credentials** → **OAuth 2.0 Client ID**
   - Choose **Desktop application**
   - Download the credentials file
   - Rename it to `credentials.json` and place in project root

### 3. Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in your credentials in `.env`:
   ```bash
   # OpenAI API key from https://platform.openai.com/api-keys
   OPENAI_API_KEY=sk-your-key-here
   
   # Hunter.io API key from https://hunter.io/api_keys
   HUNTER_API_KEY=your-key-here
   
   # Google Spreadsheet ID (from the URL)
   GOOGLE_SPREADSHEET_ID=your-spreadsheet-id-here
   ```

### 4. Google Sheets Preparation

Create a Google Spreadsheet with the following structure:

**Sheet1** (Main data):
- Column A: Company URLs (e.g., https://example.com)

**Success** sheet (for successful contacts):
- Column A: Company URL
- Column B: Contact Email
- Column C: Contact Name

**Failures** sheet (for failed lookups):
- Column A: Failed Company URL

### 5. First Run Authentication

On the first run, you'll need to authenticate with Google:

**Interactive Environment** (Local):
- Browser will open automatically
- Authorize the application
- Token will be saved automatically

**WSL Environment**:
- Follow terminal instructions
- Use `wslview <url>` or `explorer.exe <url>` to open the authorization URL
- Copy and paste the authorization code back

**Headless Environment** (SSH):
- Copy the authorization URL from terminal
- Open it in a browser on another machine
- Copy and paste the authorization code back

## Usage

Run the workflow:

```bash
python workflow.py
```

The workflow will:
1. Read company URLs from Google Sheets
2. Process each company sequentially
3. Generate personalized emails for contacts found
4. Create Gmail drafts
5. Log results to Success/Failures sheets

## Node Conversion Table

| n8n Node Name | n8n Node Type | Functionality | LangGraph Implementation | Dependencies |
|---------------|---------------|---------------|-------------------------|--------------|
| When clicking 'Execute workflow' | Manual Trigger | Manual workflow start | Main execution block | - |
| Google Sheets | Google Sheets | Read company URLs | `read_company_urls_from_sheets()` | google-api-python-client |
| HTTP Request | HTTP Request | Fetch website HTML | `@task fetch_website_content()` | requests |
| HTML | HTML Extractor | Extract text from body | `@task extract_text_from_html()` | beautifulsoup4 |
| OpenAI- Summarizer | OpenAI Chat | Summarize website | `@task summarize_company()` | langchain-openai |
| Hunter | Hunter.io | Find email addresses | `@task find_contacts_hunter()` | requests |
| If | Conditional | Check if emails found | if/else in entrypoint | - |
| OpenAI1- email body | OpenAI Chat | Generate email body | `@task generate_email_body()` | langchain-openai |
| OpenAI- subject | OpenAI Chat | Generate subject line | `@task generate_email_subject()` | langchain-openai |
| Gmail | Gmail | Create draft email | `create_gmail_draft()` | google-api-python-client |
| Google Sheets - Update Success Log | Google Sheets | Log successful contacts | `update_success_log()` | google-api-python-client |
| Google Sheets- Log Failed Lookups | Google Sheets | Log failed lookups | `log_failed_lookup()` | google-api-python-client |
| Edit Fields-Prepare Update Data | Set Node | Prepare data for logging | Inline data preparation | - |

## Architecture

### Paradigm Selection

**Chosen**: Functional API with `@entrypoint` decorator

**Justification**:
- Sequential workflow with simple if/else conditional branching
- No need for complex state management or parallel execution
- Standard Python control flow is adequate
- No requirement for workflow visualization or time-travel debugging
- Matches "Simple to Moderate" complexity profile

### Execution Pattern

**Chosen**: Synchronous pattern (regular functions with `.invoke()`)

**Justification**:
- Sequential processing is sufficient (no concurrent API calls needed within tasks)
- Simpler implementation and debugging
- Matches workflow's linear processing model

### Key Implementation Details

1. **Serialization**: All credentials and API clients initialized globally
2. **Entrypoint Input**: Receives only serializable data (list of URLs)
3. **Task Functions**: Long-running operations decorated with `@task`
4. **State Management**: Uses MemorySaver checkpointer for persistence
5. **Error Handling**: Try-except blocks with detailed logging
6. **API Integration**: Proper base64url encoding for Gmail API (RFC 2822 compliance)

## Troubleshooting

### Authentication Issues

**"No valid authentication method found"**
- Ensure `credentials.json` exists in project root
- Download from Google Cloud Console if missing

**"Token expired"**
- Delete `token.json` and re-run to re-authenticate
- Token will refresh automatically if refresh token is valid

**"Permission denied"**
- Enable Gmail and Sheets APIs in Google Cloud Console
- Check OAuth consent screen configuration

### API Issues

**"Invalid value at 'raw' (TYPE_BYTES)"**
- Gmail API requires base64url encoding (already implemented)
- Ensure message uses proper RFC 2822 format

**Hunter.io quota exceeded**
- Check your Hunter.io plan limits
- Implement rate limiting if processing many URLs

**OpenAI rate limits**
- Add delays between requests if needed
- Consider upgrading OpenAI plan

### Environment Issues

**WSL: Browser doesn't open**
- Use `wslview <url>` or `explorer.exe <url>` manually
- Install wslu if needed: `sudo apt update && sudo apt install wslu`

**Headless: Can't authenticate**
- Use manual authorization code flow (automatically detected)
- Copy authorization URL to browser on another machine

## Project Structure

```
validationrun/
├── src/
│   ├── workflow.py                      # Main LangGraph workflow implementation
│   ├── IMPLEMENTATION_DOCUMENTATION.md  # Detailed implementation notes
│   ├── FINAL_REVIEW_CHECKLIST.md        # Review checklist
│   └── token.json                       # Google OAuth token (auto-generated, git-ignored)
├── guides/
│   ├── api-integration.md               # API integration guide
│   ├── authentication-setup.md          # Google OAuth setup instructions
│   ├── functional-api-implementation.md # Functional API implementation details
│   ├── graph-api-implementation.md      # Graph API implementation details
│   ├── output-requirements.md           # Output requirements documentation
│   ├── paradigm-selection.md            # Paradigm selection rationale
│   ├── project-structure.md             # Project structure documentation
│   └── testing-and-troubleshooting.md   # Testing and troubleshooting guide
├── README.md                            # This file - project overview and setup
├── requirements.txt                     # Python dependencies
├── env_template.txt                     # Environment variables template
├── prompt.md                            # Project prompt/specifications
├── .gitignore                           # Git ignore rules
├── .env                                 # Environment variables (create from template, git-ignored)
├── credentials.json                     # Google OAuth credentials (git-ignored)
├── __pycache__/                         # Python bytecode cache (git-ignored)
└── .vscode/                             # VS Code configuration (git-ignored)
```

**Key Files:**
- `src/workflow.py` - Main entry point with LangGraph workflow implementation
- `requirements.txt` - All Python package dependencies
- `env_template.txt` - Template for `.env` file configuration
- `guides/` - Detailed documentation for various aspects of the project

**Note:** Files marked as "git-ignored" are not tracked in version control for security reasons.

## Security Notes

- Never commit `.env`, `credentials.json`, or `token.json` to version control
- These files are automatically excluded via `.gitignore`
- Rotate API keys regularly
- Use minimal OAuth scopes required

## Documentation References

- [LangGraph Functional API Overview](https://blog.langchain.com/introducing-the-langgraph-functional-api/)
- [LangGraph Functional API Concepts](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/functional_api.md)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Hunter.io API Documentation](https://hunter.io/api-documentation)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## License

This is a conversion project for demonstration purposes.

