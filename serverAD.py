import socket
import sys
import subprocess
import platform
from ipaddress import IPv4Network

import psutil

def serveur():
    msg = ""
    while msg != "kill" :
        msg = ""
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 10006))
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
                        if msg == 'OS':
                            conn.send(f"{platform.system()}".encode())

                        elif msg == 'CPU':
                            cpup = psutil.cpu_percent()
                            cpu = str(cpup)
                            conn.send(f"Utilisation des CPU : {cpu} % .".encode())

                        elif msg == 'Nb CPU':
                            nbcpu = psutil.cpu_count()
                            conn.send(f"Nombre de CPU {nbcpu}".encode())


                        elif msg == 'RAM utilisé':
                            memuse = psutil.virtual_memory().percent
                            conn.send(f" RAM utilsé : {memuse} Go".encode())

                        elif msg == 'RAM restante':
                            memrest = psutil.virtual_memory().available * 100/ psutil.virtual_memory().total
                            conn.send(f"Ram restante : {memrest} Go.".encode())

                        elif msg == 'IP':
                            ipa = []
                            for nic, addrs in psutil.net_if_addrs().items():
                                for addr in addrs:
                                    address = addr.address
                                    if addr.family == socket.AF_INET and not address.startswith("169.254"):
                                        ipa.append(f"{address}/{IPv4Network('0.0.0.0/' + addr.netmask).prefixlen}")
                            ipfinal = str(ipa)[1:-1]
                            conn.send(f"IP de la machine : {ipfinal}".encode())


                        elif msg == 'Name':
                            conn.send(f"Nom de la machine : {socket.gethostname()}".encode())



                        elif msg == 'Connexion information':
                            conn.send(
                                f"Le nom de la machine est {platform.node()}, son IP est la suivante : {socket.gethostbyname(socket.gethostname())}".encode())



                        elif msg[0:4] == "Linux:":
                            if sys.platform == 'linux':
                                divise = msg.split(':')[1]
                                resultat = subprocess.check_output(divise, shell=True).decode('cp850')
                                conn.send(f"Commande {divise} : {resultat}".encode())
                            else:
                                conn.send("Commande échouée : OS inadéquat".encode())


                        elif msg[0:4] == "DOS:":
                            if sys.platform == 'win32':
                                divise = msg.split(':')[1]
                                resultat = subprocess.check_output(divise, shell=True).decode('cp850')
                                conn.send(f"Commande {divise} : {resultat}".encode())
                            else:
                                conn.send("Commande échouée : OS inadéquat".encode())


                        elif msg == "python --version":
                            python = subprocess.getoutput('python --version')
                            conn.send(f"La version de python est la suivante : {python}".encode())


                        elif msg[0:4] == 'ping':
                            p = msg.split(' ')
                            destinataire = p[1]
                            conn.send(subprocess.getoutput('ping ' + destinataire).encode())
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
