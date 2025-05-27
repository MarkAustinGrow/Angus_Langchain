# 🔌 Agent Angus OpenAI-Compatible Wrapper

This guide explains how to use the OpenAI-compatible HTTP API wrapper for Agent Angus, which enables integration with Coraliser and other systems that expect OpenAI-style APIs.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Coraliser / External System              │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP POST /v1/chat/completions
                      │ (OpenAI-compatible format)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI OpenAI Wrapper (Port 8001)            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • /v1/chat/completions (OpenAI-compatible)             │ │
│  │ • /v1/models (List available models)                   │ │
│  │ • /health (Health check)                               │ │
│  │ • /v1/agent/status (Agent status)                      │ │
│  │ • /v1/agent/tools (List tools)                         │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────────────────┘
                      │ MCP Protocol (STDIO)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                Agent Angus MCP Client                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │ YouTube     │ │ Database    │ │ AI Tools                │ │
│  │ Tools (6)   │ │ Tools (7)   │ │ (6)                     │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys (OpenAI, Supabase, YouTube)
```

### 3. **Start the OpenAI Wrapper**
```bash
# Simple start
python start_angus_openai_wrapper.py

# With custom options
python start_angus_openai_wrapper.py --host 0.0.0.0 --port 8001 --log-level DEBUG

# Check dependencies only
python start_angus_openai_wrapper.py --check-only
```

### 4. **Verify the Server**
```bash
# Health check
curl http://localhost:8001/health

# List models
curl http://localhost:8001/v1/models

# Test chat completion
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "angus-v1",
    "messages": [
      {"role": "user", "content": "Upload 3 songs to YouTube"}
    ]
  }'
```

## 🔗 Coraliser Integration

### 1. **Use the Provided Settings File**
The `coraliser_settings.json` file is pre-configured for Agent Angus:

```json
{
  "agents": [
    {
      "name": "angus",
      "host": "http://localhost:8001",
      "description": "Music automation agent using STDIO MCP",
      "api_key": ""
    }
  ],
  "coral_server_url": "http://localhost:5000"
}
```

### 2. **Start Coraliser**
```bash
# In the Coraliser directory
python coraliser.py --settings /path/to/Angus_Langchain/coraliser_settings.json
```

## 📡 API Endpoints

### **Chat Completions** (OpenAI-compatible)
```http
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "angus-v1",
  "messages": [
    {"role": "user", "content": "Your request here"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response:**
```json
{
  "id": "chatcmpl-angus-12345678",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "angus-v1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Task completed successfully..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### **List Models**
```http
GET /v1/models
```

### **Health Check**
```http
GET /health
```

### **Agent Status**
```http
GET /v1/agent/status
```

### **List Tools**
```http
GET /v1/agent/tools
```

## 🎵 Agent Angus Capabilities

When you send requests to the OpenAI wrapper, Agent Angus can handle:

### **YouTube Operations**
- `"Upload 5 songs to YouTube"`
- `"Check my YouTube upload quota"`
- `"Get comments from video ABC123"`
- `"Reply to comment XYZ with a friendly message"`

### **Database Operations**
- `"Show me pending songs"`
- `"Get details for song ID 123"`
- `"List uploaded videos"`
- `"Update song status to completed"`

### **AI Analysis**
- `"Analyze the music content of song.mp3"`
- `"Generate a description for my pop song"`
- `"Suggest tags for an electronic music video"`
- `"Analyze sentiment of this comment: 'Great song!'"`

### **Workflow Operations**
- `"Run the complete upload workflow for 3 songs"`
- `"Process comments for all uploaded videos"`
- `"Upload and analyze 5 pending songs"`

## 🔧 Configuration Options

### **Startup Script Options**
```bash
python start_angus_openai_wrapper.py --help

Options:
  --host TEXT          Host to bind to (default: 0.0.0.0)
  --port INTEGER       Port to bind to (default: 8001)
  --log-level TEXT     Log level: DEBUG, INFO, WARNING, ERROR
  --reload             Enable auto-reload for development
  --check-only         Only check dependencies, don't start server
```

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

## 🐛 Troubleshooting

### **Common Issues**

1. **MCP Client Not Available**
   ```bash
   # Install MCP dependencies
   pip install mcp langchain-mcp-adapters
   ```

2. **Environment Variables Missing**
   ```bash
   # Check your .env file
   python start_angus_openai_wrapper.py --check-only
   ```

3. **Port Already in Use**
   ```bash
   # Use a different port
   python start_angus_openai_wrapper.py --port 8002
   ```

4. **YouTube Authentication Issues**
   ```bash
   # Re-run YouTube authentication
   python youtube_auth_langchain.py
   ```

### **Debug Mode**
```bash
# Start with debug logging
python start_angus_openai_wrapper.py --log-level DEBUG

# Check logs
tail -f angus_openai_wrapper.log
```

### **Health Checks**
```bash
# Check if server is running
curl http://localhost:8001/health

# Check agent status
curl http://localhost:8001/v1/agent/status

# List available tools
curl http://localhost:8001/v1/agent/tools
```

## 🔄 Development

### **Testing the Wrapper**
```python
import requests

# Test chat completion
response = requests.post(
    "http://localhost:8001/v1/chat/completions",
    json={
        "model": "angus-v1",
        "messages": [
            {"role": "user", "content": "Check my YouTube quota"}
        ]
    }
)

print(response.json())
```

### **Adding Custom Endpoints**
Edit `angus_openai_wrapper.py` to add new endpoints:

```python
@app.get("/v1/custom/endpoint")
async def custom_endpoint():
    """Your custom endpoint."""
    return {"message": "Custom response"}
```

## 📋 Integration Examples

### **Python Client**
```python
import openai

# Configure to use Agent Angus wrapper
client = openai.OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="not-needed"  # No API key required
)

# Use like normal OpenAI client
response = client.chat.completions.create(
    model="angus-v1",
    messages=[
        {"role": "user", "content": "Upload 2 songs to YouTube"}
    ]
)

print(response.choices[0].message.content)
```

### **JavaScript/Node.js**
```javascript
const OpenAI = require('openai');

const client = new OpenAI({
  baseURL: 'http://localhost:8001/v1',
  apiKey: 'not-needed'
});

async function uploadSongs() {
  const response = await client.chat.completions.create({
    model: 'angus-v1',
    messages: [
      { role: 'user', content: 'Upload 3 songs to YouTube' }
    ]
  });
  
  console.log(response.choices[0].message.content);
}
```

### **cURL Examples**
```bash
# Upload songs
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "angus-v1",
    "messages": [
      {"role": "user", "content": "Upload 5 songs to YouTube"}
    ]
  }'

# Process comments
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "angus-v1",
    "messages": [
      {"role": "user", "content": "Process comments for all videos"}
    ]
  }'
```

## 🎯 Production Deployment

### **Using Docker**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["python", "start_angus_openai_wrapper.py", "--host", "0.0.0.0"]
```

### **Using systemd**
```ini
[Unit]
Description=Agent Angus OpenAI Wrapper
After=network.target

[Service]
Type=simple
User=angus
WorkingDirectory=/opt/Angus_Langchain
ExecStart=/usr/bin/python3 start_angus_openai_wrapper.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### **Behind Reverse Proxy (nginx)**
```nginx
server {
    listen 80;
    server_name angus-api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📞 Support

- **Issues**: Check the logs in `angus_openai_wrapper.log`
- **Health**: Monitor `/health` endpoint
- **Status**: Check `/v1/agent/status` for detailed information
- **Documentation**: Visit `http://localhost:8001/docs` for interactive API docs

---

**🎉 Status**: OpenAI-Compatible Wrapper Ready!
**🔗 Endpoint**: http://localhost:8001/v1/chat/completions
**🎵 Capabilities**: Full Agent Angus functionality via OpenAI-style API
