import socket
import subprocess
import platform
import psutil

def serveur():
    msg = ""
    while msg != "kill" :
        msg = ""
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 14000))
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
                try:
                    while msg != "kill" and msg != "reset" and msg != "disconnect":
                        msg = conn.recv(1024).decode()
                        print ("Received from client: ", msg)
                        if msg == "DOS:dir":
                            message = subprocess.getoutput('dir')
                            conn.send(message.encode())
                            print("Voici le dir")

                        elif msg == "DOS:mkdir toto":
                            message = subprocess.getoutput('mkdir toto')
                            conn.send(message.encode())
                            print("Voici le mkdir")

                        elif msg == "Linux:ls -la":
                            message = subprocess.getoutput('ls -la')
                            conn.send(message.encode())
                            print("Voici le ls -la")

                        elif msg == "Powershell:get-process":
                            message = subprocess.getoutput('get-process')
                            conn.send(message.encode())
                            print("Voici le get-process")

                        elif msg == "python --version":
                            message = subprocess.getoutput('version')
                            conn.send(message.encode())
                            print("Voici la version de python")

                        elif msg == "ping 192.157.65.78":
                            message = subprocess.getoutput('ping')
                            conn.send(message.encode())
                            print("Voici le ping")

                        elif msg == "RAM Use":
                            message = subprocess.getoutput(psutil.virtual_memory().percent)
                            conn.send(message.encode())
                            print("Voici la RAM utilisé")

                        elif msg == "RAM restante":
                            message = subprocess.getoutput(
                            psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
                            conn.send(message.encode())
                            print("Voici la RAM restante")

                        elif msg == "CPU Use":
                            message = subprocess.getoutput(psutil.cpu_percent())
                            conn.send(message.encode())
                            print("Voici le % CPU utilisé")

                        elif msg == "OS":
                            message = subprocess.getoutput(platform.system())
                            conn.send(message.encode())
                            print("Voici l'OS")

                        elif msg == "Nom de Machine":
                            message = subprocess.getoutput(socket.gethostname())
                            conn.send(message.encode())
                            print("Voici le nom de la machine")

                        elif msg == "Adresse IP":
                            message = subprocess.getoutput(socket.gethostbyname(socket.gethostname()))
                            conn.send(message.encode())
                            print("Voici l'adresse IP")
                except ConnectionResetError:
                    print("")
                except KeyboardInterrupt:
                    print("Application arrêtée brusquement")
                conn.close()
        print ("Connection closed")
        server_socket.close()
        print ("Server closed")

if __name__ == '__main__':
    serveur()
