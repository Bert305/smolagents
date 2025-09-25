#!/usr/bin/env python3
"""
Simple Gradio UI for smolagents
"""

import os
from smolagents import CodeAgent, InferenceClientModel, WebSearchTool, GradioUI, tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@tool
def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression safely.
    
    Args:
        expression: The mathematical expression to evaluate
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def create_agent():
    """Create and return a configured agent"""
    model = InferenceClientModel(
        model_id="meta-llama/Llama-3.3-70B-Instruct", 
        provider="fireworks-ai"
    )
    
    agent = CodeAgent(
        tools=[WebSearchTool(), calculate],
        model=model,
        verbosity_level=1,
        planning_interval=3,
        name="MySmolAgent",
        description="A helpful assistant that can search the web and do calculations",
        stream_outputs=True,
    )
    
    return agent

if __name__ == "__main__":
    if not os.getenv("HF_TOKEN"):
        print("⚠️ Please add your HF_TOKEN to the .env file!")
        exit(1)
        
    print("🚀 Starting Gradio UI for smolagents...")
    agent = create_agent()
    
    # Create and launch the Gradio interface
    ui = GradioUI(
        agent, 
        file_upload_folder="./uploads",  # Optional: for file uploads
    )
    
    # Launch with specific settings
    ui.launch(
        share=False,  # Set to True to create a public link
        server_name="127.0.0.1",  # localhost
        server_port=7860,  # default Gradio port
        show_error=True
    )