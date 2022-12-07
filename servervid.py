import socket
import threading

def handle_client(conn,address):
    print(f"[Nouvelle connexion] {address} connecté.")
    connected=True
    while connected :
        msg = conn.recv(1024).decode()
        if msg == "disconnect" or msg == "reset":
            connected = False
        print(f"[{address}],{msg}")
        msg = f"Msg recu : {msg}"
        conn.send(msg.encode())
    conn.close()

def main():
    server_socket = socket.socket()
    server_socket.bind(("localhost", 12000))
    server_socket.listen(1)

    while True :
        conn, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[Connexion activé]")


if __name__ == "__main__" :
    main()

