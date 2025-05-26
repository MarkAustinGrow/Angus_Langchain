"""
Angus YouTube Agent - Specialized agent for YouTube API operations using Coral Protocol.

This agent handles all YouTube operations for the Agent Angus system including
video uploads, comment fetching, and comment replies.
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

# Import our YouTube tools
from tools.youtube_tools import (
    upload_song_to_youtube, fetch_youtube_comments, reply_to_youtube_comment,
    check_upload_quota, get_video_details, process_video_comments
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
    "agentId": "angus_youtube",
    "agentDescription": "YouTube specialist for Agent Angus system, handling video uploads, comment fetching, and automated replies using YouTube API."
}
query_string = "&".join([f"{k}={v}" for k, v in params.items()])
MCP_SERVER_URL = f"{base_url}?{query_string}"

AGENT_NAME = "angus_youtube"

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
                
                # Add our YouTube tools
                youtube_tools = [
                    Tool(
                        name="upload_song_to_youtube",
                        func=upload_song_to_youtube,
                        description="Upload a song video to YouTube with metadata and tags.",
                        coroutine=upload_song_to_youtube
                    ),
                    Tool(
                        name="fetch_youtube_comments",
                        func=fetch_youtube_comments,
                        description="Fetch comments from a YouTube video for processing.",
                        coroutine=fetch_youtube_comments
                    ),
                    Tool(
                        name="reply_to_youtube_comment",
                        func=reply_to_youtube_comment,
                        description="Reply to a specific YouTube comment with generated text.",
                        coroutine=reply_to_youtube_comment
                    ),
                    Tool(
                        name="check_upload_quota",
                        func=check_upload_quota,
                        description="Check YouTube API upload quota status and limits.",
                        coroutine=check_upload_quota
                    ),
                    Tool(
                        name="get_video_details",
                        func=get_video_details,
                        description="Get details and metadata for a YouTube video.",
                        coroutine=get_video_details
                    ),
                    Tool(
                        name="process_video_comments",
                        func=process_video_comments,
                        description="Process all comments for a video: fetch, analyze, and reply.",
                        coroutine=process_video_comments
                    )
                ]
                
                # Combine all tools
                all_tools = coral_tools + youtube_tools
                
                logger.info(f"YouTube Agent tools available: {[tool.name for tool in youtube_tools]}")
                
                # Create the YouTube agent
                model = ChatOpenAI(
                    model="gpt-4o",
                    model_provider="openai",
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        f"""You are the Angus YouTube Agent, specialized in handling all YouTube API operations for the Agent Angus music automation system.

Your responsibilities:
1. Upload song videos to YouTube with proper metadata and tags
2. Fetch comments from uploaded videos for processing
3. Reply to YouTube comments with AI-generated responses
4. Monitor YouTube API quota and usage limits
5. Manage video details and metadata
6. Process video comments efficiently and accurately

YouTube operations you handle:
- Video Uploads: Upload songs with titles, descriptions, and tags
- Comment Management: Fetch, process, and reply to comments
- Quota Management: Monitor and respect API rate limits
- Video Analytics: Track video performance and engagement
- Content Moderation: Handle appropriate responses to comments

Available tools: {get_tools_description(all_tools)}

Always respect YouTube API rate limits and community guidelines.
Provide helpful and appropriate responses to comments.
Handle upload errors gracefully and report status accurately."""
                    ),
                    ("placeholder", "{agent_scratchpad}")
                ])
                
                agent = create_tool_calling_agent(model, all_tools, prompt)
                agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)
                
                # Main YouTube agent loop
                print(f"\n🎬 Angus YouTube Agent started!")
                print("Available commands:")
                print("- 'upload <song_id>' - Upload a song to YouTube")
                print("- 'comments <video_id>' - Fetch comments from a video")
                print("- 'reply <comment_id> <text>' - Reply to a specific comment")
                print("- 'process <video_id>' - Process all comments for a video")
                print("- 'quota' - Check YouTube API quota status")
                print("- 'details <video_id>' - Get video details")
                print("- 'status' - Show YouTube agent status")
                print("- 'quit' - Exit")
                
                while True:
                    try:
                        user_input = input("\nYouTube> ").strip()
                        
                        if user_input.lower() == 'quit':
                            break
                        elif user_input.lower() == 'status':
                            print("🟢 YouTube Agent: Active")
                            print(f"🔗 Connected to Coral Server: {MCP_SERVER_URL}")
                            print(f"🛠️  YouTube tools available: {len(youtube_tools)}")
                        elif user_input.lower() == 'quota':
                            result = await agent_executor.ainvoke({
                                "input": "Check the current YouTube API quota status and usage limits."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('upload'):
                            parts = user_input.split()
                            if len(parts) > 1:
                                song_id = parts[1]
                                result = await agent_executor.ainvoke({
                                    "input": f"Upload song with ID {song_id} to YouTube. Use appropriate title, description, and tags."
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a song ID")
                        elif user_input.startswith('comments'):
                            parts = user_input.split()
                            if len(parts) > 1:
                                video_id = parts[1]
                                result = await agent_executor.ainvoke({
                                    "input": f"Fetch comments from YouTube video {video_id}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a video ID")
                        elif user_input.startswith('reply'):
                            parts = user_input.split(maxsplit=2)
                            if len(parts) > 2:
                                comment_id = parts[1]
                                reply_text = parts[2]
                                result = await agent_executor.ainvoke({
                                    "input": f"Reply to comment {comment_id} with text: {reply_text}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide comment ID and reply text")
                        elif user_input.startswith('process'):
                            parts = user_input.split()
                            if len(parts) > 1:
                                video_id = parts[1]
                                result = await agent_executor.ainvoke({
                                    "input": f"Process all comments for video {video_id}: fetch comments, generate appropriate replies, and post responses."
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a video ID")
                        elif user_input.startswith('details'):
                            parts = user_input.split()
                            if len(parts) > 1:
                                video_id = parts[1]
                                result = await agent_executor.ainvoke({
                                    "input": f"Get detailed information for YouTube video {video_id}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a video ID")
                        else:
                            # General YouTube query
                            result = await agent_executor.ainvoke({"input": user_input})
                            print(f"Result: {result['output']}")
                            
                    except KeyboardInterrupt:
                        print("\nShutting down YouTube agent...")
                        break
                    except Exception as e:
                        logger.error(f"Error in YouTube agent loop: {e}")
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
