"""
Operations Agent - Train Operations Intelligence
Handles train schedules, delay propagation, and operational decisions
"""
import os
from config import AGENT_CONFIG, MOCK_MODE
from utils.llm_client import LLMClient

from typing import Dict, List, Any, Optional
import json
from datetime import datetime, timedelta
from config import GEMINI_API_KEY, AGENT_CONFIG
from tools.train_schedule_tool import TrainScheduleTool
from tools.delay_simulator import DelaySimulator

class OperationsAgent:
    """
    Responsible for:
    - Reading train schedule data
    - Detecting delay propagation
    - Suggesting platform or schedule adjustments
    """
    
    def __init__(self):
        if not MOCK_MODE:
            try:
                self.model = LLMClient(AGENT_CONFIG["operations"])
            except:
                self.model = None
        else:
            self.model = None
        self.schedule_tool = TrainScheduleTool()
        self.delay_simulator = DelaySimulator()
        
    def analyze_delay(self, train_number: str, delay_minutes: int, 
                     current_location: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze delay impact and propagation
        
        Args:
            train_number: Train identifier
            delay_minutes: Delay in minutes
            current_location: Current station (optional)
            
        Returns:
            Analysis with impact assessment and recommendations
        """
        # Get train schedule
        schedule = self.schedule_tool.get_train_schedule(train_number)
        
        # Simulate delay propagation
        propagation = self.delay_simulator.simulate_delay(
            train_number, delay_minutes, current_location
        )
        
        prompt = f"""
You are the Operations Agent for a railway intelligence system.

TRAIN: {train_number}
DELAY: {delay_minutes} minutes
CURRENT LOCATION: {current_location or 'Unknown'}

SCHEDULE DATA:
{json.dumps(schedule, indent=2)}

DELAY PROPAGATION SIMULATION:
{json.dumps(propagation, indent=2)}

Analyze the situation and provide:
1. Impact Assessment
   - Affected stations and arrival times
   - Connected trains that might be impacted
   - Platform conflicts
   
2. Operational Recommendations
   - Should the train skip any stations?
   - Platform reallocation needed?
   - Should connected trains be held?
   - Alternative routing options
   
3. Cascading Effects
   - Other trains affected by this delay
   - Platform availability issues
   - Crew scheduling impacts

Respond in JSON format:
{{
    "impact_summary": "Brief summary",
    "severity": "low|medium|high|critical",
    "affected_stations": [
        {{
            "station": "Station name",
            "original_time": "HH:MM",
            "new_time": "HH:MM",
            "delay": 45
        }}
    ],
    "connected_trains": [
        {{
            "train_number": "12345",
            "connection_station": "Station",
            "risk": "missed|tight|safe",
            "recommendation": "hold|inform|no_action"
        }}
    ],
    "recommendations": [
        {{
            "action": "Description",
            "priority": "high|medium|low",
            "reason": "Why this action"
        }}
    ],
    "platform_changes": [
        {{
            "station": "Station",
            "current_platform": "1",
            "suggested_platform": "3",
            "reason": "Conflict with train X"
        }}
    ]
}}
"""
        
        if MOCK_MODE or not self.model:
            return {
                "impact_summary": f"Mock Analysis for train {train_number}",
                "severity": "medium",
                "affected_stations": [{"station": "Station A", "delay": delay_minutes}],
                "recommendations": [{"action": "Inform passengers", "priority": "high"}]
            }

        try:
            response = self.model.generate_content(prompt)
            analysis = self._parse_response(response.text)
            
            # Add metadata
            analysis["train_number"] = train_number
            analysis["delay_minutes"] = delay_minutes
            analysis["analyzed_at"] = datetime.now().isoformat()
            
            return analysis
        except Exception as e:
            return {
                "error": str(e),
                "train_number": train_number,
                "delay_minutes": delay_minutes
            }
    
    def suggest_schedule_adjustment(self, trains_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Suggest schedule adjustments for multiple trains
        """
        prompt = f"""
You are the Operations Agent. Multiple trains are experiencing issues.

TRAINS DATA:
{json.dumps(trains_data, indent=2)}

Suggest optimal schedule adjustments that:
1. Minimize overall passenger impact
2. Prevent cascading delays
3. Optimize platform usage
4. Consider crew scheduling

Provide comprehensive recommendations in JSON format.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    def check_platform_availability(self, station: str, time_window: tuple) -> Dict[str, Any]:
        """
        Check platform availability at a station
        """
        availability = self.schedule_tool.get_platform_availability(
            station, time_window
        )
        return availability
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response and extract JSON"""
        try:
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
            try:
                return json.loads(response_text)
            except:
                return {"error": "Failed to parse response", "raw": response_text}
