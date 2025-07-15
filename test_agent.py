#!/usr/bin/env python3
"""
API Test Script for Test agent
Test your agent API endpoints
"""

import requests
import json
import time
import sys

# Configuration
API_BASE = "http://localhost:8000"
AGENT_ID = "test_agent"
USER_ID = "test_user"
SESSION_ID = "test_session"

def test_agent_list():
    """Test listing available agents"""
    print("🔍 Testing: List available agents")
    try:
        response = requests.get(f"{API_BASE}/v1/agents", timeout=10)
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ Found {len(agents)} agent(s): {agents}")
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_agent_chat(message: str):
    """Test chatting with the agent"""
    print(f"💬 Testing chat: '{message}'")
    
    payload = {
        "message": message,
        "user_id": USER_ID,
        "session_id": SESSION_ID,
        "stream": False
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/v1/agents/{AGENT_ID}/runs",
            json=payload,
            timeout=60
        )
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Response ({duration:.1f}s): {str(result)[:100]}..." if len(str(result)) > 100 else f"✅ Response ({duration:.1f}s): {result}")
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 API TESTING: TEST AGENT")
    print("=" * 60)
    print(f"📡 API Base: {API_BASE}")
    print(f"🤖 Agent ID: {AGENT_ID}")
    print("=" * 60)
    
    # Test 1: Check if server is running
    print("\n1️⃣ Testing server connection...")
    if not test_agent_list():
        print("\n❌ Server not responding. Make sure:")
        print("   1. Server is running: python -m uvicorn api.main:app --reload")
        print("   2. Port 8000 is available")
        sys.exit(1)
    
    # Test 2: Basic chat
    print("\n2️⃣ Testing basic chat...")
    test_agent_chat("Hello! What can you do?")
    
    # Test 3: Memory test (if applicable)
    print("\n3️⃣ Testing memory (follow-up questions)...")
    test_agent_chat("Show me some data analysis")
    time.sleep(1)  # Brief pause
    test_agent_chat("Can you tell me more about that analysis?")
    
    print("\n" + "=" * 60)
    print("🎉 Testing complete!")
    print("\n💡 Try these URLs:")
    print(f"   📚 API Docs: {API_BASE}/docs")
    print(f"   📖 ReDoc: {API_BASE}/redoc")
    print("=" * 60)

if __name__ == "__main__":
    main()
