"""
Angus Database Agent - Specialized agent for Supabase database operations using Coral Protocol.

This agent handles all database operations for the Agent Angus system including
song management, feedback storage, and status updates.
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

# Import our Supabase tools
from tools.supabase_tools import (
    get_pending_songs, get_song_details, update_song_status,
    get_uploaded_videos, store_feedback, get_existing_feedback,
    log_agent_activity
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
base_url = "http://localhost:5555/devmode/exampleApplication/privkey/session1/sse"
params = {
    "waitForAgents": 2,
    "agentId": "angus_database",
    "agentDescription": "Database specialist for Agent Angus system, handling all Supabase operations including song management, feedback storage, and status tracking."
}
query_string = "&".join([f"{k}={v}" for k, v in params.items()])
MCP_SERVER_URL = f"{base_url}?{query_string}"

AGENT_NAME = "angus_database"

def get_tools_description(tools):
    return "\n".join(
        f"Tool: {tool.name}, Schema: {json.dumps(tool.args).replace('{', '{{').replace('}', '}}')}"
        for tool in tools
    )

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
                
                # Get tools from Coral Protocol
                coral_tools = client.get_tools()
                
                # Add our Supabase tools
                database_tools = [
                    Tool(
                        name="get_pending_songs",
                        func=get_pending_songs,
                        description="Get songs that are ready for YouTube upload from the database.",
                        coroutine=get_pending_songs
                    ),
                    Tool(
                        name="get_song_details",
                        func=get_song_details,
                        description="Retrieve detailed information about a specific song from the database.",
                        coroutine=get_song_details
                    ),
                    Tool(
                        name="update_song_status",
                        func=update_song_status,
                        description="Update the upload status of a song in the database.",
                        coroutine=update_song_status
                    ),
                    Tool(
                        name="get_uploaded_videos",
                        func=get_uploaded_videos,
                        description="Get videos that have been uploaded to YouTube from the database.",
                        coroutine=get_uploaded_videos
                    ),
                    Tool(
                        name="store_feedback",
                        func=store_feedback,
                        description="Store YouTube comment feedback in the database.",
                        coroutine=store_feedback
                    ),
                    Tool(
                        name="get_existing_feedback",
                        func=get_existing_feedback,
                        description="Get existing feedback for a song to avoid duplicate processing.",
                        coroutine=get_existing_feedback
                    ),
                    Tool(
                        name="log_agent_activity",
                        func=log_agent_activity,
                        description="Log agent activities and system events to the database.",
                        coroutine=log_agent_activity
                    )
                ]
                
                # Combine all tools
                all_tools = coral_tools + database_tools
                
                logger.info(f"Database Agent tools available: {[tool.name for tool in database_tools]}")
                
                # Create the database agent
                model = ChatOpenAI(
                    model="gpt-4o",
                    model_provider="openai",
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        f"""You are the Angus Database Agent, specialized in handling all Supabase database operations for the Agent Angus music automation system.

Your responsibilities:
1. Manage song data and metadata in the Supabase database
2. Track upload statuses and video information
3. Store and retrieve YouTube comment feedback
4. Log all agent activities and system events
5. Provide data consistency and integrity
6. Handle database queries efficiently

Database operations you handle:
- Song Management: Get pending songs, song details, update statuses
- Video Tracking: Manage uploaded video records and metadata
- Feedback Storage: Store and retrieve YouTube comment data
- Activity Logging: Track all system activities and events
- Data Integrity: Ensure consistent data across all operations

Available tools: {get_tools_description(all_tools)}

Always ensure data consistency and provide detailed responses about database operations.
Handle errors gracefully and log all significant database activities."""
                    ),
                    ("placeholder", "{agent_scratchpad}")
                ])
                
                agent = create_tool_calling_agent(model, all_tools, prompt)
                agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)
                
                # Main database agent loop
                print(f"\n🗄️ Angus Database Agent started!")
                print("Available commands:")
                print("- 'pending <limit>' - Get pending songs for upload")
                print("- 'details <song_id>' - Get detailed song information")
                print("- 'videos <limit>' - Get uploaded videos")
                print("- 'status <song_id> <status>' - Update song status")
                print("- 'feedback <song_id>' - Get existing feedback for a song")
                print("- 'log <level> <message>' - Log an activity")
                print("- 'stats' - Show database statistics")
                print("- 'quit' - Exit")
                
                while True:
                    try:
                        user_input = input("\nDatabase> ").strip()
                        
                        if user_input.lower() == 'quit':
                            break
                        elif user_input.lower() == 'stats':
                            result = await agent_executor.ainvoke({
                                "input": "Get database statistics: count of pending songs, uploaded videos, and recent feedback entries."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('pending'):
                            parts = user_input.split()
                            limit = int(parts[1]) if len(parts) > 1 else 10
                            result = await agent_executor.ainvoke({
                                "input": f"Get {limit} pending songs that are ready for YouTube upload."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('details'):
                            parts = user_input.split()
                            if len(parts) > 1:
                                song_id = parts[1]
                                result = await agent_executor.ainvoke({
                                    "input": f"Get detailed information for song ID: {song_id}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a song ID")
                        elif user_input.startswith('videos'):
                            parts = user_input.split()
                            limit = int(parts[1]) if len(parts) > 1 else 10
                            result = await agent_executor.ainvoke({
                                "input": f"Get {limit} uploaded videos from the database."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('status'):
                            parts = user_input.split()
                            if len(parts) > 2:
                                song_id = parts[1]
                                status = parts[2]
                                result = await agent_executor.ainvoke({
                                    "input": f"Update status for song {song_id} to {status}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide song ID and status")
                        elif user_input.startswith('feedback'):
                            parts = user_input.split()
                            if len(parts) > 1:
                                song_id = parts[1]
                                result = await agent_executor.ainvoke({
                                    "input": f"Get existing feedback for song ID: {song_id}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a song ID")
                        elif user_input.startswith('log'):
                            parts = user_input.split(maxsplit=2)
                            if len(parts) > 2:
                                level = parts[1]
                                message = parts[2]
                                result = await agent_executor.ainvoke({
                                    "input": f"Log activity with level {level}: {message}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide log level and message")
                        else:
                            # General database query
                            result = await agent_executor.ainvoke({"input": user_input})
                            print(f"Result: {result['output']}")
                            
                    except KeyboardInterrupt:
                        print("\nShutting down database agent...")
                        break
                    except Exception as e:
                        logger.error(f"Error in database agent loop: {e}")
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
