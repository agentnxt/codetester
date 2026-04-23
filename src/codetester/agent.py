"""CodeTester Agent - AI-powered code testing using GitHub Copilot SDK."""

import asyncio
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field

from copilot import CopilotClient, SubprocessConfig, define_tool
from copilot.generated.session_events import (
    AssistantMessageData,
    SessionIdleData,
)
from copilot.session import PermissionHandler


class TestResult(BaseModel):
    """Result of a test run."""

    status: str = Field(description="Test status: passed, failed, or error")
    output: str = Field(description="Test output")
    passed: int = Field(default=0, description="Number of tests passed")
    failed: int = Field(default=0, description="Number of tests failed")
    errors: int = Field(default=0, description="Number of errors")
    file_path: str = Field(description="Path to the tested file")


class RunTestParams(BaseModel):
    """Parameters for running tests on a file."""

    file_path: str = Field(description="Path to the file to test")
    test_command: str = Field(
        default="python -m pytest",
        description="Command to run tests"
    )


def parse_pytest_output(output: str) -> dict:
    """Parse pytest output to extract test results."""
    result = {
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "status": "error"
    }

    # Match patterns like "5 passed" or "3 failed, 2 passed"
    passed_match = re.search(r'(\d+) passed', output)
    failed_match = re.search(r'(\d+) failed', output)
    error_match = re.search(r'(\d+) error', output)

    if passed_match:
        result["passed"] = int(passed_match.group(1))
    if failed_match:
        result["failed"] = int(failed_match.group(1))
    if error_match:
        result["errors"] = int(error_match.group(1))

    if result["errors"] > 0:
        result["status"] = "error"
    elif result["failed"] > 0:
        result["status"] = "failed"
    elif result["passed"] > 0 or "passed" in output.lower():
        result["status"] = "passed"
    else:
        result["status"] = "error"

    return result


@define_tool(description="Run tests on a code file using pytest")
async def run_tests(params: RunTestParams) -> str:
    """Run tests on a code file."""
    file_path = Path(params.file_path)
    if not file_path.exists():
        return json.dumps({"error": f"File not found: {params.file_path}"})

    # Determine the test command
    test_cmd = params.test_command or "python -m pytest"

    # Get the directory of the file
    file_dir = str(file_path.parent)

    try:
        # Run the test command
        result = subprocess.run(
            f"{test_cmd} {file_path}",
            shell=True,
            capture_output=True,
            text=True,
            cwd=file_dir,
            timeout=300
        )

        output = result.stdout + result.stderr

        # Parse the output
        parsed = parse_pytest_output(output)
        parsed["output"] = output
        parsed["file_path"] = params.file_path
        parsed["return_code"] = result.returncode

        return json.dumps(parsed)
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Test execution timed out", "status": "error"})
    except Exception as e:
        return json.dumps({"error": str(e), "status": "error"})


@define_tool(description="Read file content for analysis")
async def read_file_for_analysis(params: dict) -> str:
    """Read a file and return its content for analysis."""
    file_path = Path(params.get("path", ""))
    if not file_path.exists():
        return f"Error: File not found: {params.get('path')}"

    try:
        content = file_path.read_text(encoding="utf-8")
        # Truncate if too long
        max_length = 10000
        if len(content) > max_length:
            content = content[:max_length] + f"\n\n... (truncated, total {len(content)} chars)"
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


class CodeTesterAgent:
    """
    An AI-powered code testing agent using GitHub Copilot SDK.

    This agent can automatically test code files and provide feedback
    on test outcomes using the Copilot agentic workflow.
    """

    def __init__(
        self,
        config: Optional[SubprocessConfig] = None,
        auto_start: bool = True,
    ):
        """
        Initialize the CodeTester agent.

        Args:
            config: Optional Copilot client configuration.
            auto_start: Whether to auto-start the Copilot CLI.
        """
        self._config = config
        self._auto_start = auto_start
        self._client: Optional[CopilotClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = CopilotClient(self._config, auto_start=self._auto_start)
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def test_file(
        self,
        file_path: str,
        test_command: str = "python -m pytest",
        custom_tools: Optional[list] = None,
        model: str = "gpt-5",
    ) -> dict:
        """
        Run tests on a code file.

        Args:
            file_path: Path to the file to test.
            test_command: Command to run tests (default: pytest).
            custom_tools: Optional list of custom tools to register.
            model: Model to use for the agent.

        Returns:
            Dictionary with test results including status, output, and counts.
        """
        if not self._client:
            raise RuntimeError("Agent not started. Use 'async with' context manager.")

        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            return {
                "status": "error",
                "output": f"File not found: {file_path}",
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "file_path": file_path,
            }

        # Build list of tools
        tools = [run_tests]

        if custom_tools:
            tools.extend(custom_tools)

        # Create session and run tests
        async with await self._client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model=model,
            tools=tools,
        ) as session:
            done = asyncio.Event()

            result = {"status": "pending", "output": "", "file_path": file_path}

            def on_event(event):
                nonlocal result
                if isinstance(event.data, AssistantMessageData):
                    # Parse the assistant's response for test results
                    content = event.data.content
                    if content:
                        # Try to extract JSON from the response
                        try:
                            # Look for JSON in the response
                            json_match = re.search(r'\{[^{}]*\}', content)
                            if json_match:
                                parsed = json.loads(json_match.group())
                                result.update(parsed)
                        except (json.JSONDecodeError, AttributeError):
                            # Just use the raw content
                            result["output"] = content
                elif isinstance(event.data, SessionIdleData):
                    done.set()

            session.on(on_event)

            # Send a message to run tests
            await session.send(
                f"Please run tests on the file at `{file_path}` using the `run_tests` tool. "
                f"Use the test command: {test_command}. "
                f"After running the tests, provide a summary of the results in JSON format."
            )

            await done.wait()

            return result

    async def test_directory(
        self,
        directory: str,
        test_command: str = "python -m pytest",
        pattern: str = "*.py",
    ) -> list[dict]:
        """
        Run tests on all files matching a pattern in a directory.

        Args:
            directory: Directory to search for files.
            test_command: Command to run tests.
            pattern: File pattern to match (default: "*.py").

        Returns:
            List of test results for each file.
        """
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            return [{"status": "error", "output": f"Directory not found: {directory}"}]

        # Find all matching files
        files = list(dir_path.rglob(pattern))

        results = []
        for file_path in files:
            result = await self.test_file(
                str(file_path),
                test_command=test_command,
            )
            results.append(result)

        return results

    async def analyze_and_fix(
        self,
        file_path: str,
        test_command: str = "python -m pytest",
    ) -> dict:
        """
        Run tests on a file and ask the agent to analyze failures and suggest fixes.

        Args:
            file_path: Path to the file to test.
            test_command: Command to run tests.

        Returns:
            Dictionary with test results and any suggested fixes.
        """
        if not self._client:
            raise RuntimeError("Agent not started. Use 'async with' context manager.")

        # First run the tests
        test_result = await self.test_file(file_path, test_command)

        # If tests passed, return early
        if test_result.get("status") == "passed":
            test_result["suggestions"] = []
            return test_result

        # If tests failed, ask for analysis
        async with await self._client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-5",
        ) as session:
            done = asyncio.Event()
            analysis = {"suggestions": []}

            def on_event(event):
                nonlocal analysis
                if isinstance(event.data, AssistantMessageData):
                    content = event.data.content
                    if content:
                        analysis["suggestions"].append(content)
                elif isinstance(event.data, SessionIdleData):
                    done.set()

            session.on(on_event)

            await session.send(
                f"The tests for `{file_path}` failed. "
                f"Test output:\n{test_result.get('output', '')}\n\n"
                f"Please analyze the test failures and suggest how to fix them."
            )

            await done.wait()

            test_result["suggestions"] = analysis["suggestions"]
            return test_result


# Convenience function for quick testing
async def quick_test(
    file_path: str,
    test_command: str = "python -m pytest",
) -> dict:
    """
    Quickly test a file without creating an explicit agent context.

    Args:
        file_path: Path to the file to test.
        test_command: Command to run tests.

    Returns:
        Test results dictionary.
    """
    async with CodeTesterAgent() as agent:
        return await agent.test_file(file_path, test_command)