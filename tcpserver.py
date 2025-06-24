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
    return datetime.now().strftime("[%d-%m %H:%M:%S]")


def broadcast(message, exclude_client=None):
    for client in clients:
        if client != exclude_client:
            try:
                client.send(message)
            except:
                # Remove disconnected clients
                if client in clients:
                    remove_client(client)


def remove_client_safely(client):
    """Safely remove a client from the lists with proper synchronization"""
    try:
        if client in clients:
            index = clients.index(client)
            nickname = nicknames[index]
            
            # Remove from lists
            clients.remove(client)
            nicknames.remove(nickname)
            
            # Close the connection
            try:
                client.close()
            except:
                pass
            
            timestamp = get_timestamp()
            
            # Handle different disconnect reasons
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
            
    except Exception as e:
        print(f"Error removing client safely: {e}")
        # Force removal if client is still in list
        if client in clients:
            try:
                clients.remove(client)
            except:
                pass
        try:
            client.close()
        except:
            pass


def remove_client(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            msg_decoded = message.decode('utf-8')

            # Get current client's nickname for admin checks
            try:
                client_index = clients.index(client)
                client_nickname = nicknames[client_index]
            except ValueError:
                # Client not found in list, disconnect
                break
            except IndexError:
                # Index out of range, disconnect
                break

            # DM
            if msg_decoded.startswith('/dm '):
                parts = msg_decoded.split(' ', 2)
                if len(parts) < 3:
                    client.send("❌ Invalid DM format. Use: /dm <username> <message>".encode('utf-8'))
                else:
                    target_name = parts[1].strip()
                    dm_message = parts[2].strip()
                    sender_name = client_nickname

                    if target_name in nicknames:
                        target_index = nicknames.index(target_name)
                        target_client = clients[target_index]
                        timestamp = get_timestamp()

                        formatted = f"{timestamp} [DM] {sender_name} → you: {dm_message}".encode('utf-8')
                        target_client.send(formatted)

                        confirmation = f"{timestamp} [DM] you → {target_name}: {dm_message}".encode('utf-8')
                        client.send(confirmation)
                    else:
                        client.send(f"❌ User '{target_name}' is not in the chatroom.".encode('utf-8'))
                continue

            # Show online users
            elif msg_decoded.startswith('/users'):
                online_list = "\n🟢 Online Users:\n" + "\n".join(f"- {name}" for name in nicknames)
                client.send(online_list.encode('utf-8'))
                continue

            # Admin-only: Kick
            elif msg_decoded.startswith('/kick ') or msg_decoded.startswith('KICK '):
                if client_nickname == 'admin':
                    name_to_kick = msg_decoded.split(' ', 1)[1].strip()
                    if name_to_kick:
                        result = kick_user(name_to_kick)
                        if result:
                            client.send(f"✅ Successfully kicked {name_to_kick}".encode('utf-8'))
                        else:
                            client.send(f"❌ User '{name_to_kick}' not found or cannot be kicked".encode('utf-8'))
                    else:
                        client.send("❌ Please specify a username to kick".encode('utf-8'))
                else:
                    client.send('⚠️ Admin commands can only be executed by the admin.'.encode('utf-8'))
                continue

            # Admin-only: Ban
            elif msg_decoded.startswith('/ban ') or msg_decoded.startswith('BAN '):
                if client_nickname == 'admin':
                    name_to_ban = msg_decoded.split(' ', 1)[1].strip()
                    if name_to_ban:
                        result = ban_user(name_to_ban)
                        if result:
                            client.send(f"✅ Successfully banned {name_to_ban}".encode('utf-8'))
                        else:
                            client.send(f"❌ User '{name_to_ban}' not found or cannot be banned".encode('utf-8'))
                    else:
                        client.send("❌ Please specify a username to ban".encode('utf-8'))
                else:
                    client.send('⚠️ Admin commands can only be executed by the admin.'.encode('utf-8'))
                continue

            # Normal message
            else:
                timestamp = get_timestamp()
                timestamped_message = f"{timestamp} {msg_decoded}".encode('utf-8')
                broadcast(timestamped_message)
                print(f"{timestamp} {msg_decoded}")

        except Exception as e:
            print(f"Error handling client: {e}")
            # Safely remove client
            remove_client_safely(client)
            break


def receive():
    while True:
        try:
            client, address = server.accept()
            timestamp = get_timestamp()
            print(f"{timestamp} Connected with {str(address)}")

            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')

            # Check if user is banned
            try:
                with open('bans.txt', 'r') as f:
                    bans = f.readlines()
            except FileNotFoundError:
                # Create bans.txt if it doesn't exist
                with open('bans.txt', 'w') as f:
                    pass
                bans = []

            if nickname + '\n' in bans:
                client.send('BAN'.encode('utf-8'))
                client.close()
                continue

            # Admin password check
            if nickname == 'admin':
                client.send('Password?: '.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')
                if password != 'kv123':
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

        except Exception as e:
            print(f"Error accepting connection: {e}")


def kick_user(name):
    if name in nicknames:
        if name == 'admin':
            return False
        
        try:
            name_index = nicknames.index(name)
            client_to_kick = clients[name_index]
            timestamp = get_timestamp()
            
            kicked_users.add(name)

            # kick message to user
            try:
                client_to_kick.send('You were kicked by an admin!'.encode('utf-8'))
            except:
                pass
            
            # Remove client safely
            remove_client_safely(client_to_kick)

            kick_msg = f'{timestamp} {name} was kicked by an admin!'.encode('utf-8')
            broadcast(kick_msg)
            print(kick_msg.decode('utf-8'))
            return True
            
        except Exception as e:
            print(f"Error kicking user {name}: {e}")
            return False
    else:
        return False


def ban_user(name):
    if name in nicknames:
        # Don't ban admin
        if name == 'admin':
            return False

        try:
            name_index = nicknames.index(name)
            client_to_ban = clients[name_index]
            timestamp = get_timestamp()

            banned_users.add(name)
            
            # Send ban message to the user
            try:
                client_to_ban.send('You were banned by an admin!'.encode('utf-8'))
            except:
                pass

            # Add to bans file
            try:
                with open('bans.txt', 'a') as f:
                    f.write(f'{name}\n')
            except Exception as e:
                print(f"Error writing to bans.txt: {e}")

            # Remove client safely
            remove_client_safely(client_to_ban)

            ban_msg = f'{timestamp} {name} was banned by an admin!'.encode('utf-8')
            broadcast(ban_msg)
            print(ban_msg.decode('utf-8'))
            return True
            
        except Exception as e:
            print(f"Error banning user {name}: {e}")
            return False
    else:
        return False


print("Server is listening..")
receive()

#&"C:\Users\KHYATI VERMA\AppData\Local\Programs\Python\Python313\python.exe" gui_client.py
