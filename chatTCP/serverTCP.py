#Alunas:
#Jully Manuele Dias Lima - 10420556
#Karina da Cunha Alves - 10420180

import socket
 
TCP_IP = '192.168.0.3'
TCP_PORTA = 10420
TAMANHO_BUFFER = 1024
 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((TCP_IP, TCP_PORTA))  # define IP e porta
servidor.listen(1)  # espera conexão

print("Servidor disponível e escutando.....") 

conn, addr = servidor.accept()  # aceita cliente
print ('Endereço conectado:', addr)

while 1:
    data = conn.recv(TAMANHO_BUFFER).decode()  # recebe mensagem

    if data.upper() == "QUIT":  # cliente quer sair
        print("Cliente encerrou")
        break

    if data: 
        print ("Mensagem recebida:", data)  

        resposta = input("Servidor: ")
        conn.send(resposta.encode())  # envia resposta

        if resposta.upper() == "QUIT":  # servidor quer sair
            break

conn.close()