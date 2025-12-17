"""
LangChain Orchestrator - The Brain
Coordinates all agents and executes plans
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from agents.planner_agent import planner_agent
from agents.extraction_agent import extraction_agent
from agents.validator_agent import validator_agent
from mcp.tool_layer import mcp_registry
from mcp.tools.email_tool import EmailTool
from context.context_protocol import UserContext, ConversationState
from memory.memory_manager import memory_manager
from config import settings


class OrchestrationResult:
    """Result of orchestration"""
    def __init__(
        self,
        success: bool,
        response: str,
        metadata: Optional[Dict[str, Any]] = None,
        executed_steps: Optional[List[Dict[str, Any]]] = None
    ):
        self.success = success
        self.response = response
        self.metadata = metadata or {}
        self.executed_steps = executed_steps or []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "response": self.response,
            "metadata": self.metadata,
            "executed_steps": self.executed_steps
        }


class LangChainOrchestrator:
    """
    Central Orchestrator - The Brain of the System
    
    Coordinates:
    1. Planner Agent - Creates plans
    2. Tool Agents - Execute via MCP
    3. Memory - Maintains context
    4. Validation - Ensures accuracy
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0.3
        )
        
        # Register MCP tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all MCP tools"""
        email_tool = EmailTool()
        mcp_registry.register_tool(email_tool)
        # Add more tools as needed
    
    async def process_message(
        self,
        user_message: str,
        context: UserContext
    ) -> OrchestrationResult:
        """
        Main orchestration flow
        
        Steps:
        1. Get memory snapshot
        2. Planner creates execution plan
        3. Execute plan step-by-step
        4. Validate results
        5. Generate response
        6. Update memory
        """
        try:
            # Step 1: Get memory snapshot
            memory_snapshot = None
            if settings.enable_memory:
                memory_snapshot = memory_manager.get_memory_snapshot(context.user_id)
            
            # Step 2: Planner creates plan
            plan = await planner_agent.plan(user_message, context, memory_snapshot)
            
            # Check if clarification needed
            if plan.get("requires_clarification"):
                questions = plan.get("clarification_questions", [])
                return OrchestrationResult(
                    success=False,
                    response=self._format_clarification_questions(questions),
                    metadata={"needs_clarification": True, "plan": plan}
                )
            
            # Step 3: Execute plan
            execution_results = await self._execute_plan(plan, context)
            
            # Step 4: Check if re-planning needed
            if self._needs_replanning(execution_results):
                # Agentic loop - replan and retry
                new_plan = await planner_agent.replan(
                    plan, execution_results, user_message, context
                )
                execution_results = await self._execute_plan(new_plan, context)
            
            # Step 5: Generate final response
            response = await self._generate_response(
                user_message, plan, execution_results, context
            )
            
            # Step 6: Update memory
            if settings.enable_memory:
                memory_manager.add_interaction(
                    user_id=context.user_id,
                    user_message=user_message,
                    assistant_message=response,
                    metadata={
                        "plan": plan,
                        "execution_results": execution_results
                    }
                )
            
            # Update context state
            context.update_state(ConversationState.COMPLETED)
            
            return OrchestrationResult(
                success=True,
                response=response,
                metadata={
                    "plan": plan,
                    "execution_results": execution_results
                },
                executed_steps=execution_results
            )
            
        except Exception as e:
            context.update_state(ConversationState.ERRORED)
            return OrchestrationResult(
                success=False,
                response=f"I encountered an error: {str(e)}",
                metadata={"error": str(e)}
            )
    
    async def _execute_plan(
        self,
        plan: Dict[str, Any],
        context: UserContext
    ) -> List[Dict[str, Any]]:
        """Execute plan step by step"""
        execution_results = []
        execution_plan = plan.get("execution_plan", [])
        
        for step in execution_plan:
            step_num = step.get("step", 0)
            agent_name = step.get("agent", "")
            tool_name = step.get("tool", "")
            action = step.get("action", "")
            parameters = step.get("parameters", {})
            
            print(f"Executing Step {step_num}: {action}")
            
            try:
                # Execute based on agent/tool
                if tool_name and tool_name.startswith("email"):
                    # Email tool
                    result = await mcp_registry.execute_tool(
                        tool_name, context, parameters
                    )
                elif "extraction" in agent_name.lower():
                    # Extraction agent
                    text = parameters.get("text", "")
                    fields = parameters.get("fields", [])
                    extraction_type = parameters.get("type", "general")
                    
                    result = await extraction_agent.extract(
                        text, fields, extraction_type
                    )
                elif "validator" in agent_name.lower():
                    # Validator agent
                    data = parameters.get("data", {})
                    source = parameters.get("source", "")
                    validation_type = parameters.get("type", "general")
                    
                    validation_result = await validator_agent.validate(
                        data, source, validation_type
                    )
                    result = validation_result.to_dict()
                else:
                    result = {"error": f"Unknown agent/tool: {agent_name}/{tool_name}"}
                
                execution_results.append({
                    "step": step_num,
                    "action": action,
                    "status": "success" if not result.get("error") else "failed",
                    "result": result
                })
                
            except Exception as e:
                execution_results.append({
                    "step": step_num,
                    "action": action,
                    "status": "error",
                    "error": str(e)
                })
        
        return execution_results
    
    def _needs_replanning(self, execution_results: List[Dict[str, Any]]) -> bool:
        """Check if any steps failed and need replanning"""
        for result in execution_results:
            if result.get("status") in ["failed", "error"]:
                return True
        return False
    
    async def _generate_response(
        self,
        user_message: str,
        plan: Dict[str, Any],
        execution_results: List[Dict[str, Any]],
        context: UserContext
    ) -> str:
        """Generate final user-facing response"""
        # Build context from execution results
        results_summary = self._summarize_execution_results(execution_results)
        
        messages = [
            SystemMessage(content="""You are a helpful assistant that provides clear, concise answers based on factual data.

Rules:
1. Only use information from the execution results
2. Do NOT hallucinate or make up information
3. If data is missing, say so clearly
4. Be conversational but accurate
5. Format for WhatsApp (short, clear)
6. Include relevant details (amounts, dates, etc.)
"""),
            HumanMessage(content=f"""User Question: "{user_message}"

Execution Results:
{results_summary}

Generate a clear, accurate response for the user.""")
        ]
        
        response = await self.llm.apredict_messages(messages)
        return response.content
    
    def _summarize_execution_results(
        self,
        execution_results: List[Dict[str, Any]]
    ) -> str:
        """Summarize execution results for response generation"""
        summary_parts = []
        
        for result in execution_results:
            step = result.get("step", 0)
            action = result.get("action", "")
            status = result.get("status", "")
            
            if status == "success":
                result_data = result.get("result", {})
                summary_parts.append(f"Step {step} ({action}): {result_data}")
            else:
                error = result.get("error", "Unknown error")
                summary_parts.append(f"Step {step} ({action}): Failed - {error}")
        
        return "\n".join(summary_parts)
    
    def _format_clarification_questions(self, questions: List[str]) -> str:
        """Format clarification questions for user"""
        if not questions:
            return "I need more information to help you."
        
        if len(questions) == 1:
            return questions[0]
        
        formatted = "I need some clarification:\n"
        for i, question in enumerate(questions, 1):
            formatted += f"{i}. {question}\n"
        
        return formatted


# Global orchestrator instance
orchestrator = LangChainOrchestrator()
