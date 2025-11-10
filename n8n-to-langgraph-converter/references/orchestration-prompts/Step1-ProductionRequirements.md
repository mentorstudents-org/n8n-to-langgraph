You are an expert N8N developer and system analyst. Your task is to analyze the provided n8n workflow JSON and create a detailed technical specification for building and debugging an equivalent Express.js application. Separate platform features (implementation capabilities) from workflow configuration (business-specific values).

IMPORTANT: Always describe configurations in plain language. Do not use n8n expressions directly--instead, explain the logic in plain English.

### Global Workflow Summary

- **Objective:** Concisely state the workflow's main purpose and business goal.
- **Workflow Settings:** List any workflow-level configurations found in the JSON (e.g., error workflow reference, timezone, save execution progress).
- **Triggers:** List all entry points (e.g., webhook method/path, cron schedule) and when responses are sent (immediate vs. after execution). Include any trigger-specific configurations.
- **Execution Rules:** Concurrency limits, batching rules, retry/backoff strategy, and timeout settings (global and per-node).
- **Security:** Inbound auth (method, scopes, CORS/CSRF, body limits) and outbound auth (type, token handling, secret source).
- **Error Handling:** How the workflow handles failures globally (stop, skip, error node).

### Per Node Specification

For each node (use the name or type as the heading):

- **Functionality:** Plain-English description of what the node does and any external services used.
- **Built-in Parameters to Replicate:** List the n8n node's native capabilities and configuration options that define HOW the node operates. Features such as authentication modes, execution mode (per-item/per-batch), retries, timeouts, continue-on-fail, output format, pagination, rate limits, and error output handling.
- **Workflow-Specific Configuration:** Actual business values like API endpoints, database names/tables, query params, field mappings, or constants--describe in plain language.
- **Data Mapping:** How input data is transformed to output data, including defaults and conditions.
- **Success Path:** Which node(s) run next and under what conditions.
- **Error Path:** Behavior if the node fails (stop, skip, or route to error handler).

- **If the node is a custom node** (e.g., Function, Lambda, or not part of the standard n8n library), generate a stub specification:
    - Clearly mark it as **custom**.
    - Describe any visible inputs/outputs in plain English if possible.
    - Add a note: "Implementation for this node lives in `/req-for-custom-nodes/<node-name>.md`."
    - Do not invent internal logic -- just reference the external file.

### Additional Requirements for Express.js Implementation

Based on the workflow analysis, note any additional requirements:
- Required middleware (body parsing, CORS, authentication)
- External service dependencies
- Rate limiting or throttling needs
- Error handling strategy
- Data validation requirements

n8n JSON Code:
[PASTE YOUR N8N JSON CODE HERE]

