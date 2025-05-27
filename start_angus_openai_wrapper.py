#!/usr/bin/env python3
"""
Startup script for Agent Angus OpenAI-Compatible Wrapper.

This script starts the FastAPI server that provides an OpenAI-compatible
HTTP API interface for Agent Angus's MCP functionality.
"""

import os
import sys
import logging
import argparse
from pathlib import Path

def setup_logging(log_level: str = "INFO"):
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('angus_openai_wrapper.log')
        ]
    )

def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    try:
        import fastapi
    except ImportError:
        missing_deps.append("fastapi")
    
    try:
        import uvicorn
    except ImportError:
        missing_deps.append("uvicorn")
    
    try:
        from coral_integration.mcp_client import create_angus_mcp_client
    except ImportError:
        missing_deps.append("langchain-mcp-adapters (for MCP client)")
    
    if missing_deps:
        print("❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n💡 Install missing dependencies with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_environment():
    """Check if environment is properly configured."""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found")
        print("   Copy .env.example to .env and configure your API keys")
        return False
    
    # Check for essential environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "OPENAI_API_KEY",
        "SUPABASE_URL", 
        "SUPABASE_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Configure these in your .env file")
        return False
    
    return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Start Agent Angus OpenAI-Compatible Wrapper"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8001, 
        help="Port to bind to (default: 8001)"
    )
    parser.add_argument(
        "--log-level", 
        default="INFO", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log level (default: INFO)"
    )
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--check-only", 
        action="store_true", 
        help="Only check dependencies and environment, don't start server"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    print("🎵 Agent Angus OpenAI-Compatible Wrapper")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ Dependencies OK")
    
    # Check environment
    print("🔍 Checking environment...")
    env_ok = check_environment()
    if env_ok:
        print("✅ Environment OK")
    else:
        print("⚠️  Environment issues detected (see above)")
        if not args.check_only:
            response = input("Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    if args.check_only:
        print("\n✅ Pre-flight checks complete!")
        return
    
    # Start the server
    print(f"\n🚀 Starting server on {args.host}:{args.port}")
    print(f"📖 API documentation: http://{args.host}:{args.port}/docs")
    print(f"🔗 OpenAI endpoint: http://{args.host}:{args.port}/v1/chat/completions")
    print(f"❤️  Health check: http://{args.host}:{args.port}/health")
    print("\n💡 For Coraliser integration, use the coraliser_settings.json file")
    print("   Example: python coraliser.py --settings coraliser_settings.json")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        import uvicorn
        uvicorn.run(
            "angus_openai_wrapper:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level=args.log_level.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
