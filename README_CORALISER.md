# 🌊 Agent Angus - Coraliser Integration

Agent Angus is now fully compatible with the Coral Protocol ecosystem through proper Coraliser integration. This implementation follows the official LangChain WorldNews example pattern from the Coral Protocol repository.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Coraliser Network                        │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────┐  │
│  │ Other Agents    │ │ Coral Server    │ │ Shared Tools  │  │
│  └─────────────────┘ └─────────────────┘ └───────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │ MCP Protocol
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                Agent Angus (angus_music_agent)              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Coral Protocol Integration                 │ │
│  │  • wait_for_mentions  • send_message                   │ │
│  │  • Inter-agent communication                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Specialized Music Tools                    │ │
│  │  • AngusYouTubeUploadTool                              │ │
│  │  • AngusCommentProcessingTool                          │ │
│  │  • AngusQuotaCheckTool                                 │ │
│  └─────────────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Core Agent Angus Tools                     │ │
│  │  • YouTube Tools (6)  • Database Tools (7)            │ │
│  │  • AI Tools (6)                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Coraliser Files

### **Core Files:**
- `0_langchain_interface.py` - Coraliser interface configuration
- `1_langchain_angus_agent.py` - Main Coraliser-compatible agent
- `README_CORALISER.md` - This documentation

### **Supporting Files:**
- `tools/` - All Agent Angus specialized tools
- `config/` - Configuration and environment management
- `.env` - Environment variables (create from `.env.example`)

## 🚀 Quick Start

### **1. Prerequisites**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### **2. Verify Configuration**
```bash
# Check agent interface
python 0_langchain_interface.py

# Expected output:
# 🎵 Agent Angus - Coraliser Interface
# ==========================================
# {
#   "name": "angus_music_agent",
#   "description": "Agent Angus - Music Publishing Automation Specialist",
#   ...
# }
```

### **3. Start Agent Angus in Coraliser Mode**
```bash
# Start the Coraliser-compatible agent
python 1_langchain_angus_agent.py

# Expected behavior:
# - Connects to Coral Protocol server
# - Registers as "angus_music_agent"
# - Waits for mentions from other agents
# - Provides music automation services
```

## 🔧 Configuration

### **Environment Variables**
Required in `.env` file:
```env
# OpenAI (for AI tools)
OPENAI_API_KEY=your-openai-api-key

# Supabase (for database)
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# YouTube API
YOUTUBE_CLIENT_ID=your-youtube-client-id
YOUTUBE_CLIENT_SECRET=your-youtube-client-secret
YOUTUBE_API_KEY=your-youtube-api-key
YOUTUBE_CHANNEL_ID=your-youtube-channel-id
```

### **Coral Protocol Settings**
```python
# Default configuration in 1_langchain_angus_agent.py
MCP_SERVER_URL = "http://localhost:5555/devmode/exampleApplication/privkey/session1/sse"
AGENT_NAME = "angus_music_agent"
```

## 🎵 Agent Capabilities

### **Specialized Tools:**

#### **1. AngusYouTubeUploadTool**
```python
# Upload songs with AI-generated metadata
{
    "song_limit": 5,                    # Max songs to upload
    "auto_generate_metadata": True      # Auto-generate titles/descriptions
}
```

#### **2. AngusCommentProcessingTool**
```python
# Process YouTube comments with AI responses
{
    "comment_limit": 10,                # Max comments to process
    "auto_reply": True                  # Auto-reply to comments
}
```

#### **3. AngusQuotaCheckTool**
```python
# Check YouTube API quota status
# No parameters required
```

### **Core Capabilities:**
- **YouTube Automation**: Upload videos, manage comments, check quotas
- **Music Analysis**: AI-powered content analysis and metadata generation
- **Database Management**: Song tracking, feedback storage, status updates
- **AI Content Creation**: Descriptions, tags, comment responses
- **Sentiment Analysis**: Comment sentiment analysis and appropriate responses

## 🌊 Coral Protocol Integration

### **Inter-Agent Communication:**
Agent Angus follows the official Coral Protocol pattern:

1. **Wait for Mentions**: Uses `wait_for_mentions` to receive requests from other agents
2. **Process Requests**: Handles music-related requests using specialized tools
3. **Send Responses**: Uses `send_message` to respond back with thread ID
4. **Continuous Loop**: Maintains 24/7 availability for agent collaboration

### **Collaboration Features:**
- **Service Provider**: Offers music automation services to other agents
- **Tool Sharing**: Shares specialized music tools with the network
- **Workflow Coordination**: Participates in distributed music workflows
- **Status Reporting**: Provides detailed status updates on operations

## 🔄 Usage Examples

### **Direct Agent Interaction:**
```bash
# Other agents can mention Agent Angus for:
# - "Upload 5 songs to YouTube"
# - "Process comments for recent videos"
# - "Check YouTube quota status"
# - "Analyze music content for metadata"
# - "Generate descriptions for uploaded songs"
```

### **Collaborative Workflows:**
```bash
# Example multi-agent workflow:
# 1. Content Agent creates music content
# 2. Agent Angus uploads to YouTube
# 3. Marketing Agent promotes the content
# 4. Agent Angus processes resulting comments
# 5. Analytics Agent analyzes performance
```

## 🐛 Troubleshooting

### **Common Issues:**

#### **1. MCP Connection Errors**
```bash
# Check Coral server is running
curl http://localhost:5555/health

# Verify MCP dependencies
pip install langchain-mcp-adapters>=0.1.0
```

#### **2. Environment Configuration**
```bash
# Validate environment
python 0_langchain_interface.py

# Check for missing variables
python -c "from 0_langchain_interface import validate_environment; print(validate_environment())"
```

#### **3. Tool Import Errors**
```bash
# Verify Agent Angus tools are available
python -c "from tools.youtube_tools import upload_song_to_youtube; print('YouTube tools OK')"
python -c "from tools.supabase_tools import get_pending_songs; print('Database tools OK')"
python -c "from tools.ai_tools import analyze_music_content; print('AI tools OK')"
```

### **Debug Mode:**
```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG

# Run with detailed output
python 1_langchain_angus_agent.py
```

## 📊 Monitoring

### **Agent Status:**
```bash
# Check agent health
python 0_langchain_interface.py

# Monitor agent logs
tail -f agent_angus.log
```

### **Performance Metrics:**
- **Response Time**: Time to process agent mentions
- **Tool Success Rate**: Success rate of music operations
- **Collaboration Count**: Number of inter-agent interactions
- **Service Availability**: Uptime and availability metrics

## 🔗 Integration with Existing Systems

### **Backward Compatibility:**
- **OpenAI Wrapper**: Still available via `angus_openai_wrapper.py`
- **Standalone Mode**: Original functionality via `angus_langchain.py`
- **Coral Client**: Previous implementation via `agents/angus_coral_client.py`

### **Migration Path:**
1. **Current**: OpenAI-compatible wrapper for basic integration
2. **Enhanced**: Coraliser integration for full Coral Protocol features
3. **Future**: Advanced multi-agent workflows and collaboration

## 🎯 Production Deployment

### **Docker Deployment:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5555

CMD ["python", "1_langchain_angus_agent.py"]
```

### **Systemd Service:**
```ini
[Unit]
Description=Agent Angus Coraliser Integration
After=network.target

[Service]
Type=simple
User=angus
WorkingDirectory=/opt/Angus_Langchain
ExecStart=/usr/bin/python3 1_langchain_angus_agent.py
Restart=always
Environment=LOG_LEVEL=INFO

[Install]
WantedBy=multi-user.target
```

## 📞 Support

- **Coral Protocol**: [Official Documentation](https://coral.pushcollective.club)
- **LangChain MCP**: [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
- **Agent Angus**: Check main `README.md` for core functionality

---

**🎉 Status**: Coraliser Integration Complete!
**🌊 Protocol**: Full Coral Protocol compatibility
**🎵 Capabilities**: Music automation specialist ready for agent collaboration
**🔗 Network**: Connected to distributed AI ecosystem
