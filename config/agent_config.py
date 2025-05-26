"""
Agent configuration for Agent Angus LangChain implementation.

This module defines configuration for each agent in the multi-agent system.
"""
from typing import Dict, Any, List

# Coordinator Agent Configuration
COORDINATOR_AGENT_CONFIG = {
    "name": "angus_coordinator",
    "description": "Main orchestrator agent for Agent Angus operations",
    "type": "coordinator",
    "tools": [],  # Coordinator uses other agents' tools via messaging
    "max_iterations": 10,
    "timeout": 300,  # 5 minutes
    "retry_attempts": 3,
    "retry_delay": 5,
    "heartbeat_interval": 30,
    "scheduling": {
        "upload_songs_interval": 3600,  # 1 hour
        "process_comments_interval": 3600,  # 1 hour
        "cleanup_logs_interval": 86400,  # 1 day
        "health_check_interval": 300  # 5 minutes
    },
    "workflow_limits": {
        "max_songs_per_upload": 5,
        "max_replies_per_batch": 10,
        "max_videos_to_process": 10
    }
}

# YouTube Agent Configuration
YOUTUBE_AGENT_CONFIG = {
    "name": "angus_youtube",
    "description": "Specialized agent for YouTube operations",
    "type": "youtube",
    "tools": [
        "upload_song_to_youtube",
        "fetch_youtube_comments",
        "reply_to_youtube_comment",
        "check_upload_quota",
        "get_video_details"
    ],
    "max_iterations": 5,
    "timeout": 600,  # 10 minutes for uploads
    "retry_attempts": 3,
    "retry_delay": 10,
    "heartbeat_interval": 60,
    "rate_limits": {
        "uploads_per_day": 6,  # YouTube daily upload limit
        "api_calls_per_minute": 100,
        "comments_per_minute": 10
    },
    "upload_settings": {
        "default_privacy": "public",
        "default_category": "10",  # Music category
        "max_file_size_mb": 128000,  # 128GB
        "supported_formats": ["mp4", "mov", "avi", "wmv", "flv", "webm"]
    }
}

# Database Agent Configuration
DATABASE_AGENT_CONFIG = {
    "name": "angus_database",
    "description": "Specialized agent for Supabase database operations",
    "type": "database",
    "tools": [
        "get_pending_songs",
        "store_feedback",
        "update_song_status",
        "get_song_details",
        "get_uploaded_videos",
        "get_existing_feedback",
        "log_agent_activity"
    ],
    "max_iterations": 3,
    "timeout": 60,  # 1 minute
    "retry_attempts": 5,
    "retry_delay": 2,
    "heartbeat_interval": 30,
    "connection_pool": {
        "max_connections": 10,
        "min_connections": 2,
        "connection_timeout": 30
    },
    "query_limits": {
        "max_batch_size": 100,
        "max_query_timeout": 30,
        "max_retries_per_query": 3
    }
}

# AI Agent Configuration
AI_AGENT_CONFIG = {
    "name": "angus_ai",
    "description": "Specialized agent for OpenAI operations and analysis",
    "type": "ai",
    "tools": [
        "analyze_music_content",
        "generate_comment_response",
        "extract_music_metadata",
        "analyze_comment_sentiment",
        "generate_song_description",
        "suggest_video_tags"
    ],
    "max_iterations": 3,
    "timeout": 120,  # 2 minutes
    "retry_attempts": 3,
    "retry_delay": 5,
    "heartbeat_interval": 45,
    "openai_settings": {
        "default_model": "gpt-3.5-turbo",
        "analysis_model": "gpt-4o",
        "max_tokens": 1000,
        "temperature": 0.7,
        "rate_limit_rpm": 3500,  # requests per minute
        "rate_limit_tpm": 90000   # tokens per minute
    },
    "analysis_settings": {
        "max_audio_duration": 600,  # 10 minutes
        "supported_formats": ["mp3", "wav", "m4a", "flac"],
        "cache_results": True,
        "cache_duration": 3600  # 1 hour
    }
}

# Agent discovery and communication settings
AGENT_DISCOVERY_CONFIG = {
    "discovery_interval": 30,  # seconds
    "health_check_interval": 60,  # seconds
    "timeout_threshold": 180,  # seconds
    "max_missed_heartbeats": 3,
    "agent_types": ["coordinator", "youtube", "database", "ai"]
}

# Message routing configuration
MESSAGE_ROUTING_CONFIG = {
    "default_timeout": 30,  # seconds
    "max_retries": 3,
    "retry_delay": 2,  # seconds
    "message_ttl": 300,  # 5 minutes
    "priority_levels": ["low", "normal", "high", "urgent"],
    "routing_rules": {
        "upload_song": ["coordinator", "youtube", "database"],
        "process_comments": ["coordinator", "youtube", "ai", "database"],
        "analyze_music": ["coordinator", "ai"],
        "health_check": ["all"]
    }
}

# Workflow configurations
WORKFLOW_CONFIGS = {
    "upload_songs": {
        "name": "Upload Songs Workflow",
        "description": "Complete workflow for uploading songs to YouTube",
        "steps": [
            {"agent": "database", "action": "get_pending_songs"},
            {"agent": "ai", "action": "generate_song_description"},
            {"agent": "ai", "action": "suggest_video_tags"},
            {"agent": "youtube", "action": "upload_song_to_youtube"},
            {"agent": "database", "action": "update_song_status"}
        ],
        "timeout": 1800,  # 30 minutes
        "max_parallel": 3
    },
    "process_comments": {
        "name": "Process Comments Workflow", 
        "description": "Complete workflow for processing YouTube comments",
        "steps": [
            {"agent": "database", "action": "get_uploaded_videos"},
            {"agent": "youtube", "action": "fetch_youtube_comments"},
            {"agent": "ai", "action": "analyze_comment_sentiment"},
            {"agent": "ai", "action": "generate_comment_response"},
            {"agent": "youtube", "action": "reply_to_youtube_comment"},
            {"agent": "database", "action": "store_feedback"}
        ],
        "timeout": 900,  # 15 minutes
        "max_parallel": 5
    },
    "analyze_music": {
        "name": "Analyze Music Workflow",
        "description": "Workflow for analyzing music content",
        "steps": [
            {"agent": "ai", "action": "analyze_music_content"},
            {"agent": "database", "action": "update_song_status"}
        ],
        "timeout": 300,  # 5 minutes
        "max_parallel": 2
    }
}

# Performance monitoring configuration
MONITORING_CONFIG = {
    "metrics_collection_interval": 60,  # seconds
    "metrics_retention_days": 30,
    "alert_thresholds": {
        "response_time_ms": 5000,
        "error_rate_percent": 5,
        "memory_usage_percent": 80,
        "cpu_usage_percent": 80
    },
    "health_check_endpoints": {
        "coordinator": "/health",
        "youtube": "/health", 
        "database": "/health",
        "ai": "/health"
    }
}

def get_agent_config(agent_type: str) -> Dict[str, Any]:
    """
    Get configuration for a specific agent type.
    
    Args:
        agent_type: Type of agent (coordinator, youtube, database, ai)
        
    Returns:
        Configuration dictionary for the agent
    """
    configs = {
        "coordinator": COORDINATOR_AGENT_CONFIG,
        "youtube": YOUTUBE_AGENT_CONFIG,
        "database": DATABASE_AGENT_CONFIG,
        "ai": AI_AGENT_CONFIG
    }
    
    return configs.get(agent_type, {})

def get_workflow_config(workflow_name: str) -> Dict[str, Any]:
    """
    Get configuration for a specific workflow.
    
    Args:
        workflow_name: Name of the workflow
        
    Returns:
        Configuration dictionary for the workflow
    """
    return WORKFLOW_CONFIGS.get(workflow_name, {})

def validate_agent_config(config: Dict[str, Any]) -> bool:
    """
    Validate an agent configuration.
    
    Args:
        config: Agent configuration dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["name", "description", "type", "tools", "timeout"]
    
    for field in required_fields:
        if field not in config:
            return False
    
    return True

# Export all configurations
ALL_AGENT_CONFIGS = {
    "coordinator": COORDINATOR_AGENT_CONFIG,
    "youtube": YOUTUBE_AGENT_CONFIG,
    "database": DATABASE_AGENT_CONFIG,
    "ai": AI_AGENT_CONFIG
}
