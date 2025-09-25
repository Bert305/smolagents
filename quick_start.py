#!/usr/bin/env python3
"""
Quick smolagents command reference and usage examples
"""

# ============================================================================
# 🚀 smolagents COMMAND REFERENCE
# ============================================================================

# 1. BASIC CLI USAGE
# C:/Users/Owner/OneDrive/Desktop/hugging_face_agent/.venv/Scripts/python.exe -m smolagents.cli \
#   --model-type InferenceClientModel \
#   --model-id "meta-llama/Llama-3.3-70B-Instruct" \
#   --provider "fireworks-ai" \
#   "Your question here"

# 2. PYTHON SCRIPT USAGE
from smolagents import CodeAgent, InferenceClientModel, tool

# Create a custom tool
@tool
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together
    
    Args:
        a: First number to add
        b: Second number to add
    """
    return a + b

# Create agent
model = InferenceClientModel(
    model_id="meta-llama/Llama-3.3-70B-Instruct",
    provider="fireworks-ai"
)

agent = CodeAgent(
    tools=[add_numbers],
    model=model,
    verbosity_level=2
)

# Run the agent
if __name__ == "__main__":
    result = agent.run("What is 15 + 27?")
    print(f"\nFinal Result: {result}")