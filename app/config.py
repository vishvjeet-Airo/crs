from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Compass Risk Scanner API"
    secret_key: str = "dev-secret-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 8

    # AWS Bedrock configuration
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    # bedrock_model_id: str = "openai.gpt-oss-120b-1:0"
    bedrock_embedding_model_id: str = "amazon.titan-embed-text-v1"
    
    # Langfuse configuration
    # langfuse_secret_key: Optional[str] = None
    # langfuse_public_key: Optional[str] = None
    # langfuse_host: str = "https://cloud.langfuse.com"
    
    section_column_hints: tuple[str, ...] = ("section", "sections", "category", "area")
    technology_column_hints: tuple[str, ...] = ("technology", "tech", "stack", "tool")

    class Config:
        env_file = ".env"
        env_prefix = "CRS_"


settings = Settings()
