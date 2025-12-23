"""
WhatsApp Webhook Handler
Receives and processes incoming WhatsApp messages
"""
from flask import Flask, request, jsonify
from typing import Dict, Any
import asyncio
from datetime import datetime
import uuid

from context.context_protocol import context_protocol, ChannelType, UserContext
from orchestrator.orchestrator import orchestrator
from services.whatsapp_service import whatsapp_service
from config import settings


app = Flask(__name__)


class MessageIngestionService:
    """
    Message Ingestion Service
    Processes incoming WhatsApp messages
    """
    
    @staticmethod
    def extract_message_data(webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant data from Twilio webhook"""
        return {
            "from": webhook_data.get("From", "").replace("whatsapp:", ""),
            "to": webhook_data.get("To", ""),
            "message": webhook_data.get("Body", ""),
            "message_sid": webhook_data.get("MessageSid", ""),
            "timestamp": datetime.now().isoformat(),
            "media_count": int(webhook_data.get("NumMedia", 0)),
            "media_urls": [
                webhook_data.get(f"MediaUrl{i}", "")
                for i in range(int(webhook_data.get("NumMedia", 0)))
            ]
        }
    
    @staticmethod
    def create_user_context(message_data: Dict[str, Any]) -> UserContext:
        """Create or retrieve user context"""
        user_id = message_data["from"]
        conversation_id = f"{user_id}_{datetime.now().strftime('%Y%m%d')}"
        
        # Check if context exists
        existing_context = context_protocol.get_context(conversation_id)
        
        if existing_context:
            return existing_context
        
        # Create new context
        context = context_protocol.create_context(
            user_id=user_id,
            channel=ChannelType.WHATSAPP,
            conversation_id=conversation_id,
            permissions=["email.read", "db.read"]  # Default permissions
        )
        
        return context
    
    @staticmethod
    async def process_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming message through orchestrator"""
        # Create/get user context
        context = MessageIngestionService.create_user_context(message_data)
        
        # Process message through orchestrator
        result = await orchestrator.process_message(
            user_message=message_data["message"],
            context=context
        )
        
        return result.to_dict()


@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Twilio WhatsApp webhook endpoint
    
    Receives incoming messages from WhatsApp
    """
    try:
        # Extract message data
        webhook_data = request.form.to_dict()
        message_data = MessageIngestionService.extract_message_data(webhook_data)
        
        print(f"Received message from {message_data['from']}: {message_data['message']}")
        
        # Process message asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            MessageIngestionService.process_message(message_data)
        )
        loop.close()
        
        # Send response back to user
        response_message = result.get("response", "Sorry, I couldn't process your request.")
        
        whatsapp_service.send_message(
            to_number=message_data["from"],
            message=response_message
        )
        
        # Return empty response to Twilio (already sent message)
        return '', 200
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        
        # Try to send error message to user
        try:
            if 'message_data' in locals():
                whatsapp_service.send_message(
                    to_number=message_data["from"],
                    message="Sorry, I encountered an error. Please try again."
                )
        except:
            pass
        
        return jsonify({"error": str(e)}), 500


@app.route('/webhook/status', methods=['POST'])
def status_webhook():
    """
    Message status callback webhook
    Receives delivery status updates
    """
    try:
        status_data = request.form.to_dict()
        message_sid = status_data.get('MessageSid')
        status = status_data.get('MessageStatus')
        
        print(f"Message {message_sid} status: {status}")
        
        # Store status in database if needed
        
        return '', 200
        
    except Exception as e:
        print(f"Error processing status webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "MultiAgent WhatsApp System",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/test', methods=['POST'])
def test_endpoint():
    """
    Test endpoint for manual message testing
    
    POST body:
    {
        "from": "+1234567890",
        "message": "What is my last electricity bill?"
    }
    """
    try:
        data = request.json
        
        message_data = {
            "from": data.get("from", "+1234567890"),
            "to": settings.twilio_whatsapp_number,
            "message": data.get("message", ""),
            "message_sid": f"test_{uuid.uuid4()}",
            "timestamp": datetime.now().isoformat(),
            "media_count": 0,
            "media_urls": []
        }
        
        # Process message
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            MessageIngestionService.process_message(message_data)
        )
        loop.close()
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def run_server():
    """Run Flask server"""
    app.run(
        host=settings.host,
        port=settings.port,
        debug=settings.debug
    )


if __name__ == '__main__':
    run_server()
