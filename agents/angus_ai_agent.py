"""
Angus AI Agent - Specialized agent for OpenAI operations using Coral Protocol.

This agent handles all AI-powered operations for the Agent Angus system including
music analysis, comment response generation, and content creation.
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

# Import our AI tools
from tools.ai_tools import (
    analyze_music_content, generate_comment_response, extract_music_metadata,
    analyze_comment_sentiment, generate_song_description, suggest_video_tags
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
    "agentId": "angus_ai",
    "agentDescription": "AI specialist for Agent Angus system, providing OpenAI-powered music analysis, comment response generation, and content creation."
}
query_string = "&".join([f"{k}={v}" for k, v in params.items()])
MCP_SERVER_URL = f"{base_url}?{query_string}"

AGENT_NAME = "angus_ai"

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
                
                # Add our AI tools
                ai_tools = [
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
                    )
                ]
                
                # Combine all tools
                all_tools = coral_tools + ai_tools
                
                logger.info(f"AI Agent tools available: {[tool.name for tool in ai_tools]}")
                
                # Create the AI agent
                model = ChatOpenAI(
                    model="gpt-4o",
                    model_provider="openai",
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                
                prompt = ChatPromptTemplate.from_messages([
                    (
                        "system",
                        f"""You are the Angus AI Agent, specialized in providing OpenAI-powered analysis and content generation for the Agent Angus music automation system.

Your responsibilities:
1. Analyze music content to extract themes, genres, moods, and metadata
2. Generate appropriate and engaging responses to YouTube comments
3. Create compelling song descriptions and video metadata
4. Analyze comment sentiment and tone for appropriate responses
5. Suggest relevant tags and keywords for video optimization
6. Provide intelligent content recommendations and insights

AI operations you handle:
- Music Analysis: Extract musical themes, genres, moods, and characteristics
- Content Generation: Create descriptions, responses, and metadata
- Sentiment Analysis: Understand comment tone and context
- Tag Suggestion: Recommend relevant keywords and tags
- Response Generation: Create appropriate replies to user comments
- Metadata Extraction: Analyze and categorize music content

Available tools: {get_tools_description(all_tools)}

Always provide helpful, accurate, and contextually appropriate responses.
Maintain a friendly and professional tone in all generated content.
Respect content guidelines and community standards."""
                    ),
                    ("placeholder", "{agent_scratchpad}")
                ])
                
                agent = create_tool_calling_agent(model, all_tools, prompt)
                agent_executor = AgentExecutor(agent=agent, tools=all_tools, verbose=True)
                
                # Main AI agent loop
                print(f"\n🤖 Angus AI Agent started!")
                print("Available commands:")
                print("- 'analyze <input>' - Analyze music content or text")
                print("- 'respond <comment>' - Generate response to a comment")
                print("- 'describe <song_info>' - Generate song description")
                print("- 'tags <content>' - Suggest video tags")
                print("- 'sentiment <comment>' - Analyze comment sentiment")
                print("- 'metadata <audio_url>' - Extract music metadata")
                print("- 'status' - Show AI agent status")
                print("- 'quit' - Exit")
                
                while True:
                    try:
                        user_input = input("\nAI> ").strip()
                        
                        if user_input.lower() == 'quit':
                            break
                        elif user_input.lower() == 'status':
                            print("🟢 AI Agent: Active")
                            print(f"🔗 Connected to Coral Server: {MCP_SERVER_URL}")
                            print(f"🛠️  AI tools available: {len(ai_tools)}")
                            print(f"🧠 OpenAI Model: gpt-4o")
                        elif user_input.startswith('analyze'):
                            content = user_input[7:].strip()
                            if content:
                                result = await agent_executor.ainvoke({
                                    "input": f"Analyze this music content: {content}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide content to analyze")
                        elif user_input.startswith('respond'):
                            comment = user_input[7:].strip()
                            if comment:
                                result = await agent_executor.ainvoke({
                                    "input": f"Generate an appropriate response to this comment: {comment}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a comment to respond to")
                        elif user_input.startswith('describe'):
                            song_info = user_input[8:].strip()
                            if song_info:
                                result = await agent_executor.ainvoke({
                                    "input": f"Generate a compelling description for this song: {song_info}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide song information")
                        elif user_input.startswith('tags'):
                            content = user_input[4:].strip()
                            if content:
                                result = await agent_executor.ainvoke({
                                    "input": f"Suggest relevant tags for this content: {content}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide content for tag suggestions")
                        elif user_input.startswith('sentiment'):
                            comment = user_input[9:].strip()
                            if comment:
                                result = await agent_executor.ainvoke({
                                    "input": f"Analyze the sentiment of this comment: {comment}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide a comment for sentiment analysis")
                        elif user_input.startswith('metadata'):
                            audio_url = user_input[8:].strip()
                            if audio_url:
                                result = await agent_executor.ainvoke({
                                    "input": f"Extract metadata from this audio: {audio_url}"
                                })
                                print(f"Result: {result['output']}")
                            else:
                                print("Please provide an audio URL")
                        else:
                            # General AI query
                            result = await agent_executor.ainvoke({"input": user_input})
                            print(f"Result: {result['output']}")
                            
                    except KeyboardInterrupt:
                        print("\nShutting down AI agent...")
                        break
                    except Exception as e:
                        logger.error(f"Error in AI agent loop: {e}")
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
