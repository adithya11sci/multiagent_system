"""
Email Tool - MCP Implementation
Handles email operations via Gmail API
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from mcp.tool_layer import MCPTool, ToolDefinition, ToolCapability, ToolScope
from context.context_protocol import UserContext
from config import settings


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class EmailTool(MCPTool):
    """
    Email Tool - Reads and searches emails via Gmail API
    """
    
    def __init__(self):
        definition = ToolDefinition(
            name="read_email",
            description="Search and read emails from user's Gmail account",
            capabilities=[ToolCapability.READ, ToolCapability.SEARCH],
            scopes=[ToolScope.EMAIL_READ],
            parameters={
                "type": "object",
                "required": ["action"],
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["search", "read", "list"],
                        "description": "Action to perform"
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query (Gmail search syntax)"
                    },
                    "message_id": {
                        "type": "string",
                        "description": "Specific message ID to read"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 10
                    }
                }
            }
        )
        super().__init__(definition)
        self._credentials_cache: Dict[str, Credentials] = {}
    
    def _get_credentials(self, user_id: str) -> Optional[Credentials]:
        """Get or refresh Gmail API credentials for user"""
        if user_id in self._credentials_cache:
            creds = self._credentials_cache[user_id]
            if creds and creds.valid:
                return creds
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                return creds
        
        # Load credentials from file
        token_path = f'./credentials/token_{user_id}.json'
        creds = None
        
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Need to initiate OAuth flow
                return None
        
        self._credentials_cache[user_id] = creds
        return creds
    
    async def execute(
        self,
        context: UserContext,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute email operation"""
        action = parameters.get("action")
        
        # Get credentials
        creds = self._get_credentials(context.user_id)
        if not creds:
            return {
                "error": "Gmail not authenticated. Please complete OAuth flow.",
                "auth_required": True
            }
        
        try:
            service = build('gmail', 'v1', credentials=creds)
            
            if action == "search":
                return await self._search_emails(service, parameters)
            elif action == "read":
                return await self._read_email(service, parameters)
            elif action == "list":
                return await self._list_emails(service, parameters)
            else:
                return {"error": f"Unknown action: {action}"}
                
        except HttpError as error:
            return {"error": f"Gmail API error: {str(error)}"}
    
    async def _search_emails(
        self,
        service,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Search emails"""
        query = parameters.get("query", "")
        max_results = parameters.get("max_results", 10)
        
        # Search messages
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return {
                "found": False,
                "count": 0,
                "messages": []
            }
        
        # Get full message details
        detailed_messages = []
        for msg in messages[:max_results]:
            msg_detail = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            detailed_messages.append(self._parse_message(msg_detail))
        
        return {
            "found": True,
            "count": len(detailed_messages),
            "messages": detailed_messages
        }
    
    async def _read_email(
        self,
        service,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Read specific email"""
        message_id = parameters.get("message_id")
        
        if not message_id:
            return {"error": "message_id required"}
        
        msg = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        return {
            "found": True,
            "message": self._parse_message(msg)
        }
    
    async def _list_emails(
        self,
        service,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """List recent emails"""
        max_results = parameters.get("max_results", 10)
        
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        # Get headers only for listing
        email_list = []
        for msg in messages:
            msg_detail = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in msg_detail['payload']['headers']}
            email_list.append({
                "id": msg['id'],
                "from": headers.get('From', ''),
                "subject": headers.get('Subject', ''),
                "date": headers.get('Date', '')
            })
        
        return {
            "count": len(email_list),
            "emails": email_list
        }
    
    def _parse_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Gmail message to structured format"""
        headers = {h['name']: h['value'] for h in message['payload']['headers']}
        
        # Extract body
        body = ""
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(
                            part['body']['data']
                        ).decode('utf-8')
                        break
        else:
            if 'data' in message['payload']['body']:
                body = base64.urlsafe_b64decode(
                    message['payload']['body']['data']
                ).decode('utf-8')
        
        return {
            "id": message['id'],
            "thread_id": message['threadId'],
            "from": headers.get('From', ''),
            "to": headers.get('To', ''),
            "subject": headers.get('Subject', ''),
            "date": headers.get('Date', ''),
            "body": body,
            "snippet": message.get('snippet', ''),
            "labels": message.get('labelIds', [])
        }
