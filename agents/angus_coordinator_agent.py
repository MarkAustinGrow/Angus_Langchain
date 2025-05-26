"""
Angus Coordinator Agent - Main orchestrator for Agent Angus using Coral Protocol.

This agent coordinates the song upload and comment processing workflows by
communicating with specialized agents via the Coral Protocol server.
"""
import asyncio
import os
import json
import logging
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
base_url = "http://localhost:5555/devmode/exampleApplication/privkey/session1/sse"
params = {
    "waitForAgents": 2,
    "agentId": "angus_coordinator",
    "agentDescription": "Main coordinator for Agent Angus music automation system, responsible for orchestrating song uploads and comment processing workflows."
}
query_string = "&".join([f"{k}={v}" for k, v in params.items()])
MCP_SERVER_URL = f"{base_url}?{query_string}"

AGENT_NAME = "angus_coordinator"

def get_tools_description(tools):
    return "\n".join(
        f"Tool: {tool.name}, Schema: {json.dumps(tool.args).replace('{', '{{').replace('}', '}}')}"
        for tool in tools
    )

async def coordinate_song_upload(song_limit: int = 5) -> str:
    """
    Coordinate the song upload workflow across specialized agents.
    
    Args:
        song_limit: Maximum number of songs to upload
        
    Returns:
        Status message about the upload workflow
    """
    print(f"Coordinator: Starting song upload workflow (limit: {song_limit})")
    
    # This will be implemented to coordinate with:
    # 1. Database Agent - get pending songs
    # 2. AI Agent - analyze and generate metadata
    # 3. YouTube Agent - upload videos
    # 4. Database Agent - update status
    
    return f"Song upload workflow initiated for {song_limit} songs"

async def coordinate_comment_processing(reply_limit: int = 10) -> str:
    """
    Coordinate the comment processing workflow across specialized agents.
    
    Args:
        reply_limit: Maximum number of replies to post
        
    Returns:
        Status message about the comment processing workflow
    """
    print(f"Coordinator: Starting comment processing workflow (limit: {reply_limit})")
    
    # This will be implemented to coordinate with:
    # 1. Database Agent - get uploaded videos
    # 2. YouTube Agent - fetch comments
    # 3. AI Agent - generate responses
    # 4. YouTube Agent - post replies
    # 5. Database Agent - store feedback
    
    return f"Comment processing workflow initiated for {reply_limit} replies"

async def main():
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            async with MultiServerMCPClient(
                connections={
                    "coral": {
                        "transport": "sse",
                        "url": MCP_SERVER_URL,
                        "timeout": 300,
                        "sse_read_timeout": 300,
                    }
                }
            ) as client:
                logger.info(f"Connected to MCP server at {MCP_SERVER_URL}")
                
                # Get tools from other agents via Coral Protocol
                coral_tools = client.get_tools()
                
                # Add coordinator-specific tools
                coordinator_tools = [
                    Tool(
                        name="coordinate_song_upload",
                        func=coordinate_song_upload,
                        description="Coordinate the song upload workflow across specialized agents.",
                        coroutine=coordinate_song_upload
                    ),
                    Tool(
                        name="coordinate_comment_processing", 
                        func=coordinate_comment_processing,
                        description="Coordinate the comment processing workflow across specialized agents.",
                        coroutine=coordinate_comment_processing
                    )
                ]
                
                # Combine all tools
                all_tools = coral_tools + coordinator_tools
                
                logger.info(f"Tools available: {[tool.name for tool in all_tools]}")
                
                # Create the coordinator agent
                model = ChatOpenAI(
                    model="gpt-4o",
                    model_provider="openai",
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        f"""You are the Angus Coordinator Agent, the main orchestrator for the Agent Angus music automation system.

Your responsibilities:
1. Coordinate song upload workflows by working with Database, AI, and YouTube agents
2. Coordinate comment processing workflows across all specialized agents  
3. Schedule and manage both workflows efficiently
4. Handle errors and ensure robust operation
5. Monitor system health and performance

Available specialized agents:
- Database Agent: Handles all Supabase database operations
- YouTube Agent: Manages YouTube API operations (upload, comments, replies)
- AI Agent: Provides OpenAI-powered analysis and response generation

Workflow coordination patterns:
- Song Upload: Database → AI → YouTube → Database
- Comment Processing: Database → YouTube → AI → YouTube → Database

Use the available tools to coordinate these workflows effectively.

Available tools: {get_tools_description(all_tools)}

Always coordinate workflows step by step, ensuring each agent completes its task before proceeding to the next step."""
                    ),
                    ("placeholder", "{agent_scratchpad}")
                ])
                
                agent = create_tool_calling_agent(model, all_tools, prompt)
                agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)
                
                # Main coordination loop
                print(f"\n🎵 Angus Coordinator Agent started!")
                print("Available commands:")
                print("- 'upload <limit>' - Start song upload workflow")
                print("- 'comments <limit>' - Start comment processing workflow") 
                print("- 'both <upload_limit> <comment_limit>' - Run both workflows")
                print("- 'status' - Check system status")
                print("- 'quit' - Exit")
                
                while True:
                    try:
                        user_input = input("\nCoordinator> ").strip()
                        
                        if user_input.lower() == 'quit':
                            break
                        elif user_input.lower() == 'status':
                            print("🟢 Coordinator Agent: Active")
                            print(f"🔗 Connected to Coral Server: {MCP_SERVER_URL}")
                            print(f"🛠️  Available tools: {len(all_tools)}")
                        elif user_input.startswith('upload'):
                            parts = user_input.split()
                            limit = int(parts[1]) if len(parts) > 1 else 5
                            result = await agent_executor.ainvoke({
                                "input": f"Start the song upload workflow for {limit} songs. Coordinate with the Database Agent to get pending songs, AI Agent for analysis, YouTube Agent for uploads, and Database Agent for status updates."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('comments'):
                            parts = user_input.split()
                            limit = int(parts[1]) if len(parts) > 1 else 10
                            result = await agent_executor.ainvoke({
                                "input": f"Start the comment processing workflow for {limit} replies. Coordinate with Database Agent for videos, YouTube Agent for comments, AI Agent for responses, and YouTube Agent for replies."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('both'):
                            parts = user_input.split()
                            upload_limit = int(parts[1]) if len(parts) > 1 else 5
                            comment_limit = int(parts[2]) if len(parts) > 2 else 10
                            result = await agent_executor.ainvoke({
                                "input": f"Run both workflows: upload {upload_limit} songs and process {comment_limit} comments. Execute them efficiently and coordinate all agents."
                            })
                            print(f"Result: {result['output']}")
                        else:
                            # General query to the coordinator
                            result = await agent_executor.ainvoke({"input": user_input})
                            print(f"Result: {result['output']}")
                            
                    except KeyboardInterrupt:
                        print("\nShutting down coordinator...")
                        break
                    except Exception as e:
                        logger.error(f"Error in coordinator loop: {e}")
                        print(f"Error: {e}")
                        
        except Exception as e:
            logger.error(f"Connection error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info("Retrying in 5 seconds...")
                await asyncio.sleep(5)
                continue
            else:
                logger.error("Max retries reached. Exiting.")
                raise

if __name__ == "__main__":
    asyncio.run(main())
