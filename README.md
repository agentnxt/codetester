# CodeTester

<p align="center">
  <a href="https://github.com/agentnxt/codetester">
    <img src="https://img.shields.io/badge/GitHub-Repo-blue?style=for-the-badge" alt="GitHub">
  </a>
  <a href="https://github.com/agentnxt/codetester/pkgs/container/codetester">
    <img src="https://img.shields.io/badge/ghcr.io-Package-green?style=for-the-badge" alt="Docker">
  </a>
  <a href="https://pypi.org/project/codetester/">
    <img src="https://img.shields.io/badge/PyPI-Package-orange?style=for-the-badge" alt="PyPI">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
  </a>
</p>

An AI-powered code testing agent built using the [GitHub Copilot SDK](https://github.com/github/copilot-sdk). CodeTester leverages Copilot's agentic capabilities to automatically test code, analyze results, and provide feedback.

## ✨ Features

- **Automated Testing** - Run tests on code files using pytest or custom test commands
- **AI-Powered Analysis** - Get intelligent feedback on test failures with fix suggestions
- **Custom Tools** - Extend functionality with custom tools using the `@define_tool` decorator
- **Multiple Language Support** - Works with Python, JavaScript, TypeScript, and more
- **Docker Support** - Ready-to-use Docker container with docker-compose
- **GitHub Actions** - Automated CI/CD with included workflow

## 📋 Requirements

- Python 3.10+
- GitHub Copilot subscription (or BYOK with custom API key)
- Docker (optional, for containerized usage)

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/agentnxt/codetester.git
cd codetester

# Install with pip
pip install -e ".[dev]"

# Or with uv
uv pip install -e ".[dev]"
```

### Basic Usage

```python
import asyncio
from codetester import CodeTesterAgent

async def main():
    async with CodeTesterAgent() as agent:
        # Test a Python file
        result = await agent.test_file("path/to/your/code.py")
        print(f"Status: {result['status']}")
        print(f"Output: {result['output']}")

asyncio.run(main())
```

### Using with Custom Test Command

```python
import asyncio
from codetester import CodeTesterAgent

async def main():
    async with CodeTesterAgent() as agent:
        result = await agent.test_file(
            "path/to/your/code.py",
            test_command="python -m pytest -v --tb=short"
        )

asyncio.run(main())
```

## 🔧 API Reference

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

##### `test_file`

Run tests on a single code file.

```python
await agent.test_file(
    file_path: str,           # Path to the file to test
    test_command: str,        # Command to run tests (default: "python -m pytest")
    custom_tools: list,       # Optional custom tools to register
    model: str                # Model to use (default: "gpt-5")
) -> dict
```

Returns:
```python
{
    "status": "passed" | "failed" | "error",
    "output": "Test output text",
    "passed": 5,
    "failed": 1,
    "errors": 0,
    "file_path": "path/to/file.py"
}
```

##### `test_directory`

Run tests on all files in a directory.

```python
await agent.test_directory(
    directory: str,           # Directory to test
    test_command: str,       # Command to run tests
    pattern: str             # File pattern (default: "*.py")
) -> list[dict]
```

##### `analyze_and_fix`

Run tests and get AI-powered fix suggestions.

```python
await agent.analyze_and_fix(
    file_path: str,           # Path to the file to test
    test_command: str        # Command to run tests
) -> dict
```

Returns test results plus `suggestions` list with AI-generated fixes.

### Custom Tools

Define custom tools using the `@define_tool` decorator:

```python
from codetester import CodeTesterAgent, define_tool
from pydantic import BaseModel, Field

class MyToolParams(BaseModel):
    path: str = Field(description="Path to file")

@define_tool(description="My custom tool description")
async def my_tool(params: MyToolParams) -> str:
    # Your tool logic here
    return "Tool result"

async def main():
    async with CodeTesterAgent() as agent:
        result = await agent.test_file(
            "path/to/code.py",
            custom_tools=[my_tool]
        )

asyncio.run(main())
```

## 🐳 Docker Usage

### Pull from ghcr.io

```bash
docker pull ghcr.io/agentnxt/codetester:latest
```

### Build Locally

```bash
docker build -t ghcr.io/agentnxt/codetester:latest .
```

### Using docker-compose.yaml

```bash
# Start the service
docker-compose -f docker-compose.yaml up --build

# Run in detached mode
docker-compose -f docker-compose.yaml up -d

# View logs
docker-compose -f docker-compose.yaml logs -f

# Stop services
docker-compose -f docker-compose.yaml down
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
COPILOT_GITHUB_TOKEN=your_github_token_here
GITHUB_TOKEN=your_github_token_here
```

## ⚙️ GitHub Actions

The repository includes a CI/CD workflow (`.github/workflows/docker.yaml`) that:

- Builds and pushes Docker image to ghcr.io on main branch pushes
- Validates docker-compose configuration

### Required Secrets

For GitHub Actions to push to ghcr.io, add these secrets:

- `GITHUB_TOKEN` - Automatically provided by GitHub (with packages:write scope)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- [Copilot SDK Documentation](https://docs.github.com/en/copilot)
- [PyPI Package](https://pypi.org/project/codetester/)
- [Docker Hub](https://github.com/agentnxt/codetester/pkgs/container/codetester)

---

<p align="center">Built with ❤️ using <a href="https://github.com/github/copilot-sdk">GitHub Copilot SDK</a></p>