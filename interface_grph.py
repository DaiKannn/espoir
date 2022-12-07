import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QGridLayout, QComboBox, QMessageBox
from PyQt5.QtCore import QCoreApplication

class MainWindow(QMainWindow):
    def __init__(self,host,port):
        self.__host = host
        self.__port = port
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
        grid.addWidget(port,0,2)
        grid.addWidget(self.__text, 0, 1)
        grid.addWidget(self.__text2, 0, 3)
        grid.addWidget(cmd,2,0)
        grid.addWidget(self.__text3, 2, 1)
        grid.addWidget(conn, 2,3)
        grid.addWidget(self.__label2, 3,0)


        conn.clicked.connect(self._actioncmd)
        # # choix.currentTextChanged().connect(self._actionChoix)
        # aide.clicked.connect(self._actionAide)

        self.setWindowTitle("SAE3.02")

    def _actioncmd (self):
        self.__lab2.setText(f"Bonjour {self.__text.text()}")


    def _connexion(self):
        host= '127.0.0.1'
        port= 12000




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow(host="",port="")
    window.show()
    app.exec()