import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, Optional

class SQLiteDatabase:
    def __init__(self, db_path: str = "stem_arena.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                location TEXT NOT NULL,
                grade TEXT NOT NULL,
                birthday TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                gems INTEGER DEFAULT 1000,
                victories INTEGER DEFAULT 0,
                dominationRate INTEGER DEFAULT 0,
                rank INTEGER DEFAULT 0,
                killStreak INTEGER DEFAULT 0,
                profileIcon TEXT DEFAULT '🚀',
                joinDate TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_user(self, user_data: Dict[str, Any]) -> int:
        """Insert a new user and return the user ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (username, email, password, firstName, lastName, 
                             location, grade, birthday, level, gems, victories, 
                             dominationRate, rank, killStreak, profileIcon)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data['username'], user_data['email'], user_data['password'],
            user_data['firstName'], user_data['lastName'], user_data['location'],
            user_data['grade'], user_data['birthday'], user_data.get('level', 1),
            user_data.get('gems', 1000), user_data.get('victories', 0),
            user_data.get('dominationRate', 0), user_data.get('rank', 0),
            user_data.get('killStreak', 0), user_data.get('profileIcon', '🚀')
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    
    def find_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Find user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def find_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Find user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_dict(row)
        return None
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """Convert database row to dictionary"""
        columns = ['id', 'username', 'email', 'password', 'firstName', 'lastName',
                  'location', 'grade', 'birthday', 'level', 'gems', 'victories',
                  'dominationRate', 'rank', 'killStreak', 'profileIcon', 'joinDate']
        
        return dict(zip(columns, row))

# Create global database instance
db = SQLiteDatabase()
user_collection = db  # For compatibility with existing code
collection = db  # For compatibility with existing code 