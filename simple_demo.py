#!/usr/bin/env python3
"""
Simple smolagents demo that works without optional dependencies
"""

import os
from smolagents import CodeAgent, InferenceClientModel, tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check HF token
if not os.getenv("HF_TOKEN"):
    print("⚠️ Warning: HF_TOKEN not found in .env file!")
    exit(1)

@tool
def simple_calculator(expression: str) -> str:
    """
    Calculate a mathematical expression safely.
    
    Args:
        expression: Mathematical expression like "2+2" or "10*5+3"
    """
    try:
        # Safe evaluation using eval with restricted globals
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_system_info() -> str:
    """
    Get basic system information.
    """
    import platform
    import datetime
    
    info = f"""System Information:
- OS: {platform.system()} {platform.release()}
- Python: {platform.python_version()}
- Current Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Platform: {platform.platform()}"""
    
    return info

def main():
    print("🤖 Simple smolagents Demo")
    print("=" * 40)
    
    # Create model using HF Inference API
    model = InferenceClientModel(
        model_id="meta-llama/Llama-3.3-70B-Instruct",
        provider="fireworks-ai"
    )
    
    # Create agent with basic tools
    agent = CodeAgent(
        tools=[simple_calculator, get_system_info],
        model=model,
        verbosity_level=2,
        stream_outputs=True
    )
    
    print("\n🚀 Running agent with calculation task...")
    result1 = agent.run("Calculate (25 * 4) + (100 / 5) and tell me what that equals")
    print(f"\n✅ Result 1: {result1}")
    
    print("\n" + "="*40)
    print("🚀 Running agent with system info task...")
    result2 = agent.run("Get the system information and tell me what OS I'm running")
    print(f"\n✅ Result 2: {result2}")

if __name__ == "__main__":
    main()