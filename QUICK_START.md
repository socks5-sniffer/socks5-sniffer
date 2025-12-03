# Quick Start Guide - Password Pepper Implementation

## 🚀 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate a Secure Pepper
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output (a 64-character hexadecimal string).

### Step 3: Create Environment File
```bash
cp .env.example .env
```

Edit `.env` and add your pepper:
```env
PASSWORD_PEPPER=your_generated_pepper_here
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### Step 4: Set Up Database (Optional)
```bash
psql -U postgres -d your_database_name -f database_schema.sql
```

### Step 5: Try It Out!
```bash
# Run the interactive demo
python example_app.py

# Or run the tests
python test_password_utils.py
```

## 📝 Basic Usage Examples

### Example 1: Hash a Password
```python
from password_utils import PasswordManager

pm = PasswordManager()
password_hash = pm.hash_password("MySecurePassword123!")
print(password_hash)
# Output: $argon2id$v=19$m=65536,t=3,p=4$...
```

### Example 2: Verify a Password
```python
from password_utils import PasswordManager

pm = PasswordManager()

# Hash a password
password_hash = pm.hash_password("MySecurePassword123!")

# Verify correct password
is_valid = pm.verify_password("MySecurePassword123!", password_hash)
print(is_valid)  # True

# Verify wrong password
is_valid = pm.verify_password("WrongPassword", password_hash)
print(is_valid)  # False
```

### Example 3: Create and Authenticate User (with Database)
```python
from db_manager import DatabaseManager

db = DatabaseManager()

# Create a new user
user_id = db.create_user(
    username="alice",
    email="alice@example.com",
    password="SecurePass123!"
)
print(f"User created with ID: {user_id}")

# Authenticate the user
user = db.authenticate_user("alice", "SecurePass123!")
if user:
    print(f"Welcome back, {user['username']}!")
    print(f"Email: {user['email']}")
else:
    print("Authentication failed")
```

### Example 4: Change Password
```python
from db_manager import DatabaseManager

db = DatabaseManager()

success = db.change_password(
    user_id=1,
    old_password="SecurePass123!",
    new_password="NewSecurePass456!"
)

if success:
    print("Password changed successfully!")
else:
    print("Failed to change password")
```

## 🎯 Common Commands

### Generate a New Pepper
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Run All Tests
```bash
python test_password_utils.py
```

### Run Interactive Demo (No Database Required)
```bash
python example_app.py
# Select option 6 for password hashing demo
```

### Run Password Hashing Demo
```bash
python password_utils.py
```

## 🔍 What Happens Under the Hood?

```
User Password: "MySecurePassword123!"
        ↓
Pepper Added: "e903a5a0...MySecurePassword123!"
        ↓
Random Salt: (generated: 16 bytes)
        ↓
Argon2id Hash: (computed with salt)
        ↓
Final Hash: "$argon2id$v=19$m=65536,t=3,p=4$..."
        ↓
Stored in Database
```

### Why This Is Secure:

1. **Pepper** (Global Secret)
   - Stored in `.env`, NOT in database
   - If database is breached, attacker still can't crack passwords
   - Acts as a secret key for all passwords

2. **Salt** (Per-Password Random)
   - Unique for each password
   - Prevents rainbow table attacks
   - Included in the hash string

3. **Argon2id** (Memory-Hard Hash)
   - Resistant to GPU attacks
   - Slow enough to prevent brute force
   - Fast enough for login (100-300ms)

## ⚠️ Security Reminders

### ✅ DO:
- Store pepper in environment variables
- Use `.gitignore` to exclude `.env` file
- Generate strong, random peppers (64+ characters)
- Keep pepper secret and backed up securely
- Use HTTPS in production

### ❌ DON'T:
- Commit `.env` file to git
- Share your pepper publicly
- Store passwords in plain text
- Use simple passwords (even with pepper)
- Log passwords (even hashed ones)

## 📚 Next Steps

- Read **[PASSWORD_SECURITY.md](PASSWORD_SECURITY.md)** for detailed security documentation
- Read **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** for technical details
- Check the interactive demo: `python example_app.py`
- Review the test cases: `test_password_utils.py`

## 🆘 Troubleshooting

### "PASSWORD_PEPPER environment variable not set"
**Solution**: Generate a pepper and add it to your `.env` file

### "Database error: connection refused"
**Solution**: Check your database is running and credentials in `.env` are correct

### Tests failing
**Solution**: Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

## 📞 Support

For questions or issues:
1. Check the documentation files in this repository
2. Review the example code in `example_app.py`
3. Open a GitHub issue

---

**Remember**: The pepper is like a master key. Keep it safe! 🔐
