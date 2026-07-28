# database.py
# Nova Programming Language - Database Integration

import json
import os
import sqlite3
import time
from datetime import datetime

class Database:
    """Database abstraction layer"""
    
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
        self.cursor = None
        self.driver = self._detect_driver(connection_string)
        self.connect()
    
    def _detect_driver(self, connection_string):
        """Detect database driver from connection string"""
        if connection_string.startswith('sqlite://'):
            return 'sqlite'
        elif connection_string.startswith('postgres://') or connection_string.startswith('postgresql://'):
            return 'postgres'
        elif connection_string.startswith('mysql://'):
            return 'mysql'
        elif connection_string.startswith('mongodb://'):
            return 'mongodb'
        else:
            # Default to SQLite
            return 'sqlite'
    
    def connect(self):
        """Connect to database"""
        try:
            if self.driver == 'sqlite':
                db_path = self.connection_string[9:]  # Remove 'sqlite://'
                if db_path == '':
                    db_path = 'nova.db'
                self.connection = sqlite3.connect(db_path)
                self.cursor = self.connection.cursor()
                self._init_sqlite()
            elif self.driver == 'postgres':
                # PostgreSQL connection
                import psycopg2
                # Parse connection string
                # postgres://user:password@host:port/database
                # For simplicity, we'll use SQLite for now
                self.connection = sqlite3.connect('nova.db')
                self.cursor = self.connection.cursor()
                self._init_sqlite()
            elif self.driver == 'mysql':
                # MySQL connection
                # For simplicity, we'll use SQLite for now
                self.connection = sqlite3.connect('nova.db')
                self.cursor = self.connection.cursor()
                self._init_sqlite()
            elif self.driver == 'mongodb':
                # MongoDB connection
                # For simplicity, we'll use SQLite for now
                self.connection = sqlite3.connect('nova.db')
                self.cursor = self.connection.cursor()
                self._init_sqlite()
            else:
                self.connection = sqlite3.connect('nova.db')
                self.cursor = self.connection.cursor()
                self._init_sqlite()
            
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def _init_sqlite(self):
        """Initialize SQLite database"""
        # Create default tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password_hash TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                user_id INTEGER,
                data TEXT,
                created_at TIMESTAMP,
                expires_at TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection TEXT,
                key TEXT,
                value TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')
        
        self.connection.commit()
    
    def query(self, collection, query=None):
        """Query a collection"""
        if self.driver == 'sqlite':
            if query is None:
                query = {}
            
            sql = f"SELECT * FROM data WHERE collection = ?"
            params = [collection]
            
            if 'key' in query:
                sql += " AND key = ?"
                params.append(query['key'])
            
            if 'id' in query:
                sql += " AND id = ?"
                params.append(query['id'])
            
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
            
            # Convert to list of dicts
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in results]
        return []
    
    def insert(self, collection, data):
        """Insert data into collection"""
        if self.driver == 'sqlite':
            key = data.get('key', str(int(time.time())))
            value = json.dumps(data.get('value', data))
            created_at = datetime.now().isoformat()
            
            self.cursor.execute(
                "INSERT INTO data (collection, key, value, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (collection, key, value, created_at, created_at)
            )
            self.connection.commit()
            return {'id': self.cursor.lastrowid, 'key': key}
        return {'error': 'Unsupported database driver'}
    
    def update(self, collection, query, data):
        """Update data in collection"""
        if self.driver == 'sqlite':
            key = query.get('key')
            if not key:
                return {'error': 'Key required for update'}
            
            value = json.dumps(data.get('value', data))
            updated_at = datetime.now().isoformat()
            
            self.cursor.execute(
                "UPDATE data SET value = ?, updated_at = ? WHERE collection = ? AND key = ?",
                (value, updated_at, collection, key)
            )
            self.connection.commit()
            return {'updated': self.cursor.rowcount}
        return {'error': 'Unsupported database driver'}
    
    def delete(self, collection, query):
        """Delete data from collection"""
        if self.driver == 'sqlite':
            key = query.get('key')
            if not key:
                return {'error': 'Key required for delete'}
            
            self.cursor.execute(
                "DELETE FROM data WHERE collection = ? AND key = ?",
                (collection, key)
            )
            self.connection.commit()
            return {'deleted': self.cursor.rowcount}
        return {'error': 'Unsupported database driver'}
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def create_table(self, name, schema):
        """Create a new table"""
        if self.driver == 'sqlite':
            columns = []
            for col_name, col_type in schema.items():
                columns.append(f"{col_name} {col_type}")
            
            sql = f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(columns)})"
            self.cursor.execute(sql)
            self.connection.commit()
            return {'success': True}
        return {'error': 'Unsupported database driver'}


class Model:
    """ORM Base Model"""
    
    _db = None
    _collection = None
    
    @classmethod
    def set_db(cls, db):
        cls._db = db
    
    @classmethod
    def set_collection(cls, name):
        cls._collection = name
    
    @classmethod
    def find(cls, query=None):
        """Find records"""
        if cls._db and cls._collection:
            results = cls._db.query(cls._collection, query)
            return [cls(**r) for r in results]
        return []
    
    @classmethod
    def find_one(cls, query):
        """Find one record"""
        results = cls.find(query)
        return results[0] if results else None
    
    @classmethod
    def create(cls, data):
        """Create a new record"""
        if cls._db and cls._collection:
            return cls._db.insert(cls._collection, data)
        return None
    
    @classmethod
    def update(cls, query, data):
        """Update records"""
        if cls._db and cls._collection:
            return cls._db.update(cls._collection, query, data)
        return None
    
    @classmethod
    def delete(cls, query):
        """Delete records"""
        if cls._db and cls._collection:
            return cls._db.delete(cls._collection, query)
        return None


class User(Model):
    """User model"""
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password_hash = kwargs.get('password_hash')
        self.created_at = kwargs.get('created_at')
    
    @classmethod
    def find_by_username(cls, username):
        return cls.find_one({'key': username})
    
    @classmethod
    def find_by_email(cls, email):
        return cls.find_one({'email': email})
    
    def save(self):
        """Save user to database"""
        if self.id:
            return User.update({'id': self.id}, self.__dict__)
        else:
            return User.create(self.__dict__)


def create_database(connection_string, models=None):
    """Create database connection and initialize models"""
    db = Database(connection_string)
    
    if models:
        for model in models:
            model.set_db(db)
    
    return db