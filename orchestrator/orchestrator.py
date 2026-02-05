"""
LangGraph Orchestrator - Multi-Agent Coordination
Orchestrates agent execution using LangGraph state machine
"""
from typing import Dict, Any, List, TypedDict, Annotated
try:
    from langgraph.graph import StateGraph, END
except ImportError:
    print("❌ LangGraph not found. Orchestrator will fail.")
    # We could implement a mock StateGraph here if needed, but for now let's hope it's installed
    pass

import operator
from agents import (
    PlannerAgent, OperationsAgent, PassengerAgent, 
    AlertAgent
)

class AgentState(TypedDict):
    """State shared across all agents"""
    request: str
    context: Dict[str, Any]
    plan: Dict[str, Any]
    operations_result: Annotated[List[Dict], operator.add]
    passenger_result: Annotated[List[Dict], operator.add]
    alert_result: Annotated[List[Dict], operator.add]
    final_response: Dict[str, Any]
    iteration: int
    max_iterations: int

class RailwayOrchestrator:
    """
    Orchestrates multiple agents using LangGraph
    Manages execution flow, dependencies, and state
    """
    
    def __init__(self):
        # Initialize all agents
        self.planner = PlannerAgent()
        self.operations = OperationsAgent()
        self.passenger = PassengerAgent()
        self.alert = AlertAgent()
        
        # Build the graph
        self.workflow = self._build_workflow()
        
    def _build_workflow(self) -> StateGraph:
        """
        Build the LangGraph workflow
        """
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("operations", self._operations_node)
        workflow.add_node("passenger", self._passenger_node)
        workflow.add_node("alert", self._alert_node)
        workflow.add_node("synthesize", self._synthesize_node)
        
        # Set entry point
        workflow.set_entry_point("planner")
        
        # Define edges based on plan
        workflow.add_conditional_edges(
            "planner",
            self._route_from_planner,
            {
                "operations": "operations",
                "passenger": "passenger",
                "alert": "alert",
                "end": END
            }
        )
        
        # All agents flow to synthesize
        workflow.add_edge("operations", "synthesize")
        workflow.add_edge("passenger", "synthesize")
        workflow.add_edge("alert", "synthesize")
        
        # Synthesize can loop back to planner or end
        workflow.add_conditional_edges(
            "synthesize",
            self._should_continue,
            {
                "continue": "planner",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def _planner_node(self, state: AgentState) -> AgentState:
        """
        Planner agent node - creates execution plan
        """
        if state.get("iteration", 0) == 0:
            # Initial planning
            plan = self.planner.analyze_request(
                state["request"], 
                state.get("context", {})
            )
        else:
            # Refine plan based on results
            feedback = self._generate_feedback(state)
            plan = self.planner.refine_plan(feedback)
        
        state["plan"] = plan
        state["iteration"] = state.get("iteration", 0) + 1
        return state
    
    def _operations_node(self, state: AgentState) -> AgentState:
        """
        Operations agent node - handles train operations
        """
        plan = state["plan"]
        operations_tasks = [
            task for task in plan.get("subtasks", [])
            if task.get("agent", "").lower() == "operations"
        ]
        
        results = []
        for task in operations_tasks:
            if "delay" in task.get("description", "").lower():
                # Handle delay analysis
                train_number = task.get("inputs", {}).get("train_number", "")
                delay_minutes = task.get("inputs", {}).get("delay_minutes", 0)
                result = self.operations.analyze_delay(train_number, delay_minutes)
            else:
                result = {"task": task["description"], "status": "completed"}
            
            results.append(result)
            
            # Update planner state
            self.planner.update_state(task["task_id"], result)
        
        state["operations_result"] = results
        return state
    
    def _passenger_node(self, state: AgentState) -> AgentState:
        """
        Passenger agent node - handles passenger queries
        """
        plan = state["plan"]
        passenger_tasks = [
            task for task in plan.get("subtasks", [])
            if task.get("agent", "").lower() == "passenger"
        ]
        
        results = []
        for task in passenger_tasks:
            task_desc = task.get("description", "").lower()
            
            if "alternative" in task_desc:
                # Suggest alternatives
                train = task.get("inputs", {}).get("train_number", "")
                context = task.get("inputs", {}).get("passenger_context", {})
                result = self.passenger.suggest_alternatives(train, context)
            elif "query" in task_desc or "question" in task_desc:
                # Answer query
                query = task.get("inputs", {}).get("query", "")
                result = self.passenger.answer_query(query)
            else:
                result = {"task": task["description"], "status": "completed"}
            
            results.append(result)
            self.planner.update_state(task["task_id"], result)
        
        state["passenger_result"] = results
        return state
    

    def _alert_node(self, state: AgentState) -> AgentState:
        """
        Alert agent node - handles notifications
        """
        plan = state["plan"]
        alert_tasks = [
            task for task in plan.get("subtasks", [])
            if task.get("agent", "").lower() == "alert"
        ]
        
        results = []
        for task in alert_tasks:
            alert_type = task.get("inputs", {}).get("alert_type", "general")
            target = task.get("inputs", {}).get("target_audience", "passengers")
            context = task.get("inputs", {}).get("context", {})
            
            result = self.alert.create_alert(alert_type, target, context)
            results.append(result)
            self.planner.update_state(task["task_id"], result)
        
        state["alert_result"] = results
        return state
    
    def _synthesize_node(self, state: AgentState) -> AgentState:
        """
        Synthesize results from all agents
        """
        final_response = {
            "request": state["request"],
            "plan": state["plan"],
            "results": {
                "operations": state.get("operations_result", []),
                "passenger": state.get("passenger_result", []),
                "alert": state.get("alert_result", [])
            },
            "status": "completed",
            "iteration": state["iteration"]
        }
        
        state["final_response"] = final_response
        return state
    
    def _route_from_planner(self, state: AgentState) -> str:
        """
        Route to appropriate agent based on plan
        """
        plan = state.get("plan", {})
        subtasks = plan.get("subtasks", [])
        
        if not subtasks:
            return "end"
        
        # Get the first uncompleted task
        for task in subtasks:
            agent = task.get("agent", "").lower()
            if agent in ["operations", "passenger", "alert"]:
                return agent
        
        return "end"
    
    def _should_continue(self, state: AgentState) -> str:
        """
        Decide whether to continue or end
        """
        iteration = state.get("iteration", 0)
        max_iterations = state.get("max_iterations", 3)
        
        if iteration >= max_iterations:
            return "end"
        
        plan = state.get("plan", {})
        remaining_tasks = [
            task for task in plan.get("subtasks", [])
            if task.get("status") != "completed"
        ]
        
        if not remaining_tasks:
            return "end"
        
        return "continue"
    
    def _generate_feedback(self, state: AgentState) -> str:
        """
        Generate feedback for plan refinement
        """
        results = state.get("final_response", {}).get("results", {})
        feedback_parts = []
        
        for agent, agent_results in results.items():
            if agent_results:
                feedback_parts.append(f"{agent}: {len(agent_results)} tasks completed")
        
        return "; ".join(feedback_parts)
    
    def run(self, request: str, context: Dict[str, Any] = None, 
            max_iterations: int = 3) -> Dict[str, Any]:
        """
        Run the orchestrator with a request
        
        Args:
            request: User/system request
            context: Additional context
            max_iterations: Maximum refinement iterations
            
        Returns:
            Final response with all agent results
        """
        initial_state: AgentState = {
            "request": request,
            "context": context or {},
            "plan": {},
            "operations_result": [],
            "passenger_result": [],
            "alert_result": [],
            "final_response": {},
            "iteration": 0,
            "max_iterations": max_iterations
        }
        
        # Execute the workflow
        final_state = self.workflow.invoke(initial_state)
        
        return final_state.get("final_response", {})
