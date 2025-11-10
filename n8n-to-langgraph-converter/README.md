# n8n-to-langgraph-converter Skill

A Claude Code skill for converting n8n workflow automations to LangGraph AI-orchestrated Python workflows.

## Overview

This skill enables Claude to systematically convert n8n workflows (no-code/low-code automation) into production-ready LangGraph implementations (AI-orchestrated Python workflows) using a comprehensive 3-phase methodology.

## Features

- **Systematic 3-Phase Conversion Process**
  - Phase 1: Production Requirements Analysis
  - Phase 2: Custom Logic Extraction (when needed)
  - Phase 3: LangGraph Implementation

- **Comprehensive Implementation Guides**
  - Paradigm selection (Functional API vs Graph API)
  - Authentication setup (OAuth2, environment detection)
  - API integration patterns (Gmail, Google Sheets, HTTP)
  - Testing and troubleshooting strategies
  - Best practices and common pitfalls

- **Complete Project Setup**
  - Helper script to initialize new projects
  - Requirements templates
  - Environment configuration
  - Code structure guidance

## When Claude Uses This Skill

Claude will automatically activate this skill when users:
- Provide an n8n workflow JSON export
- Request conversion from n8n to LangGraph
- Ask about migrating n8n automations to LangGraph
- Need help translating n8n nodes to LangGraph patterns

## Skill Structure

```
n8n-to-langgraph-converter/
├── SKILL.md                              # Skill definition and instructions
├── README.md                             # This file
├── scripts/
│   └── setup-project.py                  # Project initialization helper
└── references/
    ├── orchestration-prompts/            # 3-phase conversion methodology
    │   ├── Step1-ProductionRequirements.md
    │   ├── Step2-CustomLogic.md
    │   └── Step3-MainOrchestorPrompt.md
    └── guides/                           # Implementation best practices
        ├── paradigm-selection.md
        ├── functional-api-implementation.md
        ├── graph-api-implementation.md
        ├── authentication-setup.md
        ├── api-integration.md
        ├── project-structure.md
        ├── testing-and-troubleshooting.md
        └── output-requirements.md
```

## Installation

### Option 1: Use as part of this repository

If you're using this repository for n8n to LangGraph conversions, the skill is already included. Simply reference the skill in your Claude Code interactions.

### Option 2: Install as a standalone skill

1. Copy the entire `n8n-to-langgraph-converter/` directory to your Claude Code skills directory
2. Claude Code will automatically detect and load the skill

### Option 3: Clone and use

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/n8n-to-langgraph.git

# The skill is located in the n8n-to-langgraph-converter/ directory
cd n8n-to-langgraph/n8n-to-langgraph-converter
```

## Usage Example

### Basic Conversion

```
User: I have an n8n workflow that I need to convert to LangGraph.
      Here's the JSON export: [paste n8n JSON]

Claude: [Activates n8n-to-langgraph-converter skill]
        I'll help you convert this n8n workflow to LangGraph using
        a systematic 3-phase approach...

        [Proceeds with Phase 1: Requirements Analysis]
        [If needed: Phase 2: Custom Logic Extraction]
        [Phase 3: LangGraph Implementation]
        [Delivers complete Python code with setup instructions]
```

### With Helper Script

```
User: I need to set up a new LangGraph project for my converted workflow

Claude: [Uses scripts/setup-project.py]
        I'll help you set up a new LangGraph project structure...
```

## Conversion Process

1. **Phase 1: Production Requirements Analysis**
   - Analyzes n8n workflow JSON
   - Produces technical specifications
   - Identifies custom nodes and complexity

2. **Phase 2: Custom Logic Extraction** (if needed)
   - Documents custom function nodes
   - Analyzes Python/Node.js code
   - Develops translation strategies

3. **Phase 3: LangGraph Implementation**
   - Loads all implementation guides
   - Selects appropriate paradigm (Functional vs Graph API)
   - Generates complete Python code
   - Includes setup files and documentation

## Key Conversion Patterns

### Common n8n Node Mappings

| n8n Node | LangGraph Pattern |
|----------|-------------------|
| HTTP Request | `@task` with requests library |
| Function Node | `@task` or helper function |
| IF Node | Native Python `if/elif/else` |
| OpenAI Node | `@task` with LangChain LLM |
| Google Sheets | Helper function with Google API |
| Gmail | Helper function with base64url encoding |
| Loop | Python `for` loop |

### Critical Implementation Requirements

✅ **Serialization Safety**: Non-serializable objects initialized globally
✅ **Sync/Async Consistency**: No mixing of async and sync patterns
✅ **Environment-Aware Auth**: Detects headless/WSL/interactive environments
✅ **Proper Error Handling**: Comprehensive error handling and logging

❌ **Avoid These Pitfalls**:
- Never pass non-serializable objects to `@entrypoint`
- Never mix async tasks with sync entrypoint
- Never forget `.result()` when getting task returns
- Never hardcode credentials

## Helper Scripts

### setup-project.py

Initializes a new LangGraph project with proper structure:

```bash
python scripts/setup-project.py my-workflow

# Creates:
# my-workflow/
# ├── workflow.py
# ├── requirements.txt
# ├── .env.example
# ├── .gitignore
# └── README.md
```

## References

The skill includes comprehensive reference documentation:

- **Orchestration Prompts**: Step-by-step conversion methodology
- **Implementation Guides**: Best practices, patterns, and troubleshooting

All references are loaded contextually by Claude as needed during the conversion process.

## Output Quality

Successful conversions include:
- ✅ Complete Python implementation
- ✅ All n8n nodes mapped to LangGraph equivalents
- ✅ Proper serialization patterns
- ✅ Environment-aware authentication
- ✅ Error handling and logging
- ✅ `requirements.txt` with dependencies
- ✅ Environment template
- ✅ Setup and usage documentation

## Contributing

This skill is part of the n8n-to-langgraph conversion framework. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [n8n Documentation](https://docs.n8n.io/)
- [Claude Code Skills](https://github.com/anthropics/skills)
- [LangChain Documentation](https://python.langchain.com/)

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

---

**Created for**: Claude Code
**Version**: 1.0
**Last Updated**: 2025-11-10
