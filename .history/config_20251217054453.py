"""
Configuration Management
Centralizes all configuration settings
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application Settings"""
    
    # OpenAI
    openai_api_key: str = Field(..., env='OPENAI_API_KEY')
    openai_model: str = Field(default='gpt-4-turbo-preview', env='OPENAI_MODEL')
    
    # Anthropic (Optional)
    anthropic_api_key: Optional[str] = Field(default=None, env='ANTHROPIC_API_KEY')
    
    # Twilio WhatsApp
    twilio_account_sid: str = Field(..., env='TWILIO_ACCOUNT_SID')
    twilio_auth_token: str = Field(..., env='TWILIO_AUTH_TOKEN')
    twilio_whatsapp_number: str = Field(..., env='TWILIO_WHATSAPP_NUMBER')
    
    # Google Gmail API
    google_client_id: str = Field(..., env='GOOGLE_CLIENT_ID')
    google_client_secret: str = Field(..., env='GOOGLE_CLIENT_SECRET')
    google_redirect_uri: str = Field(..., env='GOOGLE_REDIRECT_URI')
    
    # Database
    database_url: str = Field(..., env='DATABASE_URL')
    redis_url: str = Field(default='redis://localhost:6379/0', env='REDIS_URL')
    mongodb_url: str = Field(..., env='MONGODB_URL')
    
    # Vector Store
    chroma_persist_dir: str = Field(default='./data/chroma', env='CHROMA_PERSIST_DIR')
    vector_dimension: int = Field(default=1536, env='VECTOR_DIMENSION')
    
    # Security
    secret_key: str = Field(..., env='SECRET_KEY')
    encryption_key: str = Field(..., env='ENCRYPTION_KEY')
    
    # Server
    host: str = Field(default='0.0.0.0', env='HOST')
    port: int = Field(default=8000, env='PORT')
    debug: bool = Field(default=False, env='DEBUG')
    
    # Agent Configuration
    max_iterations: int = Field(default=5, env='MAX_ITERATIONS')
    agent_timeout: int = Field(default=30, env='AGENT_TIMEOUT')
    enable_memory: bool = Field(default=True, env='ENABLE_MEMORY')
    enable_validation: bool = Field(default=True, env='ENABLE_VALIDATION')
    
    # Logging
    log_level: str = Field(default='INFO', env='LOG_LEVEL')
    log_file: str = Field(default='./logs/multiagent.log', env='LOG_FILE')
    
    class Config:
        env_file = '.env'
        case_sensitive = False


# Global settings instance
settings = Settings()


# Ensure directories exist
def ensure_directories():
    """Create necessary directories"""
    directories = [
        Path(settings.chroma_persist_dir),
        Path(settings.log_file).parent,
        Path('./data/memory'),
        Path('./data/cache'),
        Path('./credentials')
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


ensure_directories()
