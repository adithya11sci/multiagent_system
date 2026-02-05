"""
Alert & Action Agent - External Actions and Notifications
Handles sending alerts and triggering automated actions
"""
import os
from config import AGENT_CONFIG, MOCK_MODE
from utils.llm_client import LLMClient

from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from config import GEMINI_API_KEY, AGENT_CONFIG
from tools.notification_service import NotificationService

class AlertAgent:
    """
    Responsible for:
    - Sending alerts to passengers
    - Notifying admins
    - Triggering automated actions
    
    Tools:
    - SMS / Email API
    - App notification system
    """
    
    def __init__(self):
        if not MOCK_MODE:
            try:
                self.model = LLMClient(AGENT_CONFIG["alert"])
            except:
                 self.model = None
        else:
            self.model = None
        self.notification_service = NotificationService()
        
    def create_alert(self, alert_type: str, target_audience: str, 
                    context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create and send alert
        
        Args:
            alert_type: Type of alert (delay, cancellation, overcrowding, etc.)
            target_audience: Who to alert (specific passengers, all, admins)
            context: Alert context and details
            
        Returns:
            Alert details and delivery status
        """
        prompt = f"""
You are the Alert & Action Agent for a railway intelligence system.
Create an appropriate alert message.

ALERT TYPE: {alert_type}
TARGET AUDIENCE: {target_audience}

CONTEXT:
{json.dumps(context, indent=2)}

Create alert messages that are:
1. Clear and concise
2. Actionable
3. Empathetic to passenger concerns
4. Include relevant details
5. Provide next steps

For different channels (SMS, Email, App Notification), adjust the format.

Respond in JSON format:
{{
    "alert_id": "unique_id",
    "priority": "low|medium|high|critical",
    "channels": ["sms", "email", "app"],
    "messages": {{
        "sms": "Short SMS message (160 chars)",
        "email": {{
            "subject": "Email subject",
            "body": "Detailed email body"
        }},
        "app": {{
            "title": "Push notification title",
            "body": "Notification body",
            "action_button": "View Details"
        }}
    }},
    "target_criteria": {{
        "train_numbers": ["12627"],
        "stations": ["Station A", "Station B"],
        "booking_ids": []
    }},
    "automated_actions": [
        {{
            "action": "auto_refund|hold_train|reallocate",
            "trigger_condition": "if delay > 2 hours",
            "parameters": {{}}
        }}
    ]
}}
"""
        
        if MOCK_MODE or not self.model:
             return {
                 "alert_id": "mock_alert_1",
                 "messages": {"sms": f"Mock Alert: {alert_type}"},
                 "delivery_status": {"sms": {"sent": 1, "failed": 0}}
             }

        try:
            response = self.model.generate_content(prompt)
            alert_spec = self._parse_response(response.text)
            
            # Execute alert sending
            delivery_status = self._send_alert(alert_spec)
            
            alert_spec["delivery_status"] = delivery_status
            alert_spec["created_at"] = datetime.now().isoformat()
            
            return alert_spec
        except Exception as e:
            return {
                "error": str(e),
                "alert_type": alert_type,
                "target_audience": target_audience
            }
    
    def _send_alert(self, alert_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actually send the alert through various channels
        """
        delivery_status = {
            "sms": {"sent": 0, "failed": 0},
            "email": {"sent": 0, "failed": 0},
            "app": {"sent": 0, "failed": 0}
        }
        
        channels = alert_spec.get("channels", [])
        messages = alert_spec.get("messages", {})
        target_criteria = alert_spec.get("target_criteria", {})
        
        # Get target recipients
        recipients = self._get_recipients(target_criteria)
        
        # Send through each channel
        if "sms" in channels and messages.get("sms"):
            sms_result = self.notification_service.send_sms(
                recipients, messages["sms"]
            )
            delivery_status["sms"] = sms_result
        
        if "email" in channels and messages.get("email"):
            email_result = self.notification_service.send_email(
                recipients, 
                messages["email"]["subject"],
                messages["email"]["body"]
            )
            delivery_status["email"] = email_result
        
        if "app" in channels and messages.get("app"):
            app_result = self.notification_service.send_push_notification(
                recipients,
                messages["app"]["title"],
                messages["app"]["body"]
            )
            delivery_status["app"] = app_result
        
        return delivery_status
    
    def _get_recipients(self, target_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get list of recipients based on criteria
        """
        # This would query the database for matching passengers
        # For now, return mock data
        return [
            {
                "passenger_id": "P001",
                "name": "John Doe",
                "phone": "+1234567890",
                "email": "john@example.com"
            }
        ]
    
    def trigger_automated_action(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger automated actions based on conditions
        """
        prompt = f"""
You are the Alert & Action Agent. Execute an automated action.

ACTION: {action}
PARAMETERS:
{json.dumps(parameters, indent=2)}

Determine:
1. Pre-conditions to verify
2. Steps to execute
3. Rollback plan if needed
4. Success criteria

Respond in JSON format with execution plan.
"""
        
        try:
            response = self.model.generate_content(prompt)
            execution_plan = self._parse_response(response.text)
            
            # Execute the action
            result = self._execute_action(action, parameters, execution_plan)
            
            return {
                "action": action,
                "execution_plan": execution_plan,
                "result": result,
                "executed_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "action": action}
    
    def _execute_action(self, action: str, parameters: Dict[str, Any], 
                       execution_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the actual automated action
        """
        # This would integrate with various systems
        # For now, return mock result
        return {
            "status": "success",
            "message": f"Action {action} executed successfully"
        }
    
    def send_admin_notification(self, notification_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send notification to system administrators
        """
        message = f"ADMIN ALERT: {notification_type}\n\n{json.dumps(details, indent=2)}"
        
        result = self.notification_service.send_email(
            [{"email": "admin@railway.com"}],
            f"Railway System Alert: {notification_type}",
            message
        )
        
        return {
            "notification_type": notification_type,
            "delivery_status": result,
            "sent_at": datetime.now().isoformat()
        }
    
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
