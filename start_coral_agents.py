"""
Startup script for Agent Angus Coral Protocol multi-agent system.

This script helps launch all the specialized agents in the correct order
and provides a unified interface for managing the distributed system.
"""
import asyncio
import subprocess
import sys
import time
import os
from pathlib import Path

def print_banner():
    print("""
🌊 ═══════════════════════════════════════════════════════════════════════════════ 🌊
   
    ░█████╗░░██████╗░███████╗███╗░░██╗████████╗  ░█████╗░███╗░░██╗░██████╗░██╗░░░██╗░██████╗
    ██╔══██╗██╔════╝░██╔════╝████╗░██║╚══██╔══╝  ██╔══██╗████╗░██║██╔════╝░██║░░░██║██╔════╝
    ███████║██║░░██╗░█████╗░░██╔██╗██║░░░██║░░░  ███████║██╔██╗██║██║░░██╗░██║░░░██║╚█████╗░
    ██╔══██║██║░░╚██╗██╔══╝░░██║╚████║░░░██║░░░  ██╔══██║██║╚████║██║░░╚██╗██║░░░██║░╚═══██╗
    ██║░░██║╚██████╔╝███████╗██║░╚███║░░░██║░░░  ██║░░██║██║░╚███║╚██████╔╝╚██████╔╝██████╔╝
    ╚═╝░░╚═╝░╚═════╝░╚══════╝╚═╝░░╚══╝░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░░╚═════╝░╚═════╝░
    
    🎵 CORAL PROTOCOL MULTI-AGENT MUSIC AUTOMATION SYSTEM 🎵
    
🌊 ═══════════════════════════════════════════════════════════════════════════════ 🌊
""")

def check_requirements():
    """Check if all required dependencies are installed."""
    print("🔍 Checking requirements...")
    
    required_packages = [
        "langchain",
        "langchain_mcp_adapters", 
        "langchain_openai",
        "openai",
        "supabase",
        "google-api-python-client"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All requirements satisfied!")
    return True

def check_environment():
    """Check if required environment variables are set."""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        "OPENAI_API_KEY",
        "SUPABASE_URL", 
        "SUPABASE_KEY",
        "YOUTUBE_CLIENT_ID",
        "YOUTUBE_CLIENT_SECRET"
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"  ✅ {var}")
        else:
            print(f"  ❌ {var}")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set them in your .env file")
        return False
    
    print("✅ All environment variables set!")
    return True

def start_coral_server():
    """Start the Coral Protocol server."""
    print("\n🌊 Starting Coral Protocol server...")
    print("Note: This requires the Coral server to be installed and available.")
    print("Please start the Coral server manually with: ./gradlew run")
    print("Server should be running at: http://localhost:5555")
    
    # Wait for user confirmation
    input("\nPress Enter when the Coral server is running...")

def start_agent(agent_name, script_path):
    """Start an individual agent."""
    print(f"\n🚀 Starting {agent_name}...")
    
    try:
        # Start the agent in a new terminal/process
        if sys.platform == "win32":
            # Windows
            subprocess.Popen([
                "cmd", "/c", "start", "cmd", "/k", 
                f"python {script_path}"
            ])
        else:
            # Unix/Linux/Mac
            subprocess.Popen([
                "gnome-terminal", "--", "python", script_path
            ])
        
        print(f"✅ {agent_name} started successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start {agent_name}: {e}")
        return False

def main():
    print_banner()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Start Coral server
    start_coral_server()
    
    # Define agents to start
    agents = [
        ("Database Agent", "agents/angus_database_agent.py"),
        ("YouTube Agent", "agents/angus_youtube_agent.py"), 
        ("AI Agent", "agents/angus_ai_agent.py"),
        ("Coordinator Agent", "agents/angus_coordinator_agent.py")
    ]
    
    print("\n🎵 Starting Agent Angus Multi-Agent System...")
    
    # Start each agent with a delay
    for agent_name, script_path in agents:
        if start_agent(agent_name, script_path):
            time.sleep(2)  # Wait between agent starts
        else:
            print(f"❌ Failed to start {agent_name}. Aborting...")
            sys.exit(1)
    
    print(f"""
🎉 All agents started successfully!

🌊 Agent Angus Coral Protocol System is now running:

📊 Database Agent    - Handles all Supabase operations
🎬 YouTube Agent     - Manages YouTube API operations  
🤖 AI Agent         - Provides OpenAI-powered analysis
🎵 Coordinator Agent - Orchestrates all workflows

💡 Usage:
1. Use the Coordinator Agent terminal to run workflows
2. Each specialized agent can be used independently
3. All agents communicate via Coral Protocol server

🔧 Commands in Coordinator Agent:
- upload <limit>     - Start song upload workflow
- comments <limit>   - Start comment processing workflow
- both <up> <comm>   - Run both workflows
- status            - Check system status
- quit              - Exit

🌊 Enjoy your distributed Agent Angus system! 🌊
""")

if __name__ == "__main__":
    main()
