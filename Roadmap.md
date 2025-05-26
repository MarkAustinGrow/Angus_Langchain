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

### Phase 1: LangChain Tool Conversion ✅ COMPLETE
Convert existing Agent Angus functionality into discrete LangChain tools:

#### 🎬 YouTube Tools (`tools/youtube_tools.py`) ✅
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

#### 🗄️ Supabase Tools (`tools/supabase_tools.py`) ✅
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

#### 🤖 AI Analysis Tools (`tools/ai_tools.py`) ✅
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

### Phase 2: MCP Infrastructure ✅ COMPLETE

#### 🌐 MCP Client Integration (`coral_integration/mcp_client.py`) ✅
```python
class AngusMultiServerMCPClient:
    """Multi-server MCP client for Agent Angus following Coral Protocol pattern."""
    
    async def initialize(self):
        """Initialize MCP client connections."""
        
    async def execute_task(self, task: str) -> str:
        """Execute a task using the agent."""
```

#### 📡 MCP Server (`tools/mcp_server.py`) ✅
```python
class AngusToolsMCPServer:
    """MCP Server for Agent Angus tools."""
    
    def _register_tools(self):
        """Register all Agent Angus tools with the MCP server."""
```

### Phase 2.5: Standalone LangChain Agent Angus 🚧 IN PROGRESS

**Goal**: Create a working LangChain version of Agent Angus that replicates all original functionality using the LangChain framework, before adding multi-agent complexity.

#### 📋 Implementation Plan

##### **Step 1: Integrate Original Agent Angus Code**
- **Reference Path**: `E:\Plank pushers\Angus\angus.py`
- **Approach**: Reference original code from current location (no copying)
- **Focus**: Update tool imports to use original Supabase/YouTube clients

**Tool Integration Pattern**:
```python
# In tools/supabase_tools.py
import sys
sys.path.append('E:/Plank pushers/Angus')
from supabase_client import get_supabase_client  # Original client

# In tools/youtube_tools.py  
from youtube_client import get_youtube_client  # Original client
```

##### **Step 2: Create Unified LangChain Agent**
- **File**: `agents/angus_langchain_agent.py`
- **Architecture**: Single agent with all 16 tools
- **Capabilities**: Both workflows running simultaneously

**Agent Structure**:
```python
class AngusLangChainAgent:
    """Unified LangChain agent replicating original Agent Angus functionality."""
    
    def __init__(self):
        self.tools = [
            # YouTube tools (5)
            upload_song_to_youtube, fetch_youtube_comments, reply_to_youtube_comment,
            check_upload_quota, get_video_details,
            
            # Database tools (7) 
            get_pending_songs, store_feedback, update_song_status,
            get_song_details, get_uploaded_videos, get_existing_feedback, log_agent_activity,
            
            # AI tools (6)
            analyze_music_content, generate_comment_response, extract_music_metadata,
            analyze_comment_sentiment, generate_song_description, suggest_video_tags
        ]
        
    async def run_song_upload_workflow(self, limit: int = 5):
        """Execute complete song upload workflow."""
        # 1. Get pending songs from database
        # 2. For each song: analyze content, generate metadata
        # 3. Upload to YouTube with generated title/description/tags
        # 4. Update database with upload status and video ID
        
    async def run_comment_processing_workflow(self, max_replies: int = 10):
        """Execute complete comment processing workflow."""
        # 1. Get uploaded videos from database
        # 2. Fetch new comments from YouTube
        # 3. Analyze sentiment and generate appropriate responses
        # 4. Reply to comments on YouTube
        # 5. Store feedback data in database
        
    async def main_loop(self):
        """Main execution loop running both workflows."""
        # Run both workflows simultaneously with proper scheduling
```

##### **Step 3: Create Main LangChain Entry Point**
- **File**: `angus_langchain.py`
- **Purpose**: LangChain equivalent of original `angus.py`
- **Features**: Scheduling, continuous operation, error handling

**Main Entry Point**:
```python
# angus_langchain.py
class AngusLangChainSystem:
    """Main system controller for LangChain Agent Angus."""
    
    def __init__(self):
        self.agent = AngusLangChainAgent()
        
    async def start_system(self):
        """Start the complete Agent Angus LangChain system."""
        # Initialize agent with all tools
        # Start main workflow loop
        # Handle scheduling and error recovery
        
    async def run_workflows(self):
        """Execute both workflows with proper timing."""
        # Song upload workflow: every 1 hour
        # Comment processing: every 30 minutes
        # Continuous monitoring and execution
```

##### **Step 4: Live Integration & Testing**
- **Target**: Live YouTube channel and Supabase instance
- **Validation**: Compare results with original Agent Angus
- **Metrics**: Upload success rate, comment response quality, data consistency

#### 🎯 Success Criteria

1. **✅ Tool Integration**: All tools work with live Supabase/YouTube data
2. **✅ Workflow Parity**: Both workflows replicate original Angus behavior exactly
3. **✅ Data Consistency**: Same results and data patterns as original Agent Angus
4. **✅ LangChain Architecture**: Proper use of LangChain agents, tools, and execution patterns
5. **✅ Live Operation**: Successfully operates on live YouTube channel without issues
6. **✅ Performance**: Matches or exceeds original Agent Angus performance

#### 🔧 Technical Architecture

**Unified Agent Structure**:
```python
# Single powerful agent with all capabilities
agent = create_tool_calling_agent(
    model=ChatOpenAI(model="gpt-4o"),
    tools=all_16_angus_tools,
    prompt=angus_system_prompt
)

executor = AgentExecutor(
    agent=agent,
    tools=all_16_angus_tools,
    verbose=True,
    handle_parsing_errors=True
)
```

**Workflow Implementation**:
```python
# Both workflows running simultaneously
async def main_agent_loop():
    while True:
        # Song upload workflow (every hour)
        if should_run_upload_workflow():
            await run_song_upload_workflow()
            
        # Comment processing workflow (every 30 minutes)  
        if should_run_comment_workflow():
            await run_comment_processing_workflow()
            
        await asyncio.sleep(60)  # Check every minute
```

### Phase 3: Multi-Agent Implementation 📋 PLANNED

Transform the unified agent into specialized agents communicating via Coral Protocol.

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

### Phase 4: Enhanced Coral Protocol Features 📋 PLANNED

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
│   ├── __init__.py ✅
│   ├── angus_langchain_agent.py      # 🚧 Phase 2.5 - Unified LangChain agent
│   ├── coordinator_agent.py ✅       # 📋 Phase 3 - Main Angus orchestrator
│   ├── youtube_agent.py ✅           # 📋 Phase 3 - YouTube operations specialist
│   ├── database_agent.py ✅          # 📋 Phase 3 - Supabase operations specialist
│   └── ai_agent.py ✅               # 📋 Phase 3 - OpenAI operations specialist
├── tools/
│   ├── __init__.py ✅
│   ├── youtube_tools.py ✅           # YouTube LangChain tools
│   ├── supabase_tools.py ✅          # Database LangChain tools
│   ├── ai_tools.py ✅              # AI analysis tools
│   └── mcp_server.py ✅             # MCP server exposing all tools
├── coral_integration/
│   ├── __init__.py ✅
│   ├── mcp_client.py ✅             # MCP client integration
│   ├── server_setup.py ✅           # Coral server configuration
│   ├── agent_registry.py 📋         # 📋 Phase 3 - Agent registration logic
│   └── message_handlers.py 📋       # 📋 Phase 3 - Inter-agent communication
├── config/
│   ├── __init__.py ✅
│   ├── coral_config.py ✅           # Coral-specific settings
│   ├── agent_config.py ✅          # Agent configurations
│   └── environment.py ✅           # Environment variables
├── utils/
│   ├── __init__.py ✅
│   ├── logging_setup.py 📋          # Enhanced logging
│   └── monitoring.py 📋            # Agent monitoring utilities
├── tests/
│   ├── test_agents.py 📋            # Agent unit tests
│   ├── test_tools.py 📋            # Tool unit tests
│   └── test_integration.py 📋      # Integration tests
├── angus_langchain.py 🚧            # 🚧 Phase 2.5 - Main LangChain entry point
├── requirements.txt ✅              # Dependencies
├── docker-compose.yml 📋           # Container orchestration
├── .env.example ✅                 # Environment template
├── README.md ✅                    # Setup instructions
└── main.py ✅                      # Entry point
```

**Legend**: ✅ Complete | 🚧 In Progress | 📋 Planned

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
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

### 3. Phase 2.5: Run Standalone LangChain Agent
```bash
# Run the unified LangChain Agent Angus
python angus_langchain.py

# Or test individual components
python main.py --validate-config
python main.py --agent database
```

### 4. Phase 3: Start Multi-Agent System
```bash
# Start the Coral Protocol server
python -m coral_integration.server_setup

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

### Phase 2.5: Standalone Agent Testing
```bash
# Test unified LangChain agent
python angus_langchain.py --test-mode

# Test individual workflows
python -c "
from agents.angus_langchain_agent import AngusLangChainAgent
agent = AngusLangChainAgent()
await agent.run_song_upload_workflow(limit=1)
"

# Test tool integration
python main.py --validate-tools
```

### Phase 3: Multi-Agent Communication Tests
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
1. **✅ Phase 1**: Convert existing functions to LangChain tools
2. **✅ Phase 2**: Set up MCP infrastructure and basic integration
3. **🚧 Phase 2.5**: Create unified LangChain agent replicating original behavior
4. **📋 Phase 3**: Migrate to multi-agent orchestration
5. **📋 Phase 4**: Add enhanced Coral Protocol features

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

**Current Status**: Phase 2.5 In Progress - Standalone LangChain Agent Implementation
**Next Step**: Integrate original Agent Angus code and create unified LangChain agent
**Timeline**: 
- Phase 2.5: 1-2 weeks
- Phase 3: 2-3 weeks  
- Phase 4: 2-3 weeks
**Priority**: High - Get LangChain Agent Angus working before multi-agent complexity
