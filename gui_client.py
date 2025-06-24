import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from emojis import convert_emojis  

HOST = '127.0.0.1'
PORT = 55545
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# GUI 
window = tk.Tk()
window.title("Chatroom GUI 🗨️")

chat_label = tk.Label(window, text="Chat:")
chat_label.pack(padx=20, pady=5)

chat_box = scrolledtext.ScrolledText(window)
chat_box.pack(padx=20, pady=5)
chat_box.config(state='disabled')

input_box = tk.Entry(window, width=80)
input_box.pack(padx=20, pady=5)

send_button = tk.Button(window, text="Send", width=20, command=lambda: send_message())
send_button.pack(padx=20, pady=5)

# Prompt for username
nickname = simpledialog.askstring("Join Chatroom", "Enter your nickname:", parent=window)

# Connect to server
try:
    client.connect((HOST, PORT))
except Exception as e:
    messagebox.showerror("Connection Error", f"Failed to connect to server: {e}")
    window.destroy()
    exit()

# Utility to update chat safely
def update_chat(message):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, message + '\n')
    chat_box.yview(tk.END)
    chat_box.config(state='disabled')

# Send message function
def send_message():
    msg = input_box.get()
    input_box.delete(0, tk.END)
    msg = convert_emojis(msg)

    if msg.startswith('/'):
        command_parts = msg.split(' ')
        command = command_parts[0].lower()
        
        if command in ['/kick', '/ban']:
            if nickname == 'admin':
                if len(command_parts) < 2:
                    update_chat("⚠️ Usage: /kick <username> or /ban <username>")
                    return
                
                target_user = command_parts[1]
                try:
                    # Send the command in the format the server expects
                    if command == '/kick':
                        to_send = f"KICK {target_user}"
                    else:  # /ban
                        to_send = f"BAN {target_user}"
                    
                    client.send(to_send.encode('utf-8'))
                    update_chat(f"✅ Admin command sent: {command} {target_user}")
                except Exception as e:
                    update_chat(f"❌ Failed to send admin command: {e}")
                return
            else:
                update_chat("⚠️ Admin commands can only be executed by the admin.")
                return
        elif command == '/help':
            help_text = (
                "\n🆘 Available Commands:\n"
                " /users            → Show online users\n"
                " /dm <user> <msg>  → Send a private message\n"
                " /kick <user>      → (Admin only) Kick a user\n"
                " /ban <user>       → (Admin only) Ban a user\n"
                " /help             → Show this help menu\n"
                " You can also use emojis like :smile:, :heart:, :fire:, etc."
            )
            update_chat(help_text)
            return
        else:
            # For other commands like /users, /dm, /help
            try:
                client.send(msg.encode('utf-8'))
            except Exception as e:
                update_chat(f"❌ Failed to send message: {e}")
            return
    else:
        # Regular,normal message
        to_send = f"{nickname}: {msg}"
        try:
            client.send(to_send.encode('utf-8'))
        except Exception as e:
            update_chat(f"❌ Failed to send message: {e}")

# Receive messages from server
def receive_messages():
    while True:
        try:
            data = client.recv(1024)
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
                update_chat("⚠️ You were kicked by an admin.")
                client.close()
                window.destroy()
                break
            elif msg == "You were banned by an admin!":
                update_chat("⛔ You were banned by an admin.")
                client.close()
                window.destroy()
                break

            msg = convert_emojis(msg)
            update_chat(msg)
        except:
            update_chat("❌ Disconnected from server")
            break

# Bind Enter key to send message
def on_enter(event):
    send_message()

input_box.bind('<Return>', on_enter)

# Start receiving thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Start GUI main loop
window.mainloop()