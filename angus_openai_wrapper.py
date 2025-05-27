"""
OpenAI-Compatible HTTP API Wrapper for Agent Angus.

This module creates a FastAPI server that exposes Agent Angus's MCP functionality
through an OpenAI-compatible REST API interface for Coraliser integration.
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Import Agent Angus MCP client
try:
    from coral_integration.mcp_client import create_angus_mcp_client, AngusMultiServerMCPClient
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)

# Global MCP client instance
mcp_client: Optional[AngusMultiServerMCPClient] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    global mcp_client
    
    # Startup
    logger.info("Starting Agent Angus OpenAI-compatible wrapper...")
    
    if not MCP_AVAILABLE:
        logger.error("MCP client not available - check dependencies")
        yield
        return
    
    try:
        # Initialize MCP client
        mcp_client = await create_angus_mcp_client()
        logger.info("MCP client initialized successfully")
        
        # Get available tools
        tools = await mcp_client.get_available_tools()
        logger.info(f"Available tools: {tools}")
        
    except Exception as e:
        logger.error(f"Failed to initialize MCP client: {str(e)}")
        mcp_client = None
    
    yield
    
    # Shutdown
    if mcp_client:
        await mcp_client.close()
        logger.info("MCP client closed")

# Create FastAPI app
app = FastAPI(
    title="Agent Angus OpenAI-Compatible API",
    description="OpenAI-compatible wrapper for Agent Angus music automation tools",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for OpenAI-compatible API
class Message(BaseModel):
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")
    name: Optional[str] = Field(None, description="Name of the sender")

class ChatCompletionRequest(BaseModel):
    model: str = Field(default="angus-v1", description="Model to use")
    messages: List[Message] = Field(..., description="List of messages")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=1000, gt=0)
    stream: Optional[bool] = Field(default=False)
    stop: Optional[List[str]] = Field(default=None)

class ChatCompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage

class ErrorResponse(BaseModel):
    error: Dict[str, Any]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global mcp_client
    
    status = {
        "status": "healthy" if mcp_client else "unhealthy",
        "mcp_available": MCP_AVAILABLE,
        "mcp_client_ready": mcp_client is not None,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if mcp_client:
        mcp_status = mcp_client.get_status()
        status.update(mcp_status)
    
    return status

# List models endpoint (OpenAI compatibility)
@app.get("/v1/models")
async def list_models():
    """List available models."""
    return {
        "object": "list",
        "data": [
            {
                "id": "angus-v1",
                "object": "model",
                "created": int(datetime.utcnow().timestamp()),
                "owned_by": "agent-angus",
                "permission": [],
                "root": "angus-v1",
                "parent": None
            }
        ]
    }

# Main chat completions endpoint
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """
    Create a chat completion using Agent Angus.
    
    This endpoint accepts OpenAI-style chat completion requests and routes them
    to Agent Angus's MCP client for processing.
    """
    global mcp_client
    
    if not mcp_client:
        raise HTTPException(
            status_code=503,
            detail={
                "error": {
                    "message": "Agent Angus MCP client not available",
                    "type": "service_unavailable",
                    "code": "mcp_client_unavailable"
                }
            }
        )
    
    try:
        # Extract the user's prompt from the last message
        if not request.messages:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": {
                        "message": "No messages provided",
                        "type": "invalid_request_error",
                        "code": "missing_messages"
                    }
                }
            )
        
        # Get the last user message
        user_message = None
        for msg in reversed(request.messages):
            if msg.role == "user":
                user_message = msg.content
                break
        
        if not user_message:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": {
                        "message": "No user message found",
                        "type": "invalid_request_error",
                        "code": "no_user_message"
                    }
                }
            )
        
        # Execute the task using Agent Angus MCP client
        logger.info(f"Executing task: {user_message}")
        result = await mcp_client.execute_task(user_message)
        
        # Create response in OpenAI format
        response_id = f"chatcmpl-angus-{uuid.uuid4().hex[:8]}"
        created_timestamp = int(datetime.utcnow().timestamp())
        
        # Estimate token usage (rough approximation)
        prompt_tokens = sum(len(msg.content.split()) for msg in request.messages)
        completion_tokens = len(result.split())
        total_tokens = prompt_tokens + completion_tokens
        
        response = ChatCompletionResponse(
            id=response_id,
            created=created_timestamp,
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(
                        role="assistant",
                        content=result
                    ),
                    finish_reason="stop"
                )
            ],
            usage=ChatCompletionUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens
            )
        )
        
        logger.info(f"Task completed successfully: {response_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat completion: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "message": f"Internal server error: {str(e)}",
                    "type": "internal_server_error",
                    "code": "execution_failed"
                }
            }
        )

# Agent status endpoint
@app.get("/v1/agent/status")
async def agent_status():
    """Get Agent Angus status and capabilities."""
    global mcp_client
    
    if not mcp_client:
        return {
            "status": "unavailable",
            "mcp_available": MCP_AVAILABLE,
            "tools": []
        }
    
    try:
        tools = await mcp_client.get_available_tools()
        status = mcp_client.get_status()
        
        return {
            "status": "ready",
            "mcp_status": status,
            "available_tools": tools,
            "capabilities": [
                "YouTube automation",
                "Database operations", 
                "AI music analysis",
                "Comment processing",
                "Song upload workflows"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting agent status: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

# Tools listing endpoint
@app.get("/v1/agent/tools")
async def list_agent_tools():
    """List all available Agent Angus tools."""
    global mcp_client
    
    if not mcp_client:
        return {"tools": [], "error": "MCP client not available"}
    
    try:
        tools = await mcp_client.get_available_tools()
        return {"tools": tools}
        
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        return {"tools": [], "error": str(e)}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Agent Angus OpenAI-Compatible API",
        "version": "1.0.0",
        "description": "OpenAI-compatible wrapper for Agent Angus music automation",
        "endpoints": {
            "chat_completions": "/v1/chat/completions",
            "models": "/v1/models",
            "health": "/health",
            "status": "/v1/agent/status",
            "tools": "/v1/agent/tools"
        },
        "documentation": "/docs"
    }

def main():
    """Main entry point for running the server."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Starting Agent Angus OpenAI-compatible wrapper server...")
    
    uvicorn.run(
        "angus_openai_wrapper:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
