-------Python Multi-threaded Chatroom-------
A real-time chatroom application built with Python using socket programming and multi-threading. Features a clean Tkinter GUI and comprehensive admin controls for managing users.
-Core Features
Real-time messaging - Instant communication between multiple users
Multi-threaded server - Handles multiple clients simultaneously
User-friendly GUI - Clean Tkinter interface for easy interaction
Timestamped messages - Every message includes date and time
Emoji support - Express yourself with emojis in messages

- Chat Commands

/help - Display all available commands
/users - Show list of online users
/dm <username> <message> - Send private direct messages
/kick <username> - (Admin only) Remove user from chat
/ban <username> - (Admin only) Permanently ban user

-Admin Features
Password-protected admin access - Secure admin login
User management - Kick disruptive users instantly
Permanent bans - Ban users with persistent ban list
Admin commands - Full control over chatroom

- Getting Started
Prerequisites

Python 3.6 or higher
Required modules: socket, threading, tkinter, datetime

Installation

Clone the repository
bashgit clone https://github.com/yourusername/python-chatroom.git
cd python-chatroom

Install dependencies
bash# All required modules are built-in Python libraries
NOTE: Make sure you have the emojis.py module for emoji support

Run the server
bashpython tcp_server.py

Connect clients
bashpython gui_client.py

- Instructions for using
Starting the Chatroom

Start the server by running tcp_server.py
Launch clients by running gui_client.py for each user
Enter your nickname when prompted
Start chatting.

Admin Access

Use username: admin
Enter the admin password when prompted
Gain access to kick and ban commands

- Available Commands
/help              - Show help menu
/users             - Display online users
/dm user message   - Send private message
/kick username     - (Admin) Kick user
/ban username      - (Admin) Ban user permanently
- Project Structure
chatroom/
│
├── tcp_server.py      # Main server handling multiple clients
├── gui_client.py      # Tkinter GUI client application
├── emojis.py          # Emoji conversion module
├── bans.txt           # Persistent ban list (auto-generated)
└── README.md          # This file
🔧 Technical Details

-Architecture
Server: Multi-threaded TCP server using Python's socket and threading modules
Client: Tkinter-based GUI with real-time message handling
Protocol: Custom text-based protocol over TCP
Concurrency: Each client handled in separate thread

- Key Components

1. Message Broadcasting: Server broadcasts messages to all connected clients
2. Private Messaging: Direct message system between users
3. ser Management: Dynamic user list with join/leave notifications
4. Admin System: Secure admin authentication and moderation tools
5. Persistent Bans: Ban list stored in file for permanent bans

- Configuration
Server Settings
pythonHOST = '127.0.0.1'  # Server IP address
PORT = 55545        # Server port

- Admin Settings
Default admin password: kv123
Ban list file: bans.txt

- Some Issues
Server must be restarted to reset ban list
GUI doesn't auto-scroll to latest messages on some systems
No message history persistence between sessions


- Author
Khyati Verma
GitHub: @Khyativ991
Email: khyativ2178@gmail.com

- Acknowledgments
Built with Python's powerful socket programming capabilities
Tkinter for the cross-platform GUI framework
Threading module for concurrent client handling
Inspired by classic IRC chatroom