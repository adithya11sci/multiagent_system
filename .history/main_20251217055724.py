"""
Main Entry Point
Starts the multi-agent system
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from services.webhook_handler import run_server
from config import settings
import logging
from loguru import logger


def setup_logging():
    """Setup logging configuration"""
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.log_level
    )
    
    # Add file handler
    logger.add(
        settings.log_file,
        rotation="500 MB",
        retention="10 days",
        level=settings.log_level
    )


def check_environment():
    """Check if environment is properly configured"""
    logger.info("Checking environment configuration...")
    
    # Check required env vars
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'SECRET_KEY'
    ]
    
    # Optional: Check if Ollama is running
    import requests
    try:
        response = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=2)
        if response.status_code == 200:
            logger.success(f"✓ Ollama is running at {settings.ollama_base_url}")
        else:
            logger.warning(f"⚠ Ollama returned status {response.status_code}")
    except:
        logger.warning("⚠ Cannot connect to Ollama. Make sure it's running: 'ollama serve'")
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please configure .env file. See .env.example for reference.")
        return False
    
    logger.success("✓ Environment configuration OK")
    return True


def display_banner():
    """Display startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         Multi-Agent WhatsApp System                          ║
║         Powered by LangChain + MCP                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)
    
    logger.info(f"Ollama URL: {settings.ollama_base_url}")
    logger.info(f"Ollama Model: {settings.ollama_model}")
    logger.info(f"Server: {settings.host}:{settings.port}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info(f"Memory Enabled: {settings.enable_memory}")
    logger.info(f"Validation Enabled: {settings.enable_validation}")
    print()


def main():
    """Main entry point"""
    # Setup logging
    setup_logging()
    
    # Display banner
    display_banner()
    
    # Check environment
    if not check_environment():
        logger.error("Environment check failed. Exiting.")
        sys.exit(1)
    
    logger.info("Starting Multi-Agent System...")
    
    try:
        # Start webhook server
        logger.info(f"Starting webhook server on {settings.host}:{settings.port}")
        run_server()
        
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        sys.exit(0)
        
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
