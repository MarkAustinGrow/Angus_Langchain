# Agent Angus LangChain + Coral Protocol

A modern, distributed multi-agent system that rebuilds Agent Angus using LangChain tools and Coral Protocol for scalable music publishing automation.

## 🎯 Overview

This project transforms the original monolithic Agent Angus into a distributed multi-agent system that:

- **Uploads songs** from Supabase to YouTube
- **Fetches and processes** YouTube comments  
- **Generates AI responses** using OpenAI
- **Analyzes music content** for metadata and insights
- **Stores feedback** and tracks upload status
- **Scales horizontally** using Coral Protocol's distributed architecture

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Coordinator     │    │ YouTube Agent   │    │ Database Agent  │
│ Agent           │◄──►│                 │◄──►│                 │
│ (Main Angus)    │    │ - Upload videos │    │ - Supabase ops  │
└─────────────────┘    │ - Fetch comments│    │ - Store feedback│
         ▲              │ - Reply to comm.│    │ - Update status │
         │              └─────────────────┘    └─────────────────┘
         ▼                        ▲                       ▲
┌─────────────────┐              │                       │
│ AI Agent        │              │                       │
│                 │◄─────────────┴───────────────────────┘
│ - Music analysis│
│ - Comment resp. │              Coral Protocol Server
│ - OpenAI calls  │         ┌─────────────────────────────┐
└─────────────────┘         │ - Agent registration        │
                            │ - Message routing           │
                            │ - Load balancing            │
                            │ - Monitoring & logging      │
                            └─────────────────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Access to original Agent Angus codebase (for YouTube/Supabase clients)
- Required API keys (OpenAI, YouTube, Supabase)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd angus_langchain

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
```bash
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_CLIENT_ID=your_youtube_oauth_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_oauth_client_secret
YOUTUBE_CHANNEL_ID=your_youtube_channel_id
```

### 4. Validate Configuration

```bash
# Check environment setup
python main.py --validate-env

# Check all configurations
python main.py --validate-config

# Print environment summary
python main.py --print-env
```

### 5. Start the System

```bash
# Start complete system (all agents + Coral server)
python main.py --start

# Start specific agents only
python main.py --start --agents coordinator youtube database

# Start only Coral server
python main.py --server-only

# Run single agent for testing
python main.py --agent youtube
```

## 📁 Project Structure

```
angus_langchain/
├── agents/                    # Agent implementations
│   ├── coordinator_agent.py   # Main orchestrator
│   ├── youtube_agent.py       # YouTube operations
│   ├── database_agent.py      # Supabase operations
│   └── ai_agent.py            # OpenAI operations
├── tools/                     # LangChain tools
│   ├── youtube_tools.py       # YouTube LangChain tools
│   ├── supabase_tools.py      # Database LangChain tools
│   └── ai_tools.py            # AI analysis tools
├── coral_integration/         # Coral Protocol integration
│   ├── server_setup.py        # Server configuration
│   ├── agent_registry.py      # Agent registration
│   └── message_handlers.py    # Inter-agent communication
├── config/                    # Configuration modules
│   ├── environment.py         # Environment variables
│   ├── agent_config.py        # Agent configurations
│   └── coral_config.py        # Coral Protocol settings
├── utils/                     # Utility modules
├── tests/                     # Test suite
├── main.py                    # Main entry point
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔧 Available Tools

### YouTube Tools
- `upload_song_to_youtube` - Upload videos to YouTube
- `fetch_youtube_comments` - Get comments from videos
- `reply_to_youtube_comment` - Post replies to comments
- `check_upload_quota` - Monitor API quota usage
- `get_video_details` - Retrieve video information

### Database Tools  
- `get_pending_songs` - Find songs ready for upload
- `store_feedback` - Save comment data
- `update_song_status` - Track upload progress
- `get_song_details` - Retrieve song information
- `get_uploaded_videos` - List uploaded content
- `log_agent_activity` - System logging

### AI Tools
- `analyze_music_content` - OpenAI music analysis
- `generate_comment_response` - AI comment replies
- `analyze_comment_sentiment` - Sentiment analysis
- `generate_song_description` - Auto-generate descriptions
- `suggest_video_tags` - Recommend tags
- `extract_music_metadata` - Audio metadata extraction

## 🎮 Usage Examples

### Basic Operations

```bash
# Upload pending songs
python main.py --start --agents coordinator youtube database

# Process YouTube comments
python main.py --start --agents coordinator youtube ai database

# Analyze music content
python main.py --start --agents coordinator ai database
```

### Development & Testing

```bash
# Run in debug mode
python main.py --start --debug

# Test single agent
python main.py --agent youtube --verbose

# Validate setup
python main.py --validate-config
```

### Monitoring

```bash
# Check system status
curl http://localhost:5555/health

# View metrics
curl http://localhost:5555/metrics

# Agent-specific health
curl http://localhost:8000/health  # Coordinator
curl http://localhost:8001/health  # YouTube
curl http://localhost:8002/health  # Database  
curl http://localhost:8003/health  # AI
```

## 🔄 Workflows

### Song Upload Workflow
1. **Database Agent** retrieves pending songs
2. **AI Agent** generates descriptions and tags
3. **YouTube Agent** uploads videos
4. **Database Agent** updates status

### Comment Processing Workflow
1. **Database Agent** gets uploaded videos
2. **YouTube Agent** fetches comments
3. **AI Agent** analyzes sentiment and generates responses
4. **YouTube Agent** posts replies
5. **Database Agent** stores feedback

## ⚙️ Configuration

### Agent Configuration
Each agent can be configured in `config/agent_config.py`:

```python
YOUTUBE_AGENT_CONFIG = {
    "name": "angus_youtube",
    "timeout": 600,  # 10 minutes for uploads
    "rate_limits": {
        "uploads_per_day": 6,
        "api_calls_per_minute": 100
    }
}
```

### Coral Protocol Settings
Server and communication settings in `config/coral_config.py`:

```python
CORAL_SERVER_CONFIG = {
    "host": "localhost",
    "port": 5555,
    "max_connections": 100,
    "heartbeat_interval": 30
}
```

## 🔍 Monitoring & Debugging

### Logs
- System logs: `angus_langchain.log`
- Coral server logs: `coral_server.log`
- Agent-specific logs in Supabase `angus_logs` table

### Health Checks
- System health: `http://localhost:5555/health`
- Individual agents: `http://localhost:800X/health`

### Metrics
- Prometheus metrics: `http://localhost:5555/metrics`
- Custom metrics for workflows and performance

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific components
pytest tests/test_tools.py
pytest tests/test_agents.py
pytest tests/test_integration.py

# Test with coverage
pytest --cov=. --cov-report=html
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Scale specific agents
docker-compose up --scale youtube-agent=2 --scale ai-agent=3
```

### Production Considerations
- Set `AUTHENTICATION_ENABLED=true`
- Configure SSL certificates
- Set up proper monitoring and alerting
- Use Redis for message queuing
- Configure load balancing

## 🔧 Development

### Adding New Tools
1. Create tool function with `@tool` decorator
2. Add to appropriate tools module
3. Update agent configuration
4. Add tests

### Adding New Agents
1. Create agent class inheriting from base agent
2. Define tools and capabilities
3. Add to agent registry
4. Update main.py imports

### Extending Workflows
1. Define workflow in `config/agent_config.py`
2. Implement in coordinator agent
3. Add monitoring and error handling

## 📋 Migration from Original Agent Angus

### Phase 1: Tool Conversion ✅
- [x] YouTube tools implemented
- [x] Supabase tools implemented  
- [x] AI tools implemented
- [x] Configuration system
- [x] Main entry point

### Phase 2: Coral Integration (Next)
- [ ] Coral server setup
- [ ] Agent registry implementation
- [ ] Message routing system

### Phase 3: Multi-Agent Implementation (Planned)
- [ ] Coordinator agent
- [ ] Specialized agents
- [ ] Workflow orchestration

### Phase 4: Enhanced Features (Future)
- [ ] Advanced monitoring
- [ ] Load balancing
- [ ] Fault tolerance
- [ ] Performance optimization

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: GitHub Issues
- **Documentation**: See `/docs` directory
- **Examples**: See `/examples` directory

## 🔗 Related Projects

- [Original Agent Angus](../Angus) - Monolithic version
- [Coral Protocol](https://github.com/Coral-Protocol/coral-server) - Multi-agent framework
- [LangChain](https://github.com/langchain-ai/langchain) - LLM application framework

---

**Status**: Phase 1 Complete - Ready for Coral Protocol Integration
**Next Steps**: Implement Coral server setup and agent registry
**Timeline**: 4-6 weeks for full implementation
