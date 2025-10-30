"""
n8n to LangGraph Conversion: Automated Outbound Sales Email Campaign

This workflow:
1. Reads company URLs from Google Sheets
2. Fetches and extracts website content
3. Generates company summaries using OpenAI
4. Finds contact emails via Hunter.io
5. Generates personalized cold emails
6. Creates Gmail drafts
7. Logs successes and failures back to Google Sheets

Implementation: Functional API with @entrypoint (Synchronous pattern)
"""

# ============================================================================
# IMPORTS AND DEPENDENCIES
# ============================================================================

import os
import sys
import base64
import logging
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse
from dotenv import load_dotenv

# LangGraph and LangChain
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

# Google API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# HTTP and HTML parsing
import requests
from bs4 import BeautifulSoup

# ============================================================================
# CONFIGURATION VARIABLES
# ============================================================================

# Google API Scopes
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.compose'
]

# OpenAI Model
DEFAULT_MODEL = "gpt-4o-mini"

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# ENVIRONMENT VALIDATION
# ============================================================================

def validate_environment() -> None:
    """Validate all required environment variables are present."""
    required_vars = [
        'OPENAI_API_KEY',
        'HUNTER_API_KEY',
        'GOOGLE_SPREADSHEET_ID'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please create a .env file with all required variables.")
        logger.error("See .env.example for reference.")
        sys.exit(1)
    
    logger.info("✓ Environment validation passed")

# ============================================================================
# AUTHENTICATION HELPER FUNCTIONS
# ============================================================================

def is_wsl() -> bool:
    """Detect if running in WSL environment."""
    if os.getenv('WSL_DISTRO_NAME') or os.getenv('WSLENV'):
        return True
    try:
        with open('/proc/version', 'r') as f:
            return 'microsoft' in f.read().lower()
    except:
        return False

def is_headless() -> bool:
    """Detect if running in headless environment."""
    if os.getenv('DISPLAY') or os.getenv('SSH_CONNECTION') or os.getenv('CI'):
        return False
    return True

def get_google_credentials() -> Credentials:
    """
    Get Google OAuth2 credentials with environment detection.
    Handles interactive, WSL, and headless environments.
    """
    creds = None
    token_file = 'token.json'
    credentials_file = 'credentials.json'
    
    # Load existing token
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, GOOGLE_SCOPES)
        except Exception as e:
            logger.warning(f"Failed to load token.json: {e}")
            creds = None
    
    # Refresh or obtain new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logger.info("Refreshing expired token...")
                creds.refresh(Request())
                logger.info("✓ Token refreshed successfully")
            except Exception as e:
                logger.warning(f"Token refresh failed: {e}")
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_file):
                logger.error(f"Missing {credentials_file}")
                logger.error("Download OAuth 2.0 Client ID credentials from Google Cloud Console")
                logger.error("https://console.cloud.google.com/apis/credentials")
                sys.exit(1)
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, GOOGLE_SCOPES
                )
                
                # Environment-specific authentication
                if is_wsl():
                    logger.info("WSL environment detected")
                    logger.info("=" * 60)
                    logger.info("AUTHENTICATION REQUIRED")
                    logger.info("=" * 60)
                    logger.info("\nPlease follow these steps:")
                    logger.info("1. A URL will be displayed below")
                    logger.info("2. Open it using one of these commands:")
                    logger.info("   - wslview <url>")
                    logger.info("   - explorer.exe <url>")
                    logger.info("3. Authorize the application in your browser")
                    logger.info("4. Copy the authorization code")
                    logger.info("5. Paste it back here")
                    logger.info("=" * 60)
                    
                    creds = flow.run_local_server(port=0)
                elif is_headless():
                    logger.info("Headless environment detected - using manual auth flow")
                    logger.info("=" * 60)
                    logger.info("MANUAL AUTHENTICATION REQUIRED")
                    logger.info("=" * 60)
                    creds = flow.run_local_server(port=0, open_browser=False)
                else:
                    logger.info("Interactive environment detected - opening browser...")
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                logger.info(f"✓ Credentials saved to {token_file}")
                
            except Exception as e:
                logger.error(f"Authentication failed: {e}")
                logger.error("\nTroubleshooting:")
                logger.error("1. Ensure credentials.json is valid")
                logger.error("2. Check that required APIs are enabled in Google Cloud Console")
                logger.error("3. Verify OAuth consent screen is configured")
                sys.exit(1)
    
    return creds

# ============================================================================
# GLOBAL INITIALIZATION (NON-SERIALIZABLE OBJECTS)
# ============================================================================

# Load environment variables
load_dotenv()

# Validate environment
validate_environment()

# Initialize Google credentials and API clients
logger.info("Initializing Google API clients...")
google_creds = get_google_credentials()
sheets_service = build('sheets', 'v4', credentials=google_creds)
gmail_service = build('gmail', 'v1', credentials=google_creds)
logger.info("✓ Google API clients initialized")

# Initialize OpenAI client
logger.info("Initializing OpenAI client...")
llm = ChatOpenAI(
    model=DEFAULT_MODEL,
    temperature=0.7,
    api_key=os.getenv('OPENAI_API_KEY')
)
logger.info(f"✓ OpenAI client initialized (model: {DEFAULT_MODEL})")

# Hunter.io API key
HUNTER_API_KEY = os.getenv('HUNTER_API_KEY')

# Google Spreadsheet ID
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')

# Initialize checkpointer for state persistence
checkpointer = MemorySaver()

# ============================================================================
# TASK FUNCTIONS (SYNCHRONOUS)
# ============================================================================

@task
def fetch_website_content(url: str) -> Optional[str]:
    """
    Fetch HTML content from a website URL.
    
    Args:
        url: Company website URL
        
    Returns:
        HTML content as string or None if failed
    """
    try:
        logger.info(f"Fetching content from: {url}")
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

@task
def extract_text_from_html(html_content: str) -> str:
    """
    Extract text content from HTML body using BeautifulSoup.
    
    Args:
        html_content: Raw HTML content
        
    Returns:
        Extracted text content
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # Get text from body
        body = soup.find('body')
        if body:
            text = body.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = ' '.join(text.split())
        return text[:5000]  # Limit to 5000 chars to avoid token limits
    except Exception as e:
        logger.error(f"Failed to extract text from HTML: {e}")
        return ""

@task
def summarize_company(text_content: str) -> str:
    """
    Generate a concise company summary using OpenAI.
    
    Args:
        text_content: Extracted website text
        
    Returns:
        AI-generated company summary
    """
    try:
        prompt = (
            "Summarize the following website content. "
            "Focus on what the company does and its main value proposition. "
            "Keep it concise, under 75 words. "
            f"Here is the content: {text_content}"
        )
        
        response = llm.invoke(prompt)
        summary = response.content.strip()
        logger.info(f"Generated summary: {summary[:100]}...")
        return summary
    except Exception as e:
        logger.error(f"Failed to generate summary: {e}")
        return ""

@task
def find_contacts_hunter(company_url: str) -> Dict[str, Any]:
    """
    Find email addresses for a company domain using Hunter.io API.
    
    Args:
        company_url: Company website URL
        
    Returns:
        Dictionary with emails, organization name, and domain
    """
    try:
        # Extract domain from URL
        parsed = urlparse(company_url)
        domain = parsed.netloc if parsed.netloc else parsed.path
        domain = domain.replace('www.', '')
        
        logger.info(f"Searching Hunter.io for domain: {domain}")
        
        # Call Hunter.io API
        response = requests.get(
            'https://api.hunter.io/v2/domain-search',
            params={
                'domain': domain,
                'api_key': HUNTER_API_KEY
            },
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('data'):
            result = {
                'emails': data['data'].get('emails', []),
                'organization': data['data'].get('organization', ''),
                'domain': domain
            }
            logger.info(f"Found {len(result['emails'])} email(s) for {domain}")
            return result
        else:
            logger.warning(f"No data returned from Hunter.io for {domain}")
            return {'emails': [], 'organization': '', 'domain': domain}
            
    except Exception as e:
        logger.error(f"Hunter.io API error: {e}")
        return {'emails': [], 'organization': '', 'domain': domain}

@task
def generate_email_body(summary: str, first_name: str, last_name: str) -> str:
    """
    Generate personalized cold email body using OpenAI.
    
    Args:
        summary: Company summary
        first_name: Contact's first name
        last_name: Contact's last name
        
    Returns:
        Generated email body
    """
    try:
        prompt = f"""AVOID PURPLE PROSE. USE AS FEW WORDS AS POSSIBLE.

USE THESE FOLLOWING EXAMPLES AS THEY'RE VERY GOOD. STICK VERY CLOSE TO THIS STYLE AND EXACT TONE.

EXAMPLE 1:

Hey Tom,

I lead the team at AgentHub.dev and found you online when looking for Intelligent Automation consultants. We're an AI-first intelligent automation platform.

We're backed by the same people as AirBnB and Doordash but looking to explore collaborating with existing companies in the field.

Would love to chat this week if you're open to it.

EXAMPLE 2:

Hey Priti,

Hope this cold email is alright — found Cognizant's website and thought I'd reach out since we're building in the intelligent automation space.

I lead the team at AgentHub.dev, we're an AI-first intelligent automation tool. We're backed by the same people as AirBnB and Doordash but fully focused on helping businesses automate work with AI.

Would love to chat about potential collaboration if you're open to it.

ALWAYS SIGN OFF WITH:

-----
Best
Kaushalya N
Co-Founder

Context:
Summary of company: {summary}
Contact person: {first_name} {last_name}"""

        response = llm.invoke(prompt)
        email_body = response.content.strip()
        logger.info("Generated email body")
        return email_body
    except Exception as e:
        logger.error(f"Failed to generate email body: {e}")
        return ""

@task
def generate_email_subject(summary: str, organization: str, first_name: str, last_name: str) -> str:
    """
    Generate email subject line using OpenAI.
    
    Args:
        summary: Company summary
        organization: Company name
        first_name: Contact's first name
        last_name: Contact's last name
        
    Returns:
        Generated subject line
    """
    try:
        prompt = f"""Context:
Summary of company: {summary}
Company Name: {organization}
Contact person: {first_name} {last_name}

Write a 3 to 4 word subject to grab their attention. Mention their company name and partnership.
Here is an example: 'Potential Partnership with Cognizant'"""

        response = llm.invoke(prompt)
        subject = response.content.strip()
        logger.info(f"Generated subject: {subject}")
        return subject
    except Exception as e:
        logger.error(f"Failed to generate email subject: {e}")
        return ""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def read_company_urls_from_sheets() -> List[str]:
    """
    Read company URLs from Google Sheets (Column A).
    
    Returns:
        List of company URLs
    """
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A:A'
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            logger.warning("No data found in Google Sheets")
            return []
        
        # Skip header row if present, filter empty values
        urls = [row[0] for row in values[1:] if row and row[0].strip()]
        logger.info(f"Read {len(urls)} company URLs from Google Sheets")
        return urls
        
    except HttpError as e:
        logger.error(f"Google Sheets API error: {e}")
        return []

def create_gmail_draft(to_email: str, subject: str, body: str) -> bool:
    """
    Create a draft email in Gmail using RFC 2822 format with base64url encoding.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create RFC 2822 formatted message
        message_text = f"To: {to_email}\r\n"
        message_text += f"Subject: {subject}\r\n"
        message_text += "\r\n"  # Blank line separates headers from body
        message_text += body
        
        # Encode as base64url (Gmail API requirement)
        # Must use UTF-8 encoding first, then base64url encoding
        message_bytes = message_text.encode('utf-8')
        encoded_message = base64.urlsafe_b64encode(message_bytes).decode('utf-8')
        
        # Create draft
        draft_body = {
            'message': {
                'raw': encoded_message
            }
        }
        
        draft = gmail_service.users().drafts().create(
            userId='me',
            body=draft_body
        ).execute()
        
        logger.info(f"✓ Created Gmail draft for {to_email} (ID: {draft['id']})")
        return True
        
    except HttpError as e:
        logger.error(f"Gmail API error: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to create Gmail draft: {e}")
        return False

def update_success_log(company_url: str, contact_email: str, contact_name: str) -> bool:
    """
    Update Google Sheets Success log with contact information.
    
    Args:
        company_url: Company website URL
        contact_email: Contact email address
        contact_name: Contact full name
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Append to "Success" sheet
        values = [[company_url, contact_email, contact_name]]
        body = {'values': values}
        
        sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Success!A:C',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        logger.info(f"✓ Updated success log for {company_url}")
        return True
        
    except HttpError as e:
        logger.error(f"Failed to update success log: {e}")
        return False

def log_failed_lookup(domain: str) -> bool:
    """
    Log failed email lookups to Google Sheets Failures sheet.
    
    Args:
        domain: Domain that failed lookup
        
    Returns:
        True if successful, False otherwise
    """
    try:
        values = [[domain]]
        body = {'values': values}
        
        sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Failures!A:A',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        logger.info(f"✓ Logged failed lookup for {domain}")
        return True
        
    except HttpError as e:
        logger.error(f"Failed to log failed lookup: {e}")
        return False

# ============================================================================
# MAIN WORKFLOW (ENTRYPOINT)
# ============================================================================

@entrypoint(checkpointer=checkpointer)
def outbound_sales_workflow(company_urls: List[str]) -> Dict[str, Any]:
    """
    Main workflow for automated outbound sales email campaign.
    
    Process:
    1. For each company URL:
       a. Fetch website content
       b. Extract and summarize text
       c. Find contact emails via Hunter.io
       d. If emails found:
          - Generate personalized email body and subject
          - Create Gmail draft
          - Log success
       e. If no emails found:
          - Log failure
    
    Args:
        company_urls: List of company website URLs (serializable input)
        
    Returns:
        Dictionary with processing results
    """
    logger.info("=" * 60)
    logger.info("STARTING AUTOMATED OUTBOUND SALES WORKFLOW")
    logger.info("=" * 60)
    logger.info(f"Processing {len(company_urls)} companies")
    
    results = {
        'processed': 0,
        'successes': 0,
        'failures': 0,
        'errors': 0
    }
    
    for idx, company_url in enumerate(company_urls, 1):
        logger.info(f"\n--- Processing company {idx}/{len(company_urls)}: {company_url} ---")
        
        try:
            # Step 1: Fetch website content
            fetch_task = fetch_website_content(company_url)
            html_content = fetch_task.result()
            
            if not html_content:
                logger.warning(f"Skipping {company_url} - failed to fetch content")
                results['errors'] += 1
                continue
            
            # Step 2: Extract text from HTML
            extract_task = extract_text_from_html(html_content)
            text_content = extract_task.result()
            
            if not text_content:
                logger.warning(f"Skipping {company_url} - failed to extract text")
                results['errors'] += 1
                continue
            
            # Step 3: Generate company summary
            summary_task = summarize_company(text_content)
            summary = summary_task.result()
            
            if not summary:
                logger.warning(f"Skipping {company_url} - failed to generate summary")
                results['errors'] += 1
                continue
            
            # Step 4: Find contact emails via Hunter.io
            hunter_task = find_contacts_hunter(company_url)
            hunter_data = hunter_task.result()
            
            emails = hunter_data.get('emails', [])
            organization = hunter_data.get('organization', '')
            domain = hunter_data.get('domain', '')
            
            # Step 5: Conditional branching based on email availability
            if emails and len(emails) > 0:
                # SUCCESS PATH: Generate email and create draft
                logger.info(f"✓ Found {len(emails)} email(s) - generating outreach email")
                
                first_email = emails[0]
                contact_email = first_email.get('value', '')
                first_name = first_email.get('first_name', '')
                last_name = first_email.get('last_name', '')
                contact_name = f"{first_name} {last_name}".strip()
                
                # Generate email body
                body_task = generate_email_body(summary, first_name, last_name)
                email_body = body_task.result()
                
                # Generate email subject
                subject_task = generate_email_subject(summary, organization, first_name, last_name)
                email_subject = subject_task.result()
                
                if email_body and email_subject:
                    # Create Gmail draft
                    if create_gmail_draft(contact_email, email_subject, email_body):
                        # Update success log
                        update_success_log(company_url, contact_email, contact_name)
                        results['successes'] += 1
                        logger.info(f"✓ SUCCESS: Completed processing for {company_url}")
                    else:
                        results['errors'] += 1
                else:
                    logger.warning("Failed to generate email content")
                    results['errors'] += 1
            else:
                # FAILURE PATH: No emails found
                logger.warning(f"✗ No emails found for {company_url}")
                log_failed_lookup(domain)
                results['failures'] += 1
            
            results['processed'] += 1
            
        except Exception as e:
            logger.error(f"Error processing {company_url}: {e}")
            results['errors'] += 1
            continue
    
    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("WORKFLOW COMPLETED")
    logger.info("=" * 60)
    logger.info(f"Total processed: {results['processed']}/{len(company_urls)}")
    logger.info(f"✓ Successes: {results['successes']} (emails generated)")
    logger.info(f"✗ Failures: {results['failures']} (no emails found)")
    logger.info(f"⚠ Errors: {results['errors']} (processing errors)")
    logger.info("=" * 60)
    
    return results

# ============================================================================
# EXECUTION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        # Read company URLs from Google Sheets
        logger.info("Reading company URLs from Google Sheets...")
        company_urls = read_company_urls_from_sheets()
        
        if not company_urls:
            logger.error("No company URLs found in Google Sheets")
            logger.error("Please add company URLs to column A in Sheet1")
            sys.exit(1)
        
        # Prepare configuration for workflow execution
        config = {
            "configurable": {
                "thread_id": "outbound-sales-001"
            }
        }
        
        # Execute workflow using synchronous invoke()
        logger.info("\nStarting workflow execution...")
        results = outbound_sales_workflow.invoke(
            company_urls,
            config=config
        )
        
        # Exit with appropriate status code
        if results['processed'] > 0 and results['errors'] < len(company_urls):
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
            
    except KeyboardInterrupt:
        logger.info("\n\nWorkflow interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n\nFatal error: {e}", exc_info=True)
        sys.exit(1)

