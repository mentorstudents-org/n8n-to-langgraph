# Testing and Troubleshooting Guide

## Environment-Specific Setup

### Setup Table by Environment

| Environment | Setup Steps | Authentication Method | Notes |
|-------------|-------------|----------------------|-------|
| Local (Interactive) | Install deps, create .env, download credentials.json, run script | Automatic browser OAuth | Browser opens automatically |
| SSH/Remote (Headless) | Install deps, create .env, download credentials.json, run script | Manual OAuth with URL | Follow terminal instructions |
| WSL | Install deps, create .env, download credentials.json, run script | Hybrid OAuth | Use `wslview <url>` or `explorer.exe <url>` |
| Docker | Build image, mount credentials volume, set env vars | Service Account or manual OAuth | Don't copy credentials into image |
| CI/CD | Set secrets in CI config | Service Account or env vars | Use secrets management |

## Authentication Troubleshooting

### Common Errors
- **"No valid authentication method found"**: Check credentials.json exists or env vars set
- **"Failed to exchange authorization code"**: Ensure code copied correctly
- **"Token expired"**: Delete token.json and re-authenticate
- **"Permission denied"**: Enable required APIs in Google Cloud Console
- **"Invalid credentials"**: Verify credentials.json not corrupted

### Environment-Specific Issues
- **SSH/Headless**: Ensure copy-paste works between terminal and browser
- **WSL**: Use Windows browsers via `wslview` or `explorer.exe`
- **Docker**: Mount credentials as volumes, not copied into image
- **CI/CD**: Use secrets management, never hardcode credentials

### Debug Mode
- Enable debug-level logging for authentication
- Display current authentication strategy
- Show environment detection results
- Verify credential validity
- Provide detailed error information

## API Integration Troubleshooting

### Common API Errors
- **"Invalid value at '<field>' (TYPE_BYTES)"**: Field expects base64-encoded bytes, not plain text
- **"Base64 decoding failed"**: Content not properly base64url encoded or contains invalid characters
- **"Request had invalid authentication credentials"**: Check API key format and expiration
- **"Quota exceeded"**: Review API usage limits and implement rate limiting
- **"Resource not found"**: Verify endpoint URLs and resource IDs are correct
- **"Permission denied"**: Check OAuth scopes and API enablement in cloud console

### Debugging Strategy
- Read full error message including field names and expected types
- Consult official API documentation for that specific field
- Test with minimal example to isolate format issues
- Verify data encoding/transformation steps
- Check for character encoding issues (UTF-8, special characters)
- Use API explorers or Postman to verify request format
- Add detailed logging before and after data transformations
- Validate data format matches API specification exactly

## Implementation Error Troubleshooting

### Common Implementation Errors
1. **Sync/Async Mismatch (CRITICAL)**: Never mix synchronous entrypoint with async tasks
2. **Wrong Method Calls**: Match sync/async pattern in method calls
3. **Wrong Invocation Method**: Use `.invoke()` for sync, `.ainvoke()` for async
4. **Missing LangGraph Decorators**: Always use `@entrypoint` and `@task` decorators
5. **Non-Serializable Inputs**: Never pass credentials or API clients as entrypoint inputs

### Error Messages and Solutions
- **"In a sync context async tasks cannot be called"**: Ensure entrypoint and tasks match sync/async pattern
- **"Cannot serialize"**: Move non-serializable objects to global initialization
- **"Missing decorator"**: Add appropriate LangGraph decorators to functions

## Testing Procedures

### Pre-Implementation Testing
- Test authentication flow in target environment
- Verify API credentials and permissions
- Test minimal API calls to validate format
- Check environment variable loading

### During Development
- Test with simple examples first
- Verify data format matches API specification
- Test encoding/decoding operations independently
- Validate with different data types and edge cases

### Post-Implementation Testing
- Test complete workflow end-to-end
- Verify error handling scenarios
- Test in different environments
- Validate performance and scalability

## Debug Mode Instructions

### Authentication Debug
- Enable debug-level logging for authentication
- Display current authentication strategy
- Show environment detection results
- Verify credential validity
- Provide detailed error information

### API Debug
- Add detailed logging before and after data transformations
- Log request/response data (sanitized)
- Verify data format matches API specification exactly
- Test with API explorers or Postman

### Workflow Debug
- Enable step-by-step execution logging
- Log state transitions
- Verify node connections and data flow
- Test error recovery scenarios
