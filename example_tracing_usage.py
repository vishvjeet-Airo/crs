#!/usr/bin/env python3
"""
Example script showing how to use LangSmith tracing with the questionnaire processor.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.process_questionnaire import process_questionnaire
from app.services.langchain_bedrock import bedrock_client

def setup_langsmith():
    """Setup LangSmith environment variables."""
    # Check if LangSmith is already configured
    if os.getenv("LANGCHAIN_API_KEY") and os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true":
        print("✅ LangSmith tracing already enabled")
        return True
    
    # Set project name if not set
    if not os.getenv("LANGCHAIN_PROJECT"):
        os.environ["LANGCHAIN_PROJECT"] = "compass-risk-scanner"
    
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("⚠️  LANGCHAIN_API_KEY not set. Set it to enable tracing.")
        print("   Example: export LANGCHAIN_API_KEY='your-api-key-here'")
        print("   Example: export LANGCHAIN_TRACING_V2='true'")
        return False
    
    # Enable tracing
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    print("✅ LangSmith tracing enabled")
    return True

def example_single_call():
    """Example of a single traced call."""
    print("\n🔍 Example: Single Traced Call")
    print("-" * 40)
    
    # Example prompt
    prompt = "What are the key compliance requirements for data security?"
    system_message = "You are a compliance expert. Provide clear, actionable advice."
    
    # Make traced call
    response = bedrock_client.invoke_with_tracing(
        prompt=prompt,
        system_message=system_message,
        metadata={
            "example_type": "single_call",
            "user_id": "demo_user"
        }
    )
    
    print(f"Response: {response}")
    
    # Get cost estimate
    cost = bedrock_client.get_cost_estimate(prompt, response)
    print(f"Cost: ${cost['total_cost_usd']:.6f}")

def example_questionnaire_processing():
    """Example of processing a questionnaire with full tracing."""
    print("\n🔍 Example: Questionnaire Processing with Tracing")
    print("-" * 50)
    
    # Check if example file exists
    example_file = "example3.xlsx"
    if not os.path.exists(example_file):
        print(f"❌ Example file {example_file} not found")
        print("   Please ensure you have an Excel file to process")
        return
    
    try:
        # Process questionnaire with tracing
        output_path = process_questionnaire(example_file)
        print(f"✅ Processing complete. Output: {output_path}")
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")

def main():
    """Run examples."""
    print("🚀 LangSmith Tracing Examples")
    print("=" * 50)
    
    # Setup LangSmith
    if not setup_langsmith():
        print("⚠️  Continuing without tracing...")
    
    # Run examples
    try:
        example_single_call()
        example_questionnaire_processing()
        
        print("\n🎉 Examples completed!")
        print("\n📊 Check your LangSmith dashboard for traces:")
        print("   https://smith.langchain.com/")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")

if __name__ == "__main__":
    main()
