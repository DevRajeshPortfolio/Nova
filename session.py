# session.py
# Nova Programming Language - Session Management

import json
import uuid
import time
import hashlib
from datetime import datetime, timedelta

class Session:
    """Session management"""
    
    def __init__(self, storage=None):
        self.storage = storage or {}
        self.session_id = None
        self.data = {}
        self.created_at = None
        self.expires_at = None
        self._dirty = False
    
    def create(self, session_id=None):
        """Create a new session"""
        self.session_id = session_id or self._generate_session_id()
        self.data = {}
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(days=7)
        self._dirty = True
        return self
    
    def load(self, session_id, storage):
        """Load an existing session"""
        self.session_id = session_id
        self.storage = storage
        session_data = storage.get(session_id)
        
        if session_data:
            self.data = session_data.get('data', {})
            self.created_at = session_data.get('created_at')
            self.expires_at = session_data.get('expires_at')
            
            # Check if expired
            if self.expires_at and datetime.now() > self.expires_at:
                self.delete()
                self.create()
        else:
            self.create()
        
        return self
    
    def save(self):
        """Save session to storage"""
        if self._dirty or self.session_id not in self.storage:
            self.storage[self.session_id] = {
                'data': self.data,
                'created_at': self.created_at,
                'expires_at': self.expires_at
            }
            self._dirty = False
    
    def delete(self):
        """Delete session"""
        if self.session_id in self.storage:
            del self.storage[self.session_id]
    
    def get(self, key, default=None):
        """Get a value from session"""
        return self.data.get(key, default)
    
    def set(self, key, value):
        """Set a value in session"""
        self.data[key] = value
        self._dirty = True
    
    def delete_key(self, key):
        """Delete a key from session"""
        if key in self.data:
            del self.data[key]
            self._dirty = True
    
    def clear(self):
        """Clear all session data"""
        self.data = {}
        self._dirty = True
    
    def is_expired(self):
        """Check if session is expired"""
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False
    
    def extend(self, days=7):
        """Extend session expiration"""
        self.expires_at = datetime.now() + timedelta(days=days)
        self._dirty = True
    
    def _generate_session_id(self):
        """Generate a unique session ID"""
        return hashlib.sha256(
            f"{uuid.uuid4()}{time.time()}{uuid.uuid4()}".encode()
        ).hexdigest()


class SessionManager:
    """Session manager for HTTP requests"""
    
    def __init__(self, storage=None, cookie_name='nova_session'):
        self.storage = storage or {}
        self.cookie_name = cookie_name
        self.sessions = {}
    
    def get_session(self, request, response=None):
        """Get or create session for request"""
        session_id = request.cookies.get(self.cookie_name)
        
        if session_id and session_id in self.storage:
            session = Session(self.storage)
            session.load(session_id, self.storage)
            return session
        
        # Create new session
        session = Session(self.storage)
        session.create()
        self.storage[session.session_id] = {
            'data': session.data,
            'created_at': session.created_at,
            'expires_at': session.expires_at
        }
        
        if response:
            response.set_cookie(
                self.cookie_name,
                session.session_id,
                max_age=60 * 60 * 24 * 7,
                path='/',
                http_only=True
            )
        
        return session
    
    def save_session(self, session):
        """Save session"""
        session.save()
    
    def destroy_session(self, session, response=None):
        """Destroy session"""
        session.delete()
        if response:
            response.set_cookie(
                self.cookie_name,
                '',
                max_age=0,
                path='/'
            )


class Cookie:
    """Cookie management"""
    
    def __init__(self, key, value, options=None):
        self.key = key
        self.value = value
        self.options = options or {}
    
    def to_header(self):
        """Convert to HTTP header"""
        cookie = f"{self.key}={self.value}"
        
        if self.options.get('max_age'):
            cookie += f"; Max-Age={self.options['max_age']}"
        if self.options.get('path'):
            cookie += f"; Path={self.options['path']}"
        if self.options.get('domain'):
            cookie += f"; Domain={self.options['domain']}"
        if self.options.get('secure'):
            cookie += "; Secure"
        if self.options.get('http_only'):
            cookie += "; HttpOnly"
        if self.options.get('same_site'):
            cookie += f"; SameSite={self.options['same_site']}"
        
        return cookie


class MemorySessionStorage:
    """In-memory session storage"""
    
    def __init__(self):
        self._storage = {}
        self._expiry = {}
    
    def __getitem__(self, key):
        return self._storage.get(key)
    
    def __setitem__(self, key, value):
        self._storage[key] = value
        # Auto-expire after 7 days
        self._expiry[key] = datetime.now() + timedelta(days=7)
    
    def __delitem__(self, key):
        if key in self._storage:
            del self._storage[key]
        if key in self._expiry:
            del self._expiry[key]
    
    def __contains__(self, key):
        # Check expiry
        if key in self._expiry:
            if datetime.now() > self._expiry[key]:
                del self._storage[key]
                del self._expiry[key]
                return False
        return key in self._storage
    
    def get(self, key, default=None):
        if key in self:
            return self._storage.get(key, default)
        return default
    
    def clear_expired(self):
        """Clear expired sessions"""
        for key in list(self._expiry.keys()):
            if datetime.now() > self._expiry[key]:
                if key in self._storage:
                    del self._storage[key]
                del self._expiry[key]
    
    def to_dict(self):
        """Convert to dict for serialization"""
        return self._storage.copy()