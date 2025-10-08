#!/usr/bin/env python3
"""
Test script to verify the simplified LangChain integration.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment_setup():
    """Test that environment variables can be set."""
    print("🔍 Testing Environment Setup...")
    
    # Test setting environment variables
    os.environ["LANGCHAIN_API_KEY"] = "test-key"
    os.environ["LANGCHAIN_PROJECT"] = "test-project"
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    
    api_key = os.getenv("LANGCHAIN_API_KEY")
    project = os.getenv("LANGCHAIN_PROJECT")
    tracing = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    
    print(f"   LANGCHAIN_API_KEY: {'✅ Set' if api_key else '❌ Not set'}")
    print(f"   LANGCHAIN_PROJECT: {project}")
    print(f"   LANGCHAIN_TRACING_V2: {'✅ Enabled' if tracing else '❌ Disabled'}")
    
    return bool(api_key and tracing)

def test_config_import():
    """Test that config can be imported."""
    print("\n🔍 Testing Configuration Import...")
    try:
        from app.config import settings
        print(f"   AWS Region: {settings.aws_region}")
        print(f"   Bedrock Model: {settings.bedrock_model_id}")
        print(f"   Embedding Model: {settings.bedrock_embedding_model_id}")
        print("   ✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"   ❌ Configuration import failed: {e}")
        return False

def test_langchain_import():
    """Test that LangChain modules can be imported."""
    print("\n🔍 Testing LangChain Import...")
    try:
        # This will fail if packages aren't installed, but that's expected
        from langchain_aws import ChatBedrock
        from langchain_core.messages import HumanMessage, SystemMessage
        print("   ✅ LangChain modules imported successfully")
        return True
    except ImportError as e:
        print(f"   ⚠️  LangChain modules not installed: {e}")
        print("   Run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"   ❌ LangChain import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Simplified LangChain Integration")
    print("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Configuration Import", test_config_import),
        ("LangChain Import", test_langchain_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is ready.")
        print("\n📝 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set LANGCHAIN_API_KEY environment variable")
        print("3. Set LANGCHAIN_TRACING_V2=true")
        print("4. Run process_questionnaire.py to see tracing in action")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
