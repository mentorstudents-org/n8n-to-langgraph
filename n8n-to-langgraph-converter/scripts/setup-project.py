#!/usr/bin/env python3
"""
Setup script for initializing a new LangGraph project structure.
This creates the necessary files and directories for a converted n8n workflow.
"""

import os
import sys
from pathlib import Path


def create_requirements_txt(project_dir: Path) -> None:
    """Create requirements.txt with necessary dependencies."""
    requirements = """# LangGraph Core
langgraph>=0.2.0
langgraph-checkpoint>=1.0.0

# LangChain and OpenAI
langchain-openai>=0.2.0
langchain-core>=0.3.0

# Google APIs (if needed)
google-auth>=2.34.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.147.0

# Web scraping & HTTP
requests>=2.32.0
beautifulsoup4>=4.12.0

# Configuration
python-dotenv>=1.0.0
"""

    requirements_path = project_dir / "requirements.txt"
    with open(requirements_path, 'w') as f:
        f.write(requirements)
    print(f"✅ Created {requirements_path}")


def create_env_template(project_dir: Path) -> None:
    """Create environment template file."""
    env_template = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Services (if using Gmail/Sheets)
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here

# Other API Keys (add as needed)
# HUNTER_API_KEY=your_hunter_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Environment
# ENVIRONMENT=development
"""

    env_path = project_dir / ".env.example"
    with open(env_path, 'w') as f:
        f.write(env_template)
    print(f"✅ Created {env_path}")


def create_gitignore(project_dir: Path) -> None:
    """Create .gitignore file."""
    gitignore = """# Environment files
.env
.env.local
token.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# Credentials
credentials.json
client_secret*.json

# OS
.DS_Store
Thumbs.db
"""

    gitignore_path = project_dir / ".gitignore"
    with open(gitignore_path, 'w') as f:
        f.write(gitignore)
    print(f"✅ Created {gitignore_path}")


def create_workflow_template(project_dir: Path) -> None:
    """Create a basic workflow template."""
    workflow_template = '''"""
LangGraph workflow converted from n8n.
Generated using n8n-to-langgraph-converter skill.
"""

import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv()

# Initialize checkpointer for state persistence
checkpointer = MemorySaver()


def validate_environment() -> None:
    """Validate that all required environment variables are set."""
    required_vars = [
        "OPENAI_API_KEY",
        # Add other required environment variables here
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}\\n"
            f"Please set them in your .env file or environment."
        )


# TODO: Initialize global non-serializable objects here
# Example:
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model="gpt-4", temperature=0.7)


@task
def example_task(input_data: str) -> Dict[str, Any]:
    """
    Example task function.
    Replace this with your actual task logic.
    """
    # TODO: Implement your task logic here
    return {"result": f"Processed: {input_data}"}


@entrypoint(checkpointer=checkpointer)
def workflow(inputs: List[str]) -> Dict[str, Any]:
    """
    Main workflow entrypoint.

    Args:
        inputs: List of input data (must be JSON-serializable)

    Returns:
        Dictionary containing workflow results
    """
    results = []

    for input_item in inputs:
        # Call task and get result
        task_result = example_task(input_item)
        result = task_result.result()
        results.append(result)

    return {
        "status": "completed",
        "results": results
    }


if __name__ == "__main__":
    # Validate environment
    validate_environment()

    # Example configuration with thread_id for checkpointing
    config = {
        "configurable": {
            "thread_id": "workflow-001"
        }
    }

    # Example input data
    example_inputs = ["item1", "item2", "item3"]

    # Execute workflow
    print("Starting workflow...")
    results = workflow.invoke(example_inputs, config=config)

    print("\\nWorkflow completed!")
    print(f"Results: {results}")
'''

    workflow_path = project_dir / "workflow.py"
    with open(workflow_path, 'w') as f:
        f.write(workflow_template)
    print(f"✅ Created {workflow_path}")


def create_readme(project_dir: Path, project_name: str) -> None:
    """Create README with setup instructions."""
    readme = f"""# {project_name}

LangGraph workflow converted from n8n using the n8n-to-langgraph-converter skill.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and fill in your API keys and configuration
   ```

3. **Set up authentication** (if using Google Services):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable required APIs (Gmail, Sheets, etc.)
   - Create OAuth 2.0 credentials
   - Download credentials as `credentials.json` and place in project root

## Usage

Run the workflow:

```bash
python workflow.py
```

## Project Structure

```
{project_name}/
├── workflow.py           # Main workflow implementation
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your configuration (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Customization

1. Edit `workflow.py` to implement your converted n8n logic
2. Add task functions using `@task` decorator
3. Implement main workflow logic in the `@entrypoint` function
4. Initialize non-serializable objects (LLMs, API clients) globally
5. Pass only JSON-serializable data to the entrypoint

## Important Notes

### Serialization Safety
- Initialize non-serializable objects (LLMs, API clients) globally
- Only pass JSON-serializable data to `@entrypoint` functions
- Access global objects from within workflow and task functions

### Sync/Async Consistency
- Keep all functions either synchronous OR asynchronous
- Never mix async tasks with sync entrypoint (or vice versa)
- Use `.result()` to get actual results from task Command objects

### Best Practices
- Use environment variables for all credentials and configuration
- Implement proper error handling in task functions
- Use checkpointing for workflow state persistence
- Test thoroughly before production deployment

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [n8n to LangGraph Converter Skill](https://github.com/anthropics/skills)
- [LangChain Documentation](https://python.langchain.com/)

## License

MIT
"""

    readme_path = project_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme)
    print(f"✅ Created {readme_path}")


def main():
    """Main setup function."""
    print("🚀 LangGraph Project Setup\n")

    # Get project name
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = input("Enter project name (default: langgraph-workflow): ").strip()
        if not project_name:
            project_name = "langgraph-workflow"

    # Create project directory
    project_dir = Path(project_name)

    if project_dir.exists():
        response = input(f"Directory '{project_name}' already exists. Continue? (y/n): ").strip().lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    else:
        project_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created project directory: {project_dir}\n")

    # Create project files
    print("Creating project files...")
    create_requirements_txt(project_dir)
    create_env_template(project_dir)
    create_gitignore(project_dir)
    create_workflow_template(project_dir)
    create_readme(project_dir, project_name)

    print(f"\n✨ Project setup complete!\n")
    print(f"Next steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. pip install -r requirements.txt")
    print(f"  3. cp .env.example .env")
    print(f"  4. Edit .env with your API keys")
    print(f"  5. Edit workflow.py to implement your n8n conversion")
    print(f"  6. python workflow.py")


if __name__ == "__main__":
    main()
