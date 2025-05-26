#!/usr/bin/env python3
"""
Agent Angus LangChain + Coral Protocol Main Entry Point

This script provides the main entry point for running the Agent Angus
multi-agent system with Coral Protocol integration.
"""
import asyncio
import argparse
import logging
import sys
import signal
from typing import Optional
from pathlib import Path

# Add the current directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.environment import (
    validate_environment, 
    print_environment_summary,
    AGENT_LOG_LEVEL,
    DEBUG_MODE
)
from config.coral_config import validate_coral_config

# Configure logging
logging.basicConfig(
    level=getattr(logging, AGENT_LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('angus_langchain.log')
    ]
)
logger = logging.getLogger(__name__)

class AgentAngusSystem:
    """
    Main system controller for Agent Angus LangChain implementation.
    """
    
    def __init__(self):
        """Initialize the Agent Angus system."""
        self.coral_server = None
        self.agents = {}
        self.running = False
        
        # Validate environment on startup
        if not validate_environment():
            logger.error("Environment validation failed. Please check your configuration.")
            sys.exit(1)
            
        if not validate_coral_config():
            logger.error("Coral configuration validation failed.")
            sys.exit(1)
            
        logger.info("Agent Angus LangChain system initialized")
    
    async def start_coral_server(self):
        """Start the Coral Protocol server."""
        try:
            logger.info("Starting Coral Protocol server...")
            
            # Import here to avoid circular imports
            from coral_integration.server_setup import CoralServerManager
            
            self.coral_server = CoralServerManager()
            await self.coral_server.start_server()
            
            logger.info("Coral Protocol server started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start Coral server: {str(e)}")
            raise
    
    async def start_agents(self, agent_types: Optional[list] = None):
        """
        Start the specified agents.
        
        Args:
            agent_types: List of agent types to start. If None, starts all agents.
        """
        if agent_types is None:
            agent_types = ["coordinator", "youtube", "database", "ai"]
        
        try:
            logger.info(f"Starting agents: {', '.join(agent_types)}")
            
            # Import agent classes
            from agents.coordinator_agent import AngusCoordinatorAgent
            from agents.youtube_agent import YouTubeAgent
            from agents.database_agent import DatabaseAgent
            from agents.ai_agent import AIAgent
            
            agent_classes = {
                "coordinator": AngusCoordinatorAgent,
                "youtube": YouTubeAgent,
                "database": DatabaseAgent,
                "ai": AIAgent
            }
            
            # Start each requested agent
            for agent_type in agent_types:
                if agent_type in agent_classes:
                    logger.info(f"Starting {agent_type} agent...")
                    
                    agent_class = agent_classes[agent_type]
                    agent = agent_class()
                    
                    # Start the agent (this will be async)
                    await agent.start()
                    
                    self.agents[agent_type] = agent
                    logger.info(f"{agent_type} agent started successfully")
                else:
                    logger.warning(f"Unknown agent type: {agent_type}")
            
            logger.info("All requested agents started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start agents: {str(e)}")
            raise
    
    async def stop_agents(self):
        """Stop all running agents."""
        try:
            logger.info("Stopping all agents...")
            
            for agent_type, agent in self.agents.items():
                logger.info(f"Stopping {agent_type} agent...")
                await agent.stop()
                logger.info(f"{agent_type} agent stopped")
            
            self.agents.clear()
            logger.info("All agents stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping agents: {str(e)}")
    
    async def stop_coral_server(self):
        """Stop the Coral Protocol server."""
        try:
            if self.coral_server:
                logger.info("Stopping Coral Protocol server...")
                await self.coral_server.stop_server()
                logger.info("Coral Protocol server stopped")
            
        except Exception as e:
            logger.error(f"Error stopping Coral server: {str(e)}")
    
    async def start_system(self, agent_types: Optional[list] = None):
        """
        Start the complete Agent Angus system.
        
        Args:
            agent_types: List of agent types to start
        """
        try:
            self.running = True
            
            # Start Coral server first
            await self.start_coral_server()
            
            # Wait a moment for server to be ready
            await asyncio.sleep(2)
            
            # Start agents
            await self.start_agents(agent_types)
            
            logger.info("Agent Angus system started successfully")
            logger.info("System is running. Press Ctrl+C to stop.")
            
            # Keep the system running
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"System error: {str(e)}")
            raise
        finally:
            await self.shutdown()
    
    async def shutdown(self):
        """Gracefully shutdown the system."""
        try:
            logger.info("Shutting down Agent Angus system...")
            self.running = False
            
            # Stop agents first
            await self.stop_agents()
            
            # Then stop Coral server
            await self.stop_coral_server()
            
            logger.info("Agent Angus system shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

def setup_signal_handlers(system: AgentAngusSystem):
    """Set up signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}")
        asyncio.create_task(system.shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def run_single_agent(agent_type: str):
    """
    Run a single agent for development/testing.
    
    Args:
        agent_type: Type of agent to run
    """
    try:
        logger.info(f"Running single {agent_type} agent...")
        
        # Import agent classes
        from agents.coordinator_agent import AngusCoordinatorAgent
        from agents.youtube_agent import YouTubeAgent
        from agents.database_agent import DatabaseAgent
        from agents.ai_agent import AIAgent
        
        agent_classes = {
            "coordinator": AngusCoordinatorAgent,
            "youtube": YouTubeAgent,
            "database": DatabaseAgent,
            "ai": AIAgent
        }
        
        if agent_type not in agent_classes:
            logger.error(f"Unknown agent type: {agent_type}")
            return
        
        agent_class = agent_classes[agent_type]
        agent = agent_class()
        
        # Start the agent
        await agent.start()
        
        logger.info(f"{agent_type} agent started. Press Ctrl+C to stop.")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        finally:
            await agent.stop()
            logger.info(f"{agent_type} agent stopped")
            
    except Exception as e:
        logger.error(f"Error running {agent_type} agent: {str(e)}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Agent Angus LangChain + Coral Protocol System')
    
    # System commands
    parser.add_argument('--start', action='store_true', help='Start the complete system')
    parser.add_argument('--agents', nargs='+', choices=['coordinator', 'youtube', 'database', 'ai'],
                       help='Specify which agents to start (default: all)')
    
    # Single agent mode
    parser.add_argument('--agent', choices=['coordinator', 'youtube', 'database', 'ai'],
                       help='Run a single agent (for development/testing)')
    
    # Utility commands
    parser.add_argument('--validate-env', action='store_true', help='Validate environment configuration')
    parser.add_argument('--print-env', action='store_true', help='Print environment summary')
    parser.add_argument('--validate-config', action='store_true', help='Validate all configurations')
    
    # Server commands
    parser.add_argument('--server-only', action='store_true', help='Start only the Coral server')
    
    # Debug options
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Handle debug mode
    if args.debug or DEBUG_MODE:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
    
    # Handle utility commands
    if args.validate_env:
        if validate_environment():
            print("✅ Environment configuration is valid")
            sys.exit(0)
        else:
            print("❌ Environment configuration is invalid")
            sys.exit(1)
    
    if args.print_env:
        print_environment_summary()
        sys.exit(0)
    
    if args.validate_config:
        env_valid = validate_environment()
        coral_valid = validate_coral_config()
        
        print(f"Environment config: {'✅ Valid' if env_valid else '❌ Invalid'}")
        print(f"Coral config: {'✅ Valid' if coral_valid else '❌ Invalid'}")
        
        if env_valid and coral_valid:
            print("✅ All configurations are valid")
            sys.exit(0)
        else:
            print("❌ Some configurations are invalid")
            sys.exit(1)
    
    # Handle server-only mode
    if args.server_only:
        async def run_server():
            from coral_integration.server_setup import CoralServerManager
            server = CoralServerManager()
            try:
                await server.start_server()
                logger.info("Coral server started. Press Ctrl+C to stop.")
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("Stopping server...")
            finally:
                await server.stop_server()
        
        asyncio.run(run_server())
        return
    
    # Handle single agent mode
    if args.agent:
        asyncio.run(run_single_agent(args.agent))
        return
    
    # Handle system start
    if args.start or not any([args.validate_env, args.print_env, args.validate_config, args.server_only, args.agent]):
        system = AgentAngusSystem()
        setup_signal_handlers(system)
        
        try:
            asyncio.run(system.start_system(args.agents))
        except KeyboardInterrupt:
            logger.info("System interrupted by user")
        except Exception as e:
            logger.error(f"System failed: {str(e)}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
