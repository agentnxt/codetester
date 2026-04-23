"""CodeTester - An AI-powered code testing agent using GitHub Copilot SDK."""

from codetester.agent import CodeTesterAgent
from copilot import CopilotClient, define_tool

__version__ = "0.1.0"

__all__ = [
    "CodeTesterAgent",
    "CopilotClient",
    "define_tool",
]