"""Example usage of CodeTester agent."""

import asyncio
from codetester import CodeTesterAgent


async def basic_example():
    """Basic example of testing a file."""
    print("=== Basic Example ===")
    
    async with CodeTesterAgent() as agent:
        # Test a Python file (replace with actual file path)
        # result = await agent.test_file("path/to/your/code.py")
        # print(f"Test result: {result}")
        print("Note: Provide a valid file path to test")
    print()


async def with_custom_test_command():
    """Example with custom test command."""
    print("=== Custom Test Command Example ===")
    
    async with CodeTesterAgent() as agent:
        # Use a custom test command
        # result = await agent.test_file(
        #     "path/to/your/code.py",
        #     test_command="python -m unittest discover"
        # )
        # print(f"Test result: {result}")
        print("Note: Provide a valid file path to test")
    print()


async def directory_test_example():
    """Example of testing all files in a directory."""
    print("=== Directory Test Example ===")
    
    async with CodeTesterAgent() as agent:
        # Test all Python files in a directory
        # results = await agent.test_directory(
        #     "path/to/your/project",
        #     test_command="pytest",
        #     pattern="test_*.py"
        # )
        # for result in results:
        #     print(f"File: {result['file_path']}, Status: {result['status']}")
        print("Note: Provide a valid directory path to test")
    print()


async def analyze_and_fix_example():
    """Example of testing and getting fix suggestions."""
    print("=== Analyze and Fix Example ===")
    
    async with CodeTesterAgent() as agent:
        # Test and get fix suggestions
        # result = await agent.analyze_and_fix(
        #     "path/to/your/code.py",
        #     test_command="pytest"
        # )
        # print(f"Status: {result['status']}")
        # if result.get('suggestions'):
        #     print("Suggestions:")
        #     for suggestion in result['suggestions']:
        #         print(f"  - {suggestion}")
        print("Note: Provide a valid file path to test")
    print()


async def quick_test_example():
    """Example using the quick_test convenience function."""
    print("=== Quick Test Example ===")
    
    # Using the convenience function
    # result = await quick_test("path/to/your/code.py")
    # print(f"Quick test result: {result}")
    print("Note: Provide a valid file path to test")
    print()


async def main():
    """Run all examples."""
    print("CodeTester Agent Examples\n")
    
    await basic_example()
    await with_custom_test_command()
    await directory_test_example()
    await analyze_and_fix_example()
    await quick_test_example()
    
    print("Examples complete!")


if __name__ == "__main__":
    asyncio.run(main())