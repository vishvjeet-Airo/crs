"""
LangChain wrapper for AWS Bedrock with automatic LangSmith tracing, Langfuse tracing, and cost monitoring.
"""

from typing import Optional, Dict, Any
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import settings
import os
from dotenv import load_dotenv
load_dotenv()

# Langfuse imports
try:
    from langfuse import Langfuse
    from langfuse.callback import CallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    print("Warning: Langfuse not installed. Install with: pip install langfuse")


class TracedBedrockClient:
    """
    A simple wrapper around LangChain's ChatBedrock that provides cost monitoring.
    LangSmith tracing is handled automatically by LangChain when environment variables are set.
    Langfuse tracing is also supported for additional observability.
    """
    
    def __init__(self):
        self.client = ChatBedrock(
            model_id=settings.bedrock_model_id,
            region_name=settings.aws_region,
            streaming=False,
            max_tokens=10000
        )

        # Initialize Langfuse client if available
        self.langfuse_client = None
        self.langfuse_callback = None
        
        if LANGFUSE_AVAILABLE:
            try:
                # Check if Langfuse configuration is available
                langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
                langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
                langfuse_host =os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
                print(f"Langfuse secret key: {langfuse_secret_key}")
                print(f"Langfuse public key: {langfuse_public_key}")
                print(f"Langfuse host: {langfuse_host}")
                if langfuse_secret_key and langfuse_public_key:
                    langfuse=Langfuse(
                    secret_key=langfuse_secret_key,
                    public_key=langfuse_public_key,
                    host=langfuse_host
                    )
                    # self.langfuse_client = langfuse_client
                    self.langfuse_callback = CallbackHandler(
                            public_key=langfuse_public_key,
                            secret_key=langfuse_secret_key,
                            host=langfuse_host
                    )
                    if langfuse.auth_check():
                        print("Langfuse authentication successful")
                    else:
                        print("Langfuse authentication failed")
                else:
                    print("Warning: Langfuse credentials not set. Set LANGFUSE_SECRET_KEY and LANGFUSE_PUBLIC_KEY environment variables or configure in settings")
            except Exception as e:
                print(f"Warning: Failed to initialize Langfuse: {e}")
                self.langfuse_client = None
                self.langfuse_callback = None
    
    def invoke_with_tracing(
        self, 
        prompt: str, 
        system_message: Optional[str] = None
    ) -> str:
        """
        Invoke the Bedrock model with both LangSmith and Langfuse tracing.
        
        Args:
            prompt: The user prompt
            system_message: Optional system message
            metadata: Optional metadata for tracing
            trace_name: Optional name for the trace (for Langfuse)
            session_id: Optional session ID for grouping traces
            
        Returns:
            The model response as a string
        """
        # Prepare messages
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))
        messages.append(HumanMessage(content=prompt))
        
        # Start Langfuse trace if available
        # langfuse_trace = None
        # if self.langfuse_client and trace_name:
        #     try:
        #         langfuse_trace = self.langfuse_client(
        #             name=trace_name,
        #             session_id=session_id,
        #             metadata=metadata or {}
        #         )
        #     except Exception as e:
        #         print(f"Warning: Failed to start Langfuse trace: {e}")
        
        try:
            # Invoke with Langfuse callback if available
                 
            if self.langfuse_callback:
                self.langfuse_callback.flush()
                # Use Langfuse callback for automatic tracing
                response = self.client.invoke(messages, config={"callbacks": [self.langfuse_callback]})
            else:
                # Standard invoke - LangChain handles LangSmith tracing automatically
                response = self.client.invoke(messages)
            
            return response.content
            
        except Exception as e:
            print(f"Warning: Failed to log error to Langfuse: {e}")
            raise e
    
    def create_trace(self, name: str, session_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """
        Create a Langfuse trace for manual tracing.
        
        Args:
            name: Name of the trace
            session_id: Optional session ID for grouping traces
            metadata: Optional metadata for the trace
            
        Returns:
            Langfuse trace object or None if not available
        """
        if self.langfuse_client:
            try:
                return self.langfuse_client.trace(
                    name=name,
                    session_id=session_id,
                    metadata=metadata or {}
                )
            except Exception as e:
                print(f"Warning: Failed to create Langfuse trace: {e}")
        return None
    
    def flush_langfuse(self):
        """
        Flush pending Langfuse events to ensure they are sent.
        """
        if self.langfuse_client:
            try:
                self.langfuse_client.flush()
            except Exception as e:
                print(f"Warning: Failed to flush Langfuse events: {e}")
    
    def get_cost_estimate(self, prompt: str, response: str) -> Dict[str, float]:
        """
        Get cost estimate for the API call.
        Note: This is a simplified estimation. Actual costs may vary.
        
        Args:
            prompt: Input prompt
            response: Model response
            
        Returns:
            Dictionary with cost estimates
        """
        # Claude 3 Sonnet pricing (as of 2024)
        # Input: $3.00 per 1M tokens
        # Output: $15.00 per 1M tokens
        
        # Rough token estimation (1 token ≈ 4 characters)
        input_tokens = len(prompt) / 4
        output_tokens = len(response) / 4
        
        input_cost = (input_tokens / 1_000_000) * 3.00
        output_cost = (output_tokens / 1_000_000) * 15.00
        total_cost = input_cost + output_cost
        
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost_usd": input_cost,
            "output_cost_usd": output_cost,
            "total_cost_usd": total_cost
        }


# Global instance
bedrock_client = TracedBedrockClient()

# Example usage:
# 
# # Basic usage (LangSmith tracing only, if env vars are set)
# response = bedrock_client.invoke_with_tracing("Hello, world!")
# 
# # With Langfuse tracing
# response = bedrock_client.invoke_with_tracing(
#     prompt="Hello, world!",
#     system_message="You are a helpful assistant.",
#     trace_name="my_conversation",
#     session_id="user_123",
#     metadata={"user_id": "123", "feature": "chat"}
# )
# 
# # Manual trace creation
# trace = bedrock_client.create_trace("manual_trace", session_id="session_1")
# if trace:
#     trace.generation(name="custom_generation", input="test", output="result")
#     trace.update(output="final_result")
# 
# # Flush events to ensure they're sent
# bedrock_client.flush_langfuse()
