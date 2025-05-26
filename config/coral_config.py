"""
Coral Protocol configuration for Agent Angus LangChain implementation.

This module defines configuration for Coral Protocol server and agent registry.
"""
from typing import Dict, Any, List
from .environment import CORAL_SERVER_HOST, CORAL_SERVER_PORT, CORAL_SERVER_URL

# Coral Server Configuration
CORAL_SERVER_CONFIG = {
    "host": CORAL_SERVER_HOST,
    "port": CORAL_SERVER_PORT,
    "url": CORAL_SERVER_URL,
    "max_connections": 100,
    "connection_timeout": 30,
    "heartbeat_interval": 30,
    "message_queue_size": 1000,
    "worker_threads": 4,
    "enable_ssl": False,
    "ssl_cert_path": None,
    "ssl_key_path": None,
    "cors_enabled": True,
    "cors_origins": ["*"],
    "logging": {
        "level": "INFO",
        "file": "coral_server.log",
        "max_size_mb": 100,
        "backup_count": 5
    },
    "metrics": {
        "enabled": True,
        "endpoint": "/metrics",
        "collection_interval": 60
    }
}

# Agent Registry Configuration
AGENT_REGISTRY_CONFIG = {
    "registration_timeout": 30,  # seconds
    "heartbeat_timeout": 90,  # seconds
    "max_missed_heartbeats": 3,
    "cleanup_interval": 60,  # seconds
    "agent_ttl": 300,  # 5 minutes
    "discovery_broadcast_interval": 30,  # seconds
    "health_check_interval": 60,  # seconds
    "registration_retry_attempts": 3,
    "registration_retry_delay": 5,  # seconds
    "agent_metadata_schema": {
        "required_fields": ["name", "type", "version", "capabilities"],
        "optional_fields": ["description", "tags", "endpoints"]
    }
}

# Message Routing Configuration
MESSAGE_ROUTING_CONFIG = {
    "default_timeout": 30,  # seconds
    "max_retries": 3,
    "retry_delay": 2,  # seconds
    "message_ttl": 300,  # 5 minutes
    "max_message_size": 1048576,  # 1MB
    "compression_enabled": True,
    "encryption_enabled": False,
    "priority_queue_enabled": True,
    "dead_letter_queue_enabled": True,
    "routing_strategies": {
        "round_robin": True,
        "load_balanced": True,
        "priority_based": True,
        "capability_based": True
    }
}

# Load Balancing Configuration
LOAD_BALANCING_CONFIG = {
    "strategy": "round_robin",  # round_robin, least_connections, weighted
    "health_check_enabled": True,
    "health_check_interval": 30,  # seconds
    "unhealthy_threshold": 3,  # failed health checks
    "recovery_threshold": 2,  # successful health checks
    "circuit_breaker_enabled": True,
    "circuit_breaker_threshold": 5,  # failures
    "circuit_breaker_timeout": 60,  # seconds
    "weights": {
        "coordinator": 1.0,
        "youtube": 1.0,
        "database": 1.5,  # Higher weight for database operations
        "ai": 0.8  # Lower weight due to longer processing times
    }
}

# Security Configuration
SECURITY_CONFIG = {
    "authentication_enabled": False,  # Set to True in production
    "authorization_enabled": False,   # Set to True in production
    "api_key_required": False,
    "rate_limiting_enabled": True,
    "rate_limits": {
        "requests_per_minute": 1000,
        "requests_per_hour": 10000,
        "burst_size": 100
    },
    "allowed_origins": ["*"],  # Restrict in production
    "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
    "max_request_size": 10485760,  # 10MB
    "session_timeout": 3600,  # 1 hour
    "token_expiry": 86400  # 24 hours
}

# Monitoring and Observability Configuration
MONITORING_CONFIG = {
    "metrics_enabled": True,
    "tracing_enabled": True,
    "logging_enabled": True,
    "prometheus_endpoint": "/metrics",
    "health_endpoint": "/health",
    "status_endpoint": "/status",
    "metrics_collection_interval": 30,  # seconds
    "log_level": "INFO",
    "log_format": "json",
    "trace_sampling_rate": 0.1,  # 10% of requests
    "custom_metrics": [
        "agent_registration_count",
        "message_routing_latency",
        "workflow_execution_time",
        "error_rate_by_agent",
        "throughput_by_endpoint"
    ]
}

# Workflow Orchestration Configuration
WORKFLOW_CONFIG = {
    "max_concurrent_workflows": 50,
    "workflow_timeout": 1800,  # 30 minutes
    "step_timeout": 300,  # 5 minutes
    "retry_policy": {
        "max_attempts": 3,
        "backoff_strategy": "exponential",
        "initial_delay": 1,  # seconds
        "max_delay": 60,  # seconds
        "multiplier": 2
    },
    "persistence_enabled": True,
    "persistence_backend": "memory",  # memory, redis, database
    "checkpoint_interval": 60,  # seconds
    "cleanup_completed_workflows": True,
    "completed_workflow_ttl": 3600  # 1 hour
}

# Agent Communication Protocols
COMMUNICATION_PROTOCOLS = {
    "default_protocol": "http",
    "supported_protocols": ["http", "websocket", "grpc"],
    "message_formats": ["json", "protobuf", "msgpack"],
    "compression_algorithms": ["gzip", "lz4", "snappy"],
    "serialization_format": "json",
    "keep_alive_enabled": True,
    "keep_alive_interval": 30,  # seconds
    "connection_pooling": {
        "enabled": True,
        "max_pool_size": 20,
        "min_pool_size": 5,
        "pool_timeout": 30
    }
}

# Error Handling and Recovery Configuration
ERROR_HANDLING_CONFIG = {
    "global_error_handler_enabled": True,
    "error_notification_enabled": True,
    "error_recovery_enabled": True,
    "max_error_retries": 3,
    "error_retry_delay": 5,  # seconds
    "circuit_breaker_enabled": True,
    "fallback_strategies": {
        "agent_unavailable": "queue_message",
        "timeout": "retry_with_backoff",
        "rate_limit_exceeded": "delay_and_retry",
        "service_error": "fallback_agent"
    },
    "error_categories": {
        "transient": ["timeout", "connection_error", "rate_limit"],
        "permanent": ["authentication_error", "authorization_error", "not_found"],
        "recoverable": ["service_unavailable", "temporary_failure"]
    }
}

# Development and Testing Configuration
DEVELOPMENT_CONFIG = {
    "debug_mode": False,
    "mock_agents_enabled": False,
    "test_mode": False,
    "simulation_mode": False,
    "performance_testing": {
        "enabled": False,
        "load_test_agents": 10,
        "message_rate": 100,  # messages per second
        "test_duration": 300  # 5 minutes
    },
    "debugging": {
        "message_tracing": False,
        "agent_state_logging": False,
        "performance_profiling": False,
        "memory_monitoring": False
    }
}

def get_coral_server_config() -> Dict[str, Any]:
    """Get the complete Coral server configuration."""
    return {
        "server": CORAL_SERVER_CONFIG,
        "registry": AGENT_REGISTRY_CONFIG,
        "routing": MESSAGE_ROUTING_CONFIG,
        "load_balancing": LOAD_BALANCING_CONFIG,
        "security": SECURITY_CONFIG,
        "monitoring": MONITORING_CONFIG,
        "workflow": WORKFLOW_CONFIG,
        "communication": COMMUNICATION_PROTOCOLS,
        "error_handling": ERROR_HANDLING_CONFIG,
        "development": DEVELOPMENT_CONFIG
    }

def get_agent_registration_config(agent_name: str, agent_type: str) -> Dict[str, Any]:
    """
    Get agent registration configuration.
    
    Args:
        agent_name: Name of the agent
        agent_type: Type of the agent
        
    Returns:
        Registration configuration dictionary
    """
    return {
        "name": agent_name,
        "type": agent_type,
        "version": "1.0.0",
        "capabilities": get_agent_capabilities(agent_type),
        "endpoints": get_agent_endpoints(agent_type),
        "metadata": {
            "description": f"Agent Angus {agent_type} agent",
            "tags": ["angus", "music", "youtube", agent_type],
            "health_check_url": f"/agents/{agent_name}/health",
            "metrics_url": f"/agents/{agent_name}/metrics"
        },
        "registration_config": AGENT_REGISTRY_CONFIG
    }

def get_agent_capabilities(agent_type: str) -> List[str]:
    """
    Get capabilities for a specific agent type.
    
    Args:
        agent_type: Type of the agent
        
    Returns:
        List of capabilities
    """
    capabilities_map = {
        "coordinator": [
            "workflow_orchestration",
            "task_scheduling",
            "agent_coordination",
            "health_monitoring"
        ],
        "youtube": [
            "video_upload",
            "comment_management",
            "api_integration",
            "quota_management"
        ],
        "database": [
            "data_persistence",
            "query_execution",
            "transaction_management",
            "backup_recovery"
        ],
        "ai": [
            "content_analysis",
            "text_generation",
            "sentiment_analysis",
            "music_analysis"
        ]
    }
    
    return capabilities_map.get(agent_type, [])

def get_agent_endpoints(agent_type: str) -> Dict[str, str]:
    """
    Get endpoints for a specific agent type.
    
    Args:
        agent_type: Type of the agent
        
    Returns:
        Dictionary of endpoint mappings
    """
    base_port = 8000
    port_map = {
        "coordinator": base_port,
        "youtube": base_port + 1,
        "database": base_port + 2,
        "ai": base_port + 3
    }
    
    port = port_map.get(agent_type, base_port + 10)
    
    return {
        "http": f"http://localhost:{port}",
        "health": f"http://localhost:{port}/health",
        "metrics": f"http://localhost:{port}/metrics",
        "status": f"http://localhost:{port}/status"
    }

def validate_coral_config() -> bool:
    """
    Validate the Coral Protocol configuration.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        config = get_coral_server_config()
        
        # Basic validation checks
        required_sections = ["server", "registry", "routing", "monitoring"]
        for section in required_sections:
            if section not in config:
                return False
        
        # Validate server configuration
        server_config = config["server"]
        if not all(key in server_config for key in ["host", "port", "max_connections"]):
            return False
        
        return True
    except Exception:
        return False

# Export main configurations
__all__ = [
    "CORAL_SERVER_CONFIG",
    "AGENT_REGISTRY_CONFIG",
    "MESSAGE_ROUTING_CONFIG",
    "LOAD_BALANCING_CONFIG",
    "SECURITY_CONFIG",
    "MONITORING_CONFIG",
    "WORKFLOW_CONFIG",
    "get_coral_server_config",
    "get_agent_registration_config",
    "validate_coral_config"
]
