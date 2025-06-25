import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, ttk
from datetime import datetime
from emojis import convert_emojis, EMOJI_SHORTCUTS

HOST = '127.0.0.1'
PORT = 55545
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Dark theme colors
COLORS = {
    'bg_primary': '#0d1117',      # Dark background
    'bg_secondary': '#161b22',    # Slightly lighter background
    'bg_tertiary': '#21262d',     # Input/button background
    'fg_primary': '#f0f6fc',      # Main text color
    'fg_secondary': '#8b949e',    # Secondary text color
    'accent': '#238636',          # Green accent
    'accent_hover': '#2ea043',    # Green hover
    'danger': '#da3633',          # Red for errors
    'warning': '#d29922',         # Yellow for warnings
    'border': '#30363d'           # Border color
}

# GUI Setup
window = tk.Tk()
window.title("Chatroom 💬")
window.geometry("1000x700")
window.configure(bg=COLORS['bg_primary'])
window.minsize(800, 600)

# Configure style for ttk widgets
style = ttk.Style()
style.theme_use('clam')
style.configure('TNotebook', background=COLORS['bg_secondary'])
style.configure('TNotebook.Tab', background=COLORS['bg_tertiary'], foreground=COLORS['fg_primary'])

# Main container
main_container = tk.Frame(window, bg=COLORS['bg_primary'])
main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Header frame
header_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
header_frame.pack(fill=tk.X, pady=(0, 10))

# Title
title_label = tk.Label(header_frame, text="💬 Chatroom", 
                      font=("Segoe UI", 16, "bold"),
                      bg=COLORS['bg_primary'], fg=COLORS['fg_primary'])
title_label.pack(side=tk.LEFT)

# Help button in header
help_button = tk.Button(header_frame, text="❓ Help", 
                       font=("Segoe UI", 10),
                       bg=COLORS['bg_tertiary'], fg=COLORS['fg_primary'],
                       relief=tk.FLAT, padx=15, pady=5,
                       cursor="hand2")
help_button.pack(side=tk.RIGHT)

# Chat area
chat_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

chat_box = scrolledtext.ScrolledText(
    chat_frame, 
    font=("Consolas", 11),
    bg=COLORS['bg_secondary'], 
    fg=COLORS['fg_primary'],
    insertbackground=COLORS['fg_primary'],
    selectbackground=COLORS['accent'],
    selectforeground=COLORS['bg_primary'],
    relief=tk.FLAT,
    padx=10,
    pady=10,
    wrap=tk.WORD
)
chat_box.pack(fill=tk.BOTH, expand=True)
chat_box.config(state='disabled')

# Input area
input_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
input_frame.pack(fill=tk.X)

# Input box
input_box = tk.Entry(
    input_frame, 
    font=("Segoe UI", 11),
    bg=COLORS['bg_tertiary'], 
    fg=COLORS['fg_primary'],
    insertbackground=COLORS['fg_primary'],
    relief=tk.FLAT,
    bd=1
)
input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)

# Emoji button
emoji_button = tk.Button(
    input_frame, 
    text="😀", 
    font=("Segoe UI", 12),
    bg=COLORS['bg_tertiary'], 
    fg=COLORS['fg_primary'],
    relief=tk.FLAT,
    width=4,
    cursor="hand2",
    padx=5,
    pady=5
)
emoji_button.pack(side=tk.RIGHT, padx=(0, 10))

# Send button
send_button = tk.Button(
    input_frame, 
    text="Send", 
    font=("Segoe UI", 10, "bold"),
    bg=COLORS['accent'], 
    fg=COLORS['fg_primary'],
    relief=tk.FLAT,
    width=8,
    cursor="hand2",
    padx=10,
    pady=8
)
send_button.pack(side=tk.RIGHT)

# Global variables
nickname = ""
emoji_window = None

def get_timestamp():
    """Get current timestamp in HH:MM format"""
    return datetime.now().strftime("%H:%M")

def update_chat(message, message_type="normal"):
    """Update chat with color coding based on message type"""
    chat_box.config(state='normal')
    
    # Add timestamp
    timestamp = f"[{get_timestamp()}] "
    
    if message_type == "system":
        chat_box.insert(tk.END, timestamp, "timestamp")
        chat_box.insert(tk.END, message + '\n', "system")
    elif message_type == "dm":
        chat_box.insert(tk.END, timestamp, "timestamp")
        chat_box.insert(tk.END, message + '\n', "dm")
    elif message_type == "error":
        chat_box.insert(tk.END, timestamp, "timestamp")
        chat_box.insert(tk.END, message + '\n', "error")
    elif message_type == "admin":
        chat_box.insert(tk.END, timestamp, "timestamp")
        chat_box.insert(tk.END, message + '\n', "admin")
    else:
        chat_box.insert(tk.END, timestamp, "timestamp")
        chat_box.insert(tk.END, message + '\n', "normal")
    
    chat_box.yview(tk.END)
    chat_box.config(state='disabled')

# Configure text tags for different message types
def setup_chat_tags():
    chat_box.tag_configure("timestamp", foreground=COLORS['fg_secondary'], font=("Consolas", 9))
    chat_box.tag_configure("system", foreground=COLORS['warning'])
    chat_box.tag_configure("dm", foreground=COLORS['accent'])
    chat_box.tag_configure("error", foreground=COLORS['danger'])
    chat_box.tag_configure("admin", foreground="#ff6b6b")
    chat_box.tag_configure("normal", foreground=COLORS['fg_primary'])

def show_help():
    """Show help dialog with available commands"""
    help_text = """🆘 CHATROOM COMMANDS

📨 MESSAGING:
• Just type and press Enter to send messages
• Use emojis like :smile:, :heart:, :fire:
• Click 😀 button for emoji picker

💬 PRIVATE MESSAGES:
• /dm <username> <message> - Send private message
  Example: /dm john Hello there!

👥 USER COMMANDS:
• /users - Show all online users

🔧 ADMIN COMMANDS (Admin only):
• /kick <username> - Kick a user
• /ban <username> - Ban a user

🎨 EMOJIS:
Click the 😀 button to see all available emojis!
You can also type shortcuts like :smile:, :heart:, etc.

💡 TIPS:
• Press Enter to send messages
• Messages are timestamped automatically
• Private messages appear in green
• System messages appear in yellow"""
    
    # Create help window
    help_win = tk.Toplevel(window)
    help_win.title("Help - Chatroom Commands")
    help_win.geometry("500x600")
    help_win.configure(bg=COLORS['bg_primary'])
    help_win.resizable(False, False)
    
    # Center the help window
    help_win.transient(window)
    help_win.grab_set()
    
    # Help content
    help_frame = tk.Frame(help_win, bg=COLORS['bg_primary'])
    help_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    help_textbox = scrolledtext.ScrolledText(
        help_frame,
        font=("Segoe UI", 10),
        bg=COLORS['bg_secondary'],
        fg=COLORS['fg_primary'],
        relief=tk.FLAT,
        padx=15,
        pady=15,
        wrap=tk.WORD
    )
    help_textbox.pack(fill=tk.BOTH, expand=True)
    help_textbox.insert(tk.END, help_text)
    help_textbox.config(state='disabled')
    
    # Close button
    close_btn = tk.Button(
        help_frame,
        text="Close",
        font=("Segoe UI", 10, "bold"),
        bg=COLORS['accent'],
        fg=COLORS['fg_primary'],
        relief=tk.FLAT,
        command=help_win.destroy,
        padx=20,
        pady=8
    )
    close_btn.pack(pady=(10, 0))

def show_emoji_picker():
    """Show emoji picker window"""
    global emoji_window
    
    # Close existing emoji window if open
    if emoji_window and emoji_window.winfo_exists():
        emoji_window.destroy()
        return
    
    emoji_window = tk.Toplevel(window)
    emoji_window.title("Select Emoji")
    emoji_window.geometry("400x500")
    emoji_window.configure(bg=COLORS['bg_primary'])
    emoji_window.resizable(False, False)
    
    # Position near the main window
    x = window.winfo_x() + window.winfo_width() - 400
    y = window.winfo_y() + 50
    emoji_window.geometry(f"400x500+{x}+{y}")
    
    # Title
    title_frame = tk.Frame(emoji_window, bg=COLORS['bg_primary'])
    title_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
    
    tk.Label(title_frame, text="😀 Select Emoji", 
             font=("Segoe UI", 14, "bold"),
             bg=COLORS['bg_primary'], fg=COLORS['fg_primary']).pack(side=tk.LEFT)
    
    close_btn = tk.Button(title_frame, text="✕", 
                         font=("Segoe UI", 12, "bold"),
                         bg=COLORS['danger'], fg=COLORS['fg_primary'],
                         relief=tk.FLAT, width=3,
                         command=emoji_window.destroy)
    close_btn.pack(side=tk.RIGHT)
    
    # Scrollable emoji list
    canvas = tk.Canvas(emoji_window, bg=COLORS['bg_secondary'], highlightthickness=0)
    scrollbar = tk.Scrollbar(emoji_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_secondary'])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Add emojis
    row = 0
    for emoji_code, emoji_symbol in EMOJI_SHORTCUTS.items():
        emoji_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_secondary'])
        emoji_frame.pack(fill=tk.X, padx=10, pady=2)
        
        def insert_emoji(code=emoji_code):
            current_pos = input_box.index(tk.INSERT)
            input_box.insert(current_pos, code)
            input_box.focus_set()
            emoji_window.destroy()
        
        # Emoji button
        emoji_btn = tk.Button(
            emoji_frame, 
            text=emoji_symbol, 
            font=("Segoe UI", 16),
            bg=COLORS['bg_tertiary'], 
            fg=COLORS['fg_primary'],
            relief=tk.FLAT,
            width=3,
            command=insert_emoji,
            cursor="hand2"
        )
        emoji_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Emoji code
        tk.Label(emoji_frame, text=emoji_code, 
                font=("Segoe UI", 10),
                bg=COLORS['bg_secondary'], fg=COLORS['fg_secondary']).pack(side=tk.LEFT)
        
        row += 1
    
    # Pack canvas and scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0), pady=(0, 15))
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=(0, 15))
    
    # Bind mousewheel to canvas
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)

def send_message():
    """Send message to server"""
    msg = input_box.get().strip()
    if not msg:
        return
        
    input_box.delete(0, tk.END)
    msg = convert_emojis(msg)
    
    if msg.startswith('/'):
        handle_command(msg)
    else:
        # Regular message
        try:
            full_msg = f"{nickname}: {msg}"
            client.send(full_msg.encode('utf-8'))
        except Exception as e:
            update_chat(f"❌ Failed to send message: {e}", "error")

def handle_command(msg):
    """Handle slash commands"""
    command_parts = msg.split(' ', 2)  # Split into max 3 parts
    command = command_parts[0].lower()
    
    if command == '/dm':
        if len(command_parts) < 3:
            update_chat("⚠️ Usage: /dm <username> <message>", "error")
            return
        
        target_user = command_parts[1]
        dm_message = command_parts[2]
        dm_message = convert_emojis(dm_message)  # Convert emojis in DM
        
        try:
            # Send DM in format server expects
            to_send = f"/dm {target_user} {dm_message}" 
            client.send(to_send.encode('utf-8'))
            # REMOVED: Don't show DM in our own chat immediately
            # The server will send back confirmation or the actual DM
        except Exception as e:
            update_chat(f"❌ Failed to send DM: {e}", "error")
            
    elif command in ['/kick', '/ban']:
        if nickname != 'admin':
            update_chat("⚠️ Admin commands can only be executed by the admin.", "error")
            return
            
        if len(command_parts) < 2:
            update_chat(f"⚠️ Usage: {command} <username>", "error")
            return
        
        target_user = command_parts[1]
        try:
            # Send command to server
            if command == '/kick':
                to_send = f"KICK {target_user}"
            else:  # /ban
                to_send = f"BAN {target_user}"
            
            client.send(to_send.encode('utf-8'))
            update_chat(f"✅ Admin command sent: {command} {target_user}", "admin")
        except Exception as e:
            update_chat(f"❌ Failed to send admin command: {e}", "error")
            
    else:
        # Other commands (/users, etc.)
        try:
            client.send(msg.encode('utf-8'))
        except Exception as e:
            update_chat(f"❌ Failed to send command: {e}", "error")

def receive_messages():
    """Receive messages from server"""
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break
                
            msg = data.decode('utf-8')
            
            if msg == "NICK":
                client.send(nickname.encode('utf-8'))
                continue
            elif msg == 'Password?: ':
                def ask_password():
                    password = simpledialog.askstring(
                        "Admin Login", 
                        "Enter admin password:", 
                        show='*', 
                        parent=window
                    )
                    if password:
                        client.send(password.encode('utf-8'))
                    else:
                        client.send(''.encode('utf-8'))
                
                window.after(0, ask_password)
                continue
            elif msg == "REFUSE":
                messagebox.showerror("Access Denied", "Wrong password. You are not allowed as admin.")
                window.destroy()
                break
            elif msg == "You were kicked by an admin!":
                update_chat("⚠️ You were kicked by an admin.", "error")
                client.close()
                window.destroy()
                break
            elif msg == "You were banned by an admin!":
                update_chat("⛔ You were banned by an admin.", "error")
                client.close()
                window.destroy()
                break
            
            # Convert emojis and display message
            msg = convert_emojis(msg)
            
            # Determine message type for coloring
            if msg.startswith("DM from") or msg.startswith("📨") or "DM to" in msg:
                update_chat(msg, "dm")
            elif any(keyword in msg.lower() for keyword in ["kicked", "banned", "joined", "left"]):
                update_chat(msg, "system")
            elif msg.startswith("❌") or msg.startswith("⚠️"):
                update_chat(msg, "error")
            else:
                update_chat(msg, "normal")
                
        except Exception as e:
            update_chat("❌ Disconnected from server", "error")
            break

def on_enter(event):
    """Handle Enter key press"""
    send_message()

def on_closing():
    """Handle window closing"""
    try:
        client.close()
    except:
        pass
    window.destroy()

# Event bindings
input_box.bind('<Return>', on_enter)
send_button.config(command=send_message)
emoji_button.config(command=show_emoji_picker)
help_button.config(command=show_help)
window.protocol("WM_DELETE_WINDOW", on_closing)

# Setup chat tags
setup_chat_tags()

# Get nickname
nickname = simpledialog.askstring("Join Chatroom", "Enter your nickname:", parent=window)
if not nickname:
    window.destroy()
    exit()

# Connect to server
try:
    client.connect((HOST, PORT))
    update_chat(f"✅ Connected to chatroom as '{nickname}'", "system")
except Exception as e:
    messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
    window.destroy()
    exit()

# Start receiving thread
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Start GUI
window.mainloop()