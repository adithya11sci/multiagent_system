"""
Passenger Intelligence Agent - RAG-Powered Assistance
Handles passenger queries, alternative suggestions, and policy information
"""
import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json
from config import GEMINI_API_KEY, AGENT_CONFIG
from rag.rag_system import RAGSystem

class PassengerAgent:
    """
    Responsible for:
    - Answering passenger queries
    - Suggesting alternative trains
    - Explaining refund & rescheduling rules
    
    Uses RAG for:
    - Timetables
    - Railway policies
    - Refund rules
    - Route maps
    """
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(AGENT_CONFIG["passenger"]["model"])
        self.rag_system = RAGSystem()
        
    def answer_query(self, query: str, passenger_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Answer passenger query using RAG
        
        Args:
            query: Passenger question
            passenger_context: Booking details, preferences, etc.
            
        Returns:
            Answer with relevant information and suggestions
        """
        # Retrieve relevant context from RAG
        rag_context = self.rag_system.retrieve(query, top_k=5)
        
        prompt = f"""
You are the Passenger Intelligence Agent for a railway system.
Your role is to assist passengers with accurate, helpful information.

PASSENGER QUERY: {query}

PASSENGER CONTEXT:
{json.dumps(passenger_context or {}, indent=2)}

RELEVANT INFORMATION FROM KNOWLEDGE BASE:
{json.dumps(rag_context, indent=2)}

Provide a helpful response that includes:
1. Direct answer to the query
2. Alternative options if applicable
3. Relevant policies or rules
4. Actionable next steps

Respond in JSON format:
{{
    "answer": "Main answer to the query",
    "alternatives": [
        {{
            "option": "Description",
            "details": "Specifics",
            "recommendation_score": 0.9
        }}
    ],
    "policies": [
        {{
            "rule": "Policy name",
            "description": "What it means",
            "applies": true
        }}
    ],
    "next_steps": ["Step 1", "Step 2"],
    "confidence": 0.95
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            answer = self._parse_response(response.text)
            
            # Add metadata
            answer["query"] = query
            answer["rag_sources"] = [doc.get("source", "unknown") for doc in rag_context]
            
            return answer
        except Exception as e:
            return {
                "error": str(e),
                "query": query,
                "answer": "I apologize, but I encountered an error processing your query."
            }
    
    def suggest_alternatives(self, original_train: str, passenger_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest alternative trains when original is delayed/cancelled
        """
        # Get origin and destination
        origin = passenger_context.get("origin", "")
        destination = passenger_context.get("destination", "")
        travel_date = passenger_context.get("travel_date", "")
        
        # Retrieve alternative trains from RAG
        query = f"Alternative trains from {origin} to {destination} on {travel_date}"
        alternatives = self.rag_system.retrieve(query, top_k=10)
        
        prompt = f"""
You are the Passenger Intelligence Agent. A passenger's train is affected.

ORIGINAL TRAIN: {original_train}
ORIGIN: {origin}
DESTINATION: {destination}
TRAVEL DATE: {travel_date}

PASSENGER CONTEXT:
{json.dumps(passenger_context, indent=2)}

AVAILABLE ALTERNATIVES:
{json.dumps(alternatives, indent=2)}

Suggest the best alternative trains considering:
1. Similar arrival time
2. Seat availability
3. Fare difference
4. Connection convenience
5. Passenger preferences

Respond in JSON format with ranked alternatives:
{{
    "alternatives": [
        {{
            "train_number": "12345",
            "train_name": "Express",
            "departure": "10:30",
            "arrival": "18:45",
            "fare_difference": "+150",
            "seats_available": "Yes",
            "recommendation_score": 0.95,
            "pros": ["Faster", "Direct"],
            "cons": ["Higher fare"],
            "booking_action": "Can be booked immediately"
        }}
    ],
    "refund_eligible": true,
    "refund_amount": 1200,
    "auto_rebooking_available": true
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            return {"error": str(e)}
    
    def explain_refund_policy(self, ticket_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Explain refund policy for a specific ticket
        """
        # Retrieve refund rules from RAG
        refund_rules = self.rag_system.retrieve("refund policy rules", top_k=5)
        
        prompt = f"""
You are the Passenger Intelligence Agent. Explain the refund policy.

TICKET CONTEXT:
{json.dumps(ticket_context, indent=2)}

REFUND RULES:
{json.dumps(refund_rules, indent=2)}

Provide clear explanation of:
1. Eligibility for refund
2. Refund amount calculation
3. Processing time
4. How to claim

Be specific and accurate based on the rules.
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
