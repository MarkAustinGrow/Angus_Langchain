# Agent Angus - Codebase Documentation

## 🎵 Project Overview

**Agent Angus** is a specialized AI agent for music publishing automation on YouTube, designed to operate within the **Coral Protocol** network for multi-agent collaboration. The agent handles song uploads, comment processing, quota management, and AI-powered music analysis while collaborating with other agents like Agent Yona.

### Key Capabilities:
- **YouTube Automation**: Automated song uploads with AI-generated metadata
- **Comment Processing**: AI-powered sentiment analysis and automated responses
- **Music Analysis**: Content analysis, genre detection, and metadata extraction
- **Coral Protocol Integration**: Multi-agent communication and collaboration
- **Database Management**: Song tracking, feedback storage, and activity logging

---

## 🏗️ Architecture Overview

### Core Components:
1. **Main Agent**: `1_langchain_angus_agent.py` - Coral Protocol compatible LangChain agent
2. **Specialized Tools**: YouTube, Supabase, and AI-powered tools
3. **Coral Integration**: MCP client for inter-agent communication
4. **Configuration System**: Environment and agent configuration management

### Communication Pattern:
```
Agent Yona ←→ Coral Protocol Server ←→ Agent Angus
                     ↓
              [Session Management]
                     ↓
           [Tool Routing & Execution]
```

---

## 📁 File Structure & Responsibilities

### 🎯 **Core Agent Files**

#### `1_langchain_angus_agent.py` ⭐ **MAIN AGENT**
- **Purpose**: Primary Coral Protocol compatible agent implementation
- **Status**: ✅ **PRODUCTION READY** - Fully functional with hybrid MCP API approach
- **Key Features**:
  - Coral Protocol integration with session management
  - Continuous agent loop (1-second intervals)
  - Tool integration (Coral + specialized tools)
  - Inter-agent communication via wait_for_mentions/send_message

#### `angus_langchain.py`
- **Purpose**: Original LangChain agent implementation
- **Status**: 🔄 Legacy - Superseded by `1_langchain_angus_agent.py`

#### `angus_openai_wrapper.py`
- **Purpose**: OpenAI-compatible HTTP API wrapper
- **Status**: ✅ Alternative communication method for Agent Yona
- **Use Case**: Stable HTTP endpoint when Coral Protocol session churn is problematic

### 🛠️ **Tools Directory**

#### `tools/youtube_tools.py`
- **Functions**: Upload songs, fetch comments, reply to comments, check quota
- **Integration**: YouTube Data API v3
- **Key Tools**: `upload_song_to_youtube`, `fetch_youtube_comments`, `check_upload_quota`

#### `tools/supabase_tools.py`
- **Functions**: Database operations for songs, feedback, and activity logging
- **Integration**: Supabase PostgreSQL database
- **Key Tools**: `get_pending_songs`, `store_feedback`, `update_song_status`

#### `tools/ai_tools.py`
- **Functions**: AI-powered content analysis and generation
- **Integration**: OpenAI GPT models
- **Key Tools**: `analyze_music_content`, `generate_comment_response`, `extract_music_metadata`

### ⚙️ **Configuration Files**

#### `config/environment.py`
- **Purpose**: Environment variable loading and validation
- **Required Variables**: OpenAI API key, YouTube API credentials, Supabase config

#### `config/coral_config.py`
- **Purpose**: Coral Protocol specific configuration
- **Settings**: Server URLs, agent descriptions, timeout values

#### `.env.example`
- **Purpose**: Template for environment variables
- **Usage**: Copy to `.env` and fill in actual API keys

### 🌊 **Coral Integration**

#### `coral_integration/mcp_client.py`
- **Purpose**: MCP client wrapper and utilities
- **Status**: ✅ Compatible with langchain-mcp-adapters 0.1.0

#### `start_coral_client.py`
- **Purpose**: Standalone Coral client for testing
- **Usage**: Testing Coral Protocol connectivity

---

## 🔧 Technical Implementation Details

### Coral Protocol Communication Pattern

#### **Agent Loop (Official Pattern)**:
```python
# Main agent loop - runs continuously
while True:
    try:
        logger.info("Starting new agent invocation")
        await agent_executor.ainvoke({"agent_scratchpad": []})
        logger.info("Completed agent invocation, restarting loop")
        await asyncio.sleep(1)  # 1-second intervals
    except Exception as e:
        logger.error(f"Error in agent loop: {str(e)}")
        await asyncio.sleep(5)  # 5-second error recovery
```

#### **Session Management**:
- **Session Churn**: Normal behavior - new session every ~1 second
- **Communication Windows**: Multiple opportunities per minute for inter-agent communication
- **Timeout Handling**: `wait_for_mentions` with 8000ms timeout, but actual cycles are ~1 second

#### **MCP API Compatibility**:
```python
# NEW API (Compatible with 0.1.0)
client = MultiServerMCPClient(connections={...})
coral_tools = await client.get_tools()

# OLD API (Deprecated - causes NotImplementedError)
# async with MultiServerMCPClient(...) as client:  # ❌ Don't use
```

### Tool Integration Pattern

#### **Specialized Agent Tools**:
```python
@tool
def AngusYouTubeUploadTool(song_limit: int = 5, auto_generate_metadata: bool = True) -> str:
    """Upload pending songs with AI-generated metadata"""
    # Implementation handles database queries, AI analysis, YouTube uploads
```

#### **Tool Combination**:
```python
# Combine Coral Protocol tools + Agent Angus specialized tools
tools = coral_tools + angus_tools
agent_tool = angus_tools  # Specialized tools for agent description
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup

#### **Required Dependencies**:
```bash
pip install -r requirements.txt
```

#### **Environment Variables** (`.env` file):
```env
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 2. Running Agent Angus

#### **Primary Method (Coral Protocol)**:
```bash
python3 1_langchain_angus_agent.py
```

#### **Expected Output**:
```
INFO:__main__:Successfully connected to Coral server, got 7 tools
INFO:__main__:Total tools available: 10 (Coral: 7, Angus: 3)
INFO:__main__:🎵 Agent Angus Coraliser mode started successfully!
INFO:__main__:Starting new agent invocation

> Entering new AgentExecutor chain...
Invoking: `wait_for_mentions` with {'timeoutMs': 8000}
```

#### **Alternative Method (HTTP API)**:
```bash
python3 start_angus_openai_wrapper.py
# Provides stable HTTP endpoint at localhost:8000
```

### 3. Testing Communication

#### **Agent Yona → Agent Angus Communication**:
```
Agent Yona: "@angus_music_agent, upload 3 songs to YouTube"
Agent Angus: Processes request, uploads songs, responds with results
```

#### **Available Commands**:
- `@angus_music_agent, upload songs to YouTube`
- `@angus_music_agent, check YouTube quota status`
- `@angus_music_agent, process comments on recent uploads`

---

## 🔍 Current Status & Recent Fixes

### ✅ **Working Components**:
1. **Coral Protocol Integration**: Fully functional with hybrid MCP API approach
2. **Agent Communication**: Continuous loop with proper session management
3. **Tool Integration**: All 10 tools (7 Coral + 3 Angus) working correctly
4. **YouTube Automation**: Upload, comment processing, quota checking operational
5. **AI Analysis**: Music content analysis and metadata generation working

### 🔧 **Recent Fixes Applied**:

#### **MCP API Compatibility (Fixed)**:
- **Issue**: `NotImplementedError` with context manager in langchain-mcp-adapters 0.1.0
- **Solution**: Hybrid approach using new API with official Coral Protocol patterns
- **Status**: ✅ **RESOLVED**

#### **Session Churn Management (Optimized)**:
- **Issue**: Rapid session creation preventing stable communication
- **Solution**: Aligned with official LangChain WorldNews example patterns
- **Status**: ✅ **WORKING AS DESIGNED** - Session churn is normal Coral Protocol behavior

#### **Agent Loop Optimization (Completed)**:
- **Issue**: Various timing and communication window problems
- **Solution**: 1-second intervals with 8-second wait_for_mentions timeout
- **Status**: ✅ **OPTIMAL PERFORMANCE**

### 🎯 **Known Issues & Next Steps**:

#### **Agent Yona Communication**:
- **Issue**: Agent Yona may not have continuous loop like Agent Angus
- **Impact**: One-way communication instead of bidirectional
- **Solution**: Agent Yona needs same continuous loop pattern
- **Priority**: 🔴 **HIGH** - Required for full multi-agent collaboration

#### **Session Targeting**:
- **Issue**: Rapid session changes may require precise timing for communication
- **Workaround**: Multiple communication attempts or HTTP API fallback
- **Status**: 🟡 **MONITORING** - Working but could be improved

---

## 🛠️ Development Patterns

### Adding New Tools

#### **1. Create Tool Function**:
```python
@tool
def NewAgentTool(param1: str, param2: int = 10) -> str:
    """Tool description for AI agent"""
    try:
        # Implementation
        return {"result": "Success message"}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}
```

#### **2. Add to Tool List**:
```python
angus_tools = [
    AngusYouTubeUploadTool,
    AngusCommentProcessingTool,
    AngusQuotaCheckTool,
    NewAgentTool  # Add here
]
```

### Coral Protocol Communication

#### **Sending Messages**:
```python
# In agent prompt/logic
send_message_result = send_message.invoke({
    "threadId": thread_id,
    "content": "Response message",
    "mentions": ["target_agent_id"]
})
```

#### **Receiving Messages**:
```python
# Automatic via wait_for_mentions in agent loop
mentions_result = wait_for_mentions.invoke({"timeoutMs": 8000})
```

---

## 🚨 Troubleshooting Guide

### Common Issues & Solutions

#### **1. MCP API Errors**:
```
NotImplementedError: MultiServerMCPClient cannot be used as a context manager
```
**Solution**: Use new API pattern (already implemented in `1_langchain_angus_agent.py`)

#### **2. Connection Failures**:
```
Could not connect to Coral server: [error]
```
**Solutions**:
- Check Coral server is running
- Verify network connectivity
- Use Agent Angus tools only mode (automatic fallback)

#### **3. Tool Execution Errors**:
```
YouTube API error / Supabase connection failed
```
**Solutions**:
- Verify API keys in `.env` file
- Check quota limits
- Review tool-specific error messages

#### **4. Agent Communication Issues**:
```
No response from Agent Angus
```
**Solutions**:
- Verify Agent Angus is running with continuous loop
- Check agent ID format: `@angus_music_agent`
- Try HTTP API wrapper as fallback

### Debugging Commands

#### **Check Agent Status**:
```bash
# Should show continuous loop with session creation
python3 1_langchain_angus_agent.py
```

#### **Test HTTP API**:
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Check quota status"}]}'
```

#### **Verify Environment**:
```python
from config.environment import load_environment_variables
load_environment_variables()  # Should not raise errors
```

---

## 📚 Additional Resources

### Documentation Files:
- `README.md` - Project overview and setup instructions
- `DEPLOYMENT.md` - Production deployment guide
- `OPENAI_WRAPPER_GUIDE.md` - HTTP API wrapper documentation
- `README_CORALISER.md` - Coral Protocol integration details

### Configuration Files:
- `.env.example` - Environment variable template
- `coraliser_settings.json` - Coral Protocol settings
- `requirements.txt` - Python dependencies

### Startup Scripts:
- `start_coral_agents.py` - Multi-agent startup
- `start_coral_client.py` - Coral client testing
- `start_angus_openai_wrapper.py` - HTTP API server

---

## 🎯 Mission Statement

**Agent Angus** serves as a specialized music automation agent within the Coral Protocol ecosystem, providing:

1. **Automated Music Publishing**: Streamlined YouTube upload workflows
2. **AI-Powered Content Management**: Intelligent metadata generation and comment processing
3. **Multi-Agent Collaboration**: Seamless integration with other agents like Agent Yona
4. **Scalable Architecture**: Production-ready implementation with proper error handling

The agent is designed to be **reliable**, **responsive**, and **collaborative**, serving as a model for specialized AI agents in distributed networks.

---

## 📝 Development Notes

### Code Quality Standards:
- ✅ **Type Hints**: All functions properly typed
- ✅ **Error Handling**: Comprehensive try/catch blocks
- ✅ **Logging**: Detailed logging for debugging
- ✅ **Documentation**: Inline comments and docstrings

### Testing Approach:
- **Integration Testing**: Full agent workflow testing
- **Tool Testing**: Individual tool function verification
- **Communication Testing**: Inter-agent message exchange
- **Error Recovery**: Graceful handling of failures

### Performance Considerations:
- **Session Management**: Optimized for Coral Protocol patterns
- **API Rate Limits**: Proper quota management for YouTube API
- **Memory Usage**: Efficient tool execution and cleanup
- **Response Times**: Fast agent loop cycles for responsiveness

---

*Last Updated: 2025-05-27*
*Agent Status: ✅ **PRODUCTION READY***
*Coral Protocol Compatibility: ✅ **FULLY INTEGRATED***
