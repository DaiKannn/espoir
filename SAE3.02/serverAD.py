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
                print ("erreur de connexion")
                break
            else :
                try:
                    while msg != "kill" and msg != "reset" and msg != "disconnect":
                        msg = conn.recv(1024).decode()
                        print ("Received from client: ", msg)
                        if msg == 'OS':
                            conn.send(f"{platform.platform()}".encode())

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
                            ip = []
                            for nic, addrs in psutil.net_if_addrs().items():
                                for addr in addrs:
                                    address = addr.address
                                    if addr.family == socket.AF_INET and not address.startswith("169.254"):
                                        ip.append(f"{address}/{IPv4Network('0.0.0.0/' + addr.netmask).prefixlen}")
                            ipé = str(ip)[1:-1]
                            conn.send(f"IP de la machine : {ipé}".encode())


                        elif msg == 'Name':
                            conn.send(f"Nom de la machine : {socket.gethostname()}".encode())



                        elif msg == 'Connexion information':
                            conn.send(
                                f"La machine a pour nom {platform.node()}, son IP est : {socket.gethostbyname(socket.gethostname())}".encode())



                        elif msg[0:4] == "Linux:":
                            if sys.platform == 'linux':
                                eucli = msg.split(':')[1]
                                som = subprocess.check_output(eucli, shell=True).decode('cp850')
                                conn.send(f"Commande {eucli} : {som}".encode())
                            else:
                                conn.send("La commande a échoué. Ce n'est pas le bon OS.".encode())


                        elif msg[0:4] == "DOS:":
                            if sys.platform == 'win32':
                                eucli = msg.split(':')[1]
                                som = subprocess.check_output(eucli, shell=True).decode('cp850')
                                conn.send(f"Commande {eucli} : {som}".encode())
                            else:
                                conn.send("La commande a échoué. Ce n'est pas le bon OS.".encode())


                        elif msg == "python --version":
                            pv = subprocess.getoutput('python --version')
                            conn.send(f"Nous sommes sur : {pv}".encode())


                        elif msg[0:4] == 'ping':
                            ping = msg.split(' ')
                            send = ping[1]
                            conn.send(subprocess.getoutput('ping ' + send).encode())

                        elif msg == "kill" or msg == "reset" or msg == "disconnect":
                            conn.send(msg.encode())
                        else:
                            reply = "Cela ne corespond pas à une commande, veuillez entrer une commande !"
                            conn.send(reply.encode())
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