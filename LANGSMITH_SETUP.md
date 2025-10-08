# LangSmith Integration Setup

This document explains how to set up and use LangSmith tracing and cost monitoring with the Compass Risk Scanner.

## Overview

The application now includes:
- **Automatic LangSmith Tracing**: Track all LLM calls automatically via LangChain
- **Cost Monitoring**: Real-time cost estimation for AWS Bedrock calls
- **Performance Metrics**: Token usage and response time tracking

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure LangSmith (Environment Variables Only)

Set your LangSmith API key and enable tracing:

```bash
export LANGCHAIN_API_KEY="your-langsmith-api-key"
export LANGCHAIN_PROJECT="compass-risk-scanner"
export LANGCHAIN_TRACING_V2="true"
```

Or add to your `.env` file:

```env
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=compass-risk-scanner
LANGCHAIN_TRACING_V2=true
```

**That's it!** LangChain automatically handles all the tracing when these environment variables are set.

### 3. Configure AWS Bedrock

Ensure your AWS credentials are configured:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

## Usage

### Basic Usage

```python
from app.services.process_questionnaire import process_questionnaire

# Process questionnaire with tracing
output_path = process_questionnaire("example3.xlsx")
```

### Advanced Usage with Custom Tracing

```python
from app.services.langchain_bedrock import bedrock_client

# Make a traced call
response = bedrock_client.invoke_with_tracing(
    prompt="Your question here",
    system_message="You are a compliance expert.",
    metadata={
        "user_id": "user123",
        "session_id": "session456",
        "question_type": "compliance"
    }
)

# Get cost estimate
cost = bedrock_client.get_cost_estimate(prompt, response)
print(f"Cost: ${cost['total_cost_usd']:.6f}")
```

## Features

### 1. Automatic Tracing

All LLM calls are automatically traced with:
- Input prompts and system messages
- Model responses
- Metadata (batch info, question counts, etc.)
- Error handling and logging

### 2. Cost Monitoring

Real-time cost estimation includes:
- Input token count and cost
- Output token count and cost
- Total cost per call
- Cumulative cost tracking

### 3. Performance Metrics

Track:
- Response times
- Token usage patterns
- Batch processing efficiency
- Error rates

## LangSmith Dashboard

View your traces at: https://smith.langchain.com/

### Key Metrics to Monitor

1. **Cost Trends**: Track spending over time
2. **Token Usage**: Monitor input/output token patterns
3. **Error Rates**: Identify problematic prompts
4. **Response Quality**: Review model outputs
5. **Performance**: Track response times

### Useful Queries

- `run_type:llm` - View all LLM calls
- `metadata.batch_rows:exists` - View batch processing
- `inputs.prompt:contains("compliance")` - Filter by content

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LANGCHAIN_API_KEY` | LangSmith API key | Required |
| `LANGCHAIN_PROJECT` | Project name | `compass-risk-scanner` |
| `LANGCHAIN_TRACING_V2` | Enable tracing | `true` |
| `AWS_DEFAULT_REGION` | AWS region | `us-east-1` |

### Model Configuration

Edit `app/config.py` to customize AWS Bedrock settings:

```python
# AWS Bedrock configuration
aws_region: str = "us-east-1"
bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
bedrock_embedding_model_id: str = "amazon.titan-embed-text-v1"
```

**Note**: LangSmith configuration is handled entirely through environment variables - no code changes needed!

## Testing

Run the test suite:

```bash
python test_langsmith_integration.py
```

Run example usage:

```bash
python example_tracing_usage.py
```

## Troubleshooting

### Common Issues

1. **No traces appearing**: Check API key and project name
2. **Cost estimates incorrect**: Verify model pricing in code
3. **AWS errors**: Check credentials and region settings
4. **Import errors**: Ensure all dependencies are installed

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Cost Optimization

### Tips

1. **Batch Processing**: Process multiple questions together
2. **Prompt Optimization**: Use concise, clear prompts
3. **Context Management**: Limit context length when possible
4. **Model Selection**: Choose appropriate model for task complexity

### Monitoring

- Set up cost alerts in LangSmith
- Monitor token usage patterns
- Review and optimize frequent prompts
- Track cost per questionnaire processed

## Support

For issues or questions:
1. Check LangSmith documentation
2. Review AWS Bedrock pricing
3. Check application logs
4. Verify configuration settings
