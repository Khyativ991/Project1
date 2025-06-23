# Python Socket Chatroom

A terminal-based real-time chatroom built using Python's `socket` and `threading` modules. Supports multiple clients, emojis, and admin commands like kicking and banning users.

---

## Features

- Multi-client real-time messaging using threads
- Admin login with password authentication
- Kick users with `KICK <username>`
- Ban users with `BAN <username>` (saved in `bans.txt`)
- Timestamped join/leave and message logs
- Emoji support in messages

---

## Files Included

chatroom/
│
├── tcpserver.py # Server script
├── tcpclient.py # Client script
├── emojis.py # (Optional) for emoji handling
├── bans.txt # Stores permanently banned users
└── README.md # Project description

yaml
Copy
Edit

---

## 🧑‍💻 How to Use

### 1. Start the server
```bash
python tcpserver.py
2. Start each client
bash
Copy
Edit
python tcpclient.py
Enter your nickname when prompted.

If your nickname is admin, you'll be asked for a password (set in tcpserver.py).

# Admin Commands (only work for admin)
KICK username — kicks a user out of the chat

BAN username — bans the user and prevents them from joining again

# Bans
Banned usernames are saved in bans.txt

If a banned user tries to join again, the server will automatically disconnect them

# Emoji Support
You can send emojis like:

# Requirements
Python 3.x

No external dependencies
