"""
Database Manager for User Authentication

This module handles database operations for user authentication with
peppered, salted, and hashed passwords using PostgreSQL.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from password_utils import PasswordManager

# Load environment variables
load_dotenv()


class DatabaseManager:
    """
    Manages database connections and user authentication operations.
    """
    
    def __init__(self):
        """Initialize database connection parameters from environment variables."""
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        self.password_manager = PasswordManager()
    
    def get_connection(self):
        """
        Create and return a database connection.
        
        Returns:
            psycopg2 connection object
            
        Raises:
            psycopg2.Error: If connection fails
        """
        return psycopg2.connect(**self.db_config)
    
    def create_user(self, username: str, email: str, password: str) -> Optional[int]:
        """
        Create a new user with peppered, salted, and hashed password.
        
        Args:
            username: Unique username
            email: User's email address
            password: Plain text password (will be peppered and hashed)
            
        Returns:
            User ID if successful, None if failed
            
        Example:
            >>> db = DatabaseManager()
            >>> user_id = db.create_user("john_doe", "john@example.com", "SecurePass123!")
            >>> print(f"Created user with ID: {user_id}")
        """
        # Hash the password with pepper
        password_hash = self.password_manager.hash_password(password)
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO users (username, email, password_hash)
                        VALUES (%s, %s, %s)
                        RETURNING id
                        """,
                        (username, email, password_hash)
                    )
                    user_id = cursor.fetchone()[0]
                    conn.commit()
                    return user_id
        except psycopg2.IntegrityError as e:
            # User already exists (username or email duplicate)
            print(f"Error creating user: {e}")
            return None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user by username and password.
        
        Args:
            username: Username to authenticate
            password: Plain text password to verify
            
        Returns:
            User dict if authentication successful, None otherwise
            
        Example:
            >>> db = DatabaseManager()
            >>> user = db.authenticate_user("john_doe", "SecurePass123!")
            >>> if user:
            ...     print(f"Logged in as {user['username']}")
            ... else:
            ...     print("Authentication failed")
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Retrieve user by username
                    cursor.execute(
                        """
                        SELECT id, username, email, password_hash, is_active
                        FROM users
                        WHERE username = %s
                        """,
                        (username,)
                    )
                    user = cursor.fetchone()
                    
                    if not user:
                        return None
                    
                    # Check if user is active
                    if not user['is_active']:
                        return None
                    
                    # Verify password
                    if not self.password_manager.verify_password(password, user['password_hash']):
                        return None
                    
                    # Update last login timestamp
                    cursor.execute(
                        """
                        UPDATE users
                        SET last_login = CURRENT_TIMESTAMP
                        WHERE id = %s
                        """,
                        (user['id'],)
                    )
                    conn.commit()
                    
                    # Remove password_hash from returned dict for security
                    user_dict = dict(user)
                    del user_dict['password_hash']
                    
                    return user_dict
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change a user's password after verifying the old password.
        
        Args:
            user_id: ID of the user
            old_password: Current password for verification
            new_password: New password to set
            
        Returns:
            True if password changed successfully, False otherwise
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Get current password hash
                    cursor.execute(
                        """
                        SELECT password_hash
                        FROM users
                        WHERE id = %s
                        """,
                        (user_id,)
                    )
                    result = cursor.fetchone()
                    
                    if not result:
                        return False
                    
                    current_hash = result[0]
                    
                    # Verify old password
                    if not self.password_manager.verify_password(old_password, current_hash):
                        return False
                    
                    # Hash new password
                    new_hash = self.password_manager.hash_password(new_password)
                    
                    # Update password
                    cursor.execute(
                        """
                        UPDATE users
                        SET password_hash = %s
                        WHERE id = %s
                        """,
                        (new_hash, user_id)
                    )
                    conn.commit()
                    
                    return True
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve user information by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User dict without password_hash, or None if not found
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT id, username, email, created_at, updated_at, 
                               last_login, is_active
                        FROM users
                        WHERE id = %s
                        """,
                        (user_id,)
                    )
                    user = cursor.fetchone()
                    return dict(user) if user else None
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user account (soft delete).
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE users
                        SET is_active = FALSE
                        WHERE id = %s
                        """,
                        (user_id,)
                    )
                    conn.commit()
                    return cursor.rowcount > 0
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return False


if __name__ == "__main__":
    """
    Demonstration of database manager functionality.
    
    Note: Requires a PostgreSQL database to be set up with the schema
    from database_schema.sql and proper environment variables in .env
    """
    print("=" * 70)
    print("Database Manager Demonstration")
    print("=" * 70)
    print("\nThis is a demo module. To use it:")
    print("1. Set up PostgreSQL database")
    print("2. Run database_schema.sql to create tables")
    print("3. Configure .env with database credentials and PASSWORD_PEPPER")
    print("4. Import and use DatabaseManager in your application")
    print("\nExample usage:")
    print("-" * 70)
    print("""
from db_manager import DatabaseManager

# Initialize database manager
db = DatabaseManager()

# Create a new user
user_id = db.create_user("john_doe", "john@example.com", "SecurePass123!")
print(f"Created user with ID: {user_id}")

# Authenticate user
user = db.authenticate_user("john_doe", "SecurePass123!")
if user:
    print(f"Welcome back, {user['username']}!")
else:
    print("Authentication failed")

# Change password
success = db.change_password(user_id, "SecurePass123!", "NewSecurePass456!")
if success:
    print("Password changed successfully")
    """)
    print("=" * 70)
