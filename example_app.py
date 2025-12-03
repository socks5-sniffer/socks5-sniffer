#!/usr/bin/env python3
"""
Example Application: User Authentication with Peppered Passwords

This is a simple command-line application demonstrating the password pepper
implementation with database integration.
"""

import sys
from getpass import getpass
from password_utils import PasswordManager, generate_pepper
from db_manager import DatabaseManager


def print_banner():
    """Print application banner"""
    print("\n" + "=" * 70)
    print("  🔐 Secure User Authentication System")
    print("  Password Pepper + Salt + Hash (Argon2id)")
    print("=" * 70 + "\n")


def print_menu():
    """Print main menu"""
    print("\nMain Menu:")
    print("1. Register new user")
    print("2. Login")
    print("3. Change password")
    print("4. View user info")
    print("5. Generate new pepper (for .env file)")
    print("6. Demo password hashing")
    print("0. Exit")
    print()


def demo_hashing():
    """Demonstrate password hashing without database"""
    print("\n" + "-" * 70)
    print("Password Hashing Demonstration")
    print("-" * 70)
    
    # Generate a demo pepper
    demo_pepper = generate_pepper()
    print(f"\n1. Generated demo pepper: {demo_pepper}")
    print("   (In production, this goes in your .env file)")
    
    # Get password from user
    password = getpass("\n2. Enter a password to hash: ")
    if not password:
        print("   No password entered. Returning to menu.")
        return
    
    # Create password manager with demo pepper
    pm = PasswordManager(pepper=demo_pepper)
    
    # Hash the password
    password_hash = pm.hash_password(password)
    print(f"\n3. Generated hash:")
    print(f"   {password_hash}")
    
    # Verify correct password
    print("\n4. Verifying correct password...")
    is_valid = pm.verify_password(password, password_hash)
    print(f"   Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    # Verify wrong password
    print("\n5. Verifying wrong password...")
    is_valid = pm.verify_password("definitely_wrong_password", password_hash)
    print(f"   Result: {'✓ VALID' if is_valid else '✗ INVALID'}")
    
    # Show uniqueness of hashes
    print("\n6. Creating another hash of the same password...")
    password_hash_2 = pm.hash_password(password)
    print(f"   {password_hash_2}")
    print("\n   Note: Hashes are different due to unique salts!")
    print("   Both hashes verify correctly against the same password.")
    
    print("\n" + "-" * 70)


def register_user(db: DatabaseManager):
    """Register a new user"""
    print("\n" + "-" * 70)
    print("User Registration")
    print("-" * 70)
    
    username = input("\nEnter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    
    email = input("Enter email: ").strip()
    if not email:
        print("Email cannot be empty.")
        return
    
    password = getpass("Enter password: ")
    if not password:
        print("Password cannot be empty.")
        return
    
    password_confirm = getpass("Confirm password: ")
    if password != password_confirm:
        print("Passwords do not match.")
        return
    
    print("\n⏳ Creating user...")
    user_id = db.create_user(username, email, password)
    
    if user_id:
        print(f"✓ User created successfully with ID: {user_id}")
        print(f"  Username: {username}")
        print(f"  Email: {email}")
        print("  Password has been peppered, salted, and hashed securely!")
    else:
        print("✗ Failed to create user. Username or email may already exist.")
    
    print("-" * 70)


def login_user(db: DatabaseManager):
    """Authenticate a user"""
    print("\n" + "-" * 70)
    print("User Login")
    print("-" * 70)
    
    username = input("\nEnter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None
    
    password = getpass("Enter password: ")
    if not password:
        print("Password cannot be empty.")
        return None
    
    print("\n⏳ Authenticating...")
    user = db.authenticate_user(username, password)
    
    if user:
        print("✓ Login successful!")
        print(f"  User ID: {user['id']}")
        print(f"  Username: {user['username']}")
        print(f"  Email: {user['email']}")
        print(f"  Last login: {user['last_login']}")
        return user
    else:
        print("✗ Authentication failed. Invalid username or password.")
        return None


def change_password(db: DatabaseManager):
    """Change user password"""
    print("\n" + "-" * 70)
    print("Change Password")
    print("-" * 70)
    
    # First authenticate
    username = input("\nEnter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    
    old_password = getpass("Enter current password: ")
    if not old_password:
        print("Password cannot be empty.")
        return
    
    # Verify current credentials
    print("\n⏳ Verifying current credentials...")
    user = db.authenticate_user(username, old_password)
    
    if not user:
        print("✗ Authentication failed. Invalid username or password.")
        return
    
    print("✓ Current credentials verified.")
    
    # Get new password
    new_password = getpass("\nEnter new password: ")
    if not new_password:
        print("New password cannot be empty.")
        return
    
    new_password_confirm = getpass("Confirm new password: ")
    if new_password != new_password_confirm:
        print("Passwords do not match.")
        return
    
    # Change password
    print("\n⏳ Changing password...")
    success = db.change_password(user['id'], old_password, new_password)
    
    if success:
        print("✓ Password changed successfully!")
        print("  Your new password has been peppered, salted, and hashed.")
    else:
        print("✗ Failed to change password.")
    
    print("-" * 70)


def view_user_info(db: DatabaseManager):
    """View user information"""
    print("\n" + "-" * 70)
    print("View User Information")
    print("-" * 70)
    
    try:
        user_id = int(input("\nEnter user ID: ").strip())
    except ValueError:
        print("Invalid user ID.")
        return
    
    print("\n⏳ Fetching user information...")
    user = db.get_user_by_id(user_id)
    
    if user:
        print("✓ User found:")
        print(f"  ID: {user['id']}")
        print(f"  Username: {user['username']}")
        print(f"  Email: {user['email']}")
        print(f"  Created: {user['created_at']}")
        print(f"  Updated: {user['updated_at']}")
        print(f"  Last login: {user['last_login']}")
        print(f"  Active: {user['is_active']}")
    else:
        print("✗ User not found.")
    
    print("-" * 70)


def generate_pepper_cli():
    """Generate a new pepper for configuration"""
    print("\n" + "-" * 70)
    print("Generate Password Pepper")
    print("-" * 70)
    
    pepper = generate_pepper()
    print(f"\nGenerated secure pepper (256 bits):")
    print(f"  {pepper}")
    print("\n⚠️  IMPORTANT SECURITY NOTES:")
    print("  1. Add this to your .env file as: PASSWORD_PEPPER={pepper}")
    print("  2. NEVER commit this to version control")
    print("  3. Keep this secret - treat it like a private key")
    print("  4. Store backups in a secure key management system")
    print("  5. If compromised, all passwords must be rehashed")
    
    print("\nTo use this pepper:")
    print("  1. Add to .env file")
    print("  2. Restart your application")
    print("  3. All new passwords will use this pepper")
    
    print("-" * 70)


def main():
    """Main application loop"""
    print_banner()
    
    print("Checking configuration...")
    try:
        # Try to initialize database manager
        # This will check if pepper is configured
        db = DatabaseManager()
        print("✓ Configuration loaded successfully")
        print("✓ Password pepper is configured")
        print("✓ Database connection settings loaded")
    except Exception as e:
        print(f"⚠️  Configuration issue: {e}")
        print("\nYou can still use the demo features (options 5 and 6)")
        print("To use database features, please configure your .env file")
        db = None
    
    while True:
        print_menu()
        choice = input("Enter your choice (0-6): ").strip()
        
        if choice == "0":
            print("\nThank you for using the Secure Authentication System!")
            print("Stay secure! 🔐\n")
            break
        
        elif choice == "1":
            if db:
                register_user(db)
            else:
                print("\n✗ Database not configured. Please set up .env file.")
        
        elif choice == "2":
            if db:
                login_user(db)
            else:
                print("\n✗ Database not configured. Please set up .env file.")
        
        elif choice == "3":
            if db:
                change_password(db)
            else:
                print("\n✗ Database not configured. Please set up .env file.")
        
        elif choice == "4":
            if db:
                view_user_info(db)
            else:
                print("\n✗ Database not configured. Please set up .env file.")
        
        elif choice == "5":
            generate_pepper_cli()
        
        elif choice == "6":
            demo_hashing()
        
        else:
            print("\n✗ Invalid choice. Please enter a number from 0 to 6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye! 👋\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        print("Please check your configuration and try again.\n")
        sys.exit(1)
