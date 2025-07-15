#!/usr/bin/env python3
"""
Interactive Chat with Test agent
Uses the existing agent code directly for interactive chat with memory
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your existing agent
from agents.agent import test_agent_agent

def main():
    print("=" * 60)
    print("🧠 INTERACTIVE CHAT: TEST AGENT")
    print("=" * 60)
    print("✨ This agent has enhanced memory - it remembers our conversation!")
    print("💡 Try follow-up questions using 'those', 'that', 'same', etc.")
    print("🛑 Type 'exit', 'quit', or 'bye' to end")
    print("=" * 60)
    
    # Create agent instance with your session
    user_id = "interactive_user"
    session_id = "interactive_session"
    
    try:
        print("\n🚀 Initializing agent...")
        agent = test_agent_agent(
            user_id=user_id,
            session_id=session_id,
            debug_mode=False
        )
        print("✅ Agent ready! Start asking questions...\n")
        
        conversation_count = 0
        
        while True:
            try:
                conversation_count += 1
                print(f"💬 Question #{conversation_count}:")
                
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    print("Please enter a question...")
                    continue
                
                print(f"\n🤖 Test agent:")
                print("-" * 50)
                
                # Use the ask method from your memory-enabled agent
                response = agent.ask(user_input)
                print(response)
                
                # Show context for debugging (optional)
                if hasattr(agent, 'last_query_context') and agent.last_query_context:
                    print(f"\n💭 Context: {agent.last_query_context}")
                
                print("-" * 50)
                print()  # Extra line for readability
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Let's try again...\n")
                
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("\nMake sure:")
        print("1. Your .env file has the correct API keys")
        print("2. Database connection is working (if using SQL tools)")
        sys.exit(1)

if __name__ == "__main__":
    main()
