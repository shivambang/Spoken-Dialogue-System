from socket import *
import socketio
import sys
sio = socketio.Client(logger=True, engineio_logger=True)
sio.connect('http://localhost:5000/socket.io')
ip = sys.argv[1]
port = int(sys.argv[2])
s = socket(AF_INET, SOCK_STREAM)
s.bind((ip, port))
s.listen(1)
conn, addr = s.accept()
print("Connected: ", addr)
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def bot_uttered(message):
    print(message)
    msg = message['text'] + '\n'
    conn.send(msg.encode())

while True:
    r = conn.recv(1024).decode()
    if r != "": sio.emit('user_uttered', {"message": r})
        
        
        
from socket import *

HOST = "10.192.141.201"
#local host
PORT = 6000 #open port 7000
s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1) #how many connections can it receive at one time
conn, addr = s.accept() #accept the connection
print("Connected by: ", addr) #print the address of the person connected
while True:
    data = conn.recv(1024).decode() #how many bytes of data will the server receive
    print("Received: ",data)
    reply = input("Reply: ") #server 's reply to the client
    reply += '\n'    
    conn.send(reply.encode('utf-8'))
conn.close()


    

