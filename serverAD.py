import socket
import sys
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
                        if msg == 'OS':
                            conn.send(f"{platform.system()}".encode())

                        elif msg == 'CPU':
                            nbr_cpu = psutil.cpu_count()
                            cpus = psutil.cpu_percent()
                            cpusfinal = str(cpus)
                            conn.send(
                                f"Nombre de CPU logiques dans le système : {nbr_cpu}, Utilisation de tous les CPU : {cpusfinal}%".encode())


                        elif msg == 'RAM':
                            meminfo = psutil.virtual_memory()
                            total = round(meminfo.total / 1_073_741_824, 2)
                            utilise = round(meminfo.used / 1_073_741_824, 2)
                            disponible = round(meminfo.free / 1_073_741_824, 2)
                            conn.send(
                                f"Total de RAM : {total} Go, RAM utilsé : {utilise} Go, RAM disponible : {disponible} Go".encode())


                        elif msg == 'IP':
                            ipa = []
                            for nic, addrs in psutil.net_if_addrs().items():
                                for addr in addrs:
                                    address = addr.address
                                    if addr.family == AF_INET and not address.startswith("169.254"):
                                        ipa.append(f"{address}/{IPv4Network('0.0.0.0/' + addr.netmask).prefixlen}")
                            ipfinal = str(ipa)[1:-1]
                            conn.send(f"IP de la machine : {ipfinal}".encode())


                        elif msg == 'Name':
                            conn.send(f"Nom de la machine : {platform.node()}".encode())



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
