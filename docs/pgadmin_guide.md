# pgAdmin Connection Guide

## Step-by-Step Instructions to View Your Database

### 1. Open pgAdmin
- Launch pgAdmin from your Start Menu or desktop shortcut

### 2. Connect to PostgreSQL Server
When pgAdmin opens, you'll see a login screen or server list:

**If you see a login screen:**
- Enter your pgAdmin master password (if you set one)

**If you see "Add New Server" or no servers:**
- Right-click on "Servers" in the left panel
- Select "Register" → "Server..."

### 3. Configure Server Connection
In the "Create - Server" dialog:

**General Tab:**
- Name: `SignIn App Server` (or any name you prefer)

**Connection Tab:**
- Host name/address: `localhost`
- Port: `5432`
- Maintenance database: `postgres`
- Username: `postgres`
- Password: `1204`
- Save password: ✅ (check this box)

**Click "Save"**

### 4. Navigate to Your Database
Once connected, expand the server tree:

```
Servers
└── SignIn App Server
    └── Databases
        ├── postgres (default)
        ├── signin_app ← YOUR DATABASE
        └── template0
        └── template1
```

### 5. View Your Tables
Expand the `signin_app` database:

```
signin_app
└── Schemas
    └── public
        └── Tables
            ├── sessions
            └── users
```

### 6. View Data in Tables

**To view Users table:**
1. Right-click on `users` table
2. Select "View/Edit Data" → "All Rows"
3. You'll see all your users: alice, bob, Ishita, Isha

**To view Sessions table:**
1. Right-click on `sessions` table  
2. Select "View/Edit Data" → "All Rows"
3. You'll see active sessions (empty when no one is signed in)

### 7. Run Custom Queries
To run SQL queries:

1. Right-click on `signin_app` database
2. Select "Query Tool"
3. Enter SQL commands like:
   ```sql
   SELECT * FROM users;
   SELECT * FROM sessions;
   SELECT COUNT(*) FROM users;
   ```

### 8. Real-time Monitoring
Keep pgAdmin open while testing your app:
- Sign up a new user → Check `users` table
- Sign in → Check `sessions` table  
- Sign out → Check `sessions` table (session deleted)

## Troubleshooting

**If connection fails:**
- Make sure PostgreSQL service is running
- Check if password `1204` is correct
- Try host `127.0.0.1` instead of `localhost`

**If you can't see the database:**
- Refresh the server (right-click server → "Refresh")
- Check if `signin_app` database exists

**If tables are empty:**
- The tables are created automatically when you run the Flask app
- Make sure you've run `python app.py` at least once 