import socket
import threading
import tkinter as tk
root = tk.Tk()

HEADER = 64
PORT = 12345
FORMAT = "utf-8"
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
BUF = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(event=None):
    message = my_msg.get()
    my_msg.set("")
    client.send(bytes(message, FORMAT))
    if message == "!quit":
        client.close()
        root.quit()
    
def receive():
    while True:
        try :
            msg = client.recv(BUF).decode(FORMAT)
            msg_list.insert(tk.END,msg)
        except OSError:
            break

root.title("GroupChat")

msg_frame = tk.Frame(root)
my_msg = tk.StringVar()
my_msg.set("Type here")
scrollbar = tk.Scrollbar(msg_frame)
msg_list = tk.Listbox(msg_frame, height=20, width=50,yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill = tk.BOTH)
msg_list.pack()
msg_frame.pack()

e= tk.Entry(root, textvariable=my_msg)
e.bind("<Return>",send)
e.pack()

send_button=tk.Button(root, text="Send", command=send)
send_button.pack()

thread = threading.Thread(target=receive)
thread.start()
tk.mainloop()

