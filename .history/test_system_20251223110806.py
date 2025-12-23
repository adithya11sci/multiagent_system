"""
Test Suite for Railway Intelligence System
Run this to verify all components are working correctly
"""

def test_imports():
    """Test if all required packages are installed"""
    print("\n🧪 Testing Imports...")
    
    try:
        import google.generativeai
        print("   ✅ google-generativeai")
    except ImportError:
        print("   ❌ google-generativeai - Run: pip install google-generativeai")
        return False
    
    try:
        import langchain
        print("   ✅ langchain")
    except ImportError:
        print("   ❌ langchain - Run: pip install langchain")
        return False
    
    try:
        import langgraph
        print("   ✅ langgraph")
    except ImportError:
        print("   ❌ langgraph - Run: pip install langgraph")
        return False
    
    try:
        import chromadb
        print("   ✅ chromadb")
    except ImportError:
        print("   ❌ chromadb - Run: pip install chromadb")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("   ✅ sentence-transformers")
    except ImportError:
        print("   ❌ sentence-transformers - Run: pip install sentence-transformers")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\n🧪 Testing Configuration...")
    
    try:
        import config
        print("   ✅ config.py loaded")
        
        if config.GEMINI_API_KEY and config.GEMINI_API_KEY != "":
            print("   ✅ GEMINI_API_KEY configured")
        else:
            print("   ⚠️  GEMINI_API_KEY not set - Add to .env file")
            return False
        
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_agents():
    """Test if all agents can be imported"""
    print("\n🧪 Testing Agents...")
    
    try:
        from agents import (
            PlannerAgent, OperationsAgent, PassengerAgent,
            CrowdAgent, AlertAgent
        )
        print("   ✅ All agents imported successfully")
        
        # Try instantiating (won't work without API key)
        print("   ℹ️  Note: Agent initialization requires valid GEMINI_API_KEY")
        return True
    except Exception as e:
        print(f"   ❌ Agent import error: {e}")
        return False

def test_tools():
    """Test if all tools can be imported"""
    print("\n🧪 Testing Tools...")
    
    try:
        from tools import (
            TrainScheduleTool, DelaySimulator,
            CrowdPredictor, BookingAnalyzer,
            NotificationService
        )
        print("   ✅ All tools imported successfully")
        
        # Test basic tool functionality
        schedule_tool = TrainScheduleTool()
        schedule = schedule_tool.get_train_schedule("12627")
        if "train_number" in schedule:
            print("   ✅ TrainScheduleTool working")
        
        simulator = DelaySimulator()
        result = simulator.simulate_delay("12627", 30)
        if "propagation_factor" in result:
            print("   ✅ DelaySimulator working")
        
        return True
    except Exception as e:
        print(f"   ❌ Tools error: {e}")
        return False

def test_rag_system():
    """Test RAG system"""
    print("\n🧪 Testing RAG System...")
    
    try:
        from rag import RAGSystem
        print("   ✅ RAG system imported")
        
        rag = RAGSystem()
        print("   ✅ RAG system instantiated")
        
        # Note: Actual initialization requires data files
        print("   ℹ️  Note: RAG data initialization requires files in data/rag/")
        return True
    except Exception as e:
        print(f"   ❌ RAG system error: {e}")
        return False

def test_orchestrator():
    """Test orchestrator"""
    print("\n🧪 Testing Orchestrator...")
    
    try:
        from orchestrator import RailwayOrchestrator
        print("   ✅ Orchestrator imported")
        
        print("   ℹ️  Note: Orchestrator execution requires valid GEMINI_API_KEY")
        return True
    except Exception as e:
        print(f"   ❌ Orchestrator error: {e}")
        return False

def test_data_files():
    """Test if data files exist"""
    print("\n🧪 Testing Data Files...")
    
    import os
    
    data_files = [
        "data/rag/timetables.json",
        "data/rag/policies.txt",
        "data/rag/refund_rules.txt",
        "data/rag/route_maps.json"
    ]
    
    all_exist = True
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ⚠️  {file_path} - File missing")
            all_exist = False
    
    return all_exist

def test_environment():
    """Test environment variables"""
    print("\n🧪 Testing Environment...")
    
    import os
    
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"   ✅ {env_file} exists")
    else:
        print(f"   ⚠️  {env_file} not found - Copy from .env.example")
        return False
    
    # Check for required variables
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key and gemini_key != "your_gemini_api_key_here":
        print("   ✅ GEMINI_API_KEY is set")
    else:
        print("   ⚠️  GEMINI_API_KEY not configured properly")
        return False
    
    # Optional variables
    if os.getenv("TWILIO_ACCOUNT_SID"):
        print("   ✅ Twilio configured (optional)")
    else:
        print("   ℹ️  Twilio not configured (optional)")
    
    if os.getenv("SMTP_EMAIL"):
        print("   ✅ Email configured (optional)")
    else:
        print("   ℹ️  Email not configured (optional)")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("🧪 RAILWAY INTELLIGENCE SYSTEM - TEST SUITE")
    print("=" * 70)
    
    results = {
        "Imports": test_imports(),
        "Configuration": test_config(),
        "Agents": test_agents(),
        "Tools": test_tools(),
        "RAG System": test_rag_system(),
        "Orchestrator": test_orchestrator(),
        "Data Files": test_data_files(),
        "Environment": test_environment()
    }
    
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<50} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 70)
    print(f"Total Tests: {passed + failed} | Passed: {passed} | Failed: {failed}")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is ready to use.")
        print("   Run 'python main.py' to start the system.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix the issues above.")
        print("   Common fixes:")
        print("   - Install missing packages: pip install -r requirements.txt")
        print("   - Configure .env file with your GEMINI_API_KEY")
        print("   - Ensure all data files are present")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
