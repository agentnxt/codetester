# CodeTester

An AI-powered code testing agent built using the GitHub Copilot SDK.

## Overview

CodeTester is an agent that uses GitHub Copilot's agentic capabilities to automatically test code. It can:
- Run test suites on code files
- Analyze test results
- Provide feedback on test outcomes
- Assist with debugging failing tests

## Installation

```bash
pip install -e ".[dev]"
```

Or with uv:

```bash
uv pip install -e ".[dev]"
```

## Quick Start

```python
import asyncio
from codetester import CodeTesterAgent

async def main():
    async with CodeTesterAgent() as agent:
        # Test a Python file
        result = await agent.test_file("path/to/your/code.py")
        print(result)

asyncio.run(main())
```

## Usage

### Basic Testing

```python
import asyncio
from codetester import CodeTesterAgent

async def main():
    async with CodeTesterAgent() as agent:
        # Run tests on a file
        result = await agent.test_file(
            "path/to/your/code.py",
            test_command="pytest tests/"  # Optional custom test command
        )
        print(f"Test result: {result['status']}")
        print(f"Output: {result['output']}")

asyncio.run(main())
```

### Using with Custom Tools

```python
import asyncio
from codetester import CodeTesterAgent, define_tool
from pydantic import BaseModel, Field

class LintParams(BaseModel):
    path: str = Field(description="Path to file or directory to lint")

@define_tool(description="Run linter on code")
async def lint_tool(params: LintParams) -> str:
    import subprocess
    result = subprocess.run(
        ["pylint", params.path],
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

async def main():
    async with CodeTesterAgent() as agent:
        result = await agent.test_file(
            "path/to/your/code.py",
            custom_tools=[lint_tool]
        )

asyncio.run(main())
```

## API Reference

### CodeTesterAgent

The main agent class for testing code.

#### Constructor

```python
CodeTesterAgent(
    config=None,        # SubprocessConfig | ExternalServerConfig | None
    auto_start=True,    # Auto-start the Copilot CLI
)
```

#### Methods

##### test_file

Run tests on a code file.

```python
await agent.test_file(
    file_path: str,           # Path to the file to test
    test_command: str,        # Command to run tests (default: "python -m pytest")
    custom_tools: list,       # Optional custom tools to register
    model: str                # Model to use (default: "gpt-5")
) -> dict
```

Returns a dictionary with:
- `status`: "passed", "failed", or "error"
- `output`: Test output
- `passed`: Number of tests passed
- `failed`: Number of tests failed
- `errors`: Number of errors

##### test_directory

Run tests on all files in a directory.

```python
await agent.test_directory(
    directory: str,           # Directory to test
    test_command: str,       # Command to run tests
    pattern: str             # File pattern to match (default: "*.py")
) -> list[dict]
```

Returns a list of test results for each file.

## License

---

## GitHub Container Registry (ghcr.io)

To build and push the Docker image to ghcr.io:

```bash
# Login to ghcr.io
echo "$GITHUB_TOKEN" | docker login ghcr.io -u x-token-auth --password-stdin

# Build the image
docker build -t ghcr.io/agentnxt/codetester:latest .

# Push to ghcr.io
docker push ghcr.io/agentnxt/codetester:latest
```

To pull the image:
```bash
docker pull ghcr.io/agentnxt/codetester:latest
```