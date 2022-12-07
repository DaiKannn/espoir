import socket
import threading


client_socket = socket.socket()
client_socket.connect(("localhost", 10000))
message=""
data=""

def hope():
    data=""
    message=""
    while message != "disconnect" and data != "disconnect" and message != "reset" and data != "reset":
        message=input("Moi : ")
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print(f"Message du serveur : {data}")

if message == 'disconnect' or message == 'reset':
    client_socket.close()
elif message == '':
    task_message = threading.Thread(
        target=data, args=[message, client_socket])
    task_reception = threading.Thread(
        target=message, args=[data, client_socket])
    task_message.start()
    task_reception.start()
else:
    client_socket.close()

t1 = threading.Thread(target=hope)
t1.start()


