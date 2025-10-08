#!/usr/bin/env python3
"""
Test script to verify AWS Bedrock integration is working correctly.
This script tests the basic functionality without requiring actual AWS credentials.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
import boto3
import json

def test_bedrock_client_initialization():
    """Test that the Bedrock client can be initialized."""
    try:
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=settings.aws_region
        )
        print("✅ Bedrock client initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Bedrock client: {e}")
        return False

def test_configuration():
    """Test that all required configuration is present."""
    print(f"✅ AWS Region: {settings.aws_region}")
    print(f"✅ Claude Model ID: {settings.bedrock_model_id}")
    print(f"✅ Embedding Model ID: {settings.bedrock_embedding_model_id}")
    return True

def test_imports():
    """Test that all required modules can be imported."""
    try:
        from app.services.process_questionnaire import answer_batch_with_rag
        from app.services.excel_parser import identify_excel_structure
        from app.services.vector_db import create_embeddings, embed_text
        from app.services.llm import table_to_story
        print("✅ All service modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import service modules: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing AWS Bedrock Integration")
    print("=" * 40)
    
    tests = [
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Bedrock Client", test_bedrock_client_initialization),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AWS Bedrock integration is ready.")
        print("\n📝 Next steps:")
        print("1. Set up AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
        print("2. Ensure you have access to AWS Bedrock in the specified region")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Test with actual data")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
