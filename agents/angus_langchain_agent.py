"""
Unified LangChain Agent Angus - Phase 2.5 Implementation

This module implements a single, powerful LangChain agent that replicates
all original Agent Angus functionality using the LangChain framework.
"""
import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Import all tools
from tools.supabase_tools import SUPABASE_TOOLS
from tools.youtube_tools import YOUTUBE_TOOLS
from tools.ai_tools import AI_TOOLS

# Configure logging
logger = logging.getLogger(__name__)

class AngusLangChainAgent:
    """
    Unified LangChain agent that replicates original Agent Angus functionality.
    
    This agent combines all YouTube, Supabase, and AI tools into a single
    powerful agent that can handle both song upload and comment processing workflows.
    """
    
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.1):
        """
        Initialize the unified Agent Angus.
        
        Args:
            model_name: OpenAI model to use
            temperature: Temperature for AI responses
        """
        self.model_name = model_name
        self.temperature = temperature
        self.agent = None
        self.executor = None
        self.tools = []
        self.status = "not_initialized"
        
        # Combine all tools
        self.tools = SUPABASE_TOOLS + YOUTUBE_TOOLS + AI_TOOLS
        
        logger.info(f"AngusLangChainAgent initialized with {len(self.tools)} tools")
    
    async def initialize(self):
        """Initialize the LangChain agent and executor."""
        try:
            logger.info("Initializing LangChain Agent Angus...")
            
            # Initialize the language model
            llm = ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature
            )
            
            # Create the system prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", self._get_system_prompt()),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ])
            
            # Create the agent
            self.agent = create_tool_calling_agent(llm, self.tools, prompt)
            
            # Create the executor
            self.executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=10,
                max_execution_time=300  # 5 minutes max per task
            )
            
            self.status = "initialized"
            logger.info("LangChain Agent Angus initialized successfully")
            
        except Exception as e:
            self.status = "error"
            logger.error(f"Failed to initialize Agent Angus: {str(e)}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for Agent Angus."""
        return """You are Agent Angus, an AI assistant specialized in music publishing automation using LangChain tools.

Your primary responsibilities:
1. Upload pending songs from the database to YouTube
2. Process YouTube comments and generate appropriate responses
3. Analyze music content for metadata and insights
4. Maintain data consistency between systems

Available tools:
- YouTube tools: upload_song_to_youtube, fetch_youtube_comments, reply_to_youtube_comment, check_upload_quota, get_video_details, process_video_comments
- Database tools: get_pending_songs, store_feedback, update_song_status, get_song_details, get_uploaded_videos, get_existing_feedback, log_agent_activity
- AI tools: analyze_music_content, generate_comment_response, extract_music_metadata, analyze_comment_sentiment, generate_song_description, suggest_video_tags

Workflow Guidelines:

For Song Upload Workflow:
1. Use get_pending_songs to find songs ready for upload
2. For each song, use get_song_details to get full information
3. Use upload_song_to_youtube to upload the song
4. The upload tool automatically updates the database status

For Comment Processing Workflow:
1. Use get_uploaded_videos to find videos that need comment processing
2. For each video, use process_video_comments which handles the complete workflow:
   - Fetches comments
   - Stores feedback in database
   - Generates AI responses
   - Replies to comments

Always:
- Be efficient and handle errors gracefully
- Log important activities using log_agent_activity
- Provide clear status updates
- Respect API limits and quotas
- Process items in batches to avoid overwhelming systems

When encountering errors:
- Log the error details
- Continue with other items when possible
- Provide helpful error messages
- Suggest next steps for resolution"""
    
    async def execute_task(self, task: str, context: Dict[str, Any] = None) -> str:
        """
        Execute a task using the LangChain agent.
        
        Args:
            task: Task description
            context: Additional context for the task
            
        Returns:
            Task execution result
        """
        if not self.executor:
            raise RuntimeError("Agent not initialized - call initialize() first")
        
        try:
            # Prepare input with context
            input_data = {"input": task}
            if context:
                input_data["context"] = context
            
            # Execute the task
            result = await self.executor.ainvoke(input_data)
            return result.get("output", "No output generated")
            
        except Exception as e:
            error_msg = f"Task execution failed: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    async def run_song_upload_workflow(self, limit: int = 5) -> Dict[str, Any]:
        """
        Execute the complete song upload workflow.
        
        Args:
            limit: Maximum number of songs to upload
            
        Returns:
            Dictionary with workflow results
        """
        logger.info(f"Starting song upload workflow (limit: {limit})")
        
        task = f"""Execute the song upload workflow:

1. Get up to {limit} pending songs from the database
2. For each song:
   - Get the song details
   - Upload the song to YouTube
   - Update the database status
3. Provide a summary of results

Handle any errors gracefully and continue with other songs if one fails.
Log the activity and provide a detailed summary."""
        
        try:
            result = await self.execute_task(task)
            logger.info("Song upload workflow completed")
            return {
                "status": "completed",
                "result": result,
                "workflow": "song_upload"
            }
        except Exception as e:
            error_msg = f"Song upload workflow failed: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "workflow": "song_upload"
            }
    
    async def run_comment_processing_workflow(self, max_replies: int = 10) -> Dict[str, Any]:
        """
        Execute the complete comment processing workflow.
        
        Args:
            max_replies: Maximum number of comment replies to post
            
        Returns:
            Dictionary with workflow results
        """
        logger.info(f"Starting comment processing workflow (max_replies: {max_replies})")
        
        task = f"""Execute the comment processing workflow:

1. Get uploaded videos from the database
2. For each video (up to 10 videos):
   - Process comments using process_video_comments tool
   - Limit to {max_replies} total replies across all videos
3. Provide a summary of results

The process_video_comments tool handles:
- Fetching new comments
- Storing feedback in database
- Generating AI responses
- Replying to comments

Handle any errors gracefully and continue with other videos if one fails.
Log the activity and provide a detailed summary."""
        
        try:
            result = await self.execute_task(task)
            logger.info("Comment processing workflow completed")
            return {
                "status": "completed",
                "result": result,
                "workflow": "comment_processing"
            }
        except Exception as e:
            error_msg = f"Comment processing workflow failed: {str(e)}"
            logger.error(error_msg)
            return {
                "status": "error",
                "error": error_msg,
                "workflow": "comment_processing"
            }
    
    async def run_both_workflows(self, upload_limit: int = 5, reply_limit: int = 10) -> Dict[str, Any]:
        """
        Run both song upload and comment processing workflows.
        
        Args:
            upload_limit: Maximum number of songs to upload
            reply_limit: Maximum number of comment replies to post
            
        Returns:
            Dictionary with combined workflow results
        """
        logger.info("Starting combined workflow execution")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "upload_workflow": None,
            "comment_workflow": None,
            "overall_status": "running"
        }
        
        try:
            # Run song upload workflow
            logger.info("Executing song upload workflow...")
            upload_result = await self.run_song_upload_workflow(upload_limit)
            results["upload_workflow"] = upload_result
            
            # Small delay between workflows
            await asyncio.sleep(2)
            
            # Run comment processing workflow
            logger.info("Executing comment processing workflow...")
            comment_result = await self.run_comment_processing_workflow(reply_limit)
            results["comment_workflow"] = comment_result
            
            # Determine overall status
            upload_success = upload_result.get("status") == "completed"
            comment_success = comment_result.get("status") == "completed"
            
            if upload_success and comment_success:
                results["overall_status"] = "completed"
            elif upload_success or comment_success:
                results["overall_status"] = "partial_success"
            else:
                results["overall_status"] = "failed"
            
            logger.info(f"Combined workflow completed with status: {results['overall_status']}")
            return results
            
        except Exception as e:
            error_msg = f"Combined workflow failed: {str(e)}"
            logger.error(error_msg)
            results["overall_status"] = "error"
            results["error"] = error_msg
            return results
    
    async def main_loop(self, upload_interval: int = 3600, comment_interval: int = 1800):
        """
        Main execution loop running both workflows with scheduling.
        
        Args:
            upload_interval: Seconds between upload workflow runs (default: 1 hour)
            comment_interval: Seconds between comment workflow runs (default: 30 minutes)
        """
        logger.info("Starting Agent Angus main loop")
        
        last_upload_time = 0
        last_comment_time = 0
        
        # Run initial workflows
        logger.info("Running initial workflows...")
        await self.run_both_workflows(upload_limit=1, reply_limit=5)
        
        last_upload_time = time.time()
        last_comment_time = time.time()
        
        try:
            while True:
                current_time = time.time()
                
                # Check if it's time to run upload workflow
                if current_time - last_upload_time >= upload_interval:
                    logger.info("Running scheduled upload workflow...")
                    await self.run_song_upload_workflow(limit=1)
                    last_upload_time = current_time
                
                # Check if it's time to run comment workflow
                if current_time - last_comment_time >= comment_interval:
                    logger.info("Running scheduled comment workflow...")
                    await self.run_comment_processing_workflow(max_replies=5)
                    last_comment_time = current_time
                
                # Sleep for 60 seconds before checking again
                await asyncio.sleep(60)
                
        except KeyboardInterrupt:
            logger.info("Main loop interrupted by user")
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information."""
        return {
            "status": self.status,
            "model": self.model_name,
            "temperature": self.temperature,
            "tools_count": len(self.tools),
            "agent_ready": self.executor is not None,
            "phase": "Phase 2.5 - Standalone LangChain Agent"
        }

# Factory function for easy creation
async def create_angus_langchain_agent(model_name: str = "gpt-4o") -> AngusLangChainAgent:
    """
    Create and initialize an AngusLangChainAgent.
    
    Args:
        model_name: OpenAI model to use
        
    Returns:
        Initialized AngusLangChainAgent
    """
    agent = AngusLangChainAgent(model_name=model_name)
    await agent.initialize()
    return agent
