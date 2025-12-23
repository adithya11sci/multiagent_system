"""
Railway Intelligence Multi-Agent System
Main entry point for the application
"""
import asyncio
from orchestrator import RailwayOrchestrator
from rag.rag_system import RAGSystem
import json

def initialize_system():
    """Initialize the system and RAG data"""
    print("🚂 Initializing Railway Intelligence System...")
    
    # Initialize RAG system
    print("📚 Loading RAG knowledge base...")
    rag = RAGSystem()
    
    try:
        rag.initialize_data()
        print("✅ RAG system initialized")
    except Exception as e:
        print(f"⚠️  RAG initialization warning: {e}")
        print("   System will work with limited knowledge base")
    
    # Initialize orchestrator
    print("🧠 Initializing Multi-Agent Orchestrator...")
    orchestrator = RailwayOrchestrator()
    print("✅ Orchestrator ready")
    
    return orchestrator

def demo_scenario_1(orchestrator: RailwayOrchestrator):
    """Demo: Train delay scenario"""
    print("\n" + "="*70)
    print("🎬 DEMO SCENARIO 1: Train Delay")
    print("="*70)
    
    request = "Train 12627 is delayed by 45 minutes at Katpadi station"
    context = {
        "train_number": "12627",
        "delay_minutes": 45,
        "current_location": "Katpadi",
        "affected_passengers": 850
    }
    
    print(f"\n📢 Request: {request}")
    print(f"📊 Context: {json.dumps(context, indent=2)}\n")
    
    result = orchestrator.run(request, context)
    
    print("\n📋 RESULTS:")
    print(json.dumps(result, indent=2))
    
    return result

def demo_scenario_2(orchestrator: RailwayOrchestrator):
    """Demo: Passenger query scenario"""
    print("\n" + "="*70)
    print("🎬 DEMO SCENARIO 2: Passenger Query")
    print("="*70)
    
    request = "Passenger wants to know alternative trains from Bangalore to Delhi for tomorrow"
    context = {
        "passenger_id": "P1234",
        "origin": "Bangalore",
        "destination": "New Delhi",
        "travel_date": "2025-12-24",
        "class_preference": "ac_2tier"
    }
    
    print(f"\n📢 Request: {request}")
    print(f"📊 Context: {json.dumps(context, indent=2)}\n")
    
    result = orchestrator.run(request, context)
    
    print("\n📋 RESULTS:")
    print(json.dumps(result, indent=2))
    
    return result

def demo_scenario_3(orchestrator: RailwayOrchestrator):
    """Demo: Overcrowding prediction scenario"""
    print("\n" + "="*70)
    print("🎬 DEMO SCENARIO 3: Overcrowding Prediction")
    print("="*70)
    
    request = "Predict overcrowding for Train 12627 on December 25, 2025"
    context = {
        "train_number": "12627",
        "travel_date": "2025-12-25",
        "is_holiday": True
    }
    
    print(f"\n📢 Request: {request}")
    print(f"📊 Context: {json.dumps(context, indent=2)}\n")
    
    result = orchestrator.run(request, context)
    
    print("\n📋 RESULTS:")
    print(json.dumps(result, indent=2))
    
    return result

def interactive_mode(orchestrator: RailwayOrchestrator):
    """Interactive mode for custom requests"""
    print("\n" + "="*70)
    print("🎯 INTERACTIVE MODE")
    print("="*70)
    print("\nEnter your railway intelligence request (or 'quit' to exit):")
    print("Examples:")
    print("  - Train 12650 delayed by 60 minutes")
    print("  - Check overcrowding for train 12627 tomorrow")
    print("  - Send alert to passengers of train 12627")
    print()
    
    while True:
        request = input("\n💬 Your request: ").strip()
        
        if request.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not request:
            continue
        
        print("\n🤖 Processing your request...\n")
        
        result = orchestrator.run(request, {})
        
        print("\n📋 RESULTS:")
        print(json.dumps(result, indent=2))

def main():
    """Main function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  🚂 Railway Intelligence Multi-Agent System                  ║
    ║  Powered by Gemini AI + LangGraph                           ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize system
    orchestrator = initialize_system()
    
    print("\n" + "="*70)
    print("🎮 DEMO MODE")
    print("="*70)
    print("\nSelect an option:")
    print("1. Run Demo Scenario 1: Train Delay")
    print("2. Run Demo Scenario 2: Passenger Query")
    print("3. Run Demo Scenario 3: Overcrowding Prediction")
    print("4. Run All Demos")
    print("5. Interactive Mode")
    print("6. Exit")
    
    while True:
        choice = input("\n👉 Enter choice (1-6): ").strip()
        
        if choice == "1":
            demo_scenario_1(orchestrator)
        elif choice == "2":
            demo_scenario_2(orchestrator)
        elif choice == "3":
            demo_scenario_3(orchestrator)
        elif choice == "4":
            demo_scenario_1(orchestrator)
            demo_scenario_2(orchestrator)
            demo_scenario_3(orchestrator)
        elif choice == "5":
            interactive_mode(orchestrator)
        elif choice == "6":
            print("\n👋 Thank you for using Railway Intelligence System!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
