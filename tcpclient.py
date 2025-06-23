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
        
        # Add a clear input prompt
        user_input = input(f"{nickname}> ") 
        
        # Convert emojis before processing
        user_input = convert_emojis(user_input)
        
        message = f'{nickname}: {user_input}'
        
        if message[len(nickname)+2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('utf-8'))
                
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('utf-8'))
                    
                elif message[len(nickname)+2:].startswith('/emojis'):
                    print(get_emoji_list())
                    continue
                    
                elif message[len(nickname)+2:].startswith('/emoji'):
                    # /emoji search fire -> shows fire related emojis
                    parts = message[len(nickname)+2:].split()
                    if len(parts) > 1:
                        keyword = parts[1]
                        results = search_emoji(keyword)
                        print(f"Emojis matching '{keyword}':")
                        for result in results:
                            print(f"  {result}")
                    else:
                        print("Usage: /emoji <keyword>")
                    continue
            else:
                if user_input.startswith('/emojis') or user_input.startswith('/emoji'):
                    print(get_emoji_list())
                    continue
                else:
                    print("Admin commands can only be executed by the admin")
        else:
            client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()