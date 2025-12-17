"""
Security Module
Handles authentication, authorization, and encryption
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import os

from config import settings


class SecurityManager:
    """
    Handles security operations:
    - JWT token generation and validation
    - Password hashing
    - Token encryption/decryption
    """
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60
        
        # Initialize Fernet encryption
        encryption_key = settings.encryption_key.encode()
        if len(encryption_key) != 44:  # Fernet key must be 32 url-safe base64-encoded bytes
            # Generate proper key if not provided
            encryption_key = Fernet.generate_key()
        self.cipher = Fernet(encryption_key)
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encrypt_token(self, token: str) -> str:
        """Encrypt sensitive token (OAuth, API keys)"""
        encrypted = self.cipher.encrypt(token.encode())
        return encrypted.decode()
    
    def decrypt_token(self, encrypted_token: str) -> str:
        """Decrypt token"""
        decrypted = self.cipher.decrypt(encrypted_token.encode())
        return decrypted.decode()
    
    def generate_encryption_key(self) -> str:
        """Generate new Fernet encryption key"""
        return Fernet.generate_key().decode()


class OAuth2Manager:
    """
    Manages OAuth2 flows for external services
    """
    
    def __init__(self):
        self.security = SecurityManager()
        self._token_store: Dict[str, Dict[str, Any]] = {}
    
    def store_oauth_token(
        self,
        user_id: str,
        service: str,
        access_token: str,
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None
    ):
        """Store OAuth tokens securely"""
        encrypted_access = self.security.encrypt_token(access_token)
        encrypted_refresh = None
        
        if refresh_token:
            encrypted_refresh = self.security.encrypt_token(refresh_token)
        
        expires_at = None
        if expires_in:
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        key = f"{user_id}_{service}"
        self._token_store[key] = {
            "access_token": encrypted_access,
            "refresh_token": encrypted_refresh,
            "expires_at": expires_at,
            "created_at": datetime.utcnow()
        }
        
        # In production, store in database
        self._persist_token(user_id, service, self._token_store[key])
    
    def get_oauth_token(self, user_id: str, service: str) -> Optional[Dict[str, str]]:
        """Retrieve OAuth tokens"""
        key = f"{user_id}_{service}"
        
        if key not in self._token_store:
            # Try to load from database
            self._token_store[key] = self._load_token(user_id, service)
        
        if key not in self._token_store:
            return None
        
        token_data = self._token_store[key]
        
        # Check if expired
        if token_data.get("expires_at"):
            if datetime.utcnow() > token_data["expires_at"]:
                # Token expired - should refresh
                return None
        
        # Decrypt tokens
        access_token = self.security.decrypt_token(token_data["access_token"])
        refresh_token = None
        
        if token_data.get("refresh_token"):
            refresh_token = self.security.decrypt_token(token_data["refresh_token"])
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    def _persist_token(self, user_id: str, service: str, token_data: Dict[str, Any]):
        """Persist token to storage (database, file, etc.)"""
        # Save to file for now
        token_file = f"./credentials/oauth_{user_id}_{service}.json"
        
        import json
        with open(token_file, 'w') as f:
            # Serialize datetime
            serialized = token_data.copy()
            if serialized.get("expires_at"):
                serialized["expires_at"] = serialized["expires_at"].isoformat()
            if serialized.get("created_at"):
                serialized["created_at"] = serialized["created_at"].isoformat()
            
            json.dump(serialized, f)
    
    def _load_token(self, user_id: str, service: str) -> Optional[Dict[str, Any]]:
        """Load token from storage"""
        token_file = f"./credentials/oauth_{user_id}_{service}.json"
        
        if not os.path.exists(token_file):
            return None
        
        import json
        with open(token_file, 'r') as f:
            token_data = json.load(f)
            
            # Deserialize datetime
            if token_data.get("expires_at"):
                token_data["expires_at"] = datetime.fromisoformat(token_data["expires_at"])
            if token_data.get("created_at"):
                token_data["created_at"] = datetime.fromisoformat(token_data["created_at"])
            
            return token_data


class PermissionManager:
    """
    Manages user permissions and scopes
    """
    
    @staticmethod
    def validate_scope(user_permissions: list, required_scope: str) -> bool:
        """Check if user has required scope"""
        return required_scope in user_permissions
    
    @staticmethod
    def get_default_permissions(channel: str) -> list:
        """Get default permissions for channel"""
        default_permissions = {
            "whatsapp": ["email.read", "db.read"],
            "web": ["email.read", "db.read", "file.read"],
            "api": ["db.read", "api.call"]
        }
        
        return default_permissions.get(channel, ["db.read"])


# Global instances
security_manager = SecurityManager()
oauth2_manager = OAuth2Manager()
permission_manager = PermissionManager()
