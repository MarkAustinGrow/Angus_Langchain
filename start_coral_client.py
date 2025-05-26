"""
Simple launcher for Agent Angus Coral Protocol client.

This script provides an easy way to start Agent Angus connected to the Coral Protocol network.
"""
import os
import sys
import subprocess
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
    
    🌊 CORAL PROTOCOL CLIENT LAUNCHER 🌊
    
🌊 ═══════════════════════════════════════════════════════════════════════════════ 🌊
""")

def check_requirements():
    """Check if required dependencies are installed."""
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

def check_coral_connectivity():
    """Check connectivity to Coral Protocol server."""
    print("\n🌊 Checking Coral Protocol connectivity...")
    
    try:
        import requests
        # Check the correct server and port
        response = requests.get("http://coral.pushcollective.club:5555", timeout=10)
        if response.status_code == 200:
            print("  ✅ coral.pushcollective.club:5555 is reachable")
            return True
        else:
            print(f"  ⚠️  coral.pushcollective.club:5555 returned status {response.status_code}")
            return True  # Still try to connect
    except Exception as e:
        print(f"  ❌ Cannot reach coral.pushcollective.club:5555: {e}")
        print("  ⚠️  Will attempt connection anyway...")
        return True  # Still try to connect

def main():
    print_banner()
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check Coral connectivity
    check_coral_connectivity()
    
    print(f"""
🎵 Starting Agent Angus Coral Protocol Client...

🌊 Connection Details:
   Server: coral.pushcollective.club:5555
   Agent ID: angus_agent
   Target Agent: yona_agent (Team Yona)
   Protocol: Server-Sent Events (SSE)
   Application: exampleApplication
   
🛠️  Agent Capabilities:
   • YouTube automation (6 tools)
   • Database operations (7 tools)  
   • AI analysis (6 tools)
   • Workflow automation (2 tools)
   • Team Yona collaboration (1 tool)
   
🤝 Collaboration Features:
   • Request song creation from Team Yona
   • Upload and manage collaborative content
   • Process comments on shared projects
   
🚀 Launching client...
""")
    
    # Launch the Coral client
    try:
        client_path = Path("agents/angus_coral_client.py")
        if not client_path.exists():
            print(f"❌ Client file not found: {client_path}")
            sys.exit(1)
        
        # Run the client
        subprocess.run([sys.executable, str(client_path)], check=True)
        
    except KeyboardInterrupt:
        print("\n🌊 Client shutdown requested by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Client exited with error code {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"\n❌ Failed to start client: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
