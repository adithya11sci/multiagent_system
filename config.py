"""
Configuration for Railway Intelligence Multi-Agent System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configurations
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_PROVIDER = "groq" if GROQ_API_KEY else "gemini"

# Models
GEMINI_MODEL = "gemini-pro"
GROQ_MODEL = "llama-3.3-70b-versatile" # High performance model

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///railway_intelligence.db")

# Mock Mode Configuration
# Only mock if NO keys are available
MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() == "true"
if not GEMINI_API_KEY and not GROQ_API_KEY:
    MOCK_MODE = True
    print("\n⚠️  No API Keys found. Running in MOCK MODE.")
else:
    # If we have a key, we force mock mode off unless explicitly set
    if os.getenv("MOCK_MODE") is None:
        MOCK_MODE = False


# Vector Store Configuration
VECTOR_STORE_PATH = "./data/vector_store"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# RAG Configuration
RAG_DATA_SOURCES = {
    "timetables": "./data/rag/timetables.json",
    "policies": "./data/rag/policies.txt",
    "refund_rules": "./data/rag/refund_rules.txt",
    "route_maps": "./data/rag/route_maps.json"
}

# Alert Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Email Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# System Configuration
MAX_RETRY_ATTEMPTS = 3
AGENT_TIMEOUT = 30  # seconds
LOG_LEVEL = "INFO"

# Agent Configuration
AGENT_CONFIG = {
    "planner": {
        "model": GROQ_MODEL if LLM_PROVIDER == "groq" else GEMINI_MODEL,
        "temperature": 0.7,
        "max_tokens": 2048
    },
    "operations": {
        "model": GROQ_MODEL if LLM_PROVIDER == "groq" else GEMINI_MODEL,
        "temperature": 0.3,
        "max_tokens": 1500
    },
    "passenger": {
        "model": GROQ_MODEL if LLM_PROVIDER == "groq" else GEMINI_MODEL,
        "temperature": 0.5,
        "max_tokens": 1500,
        "use_rag": True
    },
    "alert": {
        "model": GROQ_MODEL if LLM_PROVIDER == "groq" else "gemini-pro",
        "description": "Handles external communications"
    }
}
