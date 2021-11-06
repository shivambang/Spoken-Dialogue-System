from socket import *
import socketio
sio = socketio.Client(logger=True, engineio_logger=True)
sio.connect('http://localhost:5252/socket.io')

s = socket(AF_INET, SOCK_STREAM)
s.bind(('192.168.0.103', 5600))
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
    

