#!/usr/bin/env python3
"""
Quick Test Script for LangChain Agent Integration
Run this to verify everything is working
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed."""
    print("🔍 Testing imports...")
    
    try:
        import langchain
        print("  ✅ langchain")
    except ImportError:
        print("  ❌ langchain - Install with: pip install langchain")
        return False
    
    try:
        import langchain_groq
        print("  ✅ langchain-groq")
    except ImportError:
        print("  ❌ langchain-groq - Install with: pip install langchain-groq")
        return False
    
    try:
        import flask
        print("  ✅ flask")
    except ImportError:
        print("  ❌ flask - Install with: pip install flask")
        return False
    
    try:
        import flask_cors
        print("  ✅ flask-cors")
    except ImportError:
        print("  ❌ flask-cors - Install with: pip install flask-cors")
        return False
    
    try:
        import dotenv
        print("  ✅ python-dotenv")
    except ImportError:
        print("  ❌ python-dotenv - Install with: pip install python-dotenv")
        return False
    
    print("✅ All imports successful!\n")
    return True


def test_env():
    """Test if environment is configured."""
    print("🔍 Testing environment...")
    
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        print(f"  ✅ GROQ_API_KEY set ({api_key[:20]}...)")
    else:
        print("  ⚠️  GROQ_API_KEY not set")
        print("     Run: export GROQ_API_KEY='your-api-key'")
        print("     Or create backend/.env file")
        return False
    
    print("✅ Environment configured!\n")
    return True


def test_agent():
    """Test if agent can be loaded."""
    print("🔍 Testing agent...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        from agent import get_agent
        
        print("  Loading agent...")
        agent = get_agent()
        
        print(f"  ✅ Agent loaded successfully")
        print(f"     Model: mixtral-8x7b-32768")
        print(f"     Tools available: {len(agent.tools)}")
        
        for tool in agent.tools:
            print(f"       • {tool.name}")
        
        print("✅ Agent working!\n")
        return True
    except Exception as e:
        print(f"  ❌ Error loading agent: {str(e)}")
        print(f"     Make sure GROQ_API_KEY is set")
        return False


def test_tools():
    """Test if tools can be imported."""
    print("🔍 Testing tools...")
    
    try:
        from tools.news_tools import get_google_news, get_local_news
        print("  ✅ News tools loaded")
    except Exception as e:
        print(f"  ❌ Error loading news tools: {e}")
        return False
    
    try:
        from tools.tech_tools import get_github_trending
        print("  ✅ Tech tools loaded")
    except Exception as e:
        print(f"  ❌ Error loading tech tools: {e}")
        return False
    
    try:
        from tools.entertainment_tools import get_trending_books
        print("  ✅ Entertainment tools loaded")
    except Exception as e:
        print(f"  ❌ Error loading entertainment tools: {e}")
        return False
    
    try:
        from tools.utility_tools import get_local_weather
        print("  ✅ Utility tools loaded")
    except Exception as e:
        print(f"  ❌ Error loading utility tools: {e}")
        return False
    
    print("✅ All tools working!\n")
    return True


def test_agent_query():
    """Test a simple agent query."""
    print("🔍 Testing agent query...")
    
    try:
        from agent import get_agent
        agent = get_agent()
        
        print("  Sending test query: 'Hello, what can you do?'")
        result = agent.run("Hello, what can you do?")
        
        if result:
            print(f"  ✅ Agent responded: {result[:100]}...")
        else:
            print("  ⚠️  Agent returned empty response")
        
        print("✅ Query successful!\n")
        return True
    except Exception as e:
        print(f"  ❌ Query failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("🚀 My Daily Log - LangChain Integration Test")
    print("="*50 + "\n")
    
    # Change to backend directory
    os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
    
    results = {
        "Imports": test_imports(),
        "Environment": test_env(),
        "Agent": test_agent(),
        "Tools": test_tools(),
    }
    
    # Only test query if everything else works
    if all(results.values()):
        results["Query"] = test_agent_query()
    
    # Summary
    print("="*50)
    print("📊 Test Summary")
    print("="*50)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print("="*50)
    
    if all(results.values()):
        print("\n✨ All tests passed! Your setup is ready.\n")
        print("Next steps:")
        print("  1. Run: python app.py")
        print("  2. Test: curl http://localhost:5000/api/query?q=Hello")
        print("  3. Check: http://localhost:5000/api/agent/info")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
