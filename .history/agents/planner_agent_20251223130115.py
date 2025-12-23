"""
Planner Agent - Master Brain
Responsible for task decomposition and decision-making
"""
import google.generativeai as genai
from typing import Dict, List, Any
import json
from config import GEMINI_API_KEY, AGENT_CONFIG

class PlannerAgent:
    """
    Master brain that understands requests, breaks them into subtasks,
    and decides which agents to invoke
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(AGENT_CONFIG["planner"]["model"])
        self.global_state = {}
        
    def analyze_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze incoming request and create execution plan
        
        Args:
            request: User/system request (e.g., "Train 12627 delayed by 45 minutes")
            context: Additional context information
            
        Returns:
            Execution plan with subtasks and agent assignments
        """
        prompt = f"""
You are the Planner Agent - the master brain of a railway intelligence system.

Analyze this request and create an execution plan:
REQUEST: {request}

CONTEXT: {json.dumps(context or {}, indent=2)}

Available Agents:
1. Operations Agent - Train operations, delay propagation, schedule adjustments
2. Passenger Agent - Passenger queries, alternative trains, refund/reschedule rules
3. Crowd Agent - Overcrowding prediction, load balancing, capacity management
4. Alert Agent - Send notifications, trigger automated actions

Your task:
1. Understand the request
2. Break it into subtasks
3. Assign each subtask to appropriate agent(s)
4. Define execution order (sequential or parallel)
5. Specify data requirements for each subtask

Respond in JSON format:
{{
    "request_type": "delay|query|alert|capacity",
    "priority": "high|medium|low",
    "subtasks": [
        {{
            "task_id": "1",
            "description": "Task description",
            "agent": "operations|passenger|crowd|alert",
            "dependencies": ["task_id"],
            "execution_type": "sequential|parallel",
            "inputs": {{}}
        }}
    ],
    "expected_outcome": "What should be achieved"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            plan = self._parse_response(response.text)
            
            # Update global state
            self.global_state["current_plan"] = plan
            self.global_state["request"] = request
            self.global_state["context"] = context
            
            return plan
        except Exception as e:
            return {
                "error": str(e),
                "request_type": "error",
                "subtasks": []
            }
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response and extract JSON"""
        try:
            # Extract JSON from markdown code blocks if present
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_str = response_text[json_start:json_end].strip()
            else:
                json_str = response_text.strip()
            
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback: try to parse the entire response
            try:
                return json.loads(response_text)
            except:
                return {"error": "Failed to parse response", "raw": response_text}
    
    def update_state(self, task_id: str, result: Any):
        """Update global state with task results"""
        if "task_results" not in self.global_state:
            self.global_state["task_results"] = {}
        self.global_state["task_results"][task_id] = result
    
    def get_state(self) -> Dict[str, Any]:
        """Get current global state"""
        return self.global_state
    
    def refine_plan(self, feedback: str) -> Dict[str, Any]:
        """
        Refine execution plan based on feedback or intermediate results
        """
        current_plan = self.global_state.get("current_plan", {})
        task_results = self.global_state.get("task_results", {})
        
        prompt = f"""
You are the Planner Agent. Refine the current execution plan based on feedback.

CURRENT PLAN: {json.dumps(current_plan, indent=2)}
TASK RESULTS SO FAR: {json.dumps(task_results, indent=2)}
FEEDBACK: {feedback}

Provide an updated execution plan in the same JSON format, adjusting:
- Remaining subtasks
- Agent assignments
- Dependencies
- Priorities

Only include tasks that haven't been completed yet.
"""
        
        try:
            response = self.model.generate_content(prompt)
            refined_plan = self._parse_response(response.text)
            self.global_state["current_plan"] = refined_plan
            return refined_plan
        except Exception as e:
            return {"error": str(e), "original_plan": current_plan}
