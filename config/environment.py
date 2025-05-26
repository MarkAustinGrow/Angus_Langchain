"""
Environment configuration for Agent Angus LangChain implementation.

This module loads environment variables and provides them as constants.
"""
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
env_file_paths = ['.env', '../.env', '../../.env']
env_loaded = False

for env_path in env_file_paths:
    if os.path.exists(env_path):
        logger.info(f"Loading environment variables from {env_path}")
        load_dotenv(env_path)
        env_loaded = True
        break

if not env_loaded:
    logger.warning("No .env file found, using system environment variables")

# Original Agent Angus credentials (from original config)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SONOTELLER_API_KEY = os.getenv("SONOTELLER_API_KEY", "58fafc6204msh41ac38769729b59p17fbc3jsneeebeb330eb2")

# Coral Protocol specific configuration
CORAL_SERVER_HOST = os.getenv("CORAL_SERVER_HOST", "coral.pushcollective.club")
CORAL_SERVER_PORT = int(os.getenv("CORAL_SERVER_PORT", "443"))
CORAL_SERVER_URL = os.getenv("CORAL_SERVER_URL", "https://coral.pushcollective.club")

# Agent configuration
AGENT_LOG_LEVEL = os.getenv("AGENT_LOG_LEVEL", "INFO")
AGENT_HEARTBEAT_INTERVAL = int(os.getenv("AGENT_HEARTBEAT_INTERVAL", "30"))  # seconds
AGENT_RETRY_ATTEMPTS = int(os.getenv("AGENT_RETRY_ATTEMPTS", "3"))
AGENT_RETRY_DELAY = int(os.getenv("AGENT_RETRY_DELAY", "5"))  # seconds

# Task scheduling configuration
UPLOAD_TASK_INTERVAL = int(os.getenv("UPLOAD_TASK_INTERVAL", "3600"))  # 1 hour in seconds
COMMENT_TASK_INTERVAL = int(os.getenv("COMMENT_TASK_INTERVAL", "3600"))  # 1 hour in seconds
CLEANUP_TASK_INTERVAL = int(os.getenv("CLEANUP_TASK_INTERVAL", "86400"))  # 1 day in seconds

# Processing limits
MAX_SONGS_PER_BATCH = int(os.getenv("MAX_SONGS_PER_BATCH", "5"))
MAX_COMMENTS_PER_VIDEO = int(os.getenv("MAX_COMMENTS_PER_VIDEO", "100"))
MAX_REPLIES_PER_BATCH = int(os.getenv("MAX_REPLIES_PER_BATCH", "10"))
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", "7"))

# Development/Debug settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
MOCK_YOUTUBE_API = os.getenv("MOCK_YOUTUBE_API", "false").lower() == "true"
MOCK_OPENAI_API = os.getenv("MOCK_OPENAI_API", "false").lower() == "true"

# Validate required environment variables
def validate_environment():
    """Validate that all required environment variables are set."""
    required_vars = {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "YOUTUBE_CLIENT_ID": YOUTUBE_CLIENT_ID,
        "YOUTUBE_CLIENT_SECRET": YOUTUBE_CLIENT_SECRET,
        "YOUTUBE_CHANNEL_ID": YOUTUBE_CHANNEL_ID
    }
    
    missing_vars = []
    for var_name, var_value in required_vars.items():
        if not var_value:
            missing_vars.append(var_name)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    logger.info("All required environment variables are set")
    return True

# Optional validation warnings
def check_optional_vars():
    """Check optional environment variables and log warnings if missing."""
    optional_vars = {
        "YOUTUBE_API_KEY": YOUTUBE_API_KEY,
        "SONOTELLER_API_KEY": SONOTELLER_API_KEY
    }
    
    for var_name, var_value in optional_vars.items():
        if not var_value:
            logger.warning(f"Optional environment variable {var_name} is not set")

# Run validation on import
if __name__ != "__main__":
    validate_environment()
    check_optional_vars()

# Environment summary for debugging
def print_environment_summary():
    """Print a summary of the current environment configuration."""
    print("\n=== Agent Angus Environment Configuration ===")
    print(f"Coral Server: {CORAL_SERVER_URL}")
    print(f"Debug Mode: {DEBUG_MODE}")
    print(f"Mock YouTube API: {MOCK_YOUTUBE_API}")
    print(f"Mock OpenAI API: {MOCK_OPENAI_API}")
    print(f"Log Level: {AGENT_LOG_LEVEL}")
    print(f"Max Songs per Batch: {MAX_SONGS_PER_BATCH}")
    print(f"Max Replies per Batch: {MAX_REPLIES_PER_BATCH}")
    print(f"Upload Task Interval: {UPLOAD_TASK_INTERVAL}s")
    print(f"Comment Task Interval: {COMMENT_TASK_INTERVAL}s")
    print("=" * 45)

if __name__ == "__main__":
    print_environment_summary()
