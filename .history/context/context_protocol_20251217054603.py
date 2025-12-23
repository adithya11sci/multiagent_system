"""
Context Protocol Implementation
Manages user context, permissions, and state across agents
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum
import json


class ChannelType(str, Enum):
    """Communication channel types"""
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    WEB = "web"
    API = "api"


class ConversationState(str, Enum):
    """Conversation states"""
    ACTIVE = "active"
    WAITING = "waiting"
    COMPLETED = "completed"
    ERRORED = "errored"


@dataclass
class UserContext:
    """
    User context that travels across all agents
    Ensures scoped access and prevents data leakage
    """
    user_id: str
    channel: ChannelType
    conversation_id: str
    permissions: List[str] = field(default_factory=list)
    conversation_state: ConversationState = ConversationState.ACTIVE
    memory_scope: str = "private"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        return permission in self.permissions
    
    def add_permission(self, permission: str):
        """Add permission to user context"""
        if permission not in self.permissions:
            self.permissions.append(permission)
            self.updated_at = datetime.now()
    
    def remove_permission(self, permission: str):
        """Remove permission from user context"""
        if permission in self.permissions:
            self.permissions.remove(permission)
            self.updated_at = datetime.now()
    
    def update_state(self, state: ConversationState):
        """Update conversation state"""
        self.conversation_state = state
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['channel'] = self.channel.value
        data['conversation_state'] = self.conversation_state.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserContext':
        """Create from dictionary"""
        data['channel'] = ChannelType(data['channel'])
        data['conversation_state'] = ConversationState(data['conversation_state'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)
    
    def to_json(self) -> str:
        """Serialize to JSON"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'UserContext':
        """Deserialize from JSON"""
        return cls.from_dict(json.loads(json_str))


class ContextProtocol:
    """
    Context Protocol Manager
    Manages context lifecycle and ensures secure access
    """
    
    def __init__(self):
        self._contexts: Dict[str, UserContext] = {}
    
    def create_context(
        self,
        user_id: str,
        channel: ChannelType,
        conversation_id: str,
        permissions: Optional[List[str]] = None
    ) -> UserContext:
        """Create new user context"""
        context = UserContext(
            user_id=user_id,
            channel=channel,
            conversation_id=conversation_id,
            permissions=permissions or [],
            memory_scope="private"
        )
        self._contexts[conversation_id] = context
        return context
    
    def get_context(self, conversation_id: str) -> Optional[UserContext]:
        """Get existing context"""
        return self._contexts.get(conversation_id)
    
    def update_context(self, conversation_id: str, context: UserContext):
        """Update existing context"""
        self._contexts[conversation_id] = context
    
    def delete_context(self, conversation_id: str):
        """Delete context"""
        if conversation_id in self._contexts:
            del self._contexts[conversation_id]
    
    def validate_permission(
        self,
        conversation_id: str,
        required_permission: str
    ) -> bool:
        """Validate if context has required permission"""
        context = self.get_context(conversation_id)
        if not context:
            return False
        return context.has_permission(required_permission)
    
    def enforce_scope(
        self,
        conversation_id: str,
        resource_scope: str
    ) -> bool:
        """Enforce memory scope boundaries"""
        context = self.get_context(conversation_id)
        if not context:
            return False
        return context.memory_scope == resource_scope or resource_scope == "public"


# Global context protocol instance
context_protocol = ContextProtocol()
