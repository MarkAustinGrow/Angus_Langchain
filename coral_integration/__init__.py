"""
Coral Protocol integration for Agent Angus LangChain system.

This package contains the Model Context Protocol (MCP) integration
following the Coral Protocol pattern:
- MCP Client: Multi-server MCP client for tool access
- Server Setup: MCP server configuration and management
- Agent Registry: Agent registration and discovery
- Message Handlers: Inter-agent communication
"""

# Import actual implementations
try:
    from coral_integration.mcp_client import AngusMultiServerMCPClient, create_angus_mcp_client
    from coral_integration.server_setup import CoralServerManager, create_coral_server
    MCP_INTEGRATION_AVAILABLE = True
except ImportError:
    MCP_INTEGRATION_AVAILABLE = False

__version__ = "1.0.0"
__phase__ = "Phase 2 - MCP Integration Ready"

# MCP integration components
MCP_COMPONENTS = {
    "mcp_client": "AngusMultiServerMCPClient",
    "server_setup": "CoralServerManager", 
    "agent_registry": "AgentRegistry",
    "message_handlers": "MessageHandler"
}

def get_coral_status():
    """Get current implementation status of Coral Protocol integration."""
    return {
        "phase": __phase__,
        "mcp_available": MCP_INTEGRATION_AVAILABLE,
        "server_ready": True,
        "registry_ready": False,
        "messaging_ready": False,
        "config_ready": True
    }

def get_mcp_components():
    """Get list of MCP integration components."""
    return list(MCP_COMPONENTS.keys())

# Backward compatibility aliases
def get_coral_components():
    """Get list of Coral Protocol components (alias for get_mcp_components)."""
    return get_mcp_components()

CORAL_COMPONENTS = MCP_COMPONENTS

# Placeholder classes for components not yet implemented
class AgentRegistry:
    """Placeholder for agent registry (Phase 3)."""
    
    def __init__(self):
        self.status = "not_implemented"
    
    def register_agent(self, agent_config):
        raise NotImplementedError("Agent registry implementation pending - Phase 3")

class MessageHandler:
    """Placeholder for message handler (Phase 3)."""
    
    def __init__(self):
        self.status = "not_implemented"
    
    def route_message(self, message):
        raise NotImplementedError("Message handling implementation pending - Phase 3")

# Export main classes
if MCP_INTEGRATION_AVAILABLE:
    __all__ = [
        "AngusMultiServerMCPClient",
        "create_angus_mcp_client", 
        "CoralServerManager",
        "create_coral_server",
        "AgentRegistry",
        "MessageHandler",
        "get_coral_status",
        "get_mcp_components",
        "get_coral_components"
    ]
else:
    # Fallback exports when MCP not available
    __all__ = [
        "AgentRegistry",
        "MessageHandler", 
        "get_coral_status",
        "get_mcp_components",
        "get_coral_components"
    ]
