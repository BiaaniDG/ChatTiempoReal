import socket
import threading

# Configuracion del servidor
host = '127.0.0.1'
port = 8888

# Creacion del socket del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Listas para gestionar las conexiones de los clientes y mensajes entrantes
clients = []
usernames = []

# Enviar mensajes a todos los clientes conectados
def broadcast(message):
    for client in clients:
        client.send(message)

# Manejo de las conexiones de los clientes
def handle(client):
    while True:
        try:
            message = client.recv(1024) # Recepcion del mensaje del cliente
            broadcast(message) # Envio del mensaje a los clientes conectados
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            break

# Recibir conexiones de los clientes y manejarlos
def receive():
    while True:
        client, address = server.accept() # Aceptacion de la conexion del cliente
        print(f"Conexion establecida con {str(address)}")

        client.send("NOMBRE DE USUARIO".encode('utf-8')) # Solicitud del nombre de usuario del cliente
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(f"{username} se ha unido al chat!") # Envio de mensaje de bienvenida a todos los clientes conectados
        broadcast(f"{username} se ha unido al chat!\n".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Servidor iniciado...")
receive()