🔧 1. Wrap the MCP STDIO Server with an HTTP API (FastAPI)
Create a new script angus_openai_wrapper.py:

bash
Copy
Edit
cd angus_repo
touch angus_openai_wrapper.py
Populate it with a FastAPI app that:

Accepts OpenAI-style POST /v1/chat/completions requests

Internally calls your existing MCP STDIO client (create_angus_mcp_client)

<details> <summary>▶ Example code</summary>
python
Copy
Edit
from fastapi import FastAPI, Request
from pydantic import BaseModel
from coral_integration.mcp_client import create_angus_mcp_client

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    prompt = request.messages[-1].content
    client = await create_angus_mcp_client()
    result = await client.execute_task(prompt)

    return {
        "id": "chatcmpl-angus",
        "object": "chat.completion",
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": result},
            "finish_reason": "stop"
        }],
        "model": "angus-v1"
    }
</details>
🚀 2. Run the Wrapper
bash
Copy
Edit
uvicorn angus_openai_wrapper:app --host 0.0.0.0 --port 8001
📄 3. Create Coraliser Settings File
json
Copy
Edit
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
▶ 4. Run Coraliser
bash
Copy
Edit
cd coraliser
python coraliser.py --settings coraliser_settings.json