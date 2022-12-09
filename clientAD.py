import threading
import sys
from threading import Lock
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication
from serverAD import *


class Client():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
        self.__thread = None

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

    def __envoi(self):
        msg = input("Message à envoyer au Serveur : ")
        try:
            self.__sock.send(msg.encode())
        except BrokenPipeError:
            print ("erreur, socket fermée")
        return msg

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

        host = QLabel("host :")
        self.__label2 = QLabel("")
        self.__text = QLineEdit("")
        port = QLabel("port :")
        self.__text2 = QLineEdit("")
        cmd = QLabel("Commande :")
        self.__text3 = QLineEdit("")
        conn = QPushButton("Connexion")

        # Ajouter les composants au grid ayout

        grid.addWidget(host, 0, 0)
        grid.addWidget(port, 0, 2)
        grid.addWidget(self.__text, 0, 1)
        grid.addWidget(self.__text2, 0, 3)
        grid.addWidget(cmd, 2, 0)
        grid.addWidget(self.__text3, 2, 1)
        grid.addWidget(conn, 2, 3)
        grid.addWidget(self.__label2, 3, 0)

        conn.clicked.connect(self._actionconn)

        self.setWindowTitle("SAE3.02")

    def _actioncmd(self):
        self.__lab2.setText(f"Bonjour {self.__text.text()} | {self.__text2.text()}")

    def _actionconn(self):
        self.__lab3.setText(f"Bonjour {self.__text.text()}")
        host=str(self.__text.text())
        port=int(self.__text2.text())
        client= Client(host, port)
        client.connect()
        client.diaglogue()
        QCoreApplication.exit(0)


    def _actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

