import platform
import socket
import psutil
import threading
import subprocess
import os

def demande(data):

    # cmd = "dir"
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
    # print(f"résultat commande : \n {p.stdout.read()}")
    # print(f"erreur commande : \n {p.stderr.read()}")
    # out, err = p.communicate()
    # print(f"retour {out}, erreur{err}")

    if data == "DOS:dir":
        cmd = "dir"
        cmd = cmd.split(' ')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read(dir)}")
        print(f"erreur commande : \n {p.stderr.read(dir)}")

    elif data == "DOS:mkdir toto":
        cmd = "mkdir toto"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "Linux:ls -la":
        cmd = "ls- la"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "Powershell:get-process":
        cmd = "Powershell:get-process"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "python":
        cmd = "python --version"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "ping":
        cmd = "ping 192.157.65.78"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "RAM Use":
        cmd = "psutil.virtual_memory().percent"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "RAM restante":
        cmd = "psutil.virtual_memory().available * 100 / psutil.virtual_memory().total"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "CPU Use":
        cmd = "psutil.cpu_percent()"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "OS":
        cmd = "platform.system()"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "Nom de Machine":
        cmd = "socket.gethostname()"
        ret = os.popen(cmd)
        print(ret.read)

    elif data == "Adresse IP":
        cmd = "socket.gethostbyname(socket.gethostname())"
        ret = os.popen(cmd)
        print(ret.read)

if __name__ == '__main__':
    server_socket = socket.socket()
    server_socket.bind(("localhost", 13000))
    message = ""
    data = ""
    server_socket.listen(1)

def hope2(server_socket):
    try :
        data=""
        while data != "disconnect" and data != "reset" :
            conn, address = server_socket.accept()
            data = conn.recv(1024).decode()
            conn.send(data.encode())
            print(f"Message du client : {data}")
        conn.close()
        server_socket.close()
    except ConnectionAbortedError:
        print("terminado")

t1 = threading.Thread(target=hope2, args=[server_socket])
t1.start()

message=""
while message != "reset" and message != "disconnect":
    conn, address = server_socket.accept()
    message=input("Moi :")
    data = conn.recv(1024).decode()
    conn.send(message.encode())
    print(f"Message du client : {data}")
    conn.close()
server_socket.close()

if message == 'disconnect' or message == 'reset':
    server_socket.close()

def facto(conn):
    data = ""
    while data != "disconnect" :
        data = conn.recv(1024).decode()
        demande(data)
    else :
        conn.close()

t2 = threading.Thread(target=facto, args=[conn])
t2.start()



