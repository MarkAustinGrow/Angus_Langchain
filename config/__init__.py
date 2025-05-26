"""
Configuration package for Agent Angus LangChain implementation.

This package contains configuration modules for the multi-agent system.
"""

from .environment import (
    SUPABASE_URL,
    SUPABASE_KEY,
    OPENAI_API_KEY,
    YOUTUBE_CLIENT_ID,
    YOUTUBE_CLIENT_SECRET,
    YOUTUBE_CHANNEL_ID,
    CORAL_SERVER_PORT,
    CORAL_SERVER_HOST
)

from .agent_config import (
    COORDINATOR_AGENT_CONFIG,
    YOUTUBE_AGENT_CONFIG,
    DATABASE_AGENT_CONFIG,
    AI_AGENT_CONFIG
)

from .coral_config import (
    CORAL_SERVER_CONFIG,
    AGENT_REGISTRY_CONFIG
)

__all__ = [
    # Environment variables
    "SUPABASE_URL",
    "SUPABASE_KEY", 
    "OPENAI_API_KEY",
    "YOUTUBE_CLIENT_ID",
    "YOUTUBE_CLIENT_SECRET",
    "YOUTUBE_CHANNEL_ID",
    "CORAL_SERVER_PORT",
    "CORAL_SERVER_HOST",
    
    # Agent configurations
    "COORDINATOR_AGENT_CONFIG",
    "YOUTUBE_AGENT_CONFIG",
    "DATABASE_AGENT_CONFIG",
    "AI_AGENT_CONFIG",
    
    # Coral configurations
    "CORAL_SERVER_CONFIG",
    "AGENT_REGISTRY_CONFIG"
]
