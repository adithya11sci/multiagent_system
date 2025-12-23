"""
Planner Agent
The brain of the system - understands intent and creates execution plans
"""
from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json

from context.context_protocol import UserContext
from memory.memory_manager import memory_manager
from config import settings


class PlannerAgent:
    """
    Planner Agent - Most Important Agent
    
    Responsibilities:
    1. Understand user intent
    2. Break down tasks into steps
    3. Decide which tools/agents are needed
    4. Create execution plan
    5. No tool execution - only reasoning
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.2
        )
        
        self.system_prompt = """You are the Planner Agent in a multi-agent system.

Your role is to:
1. Understand the user's intent from their message
2. Break down the task into clear, actionable steps
3. Identify which tools and agents are needed
4. Create a structured execution plan

Available Agents:
- Email Agent: Search and read emails
- Extraction Agent: Extract structured data from text/documents
- Validator Agent: Verify data authenticity and accuracy
- Database Agent: Query databases
- API Agent: Call external APIs

Available Tools (via MCP):
- email.read: Search and read user emails
- db.read: Query databases
- db.write: Write to databases
- api.call: Call external APIs
- file.read: Read files

Rules:
1. Do NOT execute any tools yourself
2. Only create a plan with steps
3. Be specific about what each step should do
4. Consider memory/context from previous conversations
5. Ensure steps are in logical order
6. Include validation steps to prevent hallucination

Output Format (JSON):
{
    "intent": "Clear description of user intent",
    "confidence": 0.95,
    "requires_clarification": false,
    "clarification_questions": [],
    "execution_plan": [
        {
            "step": 1,
            "agent": "Email Agent",
            "tool": "email.read",
            "action": "Search emails for 'electricity bill'",
            "parameters": {"query": "electricity bill", "max_results": 5},
            "expected_output": "List of email messages",
            "validation": "Check if emails found"
        }
    ],
    "estimated_complexity": "low|medium|high",
    "estimated_time": "2 seconds"
}
"""
    
    async def plan(
        self,
        user_message: str,
        context: UserContext,
        memory_snapshot: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create execution plan for user message
        """
        # Get memory context
        if not memory_snapshot and settings.enable_memory:
            memory_snapshot = memory_manager.get_memory_snapshot(context.user_id)
        
        # Build context for planning
        context_str = self._build_context_string(context, memory_snapshot)
        
        # Create prompt
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""User Context:
{context_str}

User Message: "{user_message}"

Create a detailed execution plan to fulfill this request.""")
        ]
        
        # Get plan from LLM
        response = await self.llm.apredict_messages(messages)
        
        try:
            # Parse JSON response
            plan = json.loads(response.content)
            
            # Validate plan structure
            if not self._validate_plan(plan):
                return self._create_error_plan("Invalid plan structure")
            
            return plan
            
        except json.JSONDecodeError:
            # Fallback: Create basic plan
            return self._create_basic_plan(user_message, response.content)
    
    def _build_context_string(
        self,
        context: UserContext,
        memory_snapshot: Optional[Dict[str, Any]]
    ) -> str:
        """Build context string for planner"""
        context_parts = [
            f"User ID: {context.user_id}",
            f"Channel: {context.channel.value}",
            f"Permissions: {', '.join(context.permissions)}",
            f"Conversation State: {context.conversation_state.value}"
        ]
        
        if memory_snapshot:
            if memory_snapshot.get('summary'):
                context_parts.append(f"\nConversation Summary:\n{memory_snapshot['summary']}")
            
            if memory_snapshot.get('facts'):
                facts_str = "\n".join([f"- {f['fact']}" for f in memory_snapshot['facts'][:5]])
                context_parts.append(f"\nKnown Facts:\n{facts_str}")
        
        return "\n".join(context_parts)
    
    def _validate_plan(self, plan: Dict[str, Any]) -> bool:
        """Validate plan structure"""
        required_keys = ["intent", "execution_plan"]
        return all(key in plan for key in required_keys)
    
    def _create_basic_plan(
        self,
        user_message: str,
        llm_response: str
    ) -> Dict[str, Any]:
        """Create basic plan when JSON parsing fails"""
        return {
            "intent": "Process user request",
            "confidence": 0.7,
            "requires_clarification": False,
            "execution_plan": [
                {
                    "step": 1,
                    "agent": "General",
                    "action": "Process request",
                    "reasoning": llm_response
                }
            ],
            "estimated_complexity": "medium"
        }
    
    def _create_error_plan(self, error_message: str) -> Dict[str, Any]:
        """Create error plan"""
        return {
            "intent": "Error",
            "confidence": 0.0,
            "requires_clarification": True,
            "clarification_questions": [error_message],
            "execution_plan": [],
            "estimated_complexity": "unknown"
        }
    
    async def replan(
        self,
        original_plan: Dict[str, Any],
        execution_results: List[Dict[str, Any]],
        user_message: str,
        context: UserContext
    ) -> Dict[str, Any]:
        """
        Re-plan based on execution results (agentic loop)
        Used when initial plan fails or is incomplete
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""Original User Message: "{user_message}"

Original Plan:
{json.dumps(original_plan, indent=2)}

Execution Results:
{json.dumps(execution_results, indent=2)}

The execution had issues. Create a new plan to complete the task.""")
        ]
        
        response = await self.llm.apredict_messages(messages)
        
        try:
            new_plan = json.loads(response.content)
            return new_plan
        except json.JSONDecodeError:
            return self._create_error_plan("Could not create recovery plan")


# Global planner agent instance
planner_agent = PlannerAgent()
