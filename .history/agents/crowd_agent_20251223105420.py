"""
Crowd & Capacity Agent - Crowd Prediction and Load Balancing
Handles overcrowding prediction and capacity management
"""
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from config import GEMINI_API_KEY, AGENT_CONFIG
from tools.crowd_predictor import CrowdPredictor
from tools.booking_analyzer import BookingAnalyzer

class CrowdAgent:
    """
    Responsible for:
    - Predicting overcrowding
    - Identifying risk stations
    - Suggesting coach reallocation or extra services
    
    Inputs:
    - Ticket bookings
    - Historical crowd data
    - Time-based demand patterns
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(AGENT_CONFIG["crowd"]["model"])
        self.crowd_predictor = CrowdPredictor()
        self.booking_analyzer = BookingAnalyzer()
        
    def predict_overcrowding(self, train_number: str, travel_date: str) -> Dict[str, Any]:
        """
        Predict overcrowding for a specific train
        
        Args:
            train_number: Train identifier
            travel_date: Date of travel
            
        Returns:
            Overcrowding prediction with recommendations
        """
        # Get booking data
        bookings = self.booking_analyzer.get_bookings(train_number, travel_date)
        
        # Get historical crowd patterns
        historical = self.crowd_predictor.get_historical_patterns(train_number)
        
        # Predict crowd levels
        prediction = self.crowd_predictor.predict(train_number, travel_date)
        
        prompt = f"""
You are the Crowd & Capacity Agent for a railway intelligence system.

TRAIN: {train_number}
DATE: {travel_date}

CURRENT BOOKINGS:
{json.dumps(bookings, indent=2)}

HISTORICAL CROWD PATTERNS:
{json.dumps(historical, indent=2)}

CROWD PREDICTION:
{json.dumps(prediction, indent=2)}

Analyze and provide:
1. Overcrowding Risk Assessment
   - Overall capacity utilization
   - Critical segments/stations
   - Peak demand periods
   
2. Station-wise Analysis
   - High-risk boarding stations
   - Expected boarding/alighting counts
   - Platform congestion risk
   
3. Recommendations
   - Add extra coaches?
   - Run special service?
   - Redistribute passengers?
   - Enhanced crowd management at stations

Respond in JSON format:
{{
    "overall_risk": "low|medium|high|critical",
    "capacity_utilization": 0.85,
    "critical_stations": [
        {{
            "station": "Station name",
            "boarding_count": 450,
            "capacity": 400,
            "risk_level": "high",
            "expected_time": "10:30"
        }}
    ],
    "segment_analysis": [
        {{
            "from_station": "A",
            "to_station": "B",
            "occupancy": 0.95,
            "risk": "overcrowded"
        }}
    ],
    "recommendations": [
        {{
            "action": "Add 2 extra coaches",
            "priority": "high",
            "impact": "Increases capacity by 200 passengers",
            "cost_estimate": "Medium",
            "implementation_time": "2 hours"
        }}
    ],
    "passenger_distribution": {{
        "sleeper": 0.9,
        "ac_3tier": 1.0,
        "ac_2tier": 0.7
    }}
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            analysis = self._parse_response(response.text)
            
            # Add metadata
            analysis["train_number"] = train_number
            analysis["travel_date"] = travel_date
            analysis["analyzed_at"] = datetime.now().isoformat()
            
            return analysis
        except Exception as e:
            return {
                "error": str(e),
                "train_number": train_number,
                "travel_date": travel_date
            }
    
    def analyze_station_crowd(self, station: str, time_window: tuple) -> Dict[str, Any]:
        """
        Analyze crowd levels at a specific station
        """
        crowd_data = self.crowd_predictor.get_station_crowd(station, time_window)
        
        prompt = f"""
You are the Crowd & Capacity Agent. Analyze station crowd levels.

STATION: {station}
TIME WINDOW: {time_window[0]} to {time_window[1]}

CROWD DATA:
{json.dumps(crowd_data, indent=2)}

Provide:
1. Current crowd status
2. Peak times
3. Platform-wise distribution
4. Safety concerns
5. Crowd management recommendations

Respond in JSON format.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    def suggest_load_balancing(self, affected_trains: List[str]) -> Dict[str, Any]:
        """
        Suggest load balancing across multiple trains
        """
        trains_data = []
        for train in affected_trains:
            bookings = self.booking_analyzer.get_bookings(train, datetime.now().strftime("%Y-%m-%d"))
            trains_data.append({
                "train": train,
                "bookings": bookings
            })
        
        prompt = f"""
You are the Crowd & Capacity Agent. Suggest load balancing strategies.

TRAINS DATA:
{json.dumps(trains_data, indent=2)}

Suggest how to:
1. Redistribute passengers across trains
2. Adjust timings to spread demand
3. Run special services if needed
4. Incentivize passengers to switch trains

Provide detailed, actionable recommendations in JSON format.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            return {"error": str(e)}
    
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
