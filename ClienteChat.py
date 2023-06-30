import socket
import threading

# Configuracion del cliente
host = '127.0.0.1'
port = 8888

# Nombre de usuario del cliente
username = input('Ingrese su nombre de usuario: ')

# Creacion del socket del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Recibir mensajes del servidor
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8') # Recepcion del mensaje del servidor
            if message == 'NICK':
                client.send(username.encode('utf-8')) # Envio del nombre de usuario al servidor
            else:
                print(message)
        except:
            print('Ha ocurrido un error al recibir el mensaje.')
            client.close()
            break

# Funcion para enviar mensajes al servidor
def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('utf-8')) # Envio del mensaje al servidor

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()