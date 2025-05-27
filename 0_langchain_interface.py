"""
Coraliser Interface for Agent Angus

This module provides the interface configuration for Agent Angus
to be properly recognized and integrated by the Coraliser system.

Based on the LangChain WorldNews example interface pattern.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Agent configuration for Coraliser
AGENT_CONFIG = {
    "name": "angus_music_agent",
    "description": "Agent Angus - Music Publishing Automation Specialist",
    "version": "1.0.0",
    "type": "langchain_mcp",
    "capabilities": [
        "YouTube automation",
        "Music analysis and metadata generation", 
        "Database management for music content",
        "AI-powered content creation",
        "Comment processing and sentiment analysis",
        "Song upload workflows",
        "Quota management"
    ],
    "tools": [
        {
            "name": "AngusYouTubeUploadTool",
            "description": "Upload pending songs from database to YouTube with AI-generated metadata",
            "parameters": {
                "song_limit": {"type": "integer", "default": 5, "description": "Maximum number of songs to upload"},
                "auto_generate_metadata": {"type": "boolean", "default": True, "description": "Whether to auto-generate titles/descriptions"}
            }
        },
        {
            "name": "AngusCommentProcessingTool", 
            "description": "Process YouTube comments for uploaded videos with AI-powered responses",
            "parameters": {
                "comment_limit": {"type": "integer", "default": 10, "description": "Maximum number of comments to process"},
                "auto_reply": {"type": "boolean", "default": True, "description": "Whether to automatically reply to comments"}
            }
        },
        {
            "name": "AngusQuotaCheckTool",
            "description": "Check YouTube API quota usage and limits",
            "parameters": {}
        }
    ],
    "coral_integration": {
        "agent_id": "angus_music_agent",
        "server_url": "http://localhost:5555/devmode/exampleApplication/privkey/session1/sse",
        "wait_for_agents": 2,
        "collaboration_features": [
            "Inter-agent communication",
            "Shared tool access",
            "Distributed workflow coordination",
            "Music service provision to other agents"
        ]
    },
    "environment_requirements": [
        "OPENAI_API_KEY",
        "SUPABASE_URL", 
        "SUPABASE_KEY",
        "YOUTUBE_CLIENT_ID",
        "YOUTUBE_CLIENT_SECRET", 
        "YOUTUBE_API_KEY",
        "YOUTUBE_CHANNEL_ID"
    ],
    "dependencies": [
        "langchain>=0.1.0",
        "langchain-mcp-adapters>=0.1.0",
        "langchain-openai>=0.0.5",
        "openai>=1.0.0",
        "supabase>=2.0.0",
        "google-api-python-client>=2.88.0",
        "python-dotenv>=1.0.0"
    ]
}

def get_agent_info():
    """Return agent configuration information."""
    return AGENT_CONFIG

def validate_environment():
    """Validate that required environment variables are set."""
    missing_vars = []
    
    for var in AGENT_CONFIG["environment_requirements"]:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        return {
            "valid": False,
            "missing_variables": missing_vars,
            "message": f"Missing required environment variables: {', '.join(missing_vars)}"
        }
    
    return {
        "valid": True,
        "message": "All required environment variables are set"
    }

def get_startup_command():
    """Return the command to start Agent Angus."""
    return "python 1_langchain_angus_agent.py"

def get_health_check():
    """Return health check information."""
    env_status = validate_environment()
    
    return {
        "agent": AGENT_CONFIG["name"],
        "status": "ready" if env_status["valid"] else "configuration_error",
        "environment": env_status,
        "capabilities_count": len(AGENT_CONFIG["capabilities"]),
        "tools_count": len(AGENT_CONFIG["tools"]),
        "coral_integration": AGENT_CONFIG["coral_integration"]["agent_id"]
    }

if __name__ == "__main__":
    # Display agent information when run directly
    import json
    
    print("🎵 Agent Angus - Coraliser Interface")
    print("=" * 50)
    print(json.dumps(get_agent_info(), indent=2))
    print("\n🔍 Health Check:")
    print(json.dumps(get_health_check(), indent=2))
    print(f"\n🚀 Startup Command: {get_startup_command()}")
