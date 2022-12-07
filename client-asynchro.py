import socket
import threading

client_socket = socket.socket()
client_socket.connect(("localhost", 9000))
message=""
data=""

while message != "disconnect" and data != "disconnect" and message != "reset" and data != "reset":
    message=input("Moi : ")
    client_socket.send(message.encode())
    data = client_socket.recv(1024).decode()
    print(f"Message du serveur : {data}")

if message == 'disconnect' or 'reset':
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
