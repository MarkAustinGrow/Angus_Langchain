# 🧠 Agent Angus LangChain + Coral Protocol Integration Roadmap

## Goal
Rebuild Agent Angus as a multi-agent LangChain system integrated with Coral Protocol that:

- Upload songs from Supabase to YouTube
- Fetch YouTube comments
- Respond to comments using OpenAI
- Analyze music
- Store/update results in Supabase
- **NEW**: Leverage Coral Protocol for distributed agent communication and scalability

## 🏗️ Architecture Overview

### Current Agent Angus Analysis
The original Agent Angus is a monolithic system with these core components:
- **AgentAngus class** - Main orchestrator with scheduled tasks
- **YouTubeClient** - Handles video uploads and comment management  
- **SupabaseClient** - Database operations for songs, feedback, and logs
- **OpenAI utilities** - Music analysis and comment response generation

### New Multi-Agent Architecture
Transform into a distributed system using Coral Protocol:

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

## 📋 Implementation Phases

### Phase 1: LangChain Tool Conversion
Convert existing Agent Angus functionality into discrete LangChain tools:

#### 🎬 YouTube Tools (`tools/youtube_tools.py`)
```python
@tool
def upload_song_to_youtube(song_id: str, video_url: str, title: str, description: str, tags: list) -> str:
    """Upload a single song to YouTube and return video ID."""

@tool  
def fetch_youtube_comments(video_id: str, max_results: int = 100) -> list:
    """Fetch comments for a YouTube video."""

@tool
def reply_to_youtube_comment(comment_id: str, reply_text: str) -> str:
    """Reply to a specific YouTube comment."""

@tool
def check_upload_quota() -> dict:
    """Check YouTube API quota status."""
```

#### 🗄️ Supabase Tools (`tools/supabase_tools.py`)
```python
@tool
def get_pending_songs(limit: int = 10) -> list:
    """Get songs ready for YouTube upload."""

@tool
def store_feedback(song_id: str, comment_data: dict) -> str:
    """Store YouTube comment feedback in database."""

@tool
def update_song_status(song_id: str, status: str, youtube_id: str = None) -> bool:
    """Update song upload status."""

@tool
def get_song_details(song_id: str) -> dict:
    """Retrieve detailed song information."""
```

#### 🤖 AI Analysis Tools (`tools/ai_tools.py`)
```python
@tool
def analyze_music_content(input_source: str, is_youtube_url: bool = False) -> dict:
    """Analyze music using OpenAI for themes, genres, moods."""

@tool
def generate_comment_response(comment_text: str, song_title: str, song_style: str = None) -> str:
    """Generate AI-powered response to YouTube comments."""

@tool
def extract_music_metadata(audio_url: str) -> dict:
    """Extract metadata from audio files."""
```

### Phase 2: Coral Server Integration

#### 🌐 Server Setup (`coral_integration/server_setup.py`)
```python
class CoralServerManager:
    """Manages Coral Protocol server setup and configuration."""
    
    def start_server(self, port: int = 5555):
        """Start the Coral Protocol server."""
        
    def register_agents(self):
        """Register all Angus agents with the server."""
        
    def setup_message_routing(self):
        """Configure inter-agent communication routes."""
```

#### 📝 Agent Registry (`coral_integration/agent_registry.py`)
```python
class AgentRegistry:
    """Handles agent registration and discovery."""
    
    def register_coordinator_agent(self):
        """Register main Angus coordinator agent."""
        
    def register_specialized_agents(self):
        """Register YouTube, Database, and AI agents."""
```

### Phase 3: Multi-Agent Implementation

#### 🎯 Coordinator Agent (`agents/coordinator_agent.py`)
```python
class AngusCoordinatorAgent:
    """Main orchestrator agent that coordinates all Angus operations."""
    
    def __init__(self):
        self.youtube_agent = "youtube_agent"
        self.database_agent = "database_agent" 
        self.ai_agent = "ai_agent"
        
    def upload_pending_songs_workflow(self, limit: int = 5):
        """Orchestrate the complete song upload workflow."""
        
    def process_comments_workflow(self, max_replies: int = 10):
        """Orchestrate comment fetching and response workflow."""
        
    def schedule_tasks(self):
        """Set up scheduled task execution."""
```

#### 🎬 YouTube Agent (`agents/youtube_agent.py`)
```python
class YouTubeAgent:
    """Specialized agent for all YouTube operations."""
    
    def __init__(self):
        self.youtube_client = YouTubeClient()
        self.tools = [upload_song_to_youtube, fetch_youtube_comments, reply_to_youtube_comment]
        
    def handle_upload_request(self, message):
        """Handle song upload requests from coordinator."""
        
    def handle_comment_request(self, message):
        """Handle comment fetching requests."""
```

#### 🗄️ Database Agent (`agents/database_agent.py`)
```python
class DatabaseAgent:
    """Specialized agent for all Supabase database operations."""
    
    def __init__(self):
        self.supabase_client = SupabaseClient()
        self.tools = [get_pending_songs, store_feedback, update_song_status]
        
    def handle_data_request(self, message):
        """Handle database operation requests."""
```

#### 🤖 AI Agent (`agents/ai_agent.py`)
```python
class AIAgent:
    """Specialized agent for OpenAI operations and analysis."""
    
    def __init__(self):
        self.openai_client = OpenAI()
        self.tools = [analyze_music_content, generate_comment_response]
        
    def handle_analysis_request(self, message):
        """Handle music analysis requests."""
        
    def handle_response_generation(self, message):
        """Handle comment response generation."""
```

### Phase 4: Enhanced Coral Protocol Features

#### 🔄 Distributed Processing
- **Parallel Operations**: Multiple YouTube agents for concurrent uploads
- **Load Balancing**: Distribute comment processing across AI agents
- **Fault Tolerance**: Agent failure recovery and redundancy

#### 📡 Advanced Communication
- **Message Queuing**: Asynchronous task processing
- **Event Broadcasting**: Real-time status updates across agents
- **Priority Handling**: Critical tasks get priority routing

#### 📊 Monitoring & Analytics
- **Agent Health Monitoring**: Track agent performance and availability
- **Workflow Analytics**: Measure end-to-end process efficiency
- **Resource Usage**: Monitor API quotas and system resources

## 🗂️ Project Structure

```
angus_langchain/
├── agents/
│   ├── __init__.py
│   ├── coordinator_agent.py      # Main Angus orchestrator
│   ├── youtube_agent.py          # YouTube operations specialist
│   ├── database_agent.py         # Supabase operations specialist
│   └── ai_agent.py              # OpenAI operations specialist
├── tools/
│   ├── __init__.py
│   ├── youtube_tools.py          # YouTube LangChain tools
│   ├── supabase_tools.py         # Database LangChain tools
│   └── ai_tools.py              # AI analysis tools
├── coral_integration/
│   ├── __init__.py
│   ├── server_setup.py           # Coral server configuration
│   ├── agent_registry.py        # Agent registration logic
│   └── message_handlers.py      # Inter-agent communication
├── config/
│   ├── __init__.py
│   ├── coral_config.py           # Coral-specific settings
│   ├── agent_config.py          # Agent configurations
│   └── environment.py           # Environment variables
├── utils/
│   ├── __init__.py
│   ├── logging_setup.py          # Enhanced logging
│   └── monitoring.py            # Agent monitoring utilities
├── tests/
│   ├── test_agents.py            # Agent unit tests
│   ├── test_tools.py            # Tool unit tests
│   └── test_integration.py      # Integration tests
├── requirements.txt              # Dependencies
├── docker-compose.yml           # Container orchestration
├── .env.example                 # Environment template
├── README.md                    # Setup instructions
└── main.py                      # Entry point
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install langchain langchain_mcp_adapters coral-server openai supabase worldnewsapi
```

### 2. Configure Environment
```bash
# Copy and configure environment variables
cp .env.example .env

# Required variables:
OPENAI_API_KEY=your-openai-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
YOUTUBE_CLIENT_ID=your-youtube-client-id
YOUTUBE_CLIENT_SECRET=your-youtube-client-secret
YOUTUBE_CHANNEL_ID=your-channel-id
CORAL_SERVER_PORT=5555
```

### 3. Start Coral Server
```bash
# Start the Coral Protocol server
python -m coral_integration.server_setup
```

### 4. Launch Agents
```bash
# In separate terminals, start each agent:
python agents/coordinator_agent.py
python agents/youtube_agent.py  
python agents/database_agent.py
python agents/ai_agent.py
```

### 5. Test the System
```bash
# Run integration tests
python -m pytest tests/test_integration.py

# Monitor agent communication
python utils/monitoring.py
```

## 🎯 Key Benefits

### 🔧 Technical Advantages
- **Modularity**: Each function is a discrete, testable tool
- **Scalability**: Multiple agents handle different aspects independently
- **Reliability**: Agent failures don't crash the entire system
- **Maintainability**: Clear separation of concerns

### 🌐 Coral Protocol Benefits
- **Distributed Processing**: Leverage multiple machines/containers
- **Load Balancing**: Automatic workload distribution
- **Fault Tolerance**: Built-in redundancy and recovery
- **Real-time Communication**: Efficient inter-agent messaging

### 📈 Operational Improvements
- **Performance**: Parallel processing of uploads and comments
- **Monitoring**: Enhanced visibility into system operations
- **Extensibility**: Easy to add new agents and capabilities
- **Resource Management**: Better API quota and resource utilization

## 🧪 Testing Scenarios

### Basic Workflow Tests
```bash
# Test song upload workflow
curl -X POST http://localhost:5555/coordinator/upload_songs -d '{"limit": 3}'

# Test comment processing workflow  
curl -X POST http://localhost:5555/coordinator/process_comments -d '{"max_replies": 5}'

# Test music analysis
curl -X POST http://localhost:5555/ai/analyze_music -d '{"url": "https://youtube.com/watch?v=abc123"}'
```

### Multi-Agent Communication Tests
```bash
# Test agent discovery
python tests/test_agent_discovery.py

# Test message routing
python tests/test_message_routing.py

# Test fault tolerance
python tests/test_fault_tolerance.py
```

## 📋 Migration Strategy

### From Original Agent Angus
1. **Phase 1**: Convert existing functions to LangChain tools
2. **Phase 2**: Set up Coral server and basic agent communication
3. **Phase 3**: Migrate workflows to multi-agent orchestration
4. **Phase 4**: Add enhanced Coral Protocol features

### Data Migration
- Existing Supabase data remains unchanged
- YouTube authentication tokens can be reused
- Configuration migrates to new environment structure

### Rollback Plan
- Keep original Agent Angus as backup
- Gradual migration with parallel running
- Easy rollback to monolithic system if needed

## 🔮 Future Enhancements

### Advanced Features
- **Machine Learning**: Predictive analytics for optimal upload timing
- **Multi-Platform**: Extend to other social media platforms
- **Advanced AI**: More sophisticated music analysis and response generation
- **API Gateway**: External API for third-party integrations

### Coral Protocol Extensions
- **Cross-Network Agents**: Agents running on different networks
- **Blockchain Integration**: Decentralized agent coordination
- **Smart Contracts**: Automated workflow execution
- **Federation**: Connect with other Coral Protocol networks

---

**Status**: Ready for implementation
**Next Step**: Begin Phase 1 - LangChain Tool Conversion
**Timeline**: 4-6 weeks for full implementation
**Priority**: High - Enables scalable, distributed music publishing automation
