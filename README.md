# CodeTester 🚀

An **AI-powered code testing agent** built with the GitHub Copilot SDK. CodeTester automatically runs tests, analyzes failures, and suggests fixes—helping you debug faster and ship with confidence.

---

## 🎥 Demo

### 🔹 CLI Demo

![CLI Demo](./assets/demo-cli.gif)

### 🔹 AI Fix Suggestions

![AI Suggestions](./assets/demo-ai-fix.png)

> 💡 Tip: Add your screenshots/GIFs inside an `assets/` folder in the repo.

---

## ✨ Why CodeTester?

Most tools stop at running tests. CodeTester goes further:

- ✅ Runs your tests automatically
- 🧠 Explains *why* they fail
- 🔧 Suggests potential fixes

Think of it as a lightweight AI QA assistant built into your workflow.

---

## ⚙️ Features

- **Automated Testing** – Run pytest or custom commands
- **AI Failure Analysis** – Understand errors instantly
- **Fix Suggestions** – Get actionable improvements
- **Custom Tooling** – Extend with `@define_tool`
- **Multi-language Ready** – Python, JS/TS, and more
- **Docker Support** – Easy containerized setup
- **CI/CD Ready** – GitHub Actions included

---

## 📦 Installation

```bash
git clone https://github.com/agentnxt/codetester.git
cd codetester
pip install -e ".[dev]"
```

---

## 🚀 Quick Example

```python
import asyncio
from codetester import CodeTesterAgent

async def main():
    async with CodeTesterAgent() as agent:
        result = await agent.test_file("app.py")
        print(result)

asyncio.run(main())
```

---

## 🧠 AI-Powered Debugging

```python
result = await agent.analyze_and_fix("app.py")
print(result["suggestions"])
```

Get:
- Root cause explanations
- Suggested fixes
- Cleaner debugging workflow

---

## 🔧 Core API

### `test_file`
Run tests on a file

### `test_directory`
Run tests across a folder

### `analyze_and_fix`
Run tests + AI suggestions

---

## 🐳 Docker

### Pull from Docker Hub

```bash
docker pull <dockerhub-username>/codetester:latest
```

### Publish to Docker Hub (GitHub Actions)

This repository includes `.github/workflows/publish-dockerhub.yml`.

1. Add repository secrets:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN` (Docker Hub access token)
2. Push to `main` (publishes `latest`) or create a tag like `v1.0.0`.
3. Or run **Publish Docker image to Docker Hub** manually from Actions.

---

## ⚙️ Environment Setup

Create `.env`:

```bash
COPILOT_GITHUB_TOKEN=your_token
GITHUB_TOKEN=your_token
```

---

## ⚠️ Requirements

- Python 3.10+
- GitHub Copilot / API access
- Docker (optional)

---

## 🤝 Contributing

PRs welcome. For major changes, open an issue first.

---

## 📄 License

MIT License

---

## 🔗 Links

- Copilot SDK: https://github.com/github/copilot-sdk
- PyPI: https://pypi.org/project/codetester/

---

<p align="center">Built with ❤️ using GitHub Copilot SDK</p>
