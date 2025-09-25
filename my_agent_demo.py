#!/usr/bin/env python3
"""
Simple demo of smolagents - Multiple ways to run agents
"""

import os
from smolagents import (
    CodeAgent,
    InferenceClientModel,
    tool,
)

# Try to import optional models - handle if not available
try:
    from smolagents import LiteLLMModel
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    print("ℹ️  LiteLLMModel not available - skipping OpenAI/Anthropic demos")

try:
    from smolagents import WebSearchTool
    WEBSEARCH_AVAILABLE = True
except ImportError:
    WEBSEARCH_AVAILABLE = False
    print("ℹ️  WebSearchTool not available")

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Verify HF token is loaded
if not os.getenv("HF_TOKEN"):
    print("⚠️ Warning: HF_TOKEN not found in environment variables!")
    print("Make sure you've added your Hugging Face token to the .env file")
    exit(1)

print("🤖 smolagents Demo - Choose your adventure!")
print("=" * 50)

# Custom tool example
@tool
def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression safely.
    
    Args:
        expression: The mathematical expression to evaluate (e.g., "2+2*3")
    """
    try:
        # Safe evaluation of mathematical expressions
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

def demo_basic_agent():
    """Demo 1: Basic agent with custom tool"""
    print("\n🔧 Demo 1: Basic CodeAgent with custom calculator tool")
    
    # Use Hugging Face Inference API (free tier)
    model = InferenceClientModel(
        model_id="meta-llama/Llama-3.3-70B-Instruct", 
        provider="fireworks-ai"
    )
    
    agent = CodeAgent(
        tools=[calculate],
        model=model,
        verbosity_level=2,
        stream_outputs=True
    )
    
    # Ask the agent to solve a math problem
    result = agent.run("Calculate (15 * 4) + (22 / 2) and explain the steps")
    print(f"\n✅ Agent Result: {result}")

def demo_search_agent():
    """Demo 2: Agent with web search capabilities"""
    if not WEBSEARCH_AVAILABLE:
        print("\n⚠️ Demo 2 Skipped: WebSearchTool not available")
        print("   Install with: pip install 'smolagents[toolkit]'")
        return
        
    print("\n🌐 Demo 2: CodeAgent with web search")
    
    model = InferenceClientModel(
        model_id="meta-llama/Llama-3.3-70B-Instruct",
        provider="fireworks-ai"
    )
    
    agent = CodeAgent(
        tools=[WebSearchTool(), calculate],
        model=model,
        verbosity_level=1,
        stream_outputs=True
    )
    
    # Ask the agent to search and calculate
    result = agent.run("What's the current population of Tokyo and calculate what percentage that is of Japan's total population?")
    print(f"\n✅ Agent Result: {result}")

def demo_with_openai():
    """Demo 3: Using OpenAI models (if API key is available)"""
    if not LITELLM_AVAILABLE:
        print("\n⚠️ Demo 3 Skipped: LiteLLMModel not available")
        print("   Install with: pip install 'smolagents[litellm]'")
        return
        
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️ Demo 3 Skipped: OPENAI_API_KEY not found in .env file")
        return
    
    print("\n🧠 Demo 3: CodeAgent with OpenAI GPT-4")
    
    model = LiteLLMModel(model_id="gpt-4o-mini")  # More cost-effective
    
    search_tool = WebSearchTool() if WEBSEARCH_AVAILABLE else None
    tools = [calculate] + ([search_tool] if search_tool else [])
    
    agent = CodeAgent(
        tools=tools,
        model=model,
        verbosity_level=1,
        stream_outputs=True
    )
    
    result = agent.run("Calculate the compound interest on $1000 at 5% annual rate for 10 years using the formula A = P(1+r)^t")
    print(f"\n✅ Agent Result: {result}")

def main():
    """Main demo selector"""
    demos = {
        "1": ("Basic Calculator Agent", demo_basic_agent),
        "2": ("Web Search Agent", demo_search_agent),
        "3": ("OpenAI Agent", demo_with_openai),
        "all": ("Run All Demos", lambda: [demo_basic_agent(), demo_search_agent(), demo_with_openai()])
    }
    
    print("\nAvailable demos:")
    for key, (name, _) in demos.items():
        print(f"  {key}: {name}")
    
    choice = input("\nChoose a demo (1, 2, 3, or 'all'): ").strip()
    
    if choice in demos:
        _, demo_func = demos[choice]
        try:
            demo_func()
        except KeyboardInterrupt:
            print("\n\n🛑 Demo interrupted by user")
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()