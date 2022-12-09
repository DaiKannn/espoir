import platform
import socket
import psutil
import subprocess

print(psutil.virtual_memory().percent)
print(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
print(psutil.cpu_percent())
print(platform.system())
print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
print(subprocess.getoutput('ping 192.157.65.78'))
print(subprocess.getoutput('dir'))
print(subprocess.getoutput('mkdir wesh'))
print(subprocess.getoutput('ls -la'))
print(subprocess.getoutput('Powershell:get-process'))
print(subprocess.getoutput('python --version'))


# message=""
# while message != "reset" and data != "reset":
#     conn, address = server_socket.accept()
#             while message != "disconnect" and data != "disconnect" and message != "reset" and data != "reset":
#                 message=input("Moi :")
#                 data = conn.recv(1024).decode()
#                 conn.send(data.encode())
#                 print(f"Message du client : {data}")
#             conn.close()
#         server_socket.close()
#     except ConnectionAbortedError:
#         print("terminado")
#
#
# if message == 'disconnect' or message == 'reset':
#     server_socket.close()
#
# def facto(conn):
#     data = ""
#     while data != "disconnect" :
#         data = conn.recv(1024).decode()
#         demande(data)
#     else :
#         conn.close()
#
# t1 = threading.Thread(target=facto, args=[conn])
# t1.start()

cmd= msg.split(':')
                    if cmd[0] == "DOS" and platform.platform()[:7] == "Windows":
                        if cmd[1] == "dir":
                            reply = subprocess.getoutput("dir")
                            conn.send(reply.encode())
                            print(f"Checkbug : DIR FAIT")
                        elif cmd[1][:6] == "mkdir ":
                            if len(cmd[1][6:]) != 0:
                                dos = cmd[1][6:]
                                reply = subprocess.getoutput(f"mkdir U:\Documents\BUT2\SAE3.02\SAE3.02\{dos}")[228:]
                                conn.send(reply.encode())
                                print(f"Checkbug : MKDIR {dos} FAIT")
                            else:
                                print("Impossible de créer un dossier sans nom")
                        else:
                            print("Erreur : Commande Windows incomplète ou inconnue")
                    elif cmd[0] == "Powershell" and platform.platform()[:7] == "Windows":
                        if cmd[1] == "get-process":
                            reply = subprocess.getoutput("powershell.exe get-process")
                            conn.send(reply.encode())
                            print(f"Checkbug : Powershell:get-process FAIT")
                        else:
                            print("Erreur : Commande Powershell inconnue")
                    elif msg == "Linux:ls -la":
                        reply = subprocess.getoutput("ls -la")
                        conn.send(reply.encode())
                        print(f"Checkbug : ls -la FAIT")
                    elif msg == "python --version":
                        reply = subprocess.getoutput("python --version")
                        conn.send(reply.encode())
                        print(f"Checkbug : python --version FAIT")
                    elif msg == "ping 192.168.152.1":
                        reply = subprocess.getoutput("ping 192.168.152.1")
                        conn.send(reply.encode())
                        print(f"Checkbug : PING FAIT")
                    elif msg == "OS":
                        reply = platform.platform()
                        conn.send(reply.encode())
                        print("OS renvoyé")
                    elif msg == "Name":
                        reply = socket.gethostname()
                        conn.send(reply.encode())
                        print("Nom envoyé")
                    elif msg == "IP":
                        hostname = socket.gethostname()
                        reply = socket.gethostbyname(hostname)
                        conn.send(reply.encode())
                        print("IP envoyé")
                    elif msg == "CPU":
                        reply = str(f"{psutil.cpu_percent()}% du CPU utilisé !")
                        conn.send(reply.encode())
                        print("Checkbug : Info CPU envoyée")
                    elif msg == "RAM":
                        reply = str(
                            f"{psutil.virtual_memory().percent}% de la RAM utilisé ! \nRAM totale disponible {psutil.virtual_memory().total / 1024 / 1024} MB")
                        conn.send(reply.encode())
                        print("Checkbug : Info RAM envoyée")
                    elif msg == "kill" or msg == "reset" or msg == "disconnect":
                        conn.send(msg.encode())



import socket, threading, sys
import sys
from threading import Lock
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication
import csv


class Client():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
        self.__thread = None



    # fonction de connection.
    def connect(self) -> int:
        try :
            self.__sock.connect((self.__host,self.__port))
        except ConnectionRefusedError:
            print ("[X] Serveur non lancé ou mauvaise information")
            return -1
        except ConnectionError:
            print ("[X] Erreur de connection")
            return -1
        else :
            print ("[+] Connexion réalisée")
            return 0


    def dialogue(self):
        msg = ""
        self.__thread = threading.Thread(target=self.__reception, args=[self.__sock,])
        self.__thread.start()
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = self.__envoi()
        self.__thread.join()
        self.__sock.close()

    # méthode d'envoi d'un message au travers la socket. Le résultat de cette methode est le message envoyé.
    def __envoi(self):
        msg = input("Message à envoyer au Serveur : ")
        try:
            self.__sock.send(msg.encode())
        except BrokenPipeError:
            print ("erreur, socket fermée")
        return msg
    """
      thread recepction, la connection étant passée en argument
    """





    def __reception(self, conn):
        msg =""
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = conn.recv(1024).decode('cp850')
            print(msg)






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        lab = QLabel("Host")
        lab4 = QLabel("Port")

        self.__lab2 = QLabel("")
        self.__lab3 = QLabel("")
        self.__text = QLineEdit("")
        self.__text2 = QLineEdit("")
        ok = QPushButton("Ok")

        grid.addWidget(self.__lab3, 3, 1)
        grid.addWidget(self.__lab2, 4, 1)
        grid.addWidget(lab, 0, 0)
        grid.addWidget(lab4, 1, 0)
        grid.addWidget(self.__text, 0, 1)
        grid.addWidget(self.__text2, 1, 1)

        grid.addWidget(ok, 5, 1)
        ok.clicked.connect(self.connexion)
        self.setWindowTitle("Application - Surveillance")




    def connexion(self):
        self.__lab2.setText(f"{self.__text.text()} | {self.__text2.text()}")
        # print(Client.msg)
        host = str(self.__text.text())
        port = int(self.__text2.text())
        client = Client(host, port)
        client.connect()
        client.dialogue()
        QCoreApplication.exit(0)
        # par exemple accès la socket

    def _actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == "__main__":
    # print(sys.argv)
    # if len(sys.argv) < 3:
    #     client = Client("127.0.0.1",15000)
    # else :
    #     host = sys.argv[1]
    #     port = int(sys.argv[2])
    #     # création de l'objet client qui est aussi un thread
    #     client = Client(host,port)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()