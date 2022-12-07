import platform
import socket
import subprocess
import psutil
import threading

def demande(data):

    if data == "DOS:dir":
        subprocess.getoutput('dir')
        print('u:\Documents>dir')

    elif data == "DOS:mkdir toto":
        subprocess.getoutput('mkdir toto')
        print(f"{data}")

    elif data == "Linux:ls -la":
        subprocess.getoutput('ls -la')
        print(f"{data}")

    elif data == "Powershell:get-process":
        subprocess.getoutput('get-process')
        print(f"{data}")

    elif data == "python --version":
        subprocess.getoutput('version')
        print(f"{data}")

    elif data == "ping 192.157.65.78":
        subprocess.getoutput('ping')
        print(f"{data}")

    elif data == "RAM Use":
        subprocess.getoutput(psutil.virtual_memory().percent)
        print(f"{data}")

    elif data == "RAM restante":
        subprocess.getoutput(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        print(f"{data}")

    elif data == "CPU Use":
        subprocess.getoutput(psutil.cpu_percent())
        print(f"{data}")

    elif data == "OS":
        subprocess.getoutput(platform.system())
        print(f"{data}")

    elif data == "Nom de Machine":
        subprocess.getoutput(socket.gethostname())
        print(f"{data}")

    elif data == "Adresse IP":
        subprocess.getoutput(socket.gethostbyname(socket.gethostname()))
        print(f"{data}")

if __name__ == '__main__':
    server_socket = socket.socket()
    server_socket.bind(("localhost", 10000))
    message = ""
    data = ""
    server_socket.listen(1)

while message != "reset" and data != "reset":
    conn, address = server_socket.accept()
    message = ""
    data = ""
    while message != "disconnect" and data != "disconnect" and message != "reset" and data != "reset":
        message=input("Moi :")
        data = conn.recv(1024).decode()
        conn.send(data.encode())
        print(f"Message du client : {data}")
    conn.close()
server_socket.close()

if message == 'disconnect' or message == 'reset':
    server_socket.close()
elif message == '':
    task_message = threading.Thread(
        target=message, args=[data, server_socket])
    task_reception = threading.Thread(
        target=data, args=[message, server_socket])
    task_message.start()
    task_reception.start()
else:
    server_socket.close()

def facto(conn):
    data = ""
    while data != "disconnect" :
        data = conn.recv(1024).decode()
        demande(data)
    else :
        conn.close()

def give(conn):
    data=""
    while data!= "disconect":
        data = conn.recv(1024).decode()
        demande(data)

t1 = threading.Thread(target=give, args=[conn])
t1.start()




# def cmd_s1mple(conn):
#     data=""
#     print(f"Mémoire utilisée {psutil.virtual_memory().percent}")
#     print(f"Mémoire restante {psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}")
#     print(f"Utilisation du CPU {psutil.cpu_percent()}")
#     print(f"OS de la machine {platform.system()}")
#     print(f"Nom de la machine {socket.gethostname()}")
#     print(f"Adresse IP de la machine {socket.gethostbyname(socket.gethostname())}")
#     while data != 'disconnect':
#         data = conn.recv(1024).decode()




