## Hi there 👋


**socks5-sniffer/socks5-sniffer** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

# 🏗️ After the military and construction beat me up, I am hanging my tool belt up for some lumbar support and a cool coffee mug.  

Newly budding developer with an interest in security.  I started out curious on how passwords were salted/ hashed and...well I kept reading.  

genAI is helping me through the giant hurdles that held me back from learning to code before, and I am so thankful for it.  

Reach out and let me know what I am doing wrong and I will thank you big!



## 🔒 Never-Change Security Notes

My projects focus on access control, API Security, and Data Protection.  Other security practices executed to keep the code safe and stable include:

Safe Input Handling:
All user input is checked and sanitized. For example, database queries use prepared statements to avoid SQL injection.

No Secrets in Code:
API keys and passwords are stored in environment variables or GitHub Secrets, never in the repo.

Dependency Safety:
The projects use tools like Dependabot to watch for vulnerable packages.

Protected Workflow:
Important branches require reviews before merging to prevent unwanted changes.


## 🛠️ Tech Stack

* **Linux/ Win
* **Server:** Apache
* **Database:** PostgreSQL
* **Languages:** Python / PHP / HTML
* **Hosting:** Hostinger, localhost, Firebase
* **Version Control:** Git / GitHub

## ✨ Features

* Password Hash, Salt & Pepper - **[Implementation Available](PASSWORD_SECURITY.md)**
* Utilize Argon2id
* 1 man DevSecOps

## 🔐 Password Pepper Implementation

This repository now includes a complete implementation of secure password storage using **pepper + salt + hash** with Argon2id!

### What's Included:
- **`password_utils.py`** - Core password hashing with pepper support
- **`db_manager.py`** - Database operations with PostgreSQL
- **`database_schema.sql`** - Database schema for user credentials
- **`example_app.py`** - Interactive CLI demo application
- **`test_password_utils.py`** - Comprehensive unit tests
- **`PASSWORD_SECURITY.md`** - Complete security documentation

### Quick Start:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate a secure pepper
python -c "import secrets; print(secrets.token_hex(32))"

# 3. Configure environment
cp .env.example .env
# Edit .env with your database credentials and pepper

# 4. Set up database
psql -U postgres -d your_database -f database_schema.sql

# 5. Run the demo
python example_app.py

# 6. Run tests
python test_password_utils.py
```

### Security Features:
- ✅ **Pepper**: Global secret key (not stored in database)
- ✅ **Salt**: Unique per-password (prevents rainbow tables)
- ✅ **Argon2id**: Memory-hard hashing (GPU-resistant)
- ✅ **Defense-in-depth**: Multiple layers of protection
- ✅ **Prepared statements**: SQL injection prevention

For detailed documentation, see **[PASSWORD_SECURITY.md](PASSWORD_SECURITY.md)**

## 🚀 Getting Started

- 🔭 I’m currently working on... 3 personal apps with genAI, 2 websites, and a raspberry pi powered automatic fish feeder (that is also my private home server).
- 🌱 I’m currently learning ...genAI Leaders / Cyber Security courses by Google, Python, HTML, PHP, and 3d printers.
- 👯 I’m looking to collaborate on ...small projects centered around security features and fun D.I.Y. projects.
- 🤔 I’m looking for help with ...sound advice for a 40 y.o. man changing carreers at a time like this.
- 💬 Ask me about ...how I even got here!
- ⚡ Fun fact: ...I have 17 animals.
-->
