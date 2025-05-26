#!/usr/bin/env python3
"""
Agent Angus LangChain - Phase 2.5 Implementation

This is the LangChain equivalent of the original angus.py, providing
a unified LangChain agent that replicates all Agent Angus functionality.
"""
import os
import sys
import asyncio
import logging
import argparse
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('angus_langchain.log')
    ]
)
logger = logging.getLogger(__name__)

# Import the unified agent
from agents.angus_langchain_agent import AngusLangChainAgent, create_angus_langchain_agent

class AngusLangChainSystem:
    """
    Main system controller for LangChain Agent Angus.
    
    This class provides the main entry point and system management
    for the LangChain version of Agent Angus.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        """
        Initialize the LangChain system.
        
        Args:
            model_name: OpenAI model to use
        """
        self.model_name = model_name
        self.agent = None
        self.status = "not_initialized"
        
        logger.info(f"AngusLangChainSystem initialized with model: {model_name}")
    
    async def initialize(self):
        """Initialize the system and agent."""
        try:
            logger.info("Initializing Agent Angus LangChain system...")
            
            # Create and initialize the agent
            self.agent = await create_angus_langchain_agent(self.model_name)
            
            self.status = "initialized"
            logger.info("Agent Angus LangChain system initialized successfully")
            
        except Exception as e:
            self.status = "error"
            logger.error(f"Failed to initialize system: {str(e)}")
            raise
    
    async def run_upload_workflow(self, limit: int = 5) -> Dict[str, Any]:
        """
        Run the song upload workflow.
        
        Args:
            limit: Maximum number of songs to upload
            
        Returns:
            Workflow results
        """
        if not self.agent:
            raise RuntimeError("System not initialized")
        
        logger.info(f"Running upload workflow (limit: {limit})")
        return await self.agent.run_song_upload_workflow(limit)
    
    async def run_comment_workflow(self, max_replies: int = 10) -> Dict[str, Any]:
        """
        Run the comment processing workflow.
        
        Args:
            max_replies: Maximum number of replies to post
            
        Returns:
            Workflow results
        """
        if not self.agent:
            raise RuntimeError("System not initialized")
        
        logger.info(f"Running comment workflow (max_replies: {max_replies})")
        return await self.agent.run_comment_processing_workflow(max_replies)
    
    async def run_both_workflows(self, upload_limit: int = 5, reply_limit: int = 10) -> Dict[str, Any]:
        """
        Run both workflows.
        
        Args:
            upload_limit: Maximum number of songs to upload
            reply_limit: Maximum number of replies to post
            
        Returns:
            Combined workflow results
        """
        if not self.agent:
            raise RuntimeError("System not initialized")
        
        logger.info(f"Running both workflows (upload_limit: {upload_limit}, reply_limit: {reply_limit})")
        return await self.agent.run_both_workflows(upload_limit, reply_limit)
    
    async def run_daemon_mode(self, upload_interval: int = 3600, comment_interval: int = 1800):
        """
        Run in daemon mode with scheduled tasks.
        
        Args:
            upload_interval: Seconds between upload workflow runs
            comment_interval: Seconds between comment workflow runs
        """
        if not self.agent:
            raise RuntimeError("System not initialized")
        
        logger.info("Starting daemon mode...")
        await self.agent.main_loop(upload_interval, comment_interval)
    
    async def execute_custom_task(self, task: str) -> str:
        """
        Execute a custom task using the agent.
        
        Args:
            task: Task description
            
        Returns:
            Task result
        """
        if not self.agent:
            raise RuntimeError("System not initialized")
        
        logger.info(f"Executing custom task: {task[:100]}...")
        return await self.agent.execute_task(task)
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status."""
        status = {
            "system_status": self.status,
            "model": self.model_name,
            "agent_status": None
        }
        
        if self.agent:
            status["agent_status"] = self.agent.get_status()
        
        return status

async def main():
    """Main entry point for Agent Angus LangChain."""
    parser = argparse.ArgumentParser(description='Agent Angus LangChain - Music Publishing Automation')
    
    # Action arguments
    parser.add_argument('--upload', action='store_true', help='Run song upload workflow')
    parser.add_argument('--comments', action='store_true', help='Run comment processing workflow')
    parser.add_argument('--both', action='store_true', help='Run both workflows')
    parser.add_argument('--daemon', action='store_true', help='Run in daemon mode with scheduled tasks')
    parser.add_argument('--task', type=str, help='Execute a custom task')
    parser.add_argument('--status', action='store_true', help='Show system status')
    
    # Configuration arguments
    parser.add_argument('--upload-limit', type=int, default=5, help='Maximum songs to upload (default: 5)')
    parser.add_argument('--reply-limit', type=int, default=10, help='Maximum replies to post (default: 10)')
    parser.add_argument('--upload-interval', type=int, default=3600, help='Upload interval in seconds (default: 3600)')
    parser.add_argument('--comment-interval', type=int, default=1800, help='Comment interval in seconds (default: 1800)')
    parser.add_argument('--model', type=str, default='gpt-4o', help='OpenAI model to use (default: gpt-4o)')
    
    # Testing arguments
    parser.add_argument('--test-tools', action='store_true', help='Test tool integration')
    parser.add_argument('--validate', action='store_true', help='Validate system configuration')
    
    args = parser.parse_args()
    
    # Initialize system
    system = AngusLangChainSystem(model_name=args.model)
    
    try:
        # Validate configuration if requested
        if args.validate:
            logger.info("Validating system configuration...")
            await system.initialize()
            status = system.get_status()
            print("System Status:")
            print(f"  System: {status['system_status']}")
            print(f"  Model: {status['model']}")
            if status['agent_status']:
                print(f"  Agent: {status['agent_status']['status']}")
                print(f"  Tools: {status['agent_status']['tools_count']}")
                print(f"  Phase: {status['agent_status']['phase']}")
            print("✅ System validation completed successfully")
            return
        
        # Test tools if requested
        if args.test_tools:
            logger.info("Testing tool integration...")
            await system.initialize()
            
            # Test basic tool functionality
            test_task = """Test the tool integration:
            
1. Use get_pending_songs to check for pending songs (limit 1)
2. Use check_upload_quota to check YouTube quota
3. Use analyze_comment_sentiment to test AI tools with text: "This music is amazing!"
4. Provide a summary of all tool test results

This is a test run - do not actually upload anything or reply to comments."""
            
            result = await system.execute_custom_task(test_task)
            print("Tool Test Results:")
            print(result)
            return
        
        # Show status if requested
        if args.status:
            await system.initialize()
            status = system.get_status()
            print("Agent Angus LangChain Status:")
            for key, value in status.items():
                print(f"  {key}: {value}")
            return
        
        # Initialize system for other operations
        await system.initialize()
        
        # Execute custom task
        if args.task:
            result = await system.execute_custom_task(args.task)
            print("Task Result:")
            print(result)
            return
        
        # Run daemon mode
        if args.daemon:
            logger.info("Starting daemon mode...")
            await system.run_daemon_mode(args.upload_interval, args.comment_interval)
            return
        
        # Run workflows
        if args.upload:
            result = await system.run_upload_workflow(args.upload_limit)
            print("Upload Workflow Result:")
            print(f"Status: {result['status']}")
            print(f"Result: {result['result']}")
        
        elif args.comments:
            result = await system.run_comment_workflow(args.reply_limit)
            print("Comment Workflow Result:")
            print(f"Status: {result['status']}")
            print(f"Result: {result['result']}")
        
        elif args.both:
            result = await system.run_both_workflows(args.upload_limit, args.reply_limit)
            print("Combined Workflow Results:")
            print(f"Overall Status: {result['overall_status']}")
            print(f"Timestamp: {result['timestamp']}")
            
            if result.get('upload_workflow'):
                print(f"Upload Status: {result['upload_workflow']['status']}")
            
            if result.get('comment_workflow'):
                print(f"Comment Status: {result['comment_workflow']['status']}")
        
        else:
            # No specific action requested, show help
            parser.print_help()
            print("\nExamples:")
            print("  python angus_langchain.py --validate                    # Validate system")
            print("  python angus_langchain.py --test-tools                  # Test tool integration")
            print("  python angus_langchain.py --upload --upload-limit 1     # Upload 1 song")
            print("  python angus_langchain.py --comments --reply-limit 5    # Process comments")
            print("  python angus_langchain.py --both                        # Run both workflows")
            print("  python angus_langchain.py --daemon                      # Run continuously")
            print("  python angus_langchain.py --task 'Check system status'  # Custom task")
    
    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
