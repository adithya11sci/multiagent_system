"""
Notification Service - Sends notifications via multiple channels
"""
from typing import Dict, Any, List
try:
    from twilio.rest import Client
    HAS_TWILIO = True
except ImportError:
    HAS_TWILIO = False

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER,
    SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD
)

class NotificationService:
    """
    Handles sending notifications through various channels:
    - SMS (Twilio)
    - Email (SMTP)
    - Push Notifications (simulated)
    """
    
    def __init__(self):
        # Initialize Twilio client if credentials are available
        self.twilio_client = None
        if HAS_TWILIO and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            try:
                self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            except Exception as e:
                print(f"Failed to initialize Twilio: {e}")
        elif not HAS_TWILIO:
            print("⚠️  Twilio not found. SMS notifications disabled.")

    
    def send_sms(self, recipients: List[Dict[str, Any]], message: str) -> Dict[str, Any]:
        """
        Send SMS to multiple recipients
        
        Args:
            recipients: List of recipient dicts with 'phone' field
            message: SMS message text
            
        Returns:
            Delivery status
        """
        sent = 0
        failed = 0
        errors = []
        
        if not self.twilio_client:
            return {
                "sent": 0,
                "failed": len(recipients),
                "error": "Twilio not configured"
            }
        
        for recipient in recipients:
            phone = recipient.get("phone")
            if not phone:
                failed += 1
                continue
            
            try:
                message_obj = self.twilio_client.messages.create(
                    body=message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=phone
                )
                sent += 1
            except Exception as e:
                failed += 1
                errors.append({"phone": phone, "error": str(e)})
        
        return {
            "sent": sent,
            "failed": failed,
            "errors": errors if errors else None
        }
    
    def send_email(self, recipients: List[Dict[str, Any]], 
                   subject: str, body: str) -> Dict[str, Any]:
        """
        Send email to multiple recipients
        
        Args:
            recipients: List of recipient dicts with 'email' field
            subject: Email subject
            body: Email body (HTML supported)
            
        Returns:
            Delivery status
        """
        sent = 0
        failed = 0
        errors = []
        
        if not SMTP_EMAIL or not SMTP_PASSWORD:
            return {
                "sent": 0,
                "failed": len(recipients),
                "error": "Email not configured"
            }
        
        for recipient in recipients:
            email = recipient.get("email")
            if not email:
                failed += 1
                continue
            
            try:
                msg = MIMEMultipart()
                msg['From'] = SMTP_EMAIL
                msg['To'] = email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(body, 'html'))
                
                with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                    server.starttls()
                    server.login(SMTP_EMAIL, SMTP_PASSWORD)
                    server.send_message(msg)
                
                sent += 1
            except Exception as e:
                failed += 1
                errors.append({"email": email, "error": str(e)})
        
        return {
            "sent": sent,
            "failed": failed,
            "errors": errors if errors else None
        }
    
    def send_push_notification(self, recipients: List[Dict[str, Any]], 
                              title: str, body: str) -> Dict[str, Any]:
        """
        Send push notification (simulated - in production use FCM/APNS)
        
        Args:
            recipients: List of recipient dicts with device tokens
            title: Notification title
            body: Notification body
            
        Returns:
            Delivery status
        """
        # Simulated push notification
        # In production, integrate with Firebase Cloud Messaging or Apple Push Notification Service
        
        sent = len(recipients)
        
        return {
            "sent": sent,
            "failed": 0,
            "method": "simulated",
            "message": f"Push notification sent to {sent} devices (simulated)"
        }
    
    def send_bulk_alert(self, channel: str, recipients: List[Dict[str, Any]], 
                       content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send bulk alert through specified channel
        
        Args:
            channel: 'sms', 'email', or 'push'
            recipients: List of recipients
            content: Content dict with appropriate fields
            
        Returns:
            Delivery status
        """
        if channel == "sms":
            message = content.get("message", "")
            return self.send_sms(recipients, message)
        
        elif channel == "email":
            subject = content.get("subject", "Railway Alert")
            body = content.get("body", "")
            return self.send_email(recipients, subject, body)
        
        elif channel == "push":
            title = content.get("title", "Railway Alert")
            body = content.get("body", "")
            return self.send_push_notification(recipients, title, body)
        
        else:
            return {
                "sent": 0,
                "failed": len(recipients),
                "error": f"Unknown channel: {channel}"
            }
    
    def format_alert_message(self, alert_type: str, data: Dict[str, Any], 
                            channel: str) -> str:
        """
        Format alert message for specific channel
        """
        if channel == "sms":
            # SMS - keep it short
            if alert_type == "delay":
                return f"Train {data.get('train_number')} delayed by {data.get('delay_minutes')}min. New arrival: {data.get('new_time')}. Apologies for inconvenience."
            elif alert_type == "cancellation":
                return f"Train {data.get('train_number')} cancelled. Contact support for rebooking. Ref: {data.get('pnr')}"
            else:
                return f"Railway Alert: {data.get('message', 'Please check your booking')}"
        
        elif channel == "email":
            # Email - can be more detailed
            return f"""
            <html>
            <body>
                <h2>Railway Alert</h2>
                <p><strong>Alert Type:</strong> {alert_type}</p>
                <p><strong>Details:</strong></p>
                <ul>
                    {''.join([f'<li><strong>{k}:</strong> {v}</li>' for k, v in data.items()])}
                </ul>
                <p>For assistance, please contact customer support.</p>
            </body>
            </html>
            """
        
        else:
            # Push notification
            return data.get("message", "You have a new railway alert")
