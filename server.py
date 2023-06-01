#server.py

import socket, threading

class Server(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.sock = socket
        
    def run(self):
        global clients
        name = self.name 
        sys = True
        while(sys):
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                print(msg)
                if msg == "l'utilisateur à quitté la conversation":
                    clients[name].close()
            except socket.error:
                sys = False
                break
            else:
                for client in clients:
                    if client != name:
                        clients[client].send(msg.encode('utf-8'))
        del(clients[name])
        for client in clients:
            clients[client].send(("client {0} est déconnecté".format(name)).encode("utf-8"))
            sys = False

HOST = "localhost"
PORT = 6543

#Création du socket server 
server_address = (HOST, PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try : 
    server_socket.bind(server_address)
except : 
    print("le serveur ne c'est pas bien lancer")
    exit(1)

#Nombres d'utilisateurs
server_socket.listen(2)
print(f"Le serveur écoute à présent sur le port {PORT}")

#Server ON/OFF
systeme = True

# Variable des utilisateurs connecter
clients = {}

while(systeme):
    # Récuperation des infos clients
    client_socket, client_address = server_socket.accept()
    print(f'Connexion acceptée avec IP : {client_address[0]} PORT : {client_address[1]}')
    
    # Ouverture du server
    serv = Server(client_socket)
    serv.start()
    
    clients[serv.name] = client_socket
    

server_socket.close()
print("Le client s'est déconnecté")
