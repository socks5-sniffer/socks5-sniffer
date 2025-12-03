# Password Security Implementation Guide

## Overview

This implementation demonstrates a secure password storage system using **pepper, salt, and hash** with the Argon2id algorithm. This provides defense-in-depth security for user credentials.

## Security Layers

### 1. **Pepper** (Global Secret)
- **What**: A secret key shared across all passwords
- **Where**: Stored in environment variables (`.env` file)
- **Why**: Provides an additional layer of security beyond the database
- **Benefit**: If database is breached, attacker still cannot crack passwords without the pepper

### 2. **Salt** (Per-Password Random Value)
- **What**: A unique random value for each password
- **Where**: Stored as part of the hash string in the database
- **Why**: Prevents rainbow table attacks
- **Benefit**: Same password for different users produces different hashes

### 3. **Hash** (One-Way Function)
- **What**: Argon2id - winner of the Password Hashing Competition
- **Why**: Memory-hard algorithm resistant to GPU and ASIC attacks
- **Configuration**: 
  - Time cost: 3 iterations
  - Memory cost: 64MB
  - Parallelism: 4 threads
  - Hash length: 32 bytes
  - Salt length: 16 bytes

## How It Works

### Password Storage Flow
```
User Password
    ↓
Pepper + Password (concatenation)
    ↓
Argon2id(peppered_password, random_salt)
    ↓
Password Hash (stored in database)
```

### Password Verification Flow
```
User enters password
    ↓
Pepper + Password (concatenation)
    ↓
Argon2id(peppered_password, salt_from_hash)
    ↓
Compare with stored hash
    ↓
Accept/Reject login
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate a Pepper
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

# Security Configuration
PASSWORD_PEPPER=your_generated_pepper_here
```

### 4. Set Up Database
```bash
psql -U your_database_user -d your_database_name -f database_schema.sql
```

## Usage Examples

### Basic Password Operations

```python
from password_utils import PasswordManager

# Initialize with pepper from environment
pm = PasswordManager()

# Hash a password
password_hash = pm.hash_password("user_password_123")
print(password_hash)
# Output: $argon2id$v=19$m=65536,t=3,p=4$...

# Verify a password
is_valid = pm.verify_password("user_password_123", password_hash)
print(is_valid)  # True

is_valid = pm.verify_password("wrong_password", password_hash)
print(is_valid)  # False
```

### Database Operations

```python
from db_manager import DatabaseManager

# Initialize database manager
db = DatabaseManager()

# Create a new user (password is automatically peppered and hashed)
user_id = db.create_user("john_doe", "john@example.com", "SecurePass123!")
print(f"Created user with ID: {user_id}")

# Authenticate user
user = db.authenticate_user("john_doe", "SecurePass123!")
if user:
    print(f"Welcome back, {user['username']}!")
    print(f"Email: {user['email']}")
    print(f"Last login: {user['last_login']}")
else:
    print("Authentication failed")

# Change password
success = db.change_password(user_id, "SecurePass123!", "NewSecurePass456!")
if success:
    print("Password changed successfully")
```

## Security Best Practices

### ✅ DO:
1. **Store pepper in environment variables** - Never in database or code
2. **Use strong, random peppers** - At least 32 characters (64 recommended)
3. **Keep pepper secret** - Treat it like a private key
4. **Backup pepper securely** - Store in secure key management system
5. **Use HTTPS** - Always transmit passwords over encrypted connections
6. **Implement rate limiting** - Prevent brute force attacks
7. **Add account lockout** - After multiple failed attempts
8. **Use prepared statements** - Prevent SQL injection (already implemented)
9. **Log authentication events** - For security monitoring
10. **Rotate pepper periodically** - With proper migration strategy

### ❌ DON'T:
1. **Don't commit pepper to version control** - Use `.gitignore`
2. **Don't store passwords in plain text** - Always hash them
3. **Don't use weak hashing algorithms** - Avoid MD5, SHA1, SHA256 for passwords
4. **Don't implement your own crypto** - Use vetted libraries
5. **Don't expose password hashes** - Even in APIs or logs
6. **Don't use the same salt for all passwords** - Argon2 handles this automatically
7. **Don't send passwords via email** - Use password reset tokens instead
8. **Don't log passwords** - Not even hashed ones in most cases

## Testing

Run the unit tests:
```bash
python test_password_utils.py
```

Run the demonstration:
```bash
python password_utils.py
```

## Threat Model

### What This Protects Against:
- ✅ **Database breach**: Pepper not in database, passwords still protected
- ✅ **Rainbow tables**: Unique salt per password
- ✅ **GPU cracking**: Argon2id is memory-hard
- ✅ **ASIC attacks**: Memory-hard algorithm
- ✅ **SQL injection**: Prepared statements used
- ✅ **Timing attacks**: Constant-time comparison in Argon2

### What This Does NOT Protect Against:
- ❌ **Weak passwords**: Still need password strength requirements
- ❌ **Phishing**: User education and 2FA needed
- ❌ **Keyloggers**: Endpoint security required
- ❌ **Application compromise**: If attacker gets pepper, game over
- ❌ **Social engineering**: User awareness needed

## Pepper Rotation Strategy

If you need to rotate the pepper (e.g., suspected compromise):

1. **Add new pepper** to environment with different name
2. **Keep old pepper** available for verification
3. **Update code** to try both peppers for verification
4. **Migrate users gradually**:
   - On successful login with old pepper, rehash with new pepper
   - Update database with new hash
5. **Monitor migration progress**
6. **Remove old pepper** once all users migrated

## Performance Considerations

Argon2id is intentionally slow to resist attacks. Typical timing:
- **Hashing**: 100-300ms per password
- **Verification**: 100-300ms per password

This is acceptable for login operations but consider:
- Implement rate limiting to prevent abuse
- Use asynchronous processing for batch operations
- Don't hash passwords on hot paths
- Cache authentication tokens (with expiration)

## Compliance

This implementation helps meet requirements for:
- **OWASP**: Top 10 - A02:2021 Cryptographic Failures
- **PCI DSS**: Requirement 8.2.1 (Strong cryptography)
- **GDPR**: Article 32 (Security of processing)
- **NIST 800-63B**: Section 5.1.1.2 (Password storage)
- **HIPAA**: Technical safeguards for PHI

## References

- [Argon2 RFC](https://tools.ietf.org/html/rfc9106)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)
- [Pepper vs Salt](https://security.stackexchange.com/questions/3272/password-hashing-add-salt-pepper-or-is-salt-enough)

## Support

For questions or issues, please open a GitHub issue or reach out to the repository maintainer.
