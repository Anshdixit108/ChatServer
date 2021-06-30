import socket
import threading


BUF = 1024
PORT = 12345
HOSTNAME = socket.gethostname()
SERVER = socket.gethostbyname(HOSTNAME)
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
clients = {}

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(ADDR)

def client_handling(conn, addr):
    name = conn.recv(BUF).decode(FORMAT)
    print(f"{name} ONLINE")
    welcome = f"Welcome {name}"
    conn.send(bytes(welcome,FORMAT))
    msg = f"{name} has joined the chat"
    broadcast(bytes(msg,FORMAT))
    clients[conn]=name

    connected = True
    while connected:
        msg = conn.recv(BUF)#return value is a byte object  
        if msg == b"!quit":
            broadcast(b"has left the chat", name+": ") 
            connected = False
        elif msg == b"!lemj" :
            broadcast(b'\xf0\x9f\x98\x82', name+": ") 
            
        else:
            broadcast(msg, name+": ")     
    
    conn.close()
    del clients[conn]
    print(f"{name} DISCONNECTED")
    

def broadcast(msg, identify=""):
    for sock in clients:
        sock.send(bytes(identify,FORMAT)+msg)
      
            
def start():
    soc.listen(5)
    print(f"{HOSTNAME} <Listening> on {SERVER}")
    while True:
        conn, addr = soc.accept()
        conn.send(bytes("Enter your name and press enter. Enter !quit to exit", FORMAT))
        thread = threading.Thread(target = client_handling, args = (conn, addr))
        thread.start()
        


if __name__ == "__main__":
    print(f"<STARTING> Server is starting on {SERVER}")
    start()