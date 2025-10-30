# API Integration Guide

## API Documentation Review Checklist

### Before Implementation
- Review API documentation for all external services used in workflow
- Understand exact data format requirements (encoding, structure, headers)
- Check for special requirements like base64 encoding, MIME formatting, or specific content types
- Verify API version and endpoints as specified in documentation

## Common API Format Issues

### Encoding Requirements
- **Base64**: Standard base64 encoding for binary data
- **Base64url**: URL-safe base64 (replace + with -, / with _, remove padding =)
- **URL Encoding**: Percent-encoding for URL parameters
- **Character Sets**: Ensure proper UTF-8 or other character encoding before transformations

### Message Structure
- **JSON**: Standard JSON format for REST APIs
- **XML**: XML structure for SOAP or legacy APIs
- **RFC Standards**: Email (RFC 2822), HTTP headers
- **MIME Types**: Multipart messages for attachments

### Header Requirements
- **Content-Type**: Specify correct MIME type
- **Authorization**: Bearer tokens, API keys, OAuth headers
- **Custom Headers**: API-specific requirements

### Field Types
- **TYPE_STRING**: Plain text fields
- **TYPE_BYTES**: Binary data requiring encoding
- **Distinguish**: Between string and bytes fields in API specifications

## Gmail API Specific Requirements

### Message Format
- **RFC 2822**: Gmail API requires RFC 2822 formatted messages
- **Base64url Encoding**: All message content must be base64url encoded
- **Raw Field**: Use base64url encoding for the raw field

### Email Structure
- **Headers**: Properly format headers (To, From, Subject)
- **Body Separation**: Blank line between headers and body
- **MIME Support**: For attachments or HTML emails, use proper MIME multipart formatting

### Implementation Details
- **Import Required**: Use base64 module for encoding operations
- **Character Encoding**: Ensure UTF-8 encoding for international characters before base64 encoding
- **Testing**: Verify encoded messages decode correctly to avoid API rejection errors

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

## Implementation Best Practices

### Data Formatting
- Always refer to official API documentation for exact requirements
- Test with simple cases first to verify format correctness
- Include proper error handling for encoding/decoding failures
- Add validation before sending to catch format errors early
- Import necessary standard library modules (base64, email.mime, etc.)
- Consider API-specific client libraries that handle formatting automatically
- Document any non-obvious data transformations with comments

### Error Handling
- Implement comprehensive error handling for API failures
- Handle rate limiting and quota exceeded scenarios
- Manage authentication token expiration
- Provide meaningful error messages for debugging

### Testing Approach
- Test with minimal examples first
- Verify data format matches API specification exactly
- Use API explorers to validate request format
- Test encoding/decoding operations independently
- Validate with different data types and edge cases
