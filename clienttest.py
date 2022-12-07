import socket
import threading

client_socket = socket.socket()
client_socket.connect(("localhost", 12000))
message=""
data=""

def hope(client_socket):
    try :
        data=""
        while data != "disconnect" and data != "reset" and data !="kill":
            data = client_socket.recv(1024).decode()
        client_socket.close()
    except ConnectionAbortedError :
        print("terminado")

t1 = threading.Thread(target=hope, args=[client_socket])
t1.start()

message=""
while message != "disconnect" and message != "reset" and message != "kill":
    message=input("Moi : ")
    client_socket.send(message.encode())
client_socket.close()

t1.join()
client_socket.close()

if message == 'disconnect' or message == 'reset' or message == 'kill':
    client_socket.close()


