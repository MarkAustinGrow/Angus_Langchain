"""
MCP Client integration for Agent Angus LangChain system.

This module handles Model Context Protocol (MCP) client connections
following the Coral Protocol pattern from the official repository.
"""

import asyncio
import os
import json
import logging
from typing import Dict, Any, List, Optional

try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
    from langchain.prompts import ChatPromptTemplate
    from langchain.chat_models import init_chat_model
    from langchain.agents import create_tool_calling_agent, AgentExecutor
    from langchain.tools import Tool
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)

class AngusMultiServerMCPClient:
    """
    Multi-server MCP client for Agent Angus.
    
    This class manages connections to multiple MCP servers and provides
    a unified interface for Agent Angus operations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the MCP client."""
        self.config = config or {}
        self.client = None
        self.agent = None
        self.executor = None
        self.status = "not_initialized"
        
        if not MCP_AVAILABLE:
            logger.warning("MCP adapters not available - install langchain_mcp_adapters")
            self.status = "mcp_unavailable"
        
        logger.info("Angus MCP client initialized")
    
    async def initialize(self):
        """Initialize MCP client connections."""
        if not MCP_AVAILABLE:
            raise ImportError("langchain_mcp_adapters not available")
        
        try:
            # Get MCP server configurations
            servers = self.config.get("servers", {})
            
            if not servers:
                # Default server configuration for Agent Angus
                servers = {
                    "angus_tools": {
                        "command": "python",
                        "args": ["-m", "tools.mcp_server"],
                        "env": {}
                    }
                }
            
            # Initialize MCP client
            self.client = MultiServerMCPClient()
            
            # Connect to servers
            for server_name, server_config in servers.items():
                await self.client.connect_to_server(
                    server_name=server_name,
                    **server_config
                )
                logger.info(f"Connected to MCP server: {server_name}")
            
            # Get available tools
            tools = await self.client.list_tools()
            logger.info(f"Available tools: {[tool.name for tool in tools]}")
            
            # Create agent
            await self._create_agent(tools)
            
            self.status = "initialized"
            logger.info("MCP client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP client: {str(e)}")
            self.status = "error"
            raise
    
    async def _create_agent(self, tools: List[Tool]):
        """Create the LangChain agent with MCP tools."""
        try:
            # Initialize chat model
            model = init_chat_model(
                model="gpt-4o-mini",
                model_provider="openai",
                temperature=0
            )
            
            # Create prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", self._get_system_prompt()),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ])
            
            # Create agent
            self.agent = create_tool_calling_agent(model, tools, prompt)
            
            # Create executor
            self.executor = AgentExecutor(
                agent=self.agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True
            )
            
            logger.info("Agent created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create agent: {str(e)}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for Agent Angus."""
        return """You are Agent Angus, an AI assistant specialized in music publishing automation.

You have access to tools for:
1. YouTube operations (upload videos, manage comments, check quotas)
2. Database operations (manage songs, store feedback, track status)
3. AI analysis (analyze music content, generate responses, sentiment analysis)

Your primary responsibilities:
- Upload pending songs from the database to YouTube
- Process YouTube comments and generate appropriate responses
- Analyze music content for metadata and insights
- Maintain data consistency between systems

Follow these steps when helping users:
1. Understand the user's request clearly
2. Use the appropriate tools to gather information
3. Execute the requested operations
4. Provide clear feedback on results
5. Handle errors gracefully and suggest alternatives

Always be helpful, accurate, and focused on music publishing workflows."""
    
    async def execute_task(self, task: str) -> str:
        """Execute a task using the agent."""
        if not self.executor:
            raise RuntimeError("Agent not initialized - call initialize() first")
        
        try:
            result = await self.executor.ainvoke({"input": task})
            return result.get("output", "No output generated")
            
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            return f"Error executing task: {str(e)}"
    
    async def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        if not self.client:
            return []
        
        try:
            tools = await self.client.list_tools()
            return [tool.name for tool in tools]
        except Exception as e:
            logger.error(f"Failed to get tools: {str(e)}")
            return []
    
    async def close(self):
        """Close MCP client connections."""
        if self.client:
            try:
                await self.client.close()
                logger.info("MCP client connections closed")
            except Exception as e:
                logger.error(f"Error closing MCP client: {str(e)}")
        
        self.status = "closed"
    
    def get_status(self) -> Dict[str, Any]:
        """Get client status."""
        return {
            "status": self.status,
            "mcp_available": MCP_AVAILABLE,
            "client_initialized": self.client is not None,
            "agent_ready": self.executor is not None,
            "phase": "Phase 2 - MCP Integration"
        }

# Factory function
async def create_angus_mcp_client(config: Optional[Dict[str, Any]] = None) -> AngusMultiServerMCPClient:
    """Create and initialize Angus MCP client."""
    client = AngusMultiServerMCPClient(config)
    await client.initialize()
    return client
