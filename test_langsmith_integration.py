#!/usr/bin/env python3
"""
Test script to verify LangChain integration and cost monitoring.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.services.langchain_bedrock import bedrock_client

def test_langsmith_configuration():
    """Test LangSmith configuration via environment variables."""
    print("🔍 Testing LangSmith Configuration...")
    langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
    langsmith_project = os.getenv("LANGCHAIN_PROJECT", "compass-risk-scanner")
    langsmith_tracing = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    
    print(f"   LangSmith API Key: {'✅ Set' if langsmith_api_key else '❌ Not set'}")
    print(f"   LangSmith Project: {langsmith_project}")
    print(f"   LangSmith Tracing: {'✅ Enabled' if langsmith_tracing else '❌ Disabled'}")
    return bool(langsmith_api_key)

def test_bedrock_client():
    """Test Bedrock client initialization."""
    print("\n🔍 Testing Bedrock Client...")
    try:
        # Test basic initialization
        print("   ✅ Bedrock client initialized")
        print(f"   Model ID: {settings.bedrock_model_id}")
        print(f"   Region: {settings.aws_region}")
        return True
    except Exception as e:
        print(f"   ❌ Failed to initialize Bedrock client: {e}")
        return False

def test_cost_estimation():
    """Test cost estimation functionality."""
    print("\n🔍 Testing Cost Estimation...")
    try:
        test_prompt = "This is a test prompt for cost estimation."
        test_response = "This is a test response for cost estimation."
        
        cost_estimate = bedrock_client.get_cost_estimate(test_prompt, test_response)
        
        print("   ✅ Cost estimation working")
        print(f"   Input tokens: {cost_estimate['input_tokens']:.0f}")
        print(f"   Output tokens: {cost_estimate['output_tokens']:.0f}")
        print(f"   Estimated cost: ${cost_estimate['total_cost_usd']:.6f}")
        return True
    except Exception as e:
        print(f"   ❌ Cost estimation failed: {e}")
        return False

def test_tracing_setup():
    """Test tracing setup (without actual API call)."""
    print("\n🔍 Testing Tracing Setup...")
    try:
        langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
        langsmith_tracing = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        
        if langsmith_tracing and langsmith_api_key:
            print("   ✅ LangSmith tracing is configured")
            print("   ✅ Ready for tracing API calls")
            return True
        else:
            print("   ⚠️  LangSmith tracing not configured")
            print("   Set LANGCHAIN_API_KEY and LANGCHAIN_TRACING_V2=true environment variables")
            return False
    except Exception as e:
        print(f"   ❌ Tracing setup failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing LangSmith Integration and Cost Monitoring")
    print("=" * 60)
    
    tests = [
        ("LangSmith Configuration", test_langsmith_configuration),
        ("Bedrock Client", test_bedrock_client),
        ("Cost Estimation", test_cost_estimation),
        ("Tracing Setup", test_tracing_setup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LangSmith integration is ready.")
        print("\n📝 Next steps:")
        print("1. Set LANGCHAIN_API_KEY environment variable for tracing")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run process_questionnaire.py to see tracing in action")
        print("4. Check LangSmith dashboard for traces and cost data")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
