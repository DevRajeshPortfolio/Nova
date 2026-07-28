# jwt_manager.py
# JWT Token Management with Refresh

import jwt
import time
import uuid
from datetime import datetime, timedelta

class JWTManager:
    """JWT token management with refresh tokens"""
    
    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.refresh_tokens = {}
        self.blacklist = set()
    
    def create_tokens(self, user_id: str, user_data: Dict = None) -> Dict:
        """Create access and refresh tokens"""
        access_token = self._create_access_token(user_id, user_data)
        refresh_token = self._create_refresh_token(user_id)
        
        # Store refresh token
        self.refresh_tokens[refresh_token] = {
            'user_id': user_id,
            'created_at': time.time()
        }
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': 900  # 15 minutes
        }
    
    def _create_access_token(self, user_id: str, user_data: Dict = None) -> str:
        """Create an access token"""
        payload = {
            'sub': user_id,
            'iat': time.time(),
            'exp': time.time() + 900,
            'jti': str(uuid.uuid4()),
            'user': user_data or {}
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def _create_refresh_token(self, user_id: str) -> str:
        """Create a refresh token"""
        payload = {
            'sub': user_id,
            'iat': time.time(),
            'exp': time.time() + 604800,  # 7 days
            'jti': str(uuid.uuid4()),
            'type': 'refresh'
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def refresh_access_token(self, refresh_token: str) -> Dict:
        """Refresh an access token"""
        # Validate refresh token
        if refresh_token not in self.refresh_tokens:
            raise ValueError("Invalid refresh token")
        
        # Decode refresh token
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload['sub']
            
            # Create new tokens
            return self.create_tokens(user_id)
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token")
    
    def revoke_token(self, token: str) -> None:
        """Revoke a token"""
        self.blacklist.add(token)