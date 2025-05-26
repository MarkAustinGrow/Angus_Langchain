"""
Agent Angus Coral Client - Connects to the Coral server for agent-to-agent communication.

This agent connects Agent Angus to the Coral Protocol network at 
coral.pushcollective.club:5555 to communicate with other AI agents, specifically Team Yona.
"""
import asyncio
import os
import json
import logging
import uuid
from datetime import datetime
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool

# Import our tools
from tools.youtube_tools import (
    upload_song_to_youtube, fetch_youtube_comments, reply_to_youtube_comment,
    check_upload_quota, get_video_details, process_video_comments
)
from tools.supabase_tools import (
    get_pending_songs, get_song_details, update_song_status,
    get_uploaded_videos, store_feedback, get_existing_feedback,
    log_agent_activity
)
from tools.ai_tools import (
    analyze_music_content, generate_comment_response, extract_music_metadata,
    analyze_comment_sentiment, generate_song_description, suggest_video_tags
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration for Coral server connection (following Team Angus guide)
base_url = "http://coral.pushcollective.club:5555/devmode/exampleApplication/privkey/session1/sse"
params = {
    "waitForAgents": 2,  # Wait for both agents
    "agentId": "angus_agent",
    "agentDescription": "Agent Angus - Music publishing automation agent for YouTube uploads and comment processing"
}
query_string = "&".join([f"{k}={v}" for k, v in params.items()])
CORAL_SERVER_URL = f"{base_url}?{query_string}"

AGENT_NAME = "angus_agent"
TARGET_AGENT = "yona_agent"  # Team Yona

def get_tools_description(tools):
    return "\n".join(
        f"Tool: {tool.name}, Schema: {json.dumps(tool.args).replace('{', '{{').replace('}', '}}')}"
        for tool in tools
    )

async def upload_workflow(song_limit: int = 5) -> str:
    """
    Execute the complete song upload workflow.
    
    Args:
        song_limit: Maximum number of songs to upload
        
    Returns:
        Status message about the upload workflow
    """
    try:
        logger.info(f"Starting upload workflow for {song_limit} songs")
        
        # Get pending songs
        pending_songs = await get_pending_songs(song_limit)
        if not pending_songs:
            return "No pending songs found for upload"
        
        uploaded_count = 0
        for song in pending_songs:
            try:
                # Upload to YouTube
                result = await upload_song_to_youtube(song['id'])
                if result and 'video_id' in result:
                    # Update status
                    await update_song_status(song['id'], 'uploaded', result['video_id'])
                    uploaded_count += 1
                    logger.info(f"Successfully uploaded song {song['id']}")
                else:
                    logger.error(f"Failed to upload song {song['id']}")
            except Exception as e:
                logger.error(f"Error uploading song {song['id']}: {e}")
        
        return f"Upload workflow completed: {uploaded_count}/{len(pending_songs)} songs uploaded successfully"
        
    except Exception as e:
        logger.error(f"Upload workflow failed: {e}")
        return f"Upload workflow failed: {str(e)}"

async def comment_processing_workflow(reply_limit: int = 10) -> str:
    """
    Execute the complete comment processing workflow.
    
    Args:
        reply_limit: Maximum number of replies to post
        
    Returns:
        Status message about the comment processing workflow
    """
    try:
        logger.info(f"Starting comment processing workflow for {reply_limit} replies")
        
        # Get uploaded videos
        videos = await get_uploaded_videos(reply_limit)
        if not videos:
            return "No uploaded videos found for comment processing"
        
        processed_count = 0
        for video in videos:
            try:
                # Process comments for this video
                result = await process_video_comments(video['video_id'], reply_limit)
                if result:
                    processed_count += 1
                    logger.info(f"Successfully processed comments for video {video['video_id']}")
            except Exception as e:
                logger.error(f"Error processing comments for video {video['video_id']}: {e}")
        
        return f"Comment processing completed: processed comments for {processed_count}/{len(videos)} videos"
        
    except Exception as e:
        logger.error(f"Comment processing workflow failed: {e}")
        return f"Comment processing workflow failed: {str(e)}"

async def send_function_call_to_yona(client, function_name: str, arguments: dict) -> dict:
    """
    Send a function call message to Team Yona agent.
    
    Args:
        client: The MCP client connection
        function_name: Name of the function to call
        arguments: Arguments for the function
        
    Returns:
        Response from Team Yona
    """
    try:
        message = {
            "type": "function_call",
            "function": function_name,
            "arguments": arguments,
            "metadata": {
                "sender": AGENT_NAME,
                "timestamp": datetime.now().isoformat(),
                "message_id": str(uuid.uuid4())
            }
        }
        
        logger.info(f"Sending function call to {TARGET_AGENT}: {function_name}")
        
        # Use direct tool invocation as per guide
        response = await client.connections["coral"].invoke_tool("send_message", {
            "target_agent": TARGET_AGENT,
            "message": json.dumps(message)
        })
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to send function call to {TARGET_AGENT}: {e}")
        return {"error": str(e)}

async def request_song_creation(client, prompt: str) -> str:
    """
    Request Team Yona to create a song.
    
    Args:
        client: The MCP client connection
        prompt: Song creation prompt
        
    Returns:
        Response from Team Yona
    """
    try:
        response = await send_function_call_to_yona(client, "create_song", {
            "prompt": prompt,
            "style": "AI-generated music",
            "duration": "3-4 minutes"
        })
        
        if "error" in response:
            return f"Error requesting song creation: {response['error']}"
        
        return f"Song creation request sent to Team Yona: {prompt}"
        
    except Exception as e:
        logger.error(f"Failed to request song creation: {e}")
        return f"Failed to request song creation: {str(e)}"

async def main():
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Connect to Coral server using the correct configuration
            async with MultiServerMCPClient(
                connections={
                    "coral": {
                        "transport": "sse",
                        "url": CORAL_SERVER_URL,
                        "timeout": 300,
                        "sse_read_timeout": 300,
                    }
                }
            ) as client:
                logger.info(f"Connected to Coral server at {CORAL_SERVER_URL}")
                
                # Wait a moment for registration
                await asyncio.sleep(2)
                
                # List agents to verify connection
                try:
                    agents = await client.connections["coral"].invoke_tool("list_agents", {})
                    logger.info(f"Available agents: {agents}")
                except Exception as e:
                    logger.warning(f"Could not list agents: {e}")
                
                # Get tools from Coral Protocol
                coral_tools = client.get_tools()
                logger.info(f"Available tools from Coral network: {[tool.name for tool in coral_tools]}")
                
                # Add Agent Angus's specialized tools
                angus_tools = [
                    # YouTube Tools
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
                    ),
                    
                    # Database Tools
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
                    ),
                    
                    # AI Tools
                    Tool(
                        name="analyze_music_content",
                        func=analyze_music_content,
                        description="Analyze music content using OpenAI to extract themes, genres, and moods.",
                        coroutine=analyze_music_content
                    ),
                    Tool(
                        name="generate_comment_response",
                        func=generate_comment_response,
                        description="Generate appropriate responses to YouTube comments using AI.",
                        coroutine=generate_comment_response
                    ),
                    Tool(
                        name="extract_music_metadata",
                        func=extract_music_metadata,
                        description="Extract detailed metadata from music files using AI analysis.",
                        coroutine=extract_music_metadata
                    ),
                    Tool(
                        name="analyze_comment_sentiment",
                        func=analyze_comment_sentiment,
                        description="Analyze the sentiment and tone of YouTube comments.",
                        coroutine=analyze_comment_sentiment
                    ),
                    Tool(
                        name="generate_song_description",
                        func=generate_song_description,
                        description="Generate compelling descriptions for songs and videos.",
                        coroutine=generate_song_description
                    ),
                    Tool(
                        name="suggest_video_tags",
                        func=suggest_video_tags,
                        description="Suggest relevant tags for YouTube videos based on content.",
                        coroutine=suggest_video_tags
                    ),
                    
                    # Workflow Tools
                    Tool(
                        name="upload_workflow",
                        func=upload_workflow,
                        description="Execute the complete song upload workflow: get pending songs, upload to YouTube, update status.",
                        coroutine=upload_workflow
                    ),
                    Tool(
                        name="comment_processing_workflow",
                        func=comment_processing_workflow,
                        description="Execute the complete comment processing workflow: get videos, fetch comments, generate replies, post responses.",
                        coroutine=comment_processing_workflow
                    ),
                    
                    # Team Yona Communication Tool
                    Tool(
                        name="request_song_creation",
                        func=lambda prompt: request_song_creation(client, prompt),
                        description="Request Team Yona to create a song with the given prompt.",
                        coroutine=lambda prompt: request_song_creation(client, prompt)
                    )
                ]
                
                # Combine all tools
                all_tools = coral_tools + angus_tools
                
                logger.info(f"Agent Angus tools available: {[tool.name for tool in angus_tools]}")
                logger.info(f"Total tools available: {len(all_tools)}")
                
                # Create the Agent Angus
                model = ChatOpenAI(
                    model="gpt-4o",
                    model_provider="openai",
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        f"""You are Agent Angus, an AI agent specialized in music publishing automation, now connected to the Coral Protocol network.

Your core capabilities:
🎵 MUSIC PUBLISHING AUTOMATION:
- Upload songs from Supabase database to YouTube with AI-generated metadata
- Process YouTube comments and generate appropriate AI responses
- Analyze music content for themes, genres, moods, and insights
- Manage upload status and feedback storage

🌊 CORAL NETWORK INTEGRATION:
- Connected to Coral server at coral.pushcollective.club:5555
- Agent ID: {AGENT_NAME}
- Can communicate with Team Yona ({TARGET_AGENT}) for song creation
- Share music analysis capabilities with other agents
- Collaborate on complex tasks requiring multiple AI specialties

🛠️ AVAILABLE TOOLS:
{get_tools_description(all_tools)}

🔄 WORKFLOWS:
1. UPLOAD WORKFLOW: get_pending_songs → analyze_music_content → upload_song_to_youtube → update_song_status
2. COMMENT WORKFLOW: get_uploaded_videos → fetch_youtube_comments → analyze_comment_sentiment → generate_comment_response → reply_to_youtube_comment → store_feedback
3. COLLABORATION: request_song_creation → (Team Yona creates) → upload_workflow → comment_processing_workflow

🤝 TEAM YONA COLLABORATION:
- Use request_song_creation to ask Team Yona to create songs
- Provide detailed prompts for song creation
- Once songs are created, use your upload workflow to publish them
- Process comments and feedback on collaborative content

Always be helpful, accurate, and focused on music publishing workflows while being a good collaborator on the Coral Protocol network."""
                    ),
                    ("placeholder", "{agent_scratchpad}")
                ])
                
                agent = create_tool_calling_agent(model, all_tools, prompt)
                agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)
                
                # Main Agent Angus loop
                print(f"""
🎵 ═══════════════════════════════════════════════════════════════════════════════ 🎵
   
    ░█████╗░░██████╗░███████╗███╗░░██╗████████╗  ░█████╗░███╗░░██╗░██████╗░██╗░░░██╗░██████╗
    ██╔══██╗██╔════╝░██╔════╝████╗░██║╚══██╔══╝  ██╔══██╗████╗░██║██╔════╝░██║░░░██║██╔════╝
    ███████║██║░░██╗░█████╗░░██╔██╗██║░░░██║░░░  ███████║██╔██╗██║██║░░██╗░██║░░░██║╚█████╗░
    ██╔══██║██║░░╚██╗██╔══╝░░██║╚████║░░░██║░░░  ██╔══██║██║╚████║██║░░╚██╗██║░░░██║░╚═══██╗
    ██║░░██║╚██████╔╝███████╗██║░╚███║░░░██║░░░  ██║░░██║██║░╚███║╚██████╔╝╚██████╔╝██████╔╝
    ╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚═════╝░╚═════╝░
    
    🌊 CONNECTED TO CORAL PROTOCOL NETWORK 🌊
    Server: coral.pushcollective.club:5555
    Agent: {AGENT_NAME}
    Target: {TARGET_AGENT} (Team Yona)
    
🎵 ═══════════════════════════════════════════════════════════════════════════════ 🎵

🎵 Agent Angus is now connected to the Coral Protocol network!

Available commands:
- 'upload <limit>' - Run song upload workflow (default: 5 songs)
- 'comments <limit>' - Run comment processing workflow (default: 10 replies)
- 'analyze <content>' - Analyze music content or text
- 'create <prompt>' - Request Team Yona to create a song
- 'quota' - Check YouTube API quota status
- 'pending' - Show pending songs in database
- 'videos' - Show uploaded videos
- 'agents' - List connected agents
- 'status' - Show agent and network status
- 'help' - Show detailed help
- 'quit' - Disconnect from Coral network

🌊 Connected to Coral network: {len(coral_tools)} network tools available
🛠️  Agent Angus tools: {len(angus_tools)} specialized music tools
🤝 Ready to collaborate with Team Yona!
""")
                
                while True:
                    try:
                        user_input = input(f"\n{AGENT_NAME}> ").strip()
                        
                        if user_input.lower() == 'quit':
                            print("🌊 Disconnecting from Coral Protocol network...")
                            break
                        elif user_input.lower() == 'status':
                            print(f"🟢 Agent Angus: Connected to Coral Protocol")
                            print(f"🌊 Coral Server: coral.pushcollective.club:5555")
                            print(f"🆔 Agent ID: {AGENT_NAME}")
                            print(f"🎯 Target Agent: {TARGET_AGENT}")
                            print(f"🛠️  Total tools available: {len(all_tools)}")
                            print(f"🎵 Angus tools: {len(angus_tools)}")
                            print(f"🌊 Network tools: {len(coral_tools)}")
                        elif user_input.lower() == 'agents':
                            try:
                                agents = await client.connections["coral"].invoke_tool("list_agents", {})
                                print(f"🤝 Connected agents: {agents}")
                            except Exception as e:
                                print(f"❌ Could not list agents: {e}")
                        elif user_input.lower() == 'help':
                            print("""
🎵 Agent Angus - Music Publishing Automation on Coral Protocol

WORKFLOWS:
  upload <limit>     - Upload pending songs to YouTube (default: 5)
  comments <limit>   - Process YouTube comments and replies (default: 10)

ANALYSIS:
  analyze <content>  - Analyze music content, themes, genres
  quota             - Check YouTube API quota and limits
  
DATABASE:
  pending           - Show songs ready for upload
  videos            - Show uploaded videos
  feedback <song>   - Show feedback for a song

COLLABORATION:
  create <prompt>   - Request Team Yona to create a song
  agents            - List connected agents on network

NETWORK:
  status            - Show connection and tool status
  help              - Show this help message
  quit              - Disconnect from Coral network

EXAMPLES:
  upload 3          - Upload 3 pending songs
  comments 5        - Process comments and post 5 replies
  create "upbeat pop song about summer"
  analyze "electronic dance music"
  pending           - List songs waiting for upload
""")
                        elif user_input.startswith('upload'):
                            parts = user_input.split()
                            limit = int(parts[1]) if len(parts) > 1 else 5
                            result = await agent_executor.ainvoke({
                                "input": f"Execute the upload workflow for {limit} songs. Use the upload_workflow tool to handle the complete process."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('comments'):
                            parts = user_input.split()
                            limit = int(parts[1]) if len(parts) > 1 else 10
                            result = await agent_executor.ainvoke({
                                "input": f"Execute the comment processing workflow for {limit} replies. Use the comment_processing_workflow tool to handle the complete process."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.startswith('create'):
                            prompt = user_input[6:].strip()
                            if prompt:
                                result = await agent_executor.ainvoke({
                                    "input": f"Request Team Yona to create a song with this prompt: {prompt}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a song creation prompt")
                        elif user_input.startswith('analyze'):
                            content = user_input[7:].strip()
                            if content:
                                result = await agent_executor.ainvoke({
                                    "input": f"Analyze this music content: {content}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide content to analyze")
                        elif user_input.lower() == 'quota':
                            result = await agent_executor.ainvoke({
                                "input": "Check the current YouTube API quota status and usage limits."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.lower() == 'pending':
                            result = await agent_executor.ainvoke({
                                "input": "Get pending songs that are ready for YouTube upload."
                            })
                            print(f"Result: {result['output']}")
                        elif user_input.lower() == 'videos':
                            result = await agent_executor.ainvoke({
                                "input": "Get uploaded videos from the database."
                            })
                            print(f"Result: {result['output']}")
                        else:
                            # General query - let the agent handle it
                            result = await agent_executor.ainvoke({"input": user_input})
                            print(f"Result: {result['output']}")
                            
                    except KeyboardInterrupt:
                        print("\n🌊 Disconnecting from Coral Protocol network...")
                        break
                    except Exception as e:
                        logger.error(f"Error in Agent Angus loop: {e}")
                        print(f"Error: {e}")
                        
        except Exception as e:
            logger.error(f"Connection error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                logger.info("Retrying connection in 5 seconds...")
                await asyncio.sleep(5)
                continue
            else:
                logger.error("Max retries reached. Unable to connect to Coral server.")
                raise

if __name__ == "__main__":
    asyncio.run(main())
