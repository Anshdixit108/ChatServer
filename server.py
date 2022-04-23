import socket
import os
import time
from _thread import *
import threading 

BUF = 1024
PORT = 12345
HOSTNAME = socket.gethostname()
SERVER = socket.gethostbyname(HOSTNAME)
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
clients = {}
name_list = []
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(ADDR)

def client_handling(conn, addr):
    name = conn.recv(BUF).decode(FORMAT)
    print(f"{name} ONLINE")
    welcome = f"Welcome {name}"
    conn.send(bytes(welcome,FORMAT))
    msg = f"{name} has joined the chat"
    broadcast(msg)
    clients[conn]=name
    name_list.append(name)

    connected = True
    while connected:
        msg = conn.recv(BUF).decode(FORMAT)
        if msg[0] == "/" and len(msg) > 3:
            if msg == "/quit":
                broadcast("has left the chat", name+": ") 
                connected = False
                

            elif msg[0:8] == "/forward":
                sender = name
                protocol, dash, message = msg.partition("-")
                uname = protocol.partition("@")[2]
                send_private_message(message, uname, conn, soc, sender)

            

      
        else:
            broadcast(msg, name+": ")     
    
    conn.close()
    del clients[conn]
    print(f"{name} DISCONNECTED")
    

def broadcast(msg, identify=""):
    message_byte = msg.encode(FORMAT)
    for sock in clients:
        sock.send(bytes(identify,FORMAT) + message_byte)
      
            
def start():
    soc.listen(8)
    print(f"{HOSTNAME} <Listening> on {SERVER}")
    while True:
        conn, addr = soc.accept()
        conn.send(bytes("Enter your name and press enter.",FORMAT))
        time.sleep(1)
        conn.send(bytes("Enter /quit to exit.", FORMAT)) 
        time.sleep(1)
        conn.send(bytes("Enter /forward@user-message to forward msg.", FORMAT))
        thread = threading.Thread(target = client_handling, args = (conn, addr))
        thread.start()
        
def send_private_message(msg, username, client_conn, server_socket, sender_name):
    l = len(clients)
    for client, name in clients.items():
        bmsg = msg.encode(FORMAT)
 
        if name == username:
            
            try:
                client.send(bytes(sender_name+": ", FORMAT) + bmsg)
                break
          
            except:
                client.close()
        else:
            l=l-1
            



if __name__ == "__main__":
    print(f"<STARTING> Server is starting on {SERVER}")
    start()