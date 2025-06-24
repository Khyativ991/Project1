import socket
import threading
from emojis import convert_emojis, get_emoji_list, search_emoji  # Import emoji functions

nickname = input("Choose a nickname: ")
if nickname == 'admin':
    password = input("Password?: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55545))

stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
                
                next_mssg = client.recv(1024).decode('utf-8')
                if next_mssg == 'Password?: ':
                    client.send(password.encode('utf-8'))
                    if client.recv(1024).decode('utf-8') == "REFUSE":
                        print("Connection Refused, Wrong Password")
                        stop_thread = True
                
                elif next_mssg == 'BAN':
                    print("Connection refused because you are **BANNED**.")
                    client.close()
                    stop_thread = True
            
            elif message == 'You were kicked by an admin!':
                print("You were kicked by an admin.")
                client.close()
                stop_thread = True
            
            elif message == 'You were banned by an admin!':
                print("You were **BANNED** by an admin.")
                client.close()
                stop_thread = True
            
            else:
                print(message)
                
        except:
            print("An error occurred.")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break

        user_input = input(f"{nickname}> ")
        user_input = convert_emojis(user_input)

        # Handle commands first
        if user_input.startswith('/'):
            # ADMIN COMMANDS
            if nickname == 'admin':
                if user_input.startswith('/kick'):
                    client.send(f'KICK {user_input[6:]}'.encode('utf-8'))

                elif user_input.startswith('/ban'):
                    client.send(f'BAN {user_input[5:]}'.encode('utf-8'))

                elif user_input.startswith('/emojis'):
                    print(get_emoji_list())
                    continue

                elif user_input.startswith('/help'):
                    print("""
                📘 Available Commands:
                /dm <user> <message>     → Send a private message
                /users                   → Show online users
                /emojis                  → View emoji list
                /emoji <keyword>         → Search for emojis

                Admin Only:
                /kick <user>             → Kick a user
                /ban <user>              → Ban a user
                """)
                    continue

                elif user_input.startswith('/emoji'):
                    parts = user_input.split()
                    if len(parts) > 1:
                        keyword = parts[1]
                        results = search_emoji(keyword)
                        print(f"Emojis matching '{keyword}':")
                        for result in results:
                            print(f"  {result}")
                    else:
                        print("Usage: /emoji <keyword>")
                    continue

                elif user_input.startswith('/dm'):
                    client.send(user_input.encode('utf-8'))

                elif user_input.startswith('/users'):
                    client.send(user_input.encode('utf-8'))
                    continue

                else:
                    print("⚠️ Unknown command.")
            else:
                # NON-ADMIN COMMANDS
                if user_input.startswith('/dm'):
                    client.send(user_input.encode('utf-8'))
                
                elif user_input.startswith('/help'):
                    print("""
                📘 Available Commands:
                /dm <user> <message>     → Send a private message
                /users                   → Show online users
                /emojis                  → View emoji list
                /emoji <keyword>         → Search for emojis
                """)
                    continue

                elif user_input.startswith('/users'):
                    client.send(user_input.encode('utf-8'))
                    continue

                elif user_input.startswith('/emojis') or user_input.startswith('/emoji'):
                    print(get_emoji_list())
                    continue

                else:
                    print("⚠️ Admin commands can only be executed by the admin.")

        else:
            # Regular message with nickname
            message = f'{nickname}: {user_input}'
            client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()