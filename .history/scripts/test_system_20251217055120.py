"""
Test Script - Test the system end-to-end
"""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from context.context_protocol import context_protocol, ChannelType
from orchestrator.orchestrator import orchestrator
from services.whatsapp_service import whatsapp_service


async def test_basic_conversation():
    """Test basic conversation flow"""
    print("=" * 60)
    print("Test: Basic Conversation")
    print("=" * 60)
    
    # Create test context
    context = context_protocol.create_context(
        user_id="+1234567890",
        channel=ChannelType.WHATSAPP,
        conversation_id="test_conversation_001",
        permissions=["email.read", "db.read"]
    )
    
    # Test message
    test_message = "Hello, can you help me?"
    
    print(f"\nUser: {test_message}")
    
    # Process message
    result = await orchestrator.process_message(test_message, context)
    
    print(f"\nAssistant: {result.response}")
    print(f"\nSuccess: {result.success}")
    print(f"Steps Executed: {len(result.executed_steps)}")
    print()


async def test_email_query():
    """Test email-related query"""
    print("=" * 60)
    print("Test: Email Query")
    print("=" * 60)
    
    # Create test context with email permissions
    context = context_protocol.create_context(
        user_id="+1234567890",
        channel=ChannelType.WHATSAPP,
        conversation_id="test_conversation_002",
        permissions=["email.read"]
    )
    
    # Test message
    test_message = "What is my last electricity bill amount? Check my email."
    
    print(f"\nUser: {test_message}")
    
    # Process message
    result = await orchestrator.process_message(test_message, context)
    
    print(f"\nAssistant: {result.response}")
    print(f"\nSuccess: {result.success}")
    
    if result.executed_steps:
        print("\nExecution Steps:")
        for step in result.executed_steps:
            print(f"  Step {step.get('step')}: {step.get('action')} - {step.get('status')}")
    
    print()


async def test_planning():
    """Test planner agent"""
    print("=" * 60)
    print("Test: Planner Agent")
    print("=" * 60)
    
    from agents.planner_agent import planner_agent
    
    context = context_protocol.create_context(
        user_id="test_user",
        channel=ChannelType.WHATSAPP,
        conversation_id="test_planning",
        permissions=["email.read"]
    )
    
    test_message = "Find my latest electricity bill from email and tell me the amount"
    
    print(f"\nUser Message: {test_message}")
    print("\nGenerating plan...")
    
    plan = await planner_agent.plan(test_message, context)
    
    print("\nPlan Generated:")
    print(f"Intent: {plan.get('intent')}")
    print(f"Confidence: {plan.get('confidence')}")
    print(f"Complexity: {plan.get('estimated_complexity')}")
    
    print("\nExecution Plan:")
    for step in plan.get('execution_plan', []):
        print(f"  Step {step.get('step')}: {step.get('action')}")
        print(f"    Agent: {step.get('agent')}")
        print(f"    Tool: {step.get('tool')}")
    
    print()


async def test_extraction():
    """Test extraction agent"""
    print("=" * 60)
    print("Test: Extraction Agent")
    print("=" * 60)
    
    from agents.extraction_agent import extraction_agent
    
    sample_email = """
    Subject: Your TNEB Electricity Bill - June 2025
    
    Dear Customer,
    
    Your electricity bill for June 2025 is ready.
    
    Bill Amount: ₹1,245
    Billing Period: 01-Jun-2025 to 30-Jun-2025
    Due Date: 15-Jul-2025
    Consumer Number: 123456789
    
    Please pay before the due date to avoid late fees.
    
    Thank you,
    TNEB
    """
    
    print("\nSample Email:")
    print(sample_email)
    
    print("\nExtracting data...")
    
    fields = ["bill_amount", "billing_period", "due_date", "provider"]
    result = await extraction_agent.extract(
        text=sample_email,
        fields=fields,
        extraction_type="bill"
    )
    
    print("\nExtracted Data:")
    for field, data in result.get('extracted_data', {}).items():
        if isinstance(data, dict):
            print(f"  {field}: {data.get('value')} (confidence: {data.get('confidence')})")
        else:
            print(f"  {field}: {data}")
    
    print()


async def test_validation():
    """Test validator agent"""
    print("=" * 60)
    print("Test: Validator Agent")
    print("=" * 60)
    
    from agents.validator_agent import validator_agent
    
    source_text = "Your electricity bill is ₹1,245 for June 2025"
    
    # Test valid data
    extracted_data = {
        "amount": {"value": "₹1,245", "confidence": 0.95},
        "period": {"value": "June 2025", "confidence": 0.9}
    }
    
    print("\nValidating extracted data...")
    print(f"Source: {source_text}")
    print(f"Data: {extracted_data}")
    
    result = await validator_agent.validate(
        extracted_data=extracted_data,
        source_text=source_text,
        validation_type="bill",
        strict=True
    )
    
    print(f"\nValidation Result:")
    print(f"  Valid: {result.is_valid}")
    print(f"  Confidence: {result.confidence}")
    print(f"  Issues: {result.issues if result.issues else 'None'}")
    print(f"  Warnings: {result.warnings if result.warnings else 'None'}")
    
    print()


async def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MULTI-AGENT SYSTEM TEST SUITE")
    print("=" * 60 + "\n")
    
    await test_basic_conversation()
    await test_planning()
    await test_extraction()
    await test_validation()
    # await test_email_query()  # Requires Gmail auth
    
    print("=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == '__main__':
    asyncio.run(run_all_tests())
