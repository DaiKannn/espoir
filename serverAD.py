import socket
import subprocess
import platform
import psutil

def serveur():
    msg = ""
    conn = None
    server_socket = None
    while msg != "kill" :
        msg = ""
        server_socket = socket.socket()
        server_socket.bind(("localhost", 13000))

        server_socket.listen(1)
        print('Serveur en attente de connexion')
        while msg != "kill" and msg != "reset":
            msg = ""
            try :
                conn, addr = server_socket.accept()
                print (addr)
            except ConnectionError:
                print ("erreur de connection")
                break
            else :
                while msg != "kill" and msg != "reset" and msg != "disconnect":
                    msg = conn.recv(1024).decode()
                    print ("Received from client: ", msg)
                conn.close()
        print ("Connection closed")
        server_socket.close()
        print ("Server closed")

def commande(msg):
    cmd = msg.split(':')
    if msg == "DOS:dir" :
        cmd = 'dir'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "OS" :
        cmd = platform.system()
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "DOS:mkdir toto" :
        cmd = 'mkdir matteo'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "RAM Use" :
        cmd = psutil.virtual_memory().percent
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "RAM not use" :
        cmd = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "CPU use" :
        cmd = psutil.cpu_percent()
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "Nom de machine" :
        cmd = socket.gethostname()
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "Adresse IP" :
        cmd = socket.gethostbyname(socket.gethostname())
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "Ping" :
        cmd = 'ping 192.157.65.78'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "python" :
        cmd = 'python --version'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "Powershell" :
        cmd = 'Powershell:get-process'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")

    elif msg == "Linux ls: -la" :
        cmd = 'ls -la'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp850', shell=True)
        print(f"résultat commande : \n {p.stdout.read()}")
        print(f"erreur commande : \n {p.stderr.read()}")


if __name__ == '__main__':
    serveur()
