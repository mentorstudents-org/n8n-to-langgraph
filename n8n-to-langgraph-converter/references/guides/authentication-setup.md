# Authentication Setup Guide

## Authentication Flow Types

### Google Client Services (Gmail, Sheets, Drive)
- **Flow Type**: OAuth2 Interactive authentication with user consent
- **Credentials**: `credentials.json` from Google Cloud Console (OAuth 2.0 Client ID)
- **Setup Process**:
  1. Download `credentials.json` from Google Cloud Console
  2. Enable required APIs (Sheets, Gmail, etc.)
  3. First run: authenticate and create `token.json`

### GCP Services (Cloud Storage, BigQuery)
- **Flow Type**: Service Account Flow (server-to-server without user interaction)
- **Credentials**: Service account JSON key from GCP Console
- **Setup**: Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable to key file path

## Environment Detection

### Detection Functions
- **WSL Detection**: Check `WSL_DISTRO_NAME`, `WSLENV`, `/proc/version` for "microsoft"
- **Headless Detection**: Check `DISPLAY`, `SSH_CONNECTION`, `CI`, Docker indicators

### Environment-Specific Authentication

| Environment | Setup Steps | Authentication Method | Notes |
|-------------|-------------|----------------------|-------|
| Local (Interactive) | Install deps, create .env, download credentials.json, run script | Automatic browser OAuth | Browser opens automatically |
| SSH/Remote (Headless) | Install deps, create .env, download credentials.json, run script | Manual OAuth with URL | Follow terminal instructions |
| WSL | Install deps, create .env, download credentials.json, run script | Hybrid OAuth | Use `wslview <url>` or `explorer.exe <url>` |
| Docker | Build image, mount credentials volume, set env vars | Service Account or manual OAuth | Don't copy credentials into image |
| CI/CD | Set secrets in CI config | Service Account or env vars | Use secrets management |

## Authentication Mode Detection

### Strategy Selection with Fallback Chain
1. Service Account → OAuth Interactive → OAuth WSL → OAuth Headless → Environment Variables
2. Clear error messages when no valid method found

### WSL-Specific Instructions
- For WSL: print instructions to open URL via `wslview <url>` or `explorer.exe <url>`, then paste code
- If `wslview` not found, prompt user with installation instructions: `sudo apt update && sudo apt install wslu`
- If interactive auth fails, surface specific error with recovery guidance

## Token Management
- Automatic refresh on expiration
- Handle token expiration and refresh automatically

## Troubleshooting

### Common Errors
- "No valid authentication method found": Check credentials.json exists or env vars set
- "Failed to exchange authorization code": Ensure code copied correctly
- "Token expired": Delete token.json and re-authenticate
- "Permission denied": Enable required APIs in Google Cloud Console
- "Invalid credentials": Verify credentials.json not corrupted

### Environment-Specific Issues
- SSH/Headless: Ensure copy-paste works between terminal and browser
- WSL: Use Windows browsers via `wslview` or `explorer.exe`
- Docker: Mount credentials as volumes, not copied into image
- CI/CD: Use secrets management, never hardcode credentials

### Debug Mode
- Enable debug-level logging for authentication
- Display current authentication strategy
- Show environment detection results
- Verify credential validity
- Provide detailed error information
