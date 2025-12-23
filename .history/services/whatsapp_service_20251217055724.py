"""
WhatsApp Service
Handles WhatsApp message sending via Twilio
"""
from typing import Dict, Any, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from config import settings


class WhatsAppService:
    """
    WhatsApp messaging service using Twilio
    """
    
    def __init__(self):
        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token
        )
        self.from_number = settings.twilio_whatsapp_number
    
    def send_message(
        self,
        to_number: str,
        message: str,
        media_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send WhatsApp message
        
        Args:
            to_number: Recipient's WhatsApp number (format: whatsapp:+1234567890)
            message: Message text
            media_url: Optional media URL to attach
        
        Returns:
            Dict with status and message SID
        """
        try:
            # Ensure number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            # Send message
            message_params = {
                'from_': self.from_number,
                'to': to_number,
                'body': message
            }
            
            if media_url:
                message_params['media_url'] = [media_url]
            
            twilio_message = self.client.messages.create(**message_params)
            
            return {
                "success": True,
                "message_sid": twilio_message.sid,
                "status": twilio_message.status,
                "to": to_number
            }
            
        except TwilioRestException as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": e.code
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_template_message(
        self,
        to_number: str,
        template_name: str,
        template_params: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Send WhatsApp template message (for notifications)
        
        Args:
            to_number: Recipient's number
            template_name: Approved template name
            template_params: Template parameter values
        """
        # Template messages require pre-approval from WhatsApp
        # This is a placeholder for template functionality
        try:
            # Format template content
            message_body = self._format_template(template_name, template_params)
            
            return self.send_message(to_number, message_body)
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_template(
        self,
        template_name: str,
        params: Dict[str, str]
    ) -> str:
        """Format template with parameters"""
        # Simple template formatting
        # In production, use WhatsApp-approved templates
        templates = {
            "bill_notification": "Your {bill_type} bill for {period} is {amount}. Due date: {due_date}",
            "confirmation": "Your request has been processed. {details}",
            "error": "We encountered an issue: {error_message}. Please try again."
        }
        
        template = templates.get(template_name, "{message}")
        return template.format(**params)
    
    def get_message_status(self, message_sid: str) -> Dict[str, Any]:
        """Get status of sent message"""
        try:
            message = self.client.messages(message_sid).fetch()
            
            return {
                "success": True,
                "sid": message.sid,
                "status": message.status,
                "to": message.to,
                "from": message.from_,
                "date_sent": str(message.date_sent),
                "error_code": message.error_code,
                "error_message": message.error_message
            }
            
        except TwilioRestException as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global WhatsApp service instance
whatsapp_service = WhatsAppService()
