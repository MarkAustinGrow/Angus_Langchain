"""
Agent Angus - Coraliser Compatible LangChain Agent

This module creates a Coraliser-compatible Agent Angus that follows the official
Coral Protocol pattern for distributed AI agent collaboration.

Based on the LangChain WorldNews example from:
https://github.com/Coral-Protocol/coraliser/tree/main/coral_examples/langchain-worldnews
"""

import asyncio
import os
import json
import logging
import re
from urllib.parse import urlencode
from dotenv import load_dotenv

# LangChain MCP imports
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

# Agent Angus tool imports
from tools.youtube_tools import (
    upload_song_to_youtube,
    fetch_youtube_comments,
    reply_to_youtube_comment,
    check_upload_quota,
    get_video_details
)
from tools.supabase_tools import (
    get_pending_songs,
    store_feedback,
    update_song_status,
    get_song_details,
    get_uploaded_videos,
    get_existing_feedback,
    log_agent_activity
)
from tools.ai_tools import (
    analyze_music_content,
    generate_comment_response,
    extract_music_metadata,
    analyze_comment_sentiment,
    generate_song_description,
    suggest_video_tags
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
base_url = "http://localhost:5555/devmode/exampleApplication/privkey/session1/sse"
params = {
    "waitForAgentS": 2,
    "agentId": "angus_music_agent",
    "agentDescription": "You are Agent Angus, responsible for music publishing automation on YouTube. You handle song uploads, comment processing, and AI-powered music analysis. You collaborate with other agents in the Coral network to provide comprehensive music automation services."
}
query_string = urlencode(params)
MCP_SERVER_URL = f"{base_url}?{query_string}"

AGENT_NAME = "angus_music_agent"

def get_tools_description(tools):
    """Generate description of available tools."""
    return "\n".join(
        f"Tool: {tool.name}, Schema: {json.dumps(tool.args).replace('{', '{{').replace('}', '}}')}"
        for tool in tools
    )

@tool
def AngusYouTubeUploadTool(
    song_limit: int = 5,
    auto_generate_metadata: bool = True,
) -> str:
    """
    Upload pending songs from database to YouTube with AI-generated metadata.
    
    Args:
        song_limit: Maximum number of songs to upload (default: 5)
        auto_generate_metadata: Whether to auto-generate titles/descriptions (default: True)
    
    Returns:
        dict: Contains 'result' key with status of upload operations
    """
    logger.info(f"Calling AngusYouTubeUploadTool with song_limit: {song_limit}")
    
    try:
        # Get pending songs
        pending_result = get_pending_songs.invoke({"limit": song_limit})
        if not pending_result or "error" in pending_result:
            return {"result": f"Failed to get pending songs: {pending_result}"}
        
        # Handle both dict and list responses
        if isinstance(pending_result, dict):
            songs = pending_result.get("songs", [])
        else:
            songs = pending_result  # Direct list response
            
        if not songs:
            return {"result": "No pending songs found for upload"}
        
        upload_results = []
        
        for song in songs[:song_limit]:
            song_id = song.get("id")
            title = song.get("title", "Untitled Song")
            
            try:
                # Generate metadata if requested
                if auto_generate_metadata and song.get("audio_path"):
                    analysis_result = analyze_music_content.invoke({
                        "audio_path": song["audio_path"]
                    })
                    
                    if analysis_result and "analysis" in analysis_result:
                        # Generate enhanced description
                        desc_result = generate_song_description.invoke({
                            "song_title": title,
                            "analysis": analysis_result["analysis"]
                        })
                        description = desc_result.get("description", song.get("description", ""))
                        
                        # Generate tags
                        tags_result = suggest_video_tags.invoke({
                            "song_title": title,
                            "genre": analysis_result["analysis"].get("genre", "music")
                        })
                        tags = tags_result.get("tags", [])
                    else:
                        description = song.get("description", "")
                        tags = []
                else:
                    description = song.get("description", "")
                    tags = []
                
                # Upload to YouTube
                upload_result = upload_song_to_youtube.invoke({
                    "song_id": song_id,
                    "title": title,
                    "description": description,
                    "tags": tags
                })
                
                if upload_result and "video_id" in upload_result:
                    # Update song status
                    update_song_status.invoke({
                        "song_id": song_id,
                        "status": "uploaded",
                        "video_id": upload_result["video_id"]
                    })
                    upload_results.append(f"✅ Uploaded '{title}' -> {upload_result['video_id']}")
                else:
                    upload_results.append(f"❌ Failed to upload '{title}': {upload_result}")
                    
            except Exception as e:
                upload_results.append(f"❌ Error uploading '{title}': {str(e)}")
        
        result_summary = f"Upload completed: {len([r for r in upload_results if '✅' in r])}/{len(songs)} successful\n" + "\n".join(upload_results)
        return {"result": result_summary}
        
    except Exception as e:
        logger.error(f"AngusYouTubeUploadTool error: {str(e)}")
        return {"result": f"Upload tool error: {str(e)}"}

@tool
def AngusCommentProcessingTool(
    comment_limit: int = 10,
    auto_reply: bool = True,
) -> str:
    """
    Process YouTube comments for uploaded videos with AI-powered responses.
    
    Args:
        comment_limit: Maximum number of comments to process (default: 10)
        auto_reply: Whether to automatically reply to comments (default: True)
    
    Returns:
        dict: Contains 'result' key with status of comment processing
    """
    logger.info(f"Calling AngusCommentProcessingTool with comment_limit: {comment_limit}")
    
    try:
        # Get uploaded videos
        videos_result = get_uploaded_videos.invoke({"limit": 20})
        if not videos_result or "error" in videos_result:
            return {"result": f"Failed to get uploaded videos: {videos_result}"}
        
        # Handle both dict and list responses
        if isinstance(videos_result, dict):
            videos = videos_result.get("videos", [])
        else:
            videos = videos_result  # Direct list response
            
        if not videos:
            return {"result": "No uploaded videos found for comment processing"}
        
        processing_results = []
        comments_processed = 0
        
        for video in videos:
            if comments_processed >= comment_limit:
                break
                
            video_id = video.get("video_id")
            video_title = video.get("title", "Unknown")
            
            try:
                # Fetch comments
                comments_result = fetch_youtube_comments.invoke({
                    "video_id": video_id,
                    "max_results": min(comment_limit - comments_processed, 10)
                })
                
                if not comments_result or "error" in comments_result:
                    processing_results.append(f"❌ Failed to fetch comments for '{video_title}'")
                    continue
                
                comments = comments_result.get("comments", [])
                
                for comment in comments:
                    if comments_processed >= comment_limit:
                        break
                        
                    comment_id = comment.get("id")
                    comment_text = comment.get("text", "")
                    
                    # Check if already processed
                    existing_result = get_existing_feedback.invoke({
                        "video_id": video_id,
                        "comment_id": comment_id
                    })
                    
                    if existing_result and existing_result.get("exists"):
                        continue
                    
                    # Analyze sentiment
                    sentiment_result = analyze_comment_sentiment.invoke({
                        "comment_text": comment_text
                    })
                    
                    # Generate response if auto_reply is enabled
                    if auto_reply:
                        response_result = generate_comment_response.invoke({
                            "comment_text": comment_text,
                            "context": {"video_title": video_title}
                        })
                        
                        if response_result and "response" in response_result:
                            reply_result = reply_to_youtube_comment.invoke({
                                "comment_id": comment_id,
                                "reply_text": response_result["response"]
                            })
                            
                            if reply_result and "success" in reply_result:
                                processing_results.append(f"✅ Replied to comment on '{video_title}'")
                            else:
                                processing_results.append(f"❌ Failed to reply to comment on '{video_title}'")
                    
                    # Store feedback
                    store_feedback.invoke({
                        "video_id": video_id,
                        "comment_data": {
                            "comment_id": comment_id,
                            "text": comment_text,
                            "sentiment": sentiment_result.get("sentiment", "neutral"),
                            "processed": True
                        }
                    })
                    
                    comments_processed += 1
                    
            except Exception as e:
                processing_results.append(f"❌ Error processing comments for '{video_title}': {str(e)}")
        
        result_summary = f"Comment processing completed: {comments_processed} comments processed\n" + "\n".join(processing_results[-10:])  # Show last 10 results
        return {"result": result_summary}
        
    except Exception as e:
        logger.error(f"AngusCommentProcessingTool error: {str(e)}")
        return {"result": f"Comment processing error: {str(e)}"}

@tool
def AngusQuotaCheckTool() -> str:
    """
    Check YouTube API quota usage and limits.
    
    Returns:
        dict: Contains 'result' key with quota information
    """
    logger.info("Calling AngusQuotaCheckTool")
    
    try:
        quota_result = check_upload_quota.invoke({})
        
        if quota_result and "quota" in quota_result:
            quota_info = quota_result["quota"]
            result = f"YouTube API Quota Status:\n"
            result += f"Daily Limit: {quota_info.get('daily_limit', 'Unknown')}\n"
            result += f"Remaining: {quota_info.get('remaining', 'Unknown')}\n"
            result += f"Used: {quota_info.get('used', 'Unknown')}\n"
            result += f"Status: {quota_info.get('status', 'Unknown')}"
            
            return {"result": result}
        else:
            return {"result": f"Failed to check quota: {quota_result}"}
            
    except Exception as e:
        logger.error(f"AngusQuotaCheckTool error: {str(e)}")
        return {"result": f"Quota check error: {str(e)}"}

async def create_angus_music_agent(client, tools, agent_tool):
    """Create Agent Angus with Coral Protocol integration."""
    tools_description = get_tools_description(tools)
    agent_tools_description = get_tools_description(agent_tool)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""You are Agent Angus, an AI agent specialized in music publishing automation on YouTube, interacting with tools from Coral Server and having your own specialized tools. Your task is to collaborate with other agents in the Coral network while managing music automation workflows.

Follow these steps in order:
1. Call wait_for_mentions from coral tools (timeoutMs: 8000) to receive mentions from other agents.
2. When you receive a mention, keep the thread ID and the sender ID.
3. Process the request using your specialized music tools or coral tools as appropriate.
4. Use send_message from coral tools to respond back to the sender agent with the thread ID.
5. Always respond back to the sender agent even if you have no answer or error.
6. Wait for 2 seconds and repeat the process from step 1.

Your specialized capabilities:
- YouTube automation (upload songs, process comments, manage videos)
- Music analysis and metadata generation
- Database management for music content
- AI-powered content creation and sentiment analysis

These are the list of all tools (Coral + your tools): {tools_description}
These are the list of your specialized tools: {agent_tools_description}

When collaborating with other agents:
- Clearly identify yourself as Agent Angus, the music automation specialist
- Offer your music-related services to other agents
- Ask for clarification if requests are outside your music domain
- Provide detailed status updates on music operations
- Share insights from music analysis when relevant

Your responses should be helpful, professional, and focused on music automation workflows."""
        ),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    model = init_chat_model(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3,
        max_tokens=16000
    )
    
    agent = create_tool_calling_agent(model, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

async def main():
    """Main function to run Agent Angus in Coraliser mode."""
    try:
        # Create MCP client (new API - no context manager)
        client = MultiServerMCPClient(
            connections={
                "coral": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-everything"],
                    "env": {"MCP_SERVER_URL": MCP_SERVER_URL}
                }
            }
        )
        
        logger.info(f"Attempting to connect to MCP server at {MCP_SERVER_URL}")
        
        # Get Coral tools (may fail if server not available)
        try:
            coral_tools = await client.get_tools()
            logger.info(f"Successfully connected to Coral server, got {len(coral_tools)} tools")
        except Exception as e:
            logger.warning(f"Could not connect to Coral server: {str(e)}")
            logger.info("Continuing with Agent Angus tools only")
            coral_tools = []
        
        # Get Agent Angus specialized tools
        angus_tools = [
            AngusYouTubeUploadTool,
            AngusCommentProcessingTool, 
            AngusQuotaCheckTool
        ]
        
        # Combine all tools
        all_tools = coral_tools + angus_tools
        
        logger.info(f"Total tools available: {len(all_tools)} (Coral: {len(coral_tools)}, Angus: {len(angus_tools)})")
        logger.info(f"Tools Description:\n{get_tools_description(all_tools)}")
        
        # Create agent
        agent_executor = await create_angus_music_agent(client, all_tools, angus_tools)
        
        logger.info("🎵 Agent Angus Coraliser mode started successfully!")
        logger.info("Ready for inter-agent collaboration and music automation tasks")
        
        # Main agent loop
        while True:
            try:
                logger.info("Starting new agent invocation")
                await agent_executor.ainvoke({"agent_scratchpad": []})
                logger.info("Completed agent invocation, restarting loop")
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in agent loop: {str(e)}")
                await asyncio.sleep(5)
                
    except Exception as e:
        logger.error(f"Failed to start Agent Angus: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
