#Alunas:
#Jully Manuele Dias Lima - 10420556
#Karina da Cunha Alves - 10420180

import socket

TCP_IP = '192.168.0.3'
TCP_PORTA = 10420
TAMANHO_BUFFER = 1024

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((TCP_IP, TCP_PORTA))  # conecta ao servidor

while True:
    MENSAGEM = input("Digite sua mensagem para o servidor: ")
    cliente.send(MENSAGEM.encode('UTF-8'))  # envia mensagem

    if MENSAGEM.upper() == "QUIT":  # cliente quer sair
        print("Cliente encerrou")
        break

    data = cliente.recv(1024)  # recebe resposta

    if not data:  # servidor fechou conexão
        print("Servidor encerrou")
        break

    print("received data:", data.decode())

    if data.decode().upper() == "QUIT":  # servidor quer sair
        print("Servidor encerrou")
        break

cliente.close()