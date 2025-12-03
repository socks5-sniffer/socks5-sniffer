"""
Password Utility Module with Pepper Support

This module implements secure password handling with pepper, salt, and hash.
The pepper is a secret value added to passwords before hashing, providing an
additional layer of security beyond the per-password salt.

Security Flow:
1. Pepper: Secret key stored in environment variables (global, not in DB)
2. Salt: Random value generated per password (stored in hash string)
3. Hash: Argon2id algorithm (memory-hard, resistant to GPU attacks)

Process: password -> pepper + password -> Argon2id(peppered_password) -> hash
"""

import os
import secrets
from typing import Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PasswordPepperError(Exception):
    """Raised when pepper is not configured or invalid"""
    pass


class PasswordManager:
    """
    Manages password hashing and verification with pepper support.
    
    The pepper is a secret key that is:
    - Stored separately from the database (in environment variables)
    - Applied to all passwords before hashing
    - Provides defense-in-depth against database breaches
    
    If an attacker gains access to the database, they still cannot crack
    passwords without also obtaining the pepper from the application server.
    """
    
    def __init__(self, pepper: Optional[str] = None):
        """
        Initialize the password manager.
        
        Args:
            pepper: Optional pepper value. If not provided, reads from PASSWORD_PEPPER
                   environment variable.
                   
        Raises:
            PasswordPepperError: If pepper is not provided and not in environment
        """
        self.pepper = pepper or os.getenv('PASSWORD_PEPPER')
        
        if not self.pepper:
            raise PasswordPepperError(
                "PASSWORD_PEPPER environment variable not set. "
                "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        
        if len(self.pepper) < 32:
            raise PasswordPepperError(
                "Pepper must be at least 32 characters long for adequate security"
            )
        
        # Initialize Argon2id password hasher with secure parameters
        # time_cost=3: Number of iterations (higher = slower but more secure)
        # memory_cost=65536: Memory usage in KiB (64MB - resistant to GPU attacks)
        # parallelism=4: Number of parallel threads
        # hash_len=32: Length of hash output in bytes
        # salt_len=16: Length of salt in bytes
        self.hasher = PasswordHasher(
            time_cost=3,
            memory_cost=65536,
            parallelism=4,
            hash_len=32,
            salt_len=16
        )
    
    def _pepper_password(self, password: str) -> str:
        """
        Apply pepper to password.
        
        Args:
            password: The plain text password
            
        Returns:
            The peppered password
        """
        return self.pepper + password
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password with pepper and salt using Argon2id.
        
        The process:
        1. Concatenate pepper + password
        2. Generate random salt (done automatically by Argon2)
        3. Hash the peppered password with Argon2id
        4. Return hash string (includes algorithm parameters and salt)
        
        Args:
            password: The plain text password to hash
            
        Returns:
            The Argon2id hash string containing algorithm params, salt, and hash
            
        Example:
            >>> pm = PasswordManager()
            >>> hash_str = pm.hash_password("user_password_123")
            >>> print(hash_str)
            $argon2id$v=19$m=65536,t=3,p=4$...$...
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        peppered_password = self._pepper_password(password)
        return self.hasher.hash(peppered_password)
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password: The plain text password to verify
            password_hash: The stored Argon2id hash
            
        Returns:
            True if password matches, False otherwise
            
        Example:
            >>> pm = PasswordManager()
            >>> hash_str = pm.hash_password("user_password_123")
            >>> pm.verify_password("user_password_123", hash_str)
            True
            >>> pm.verify_password("wrong_password", hash_str)
            False
        """
        if not password or not password_hash:
            return False
        
        try:
            peppered_password = self._pepper_password(password)
            self.hasher.verify(password_hash, peppered_password)
            
            # Check if hash needs rehashing (parameters changed)
            if self.hasher.check_needs_rehash(password_hash):
                # In a real application, you would rehash and update the database here
                pass
            
            return True
        except (VerifyMismatchError, InvalidHashError):
            return False
    
    def needs_rehash(self, password_hash: str) -> bool:
        """
        Check if a password hash needs to be updated.
        
        This is useful when you change hashing parameters (e.g., increase time_cost)
        and want to gradually update existing password hashes.
        
        Args:
            password_hash: The stored Argon2id hash
            
        Returns:
            True if hash should be regenerated with current parameters
        """
        try:
            return self.hasher.check_needs_rehash(password_hash)
        except InvalidHashError:
            return True


def generate_pepper() -> str:
    """
    Generate a cryptographically secure random pepper.
    
    Returns:
        A 64-character hexadecimal string (256 bits of entropy)
        
    Example:
        >>> pepper = generate_pepper()
        >>> len(pepper)
        64
        >>> print(f"Add this to your .env file:\nPASSWORD_PEPPER={pepper}")
    """
    return secrets.token_hex(32)


if __name__ == "__main__":
    # Demonstration of password pepper functionality
    print("=" * 70)
    print("Password Pepper Demonstration")
    print("=" * 70)
    
    # Generate a new pepper for demonstration
    demo_pepper = generate_pepper()
    print(f"\n1. Generated secure pepper:\n   {demo_pepper}")
    print("\n   ⚠️  IMPORTANT: Store this in your .env file as PASSWORD_PEPPER")
    print("   ⚠️  NEVER commit this to version control!")
    
    # Create password manager with the demo pepper
    pm = PasswordManager(pepper=demo_pepper)
    
    # Demo password
    demo_password = "MySecurePassword123!"
    print(f"\n2. Original password: {demo_password}")
    
    # Hash the password
    password_hash = pm.hash_password(demo_password)
    print(f"\n3. Peppered, salted, and hashed password:")
    print(f"   {password_hash}")
    
    # Verify correct password
    print(f"\n4. Verifying correct password...")
    is_valid = pm.verify_password(demo_password, password_hash)
    print(f"   Result: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Verify wrong password
    print(f"\n5. Verifying wrong password...")
    is_valid = pm.verify_password("WrongPassword", password_hash)
    print(f"   Result: {'✓ Valid' if is_valid else '✗ Invalid'}")
    
    # Show that different passwords create different hashes
    print(f"\n6. Creating another hash of the same password:")
    password_hash_2 = pm.hash_password(demo_password)
    print(f"   {password_hash_2}")
    print(f"\n   Note: Hashes are different due to unique salts,")
    print(f"   but both verify correctly!")
    
    is_valid_2 = pm.verify_password(demo_password, password_hash_2)
    print(f"   Verification: {'✓ Valid' if is_valid_2 else '✗ Invalid'}")
    
    print("\n" + "=" * 70)
    print("Security Notes:")
    print("=" * 70)
    print("• Pepper: Global secret key (stored in environment)")
    print("• Salt: Per-password random value (stored in hash string)")
    print("• Hash: Argon2id (memory-hard, GPU-resistant)")
    print("• Even if database is breached, passwords remain protected")
    print("  without the pepper from the application server")
    print("=" * 70)
