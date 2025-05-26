# 🎵 Agent Angus + Coral Protocol Client

A sophisticated AI agent that connects to the Coral Protocol network for distributed music publishing automation on YouTube.

## 🌟 Features

- **Automated Song Upload**: Upload songs from Supabase to YouTube with AI-generated metadata
- **Intelligent Comment Processing**: Fetch and respond to YouTube comments using OpenAI
- **Music Analysis**: AI-powered analysis of musical content for themes, genres, and moods
- **Coral Protocol Integration**: Connect to the Coral network to collaborate with other AI agents
- **Real-time Monitoring**: Track system performance and agent health
- **Robust Error Handling**: Graceful handling of API limits and network issues

## 🏗️ Architecture

### Standalone LangChain Agent ✅ COMPLETE
A unified LangChain agent that replicates all original Agent Angus functionality:

```
┌─────────────────────────────────────────────────────────────┐
│                 Unified LangChain Agent                     │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ YouTube     │ │ Database    │ │ AI Tools                │ │
│  │ Tools (6)   │ │ Tools (7)   │ │ (6)                     │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ OpenAI GPT-4o   │
                    │ Agent Executor  │
                    └─────────────────┘
```

### Coral Protocol Client ✅ COMPLETE
Agent Angus as a client connected to the Coral Protocol network:

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Angus                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ YouTube     │ │ Database    │ │ AI Tools                │ │
│  │ Tools (6)   │ │ Tools (7)   │ │ (6)                     │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Workflow Tools (2)                        │ │
│  │  • upload_workflow • comment_processing_workflow       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ OpenAI GPT-4o   │
                    │ Agent Executor  │
                    └─────────────────┘
                              │
                              ▼
              🌊 Coral Protocol Network 🌊
         ┌─────────────────────────────────────┐
         │    https://coral.pushcollective.club │
         │                                     │
         │  ┌─────────────┐ ┌─────────────────┐ │
         │  │ Other AI    │ │ Network Tools   │ │
         │  │ Agents      │ │ & Resources     │ │
         │  └─────────────┘ └─────────────────┘ │
         └─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Supabase account and credentials
- YouTube API credentials
- Internet connection to Coral Protocol network

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Angus_Langchain.git
   cd Angus_Langchain
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Set up YouTube authentication**
   ```bash
   python youtube_auth_langchain.py
   ```

### Running Agent Angus

#### Option A: Standalone LangChain Agent

```bash
# Run the unified LangChain agent
python angus_langchain.py

# Test specific workflows
python angus_langchain.py --upload --upload-limit 5
python angus_langchain.py --comments --reply-limit 10
python angus_langchain.py --both --upload-limit 3 --reply-limit 5
```

#### Option B: Coral Protocol Client 🌊 NEW!

```bash
# Connect Agent Angus to the Coral Protocol network
python agents/angus_coral_client.py
```

**Interactive Commands:**
```
Agent Angus> upload 5          # Upload 5 songs
Agent Angus> comments 10       # Process 10 comments
Agent Angus> analyze "pop song about summer"
Agent Angus> quota             # Check YouTube quota
Agent Angus> pending           # Show pending songs
Agent Angus> status            # Show network status
Agent Angus> help              # Show all commands
Agent Angus> quit              # Disconnect
```

## 📁 Project Structure

```
angus_langchain/
├── agents/                          # Agent implementations
│   ├── angus_langchain_agent.py    # Unified LangChain agent
│   └── angus_coral_client.py       # Coral Protocol client ⭐ NEW
├── tools/                          # LangChain tools
│   ├── youtube_tools.py           # YouTube operations
│   ├── supabase_tools.py          # Database operations
│   └── ai_tools.py                # AI operations
├── config/                         # Configuration
│   ├── environment.py             # Environment variables
│   ├── agent_config.py            # Agent configurations
│   └── coral_config.py            # Coral Protocol settings
├── coral_integration/              # Coral Protocol integration
├── tests/                          # Test suite
├── angus_langchain.py             # Main entry point (standalone)
└── requirements.txt               # Dependencies
```

## 🔧 Available Tools

### YouTube Tools
- `upload_song_to_youtube` - Upload videos to YouTube
- `fetch_youtube_comments` - Get comments from videos
- `reply_to_youtube_comment` - Post replies to comments
- `check_upload_quota` - Monitor API quota usage
- `get_video_details` - Retrieve video information
- `process_video_comments` - Complete comment processing workflow

### Database Tools  
- `get_pending_songs` - Find songs ready for upload
- `store_feedback` - Save comment data
- `update_song_status` - Track upload progress
- `get_song_details` - Retrieve song information
- `get_uploaded_videos` - List uploaded content
- `log_agent_activity` - System logging
- `get_existing_feedback` - Check for duplicate processing

### AI Tools
- `analyze_music_content` - OpenAI music analysis
- `generate_comment_response` - AI comment replies
- `analyze_comment_sentiment` - Sentiment analysis
- `generate_song_description` - Auto-generate descriptions
- `suggest_video_tags` - Recommend tags
- `extract_music_metadata` - Audio metadata extraction

### Workflow Tools (Coral Client Only)
- `upload_workflow` - Complete song upload process
- `comment_processing_workflow` - Complete comment processing

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Supabase Configuration
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key

# YouTube API Configuration
YOUTUBE_CLIENT_ID=your-youtube-client-id
YOUTUBE_CLIENT_SECRET=your-youtube-client-secret
YOUTUBE_API_KEY=your-youtube-api-key
YOUTUBE_CHANNEL_ID=your-youtube-channel-id

# Coral Protocol Configuration (Optional - defaults to coral.pushcollective.club)
CORAL_SERVER_URL=https://coral.pushcollective.club
CORAL_SERVER_HOST=coral.pushcollective.club
CORAL_SERVER_PORT=443
```

## 📋 Usage Examples

### Standalone Agent Commands

```bash
# Upload songs with limit
python angus_langchain.py --upload --upload-limit 5

# Process comments with limit  
python angus_langchain.py --comments --reply-limit 10

# Run both workflows
python angus_langchain.py --both --upload-limit 3 --reply-limit 5
```

### Coral Protocol Client Commands

```bash
# Start the Coral client
python agents/angus_coral_client.py

# In the interactive session:
Agent Angus> upload 5          # Upload 5 songs
Agent Angus> comments 10       # Process 10 comments  
Agent Angus> analyze "upbeat electronic music"
Agent Angus> pending           # Show pending songs
Agent Angus> videos            # Show uploaded videos
Agent Angus> status            # Network connection status
```

## 🔄 Workflows

### Song Upload Workflow
1. Get pending songs from database
2. Analyze music content with AI
3. Upload videos to YouTube with generated metadata
4. Update song status in database

### Comment Processing Workflow
1. Get uploaded videos from database
2. Fetch comments from YouTube
3. Analyze comment sentiment with AI
4. Generate appropriate responses
5. Post replies to YouTube
6. Store feedback in database

## 🌊 Coral Protocol Integration

### Network Benefits
- **Collaboration**: Work with other AI agents on the Coral network
- **Resource Sharing**: Access tools and capabilities from other agents
- **Scalability**: Distribute workload across multiple agents
- **Resilience**: Fallback options when services are unavailable

### Agent Capabilities Shared
- Music analysis and content generation
- YouTube automation expertise
- Database management for music data
- AI-powered comment processing

### Network Communication
- **Agent ID**: `agent_angus`
- **Server**: `https://coral.pushcollective.club`
- **Protocol**: Server-Sent Events (SSE) over HTTPS
- **Tools Exposed**: 21 specialized music automation tools

## 🔍 Monitoring

### System Health

```bash
# Check standalone agent
python -c "from agents.angus_langchain_agent import AngusLangChainAgent; agent = AngusLangChainAgent(); print(agent.health_check())"

# Check Coral client connection (run from within the client)
Agent Angus> status
```

### Performance Metrics

- **Upload Success Rate**: Percentage of successful song uploads
- **Comment Response Rate**: Percentage of comments that receive responses
- **API Usage**: YouTube and OpenAI API quota consumption
- **Network Latency**: Response time to Coral Protocol network

## 🚨 Troubleshooting

### Common Issues

1. **Coral Protocol Connection Issues**
   ```bash
   # Check network connectivity
   curl https://coral.pushcollective.club
   
   # Verify environment configuration
   python config/environment.py
   ```

2. **YouTube Authentication Errors**
   ```bash
   # Re-run authentication
   python youtube_auth_langchain.py
   ```

3. **Supabase Connection Issues**
   ```bash
   # Check credentials and network
   python -c "from tools.supabase_tools import get_supabase_client; get_supabase_client()"
   ```

4. **OpenAI API Errors**
   ```bash
   # Verify API key and quota
   python -c "import openai; openai.api_key='your-key'; print(openai.Model.list())"
   ```

### Debug Mode

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
export DEBUG_MODE=true

# Run with debug output
python agents/angus_coral_client.py
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific components
pytest tests/test_tools.py
pytest tests/test_agents.py
pytest tests/test_coral_integration.py

# Run with coverage
pytest --cov=agents --cov=tools
```

## 🔧 Development

### Adding New Tools

1. Create tool function in appropriate `tools/` file:
   ```python
   @tool
   def my_new_tool(param: str) -> str:
       """Tool description."""
       # Implementation
       return result
   ```

2. Add to agent's tool list in `agents/angus_coral_client.py`

3. Update agent prompt to include tool description

### Coral Protocol Integration

The Coral client automatically:
- Connects to the network on startup
- Registers Agent Angus's capabilities
- Shares tools with other agents
- Handles network communication
- Provides fallback for network issues

## 📋 Implementation Status

### ✅ COMPLETE
- **Standalone LangChain Agent**: Full Agent Angus functionality
- **Coral Protocol Client**: Connected to coral.pushcollective.club
- **Tool Integration**: All 21 tools available on the network
- **Workflow Automation**: Complete upload and comment processing
- **Error Handling**: Robust retry logic and graceful failures
- **Interactive Interface**: User-friendly command system

### 🚀 Future Enhancements
- Advanced monitoring dashboard
- Performance optimization
- Additional workflow types
- Enhanced collaboration features
- Production deployment guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the agent framework
- [Coral Protocol](https://coral.pushcollective.club/) for the distributed AI network
- [OpenAI](https://openai.com/) for AI capabilities
- [Supabase](https://supabase.com/) for database services
- [YouTube API](https://developers.google.com/youtube) for video platform integration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/Angus_Langchain/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/Angus_Langchain/discussions)
- **Coral Network**: [coral.pushcollective.club](https://coral.pushcollective.club)

---

**🎉 Status**: Coral Protocol Client Integration Complete!
**🌊 Network**: Connected to coral.pushcollective.club
**🎵 Capabilities**: Music automation agent ready for collaboration
