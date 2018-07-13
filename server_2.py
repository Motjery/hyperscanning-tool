# coding: utf-8
# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connections clientes en parallèle.
HOST = '10.216.25.133'
PORT = 40000

import socket, sys, threading

class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connection avec un client'''
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connection = conn
        
    def run(self):
        # Dialogue avec le client :
        nom = self.getName()        # Chaque thread possède un nom
        msg1 = ''

        while 1:
            msgClient = ''
            try:
                msgClient = self.connection.recv(1024)
                print msgClient 
                if msgClient is not None:
                    msg1 = msgClient
            except:
                msgClient = msg1
            if msgClient.upper() == "FIN" or msgClient =="":
                break
            message =  msgClient
            print message
            # Faire suivre le message à tous les autres clients :
            for cle in conn_client:
                if cle != nom:      # ne pas le renvoyer à l'émetteur
                    try:
                        conn_client[cle].send(message)
                    except:
                        pass                    
        # Fermeture de la connection :
        self.connection.close()      # couper la connection côté serveur
        del conn_client[nom]        # supprimer son entrée dans le dictionnaire
        print "Client %s déconnecté." % nom
        # Le thread se termine ici    

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.bind((HOST, PORT))
except socket.error:
    print "La liaison du socket à l'adresse choisie a échoué."
    sys.exit()
print "Serveur prêt, en attente de requêtes ..."
mySocket.listen(5)

# Attente et prise en charge des connections demandées par les clients :
conn_client = {}                # dictionnaire des connections clients
while 1:    
    connection, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connection :
    th = ThreadClient(connection)
    th.start()
    # Mémoriser la connection dans le dictionnaire : 
    it = th.getName()        # identifiant du thread
    conn_client[it] = connection
    print "Client %s connecté, adresse IP %s, port %s." %\
           (it, adresse[0], adresse[1])
    # Dialogue avec le client :
#    connection.send("Vous êtes connecté. Envoyez vos messages.")
