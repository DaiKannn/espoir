import pathlib
import threading, socket
import sys
from threading import Lock

from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, \
    QTextEdit, QMessageBox, QFileDialog, QShortcut
from PyQt5.QtCore import QCoreApplication, Qt
from serverAD import *


class Client():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
        self.__thread = None

    def connect(self) -> int:
        try:
            self.__sock.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            print("[X] Serveur non lancé ou mauvaise information")
            return -1
        except ConnectionError:
            print("[X] Erreur de connection")
            return -1
        else:
            print("[+] Connexion réalisée")
            return 0

    def dialogue(self):
        try:
            msg = self.__sock.recv(1024).decode('cp850')
            return msg
        except:
            print("RIP")

    def envoi(self,msg):
        self.__sock.send(msg.encode())
        rep = self.__sock.recv(32000).decode()
        return rep

    def __reception(self, msg):
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = self.__sock.recv(1024).decode('cp850')
            return msg

    def connexion(self):
        self.__sock.connect((self.__host, self.__port))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        host = QLabel("Host :")
        port = QLabel("Port :")


        self.__ip = QComboBox()
        self.__text2 = QLineEdit("")
        self.__cmd = QLabel("Commande :")
        self.__text3 = QLineEdit("")
        self.__conn = QPushButton("Connexion")
        self.__deco = QPushButton("Déconnexion")
        self.__send = QPushButton("Envoyer")
        self.__lab3 = QTextEdit(self)
        self.__label3 = QLabel("Choisir un fichier :")
        self.__label4 = QPushButton("Choisir")
        self.__labtitre = QLabel("SAE3.02")
        self.__labtitre.setAlignment(Qt.AlignCenter)
        self.__labtitre.setFont(QFont('Arial', 30))
        self.__text5 = QLineEdit("")
        self.__text6 = QLineEdit("")
        self.__label5 = QLabel("Ajouter un Host :")
        self.__label6 = QPushButton("Ajouter")
        self.__label6.hide()
        self.__label6.setEnabled(False)
        self.__fichier = QLineEdit("")
        self.__conn.setEnabled(False)
        self.__text8 = QLineEdit("")
        self.__text6.setReadOnly(True)
        self.__lab3.setReadOnly(True)
        self.__newclient = QPushButton("Nouveau Client")
        self.__cmd.hide()
        self.__send.hide()
        self.__text3.hide()
        self.__lab3.hide()
        self.__deco.hide()
        self.__fichier.hide()
        self.__text5.hide()
        self.__nc = None
        self.__client = None

        self.shortcut_raccourci = QShortcut(QKeySequence('Return'), self)
        self.shortcut_raccourci.activated.connect(self._actioncmd)
        self.shortcut_raccourci = QShortcut(QKeySequence('Enter'), self)
        self.shortcut_raccourci.activated.connect(self._actioncmd)

        grid.addWidget(host, 1, 0)
        grid.addWidget(port, 1, 2)
        grid.addWidget(self.__ip, 1, 1)
        grid.addWidget(self.__text2, 1, 3)
        grid.addWidget(self.__cmd, 4, 0)
        grid.addWidget(self.__text3, 5, 1)
        grid.addWidget(self.__conn, 3, 3)
        grid.addWidget(self.__send, 5, 3)
        grid.addWidget(self.__label3, 6, 0)
        grid.addWidget(self.__label4, 6, 3)
        grid.addWidget(self.__labtitre, 0, 1)
        grid.addWidget(self.__lab3, 6, 1, 1, 5)
        grid.addWidget(self.__deco, 3, 3)
        grid.addWidget(self.__text5, 8, 1)
        grid.addWidget(self.__label5, 8, 0)
        grid.addWidget(self.__label6, 8, 3)
        grid.addWidget(self.__fichier, 9, 2)
        grid.addWidget(self.__text6, 6, 1)
        grid.addWidget(self.__newclient, 0,7)



        self.__text2.setText("10006")

        self.__conn.clicked.connect(self._actionconn)
        self.__send.clicked.connect(self._actioncmd)
        self.__deco.clicked.connect(self._actiondeco)
        self.__label4.clicked.connect(self._nmfichier)
        self.__label6.clicked.connect(self._nvhost)
        self.__newclient.clicked.connect(self._newclient)

        self.setWindowTitle("SAE3.02")

    def _actioncmd(self):
        msg = self.__text3.text()
        try:
            rep = self.__client.envoi(msg)
        except:
            self.__lab3.append(f"Erreur\n")
        else:
            self.__lab3.append(f"{rep}\n")
            self.__text3.clear()

    def _actionconn(self):
        host=str(self.__ip.currentText())
        port=int(self.__text2.text())
        self.__client = Client(host, port)
        self.__client.connexion()
        self.__lab3.show()
        self.__send.show()
        self.__cmd.show()
        self.__text3.show()
        self.__label3.hide()
        self.__label4.hide()
        self.__conn.hide()
        self.__deco.show()
        self.__label5.hide()
        self.__label6.hide()
        self.__text5.hide()
        self.__text6.hide()
        self.__newclient.hide()

    def _newclient(self):
        self.__nc = MainWindow()
        self.__nc.show()

    def _nvhost(self):
        if self.__text5.text() != "":
            ip = self.__text6.text()
            file = open(f"{ip}", "a")
            file.write(f"\n{self.__text5.text()}")
            self.__ip.addItem(self.__text5.text())
            self.__text5.setText("")
            self.__fichier = self.__text6.text()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Impossible d'ajouter un host vide")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

    def _nmfichier(self):
        try:
            settings = QFileDialog.Options()
            settings |= QFileDialog.DontUseNativeDialog
            nom, _ = QFileDialog.getOpenFileName(self, "Choisissez votre fichier", "","Fichiers Texte (*.txt)", options=settings)
            ip = pathlib.Path(nom).name
            self.__text6.setText(nom)
            file1 = open(f"{ip}", 'r')
            Lines = file1.readlines()

            count = 0
            for line in Lines:
                count += 1
                self.__ip.addItem(line.strip())

            self.__label6.setEnabled(True)
            self.__conn.setEnabled(True)

            self.__text5.show()
            self.__label5.show()
            self.__label6.show()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Erreur ! Vous avez fermer la fenêtre sans selectionner de fichier ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()

    def _actiondeco(self):
        self.__client.envoi("disconnect")
        QCoreApplication.exit(0)


    def _actionQuitter(self):
        QCoreApplication.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
