import threading
import socket
from datetime import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55545))
server.listen()

clients = []
nicknames = []
kicked_users = set()
banned_users = set()

def get_timestamp():
    return datetime.now().strftime("[%H:%M:%S]")

def broadcast(message, exclude_client=None):
    for client in clients:
        if client != exclude_client:
            client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            msg_decoded = message.decode('utf-8')
            
            if msg_decoded.startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg_decoded[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused'.encode('utf-8'))
            
            elif msg_decoded.startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg_decoded[4:]
                    ban_user(name_to_ban)
                else:
                    client.send('Command was refused!'.encode('utf-8'))
            
            else:
                timestamp = get_timestamp()
                timestamped_message = f"{timestamp} {msg_decoded}".encode('utf-8')
                broadcast(timestamped_message)
                print(f"{timestamp} {msg_decoded}")
                
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                nicknames.remove(nickname)
                timestamp = get_timestamp()

                if nickname in kicked_users:
                    leave_msg = f'{timestamp} {nickname} was kicked from the chat.'.encode('utf-8')
                    kicked_users.remove(nickname)
                elif nickname in banned_users:
                    leave_msg = f'{timestamp} {nickname} was banned from the chat.'.encode('utf-8')
                    banned_users.remove(nickname)
                else:
                    leave_msg = f'{timestamp} {nickname} left the chat!'.encode('utf-8')

                broadcast(leave_msg)
                print(leave_msg.decode('utf-8'))
                break

def receive():
    while True:
        client, address = server.accept()
        timestamp = get_timestamp()
        print(f"{timestamp} Connected with {str(address)}")
        
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        
        if nickname + '\n' in bans:
            client.send('BAN'.encode('utf-8'))
            client.close()
            continue
        
        if nickname == 'admin':
            client.send('Password?: '.encode('utf-8'))
            password = client.recv(1024).decode('utf-8')
            if password != '$ahaj':
                client.send('REFUSE'.encode('utf-8'))
                client.close()
                continue
        
        nicknames.append(nickname)
        clients.append(client)
        
        print(f'{timestamp} {nickname} joined the chat!')
        join_msg = f'{timestamp} {nickname} joined the chat'.encode('utf-8')
        broadcast(join_msg)
        client.send('Connected to the Server!'.encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        timestamp = get_timestamp()
        kicked_users.add(name)
        
        client_to_kick.send('You were kicked by an admin!'.encode('utf-8'))
        clients.remove(client_to_kick)
        client_to_kick.close()
        nicknames.remove(name)

        kick_msg = f'{timestamp} {name} was kicked by an admin!'.encode('utf-8')
        broadcast(kick_msg)
        print(f'{timestamp} {name} was kicked by an admin!')

def ban_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_ban = clients[name_index]
        timestamp = get_timestamp()
        banned_users.add(name)
        
        client_to_ban.send('You were banned by an admin!'.encode('utf-8'))
        with open('bans.txt', 'a') as f:
            f.write(f'{name}\n')
        clients.remove(client_to_ban)
        client_to_ban.close()
        nicknames.remove(name)

        ban_msg = f'{timestamp} {name} was banned by an admin!'.encode('utf-8')
        broadcast(ban_msg)
        print(f'{timestamp} {name} was banned!')

print("Server is listening..")
receive()
