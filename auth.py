# auth.py
# Nova Programming Language - Authentication System
try:
    import jwt
except ImportError:
    try:
        import jose.jwt as jwt
    except ImportError:
        raise ImportError("Please install PyJWT or python-jose: pip install PyJWT")

# Or implement a simple JWT fallback
class SimpleJWT:
    @staticmethod
    def encode(payload, secret, algorithm='HS256'):
        import hashlib
        import json
        import base64
        import time
        
        header = base64.urlsafe_b64encode(json.dumps({'alg': algorithm, 'typ': 'JWT'}).encode()).decode().rstrip('=')
        payload_data = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        signature = base64.urlsafe_b64encode(
            hashlib.sha256(f"{header}.{payload_data}".encode() + secret.encode()).digest()
        ).decode().rstrip('=')
        return f"{header}.{payload_data}.{signature}"
    
    @staticmethod
    def decode(token, secret, algorithms=None):
        import json
        import base64
        import hashlib
        
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token")
        
        header, payload_data, signature = parts
        expected_signature = base64.urlsafe_b64encode(
            hashlib.sha256(f"{header}.{payload_data}".encode() + secret.encode()).digest()
        ).decode().rstrip('=')
        
        if signature != expected_signature:
            raise ValueError("Invalid signature")
        
        return json.loads(base64.urlsafe_b64decode(payload_data + '==').decode())
    
import hashlib
import secrets
import time
import json
from datetime import datetime, timedelta
import jwt

class Auth:
    """Authentication system"""
    
    def __init__(self, secret_key=None, session_manager=None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.session_manager = session_manager
        self.users = {}
        self.tokens = {}
    
    def hash_password(self, password):
        """Hash a password"""
        salt = secrets.token_hex(16)
        return {
            'hash': hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            ).hex(),
            'salt': salt
        }
    
    def verify_password(self, password, hash_data):
        """Verify a password against a hash"""
        if isinstance(hash_data, str):
            # Simple string hash (legacy)
            return hashlib.sha256(password.encode()).hexdigest() == hash_data
        
        # New format with salt
        hash_value = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            hash_data['salt'].encode('utf-8'),
            100000
        ).hex()
        return hash_value == hash_data['hash']
    
    def register_user(self, username, password, email=None):
        """Register a new user"""
        if username in self.users:
            return {'success': False, 'error': 'Username already exists'}
        
        hash_data = self.hash_password(password)
        user = {
            'username': username,
            'password_hash': hash_data,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'last_login': None,
            'active': True
        }
        
        self.users[username] = user
        return {'success': True, 'user': username}
    
    def login(self, username, password, session=None):
        """Login a user"""
        user = self.users.get(username)
        if not user:
            return {'success': False, 'error': 'User not found'}
        
        if not user.get('active', True):
            return {'success': False, 'error': 'Account is disabled'}
        
        if not self.verify_password(password, user['password_hash']):
            return {'success': False, 'error': 'Invalid password'}
        
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        
        # Create session
        if session:
            session.set('user_id', username)
            session.set('logged_in', True)
            session.save()
        
        # Generate token
        token = self.generate_token(username)
        
        return {
            'success': True,
            'user': username,
            'token': token,
            'session_id': session.session_id if session else None
        }
    
    def logout(self, session=None):
        """Logout a user"""
        if session:
            session.set('logged_in', False)
            session.delete_key('user_id')
            session.save()
        
        return {'success': True}
    
    def generate_token(self, username, expires_in=3600):
        """Generate a JWT token"""
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return {
                'valid': True,
                'username': payload.get('username'),
                'exp': payload.get('exp')
            }
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Invalid token'}
    
    def get_current_user(self, request):
        """Get current user from request"""
        # Check session first
        if hasattr(request, 'session'):
            user_id = request.session.get('user_id')
            if user_id and user_id in self.users:
                return self.users[user_id]
        
        # Check Authorization header
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            result = self.verify_token(token)
            if result['valid']:
                username = result['username']
                return self.users.get(username)
        
        return None
    
    def require_auth(self, func):
        """Decorator for protected routes"""
        def wrapper(request):
            user = self.get_current_user(request)
            if not user:
                from server import Response
                return Response().set_status(401).json({
                    'error': True,
                    'message': 'Authentication required'
                })
            request.user = user
            return func(request)
        return wrapper
    
    def require_role(self, role):
        """Decorator for role-based authorization"""
        def decorator(func):
            def wrapper(request):
                user = self.get_current_user(request)
                if not user:
                    from server import Response
                    return Response().set_status(401).json({
                        'error': True,
                        'message': 'Authentication required'
                    })
                
                if user.get('role') != role and 'admin' not in user.get('roles', []):
                    from server import Response
                    return Response().set_status(403).json({
                        'error': True,
                        'message': 'Insufficient permissions'
                    })
                
                request.user = user
                return func(request)
            return wrapper
        return decorator


class AuthMiddleware:
    """Authentication middleware for Nova Server"""
    
    def __init__(self, auth, session_manager=None):
        self.auth = auth
        self.session_manager = session_manager
        self.public_routes = ['/login', '/register', '/']
    
    def __call__(self, request):
        """Process request"""
        # Skip authentication for public routes
        if request.path in self.public_routes:
            return None
        
        # Check for session
        if self.session_manager:
            session = self.session_manager.get_session(request)
            if session.get('logged_in'):
                return None
        
        # Check for token
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            result = self.auth.verify_token(token)
            if result['valid']:
                return None
        
        # Not authenticated
        from server import Response
        return Response().set_status(401).json({
            'error': True,
            'message': 'Authentication required'
        })


def create_auth_service(db=None, session_manager=None):
    """Create an authentication service"""
    auth = Auth(session_manager=session_manager)
    
    # Load users from database if available
    if db:
        # Load users from database
        users = db.query('users')
        for user in users:
            auth.users[user['username']] = user
    
    return auth