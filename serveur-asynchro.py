import platform
import socket
import subprocess
import psutil

server_socket = socket.socket()
server_socket.bind(("localhost", 9000))
message=""
data=""
server_socket.listen(1)

while message !="reset" and data !="reset":
    conn, address = server_socket.accept()
    message=""
    data=""
    while message != "disconnect" and data != "disconnect" and message != "reset" and data != "reset":
        message=input("Moi :")
        data = conn.recv(1024).decode()
        conn.send(message.encode())
        print(f"Message du client : {data}")
    conn.close()
server_socket.close()

def demande(data):

    if data == "DOS:dir":
        message = subprocess.getoutput('dir')
        conn.send(message.encode())
        print("Voici le dir")

    elif data == "DOS:mkdir toto":
        message = subprocess.getoutput('mkdir toto')
        conn.send(message.encode())
        print("Voici le mkdir")

    elif data == "Linux:ls -la":
        message = subprocess.getoutput('ls -la')
        conn.send(message.encode())
        print("Voici le ls -la")

    elif data == "Powershell:get-process":
        message = subprocess.getoutput('get-process')
        conn.send(message.encode())
        print("Voici le get-process")

    elif data == "python --version":
        message = subprocess.getoutput('version')
        conn.send(message.encode())
        print("Voici la version de python")

    elif data == "ping 192.157.65.78":
        message = subprocess.getoutput('ping')
        conn.send(message.encode())
        print("Voici le ping")

    elif data == "RAM Use":
        message = subprocess.getoutput(psutil.virtual_memory().percent)
        conn.send(message.encode())
        print("Voici la RAM utilisé")

    elif data == "RAM restante":
        message = subprocess.getoutput(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        conn.send(message.encode())
        print("Voici la RAM restante")

    elif data == "CPU Use":
        message = subprocess.getoutput(psutil.cpu_percent())
        conn.send(message.encode())
        print("Voici le % CPU utilisé")

    elif data == "OS":
        message = subprocess.getoutput(platform.system())
        conn.send(message.encode())
        print("Voici l'OS")

    elif data == "Nom de Machine":
        message = subprocess.getoutput(socket.gethostname())
        conn.send(message.encode())
        print("Voici le nom de la machine")

    elif data == "Adresse IP":
        message = subprocess.getoutput(socket.gethostbyname(socket.gethostname()))
        conn.send(message.encode())
        print("Voici l'adresse IP")


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

def facto(conn):
    data = ""
    while data != "disconnect" :
        data = conn.recv(1024).decode()
        demande(data)
    else :
        conn.close()
