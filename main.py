import os
import sys
import argparse
from src.agent import SlowAgent
from src.utils.logger import Logger
from src.utils.config import Config

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Slow Agent - A deliberate AI agent")
    parser.add_argument("--browser", action="store_true", help="Enable browser functionality")
    parser.add_argument("--desktop", action="store_true", help="Enable desktop automation functionality")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--task", type=str, help="Task to execute")
    parser.add_argument("--task-file", type=str, help="File containing tasks to execute (one per line)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    return parser.parse_args()

def main():
    """Main entry point for the slow agent."""
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    logger = Logger(name="main")
    logger.info("Starting Slow Agent")
    
    # Create agent
    agent = SlowAgent(name="SlowAgent")
    
    # Initialize components based on arguments
    if args.browser:
        logger.info("Initializing browser functionality")
        agent.init_browser(headless=args.headless)
    
    if args.desktop:
        logger.info("Initializing desktop automation functionality")
        agent.init_desktop()
    
    # Load tasks
    tasks = []
    
    if args.task:
        tasks.append(args.task)
    
    if args.task_file and os.path.exists(args.task_file):
        with open(args.task_file, "r") as f:
            file_tasks = [line.strip() for line in f.readlines() if line.strip()]
            tasks.extend(file_tasks)
    
    # Run agent
    if tasks:
        logger.info(f"Running agent with {len(tasks)} task(s)")
        agent.run_session(tasks=tasks)
    elif args.interactive:
        logger.info("Running agent in interactive mode")
        try:
            print(f"Slow Agent Interactive Mode - Type 'exit' to quit")
            while True:
                user_input = input("\nEnter task: ")
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                if user_input.strip():
                    # Execute task directly in interactive mode
                    agent.add_task(user_input)
                    agent.execute_next_task()
        except KeyboardInterrupt:
            print("\nInteractive mode terminated by user")
    else:
        logger.info("No tasks provided. Use --task, --task-file, or --interactive")
        print("No tasks provided. Use --task, --task-file, or --interactive")
    
    # Cleanup
    if agent.browser:
        agent.browser.close_browser()
    
    logger.info("Slow Agent terminated")

if __name__ == "__main__":
    main()
