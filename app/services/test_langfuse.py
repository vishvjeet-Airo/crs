from app.services.langchain_bedrock import bedrock_client

def test_langfuse():
    response = bedrock_client.invoke_with_tracing(
    prompt="Hello, world!",
    system_message="You are a helpful assistant.",
    )

    print(response)
    
if __name__ == "__main__":
    test_langfuse()
