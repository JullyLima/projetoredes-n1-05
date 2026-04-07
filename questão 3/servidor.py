#Alunas:
#Jully Manuele Dias Lima - 10420556
#Karina da Cunha Alves - 10420180

import socket
import threading
import json
import time

#Configurações
HOST = '127.0.0.1'
PORTA = 12345          

LARGURA, ALTURA = 800, 600
VELOCIDADE_BOLA = 5
VELOCIDADE_RAQUETE = 7
TAMANHO_RAQUETE = 100
TAMANHO_BOLA = 15
PONTOS_PARA_VENCER = 5

#Estado do jogo 
estado = {
    "bola": {"x": LARGURA // 2, "y": ALTURA // 2},
    "vel_bola": {"x": VELOCIDADE_BOLA, "y": VELOCIDADE_BOLA},
    "raquete1": ALTURA // 2,   # jogador 1 (esquerda)
    "raquete2": ALTURA // 2,   # jogador 2 (direita)
    "placar": {"j1": 0, "j2": 0},
    "status": "aguardando",    # aguardando | jogando | fim
    "vencedor": None,
}

clientes = []       # lista de (conn, addr)
inputs = [0, 0]     # direção recebida de cada jogador (-1, 0 ou 1)
lock = threading.Lock()


def reiniciar_bola(direcao_x=1):
    estado["bola"] = {"x": LARGURA // 2, "y": ALTURA // 2}
    estado["vel_bola"] = {"x": VELOCIDADE_BOLA * direcao_x, "y": VELOCIDADE_BOLA}


def atualizar_jogo():
#"""Loop principal do jogo — roda em thread separada."""
    while True:
        if estado["status"] != "jogando":
            time.sleep(0.05)
            continue

        with lock:
            #Mover raquetes
            estado["raquete1"] = max(
                TAMANHO_RAQUETE // 2,
                min(ALTURA - TAMANHO_RAQUETE // 2,
                    estado["raquete1"] + inputs[0] * VELOCIDADE_RAQUETE)
            )
            estado["raquete2"] = max(
                TAMANHO_RAQUETE // 2,
                min(ALTURA - TAMANHO_RAQUETE // 2,
                    estado["raquete2"] + inputs[1] * VELOCIDADE_RAQUETE)
            )

            #Mover bola
            estado["bola"]["x"] += estado["vel_bola"]["x"]
            estado["bola"]["y"] += estado["vel_bola"]["y"]

            bx = estado["bola"]["x"]
            by = estado["bola"]["y"]

            #Rebater nas paredes (cima/baixo)
            if by <= 0 or by >= ALTURA:
                estado["vel_bola"]["y"] *= -1

            #Rebater na raquete 1 (esquerda, x ≈ 30)
            if bx <= 40 and abs(by - estado["raquete1"]) < TAMANHO_RAQUETE // 2:
                estado["vel_bola"]["x"] *= -1
                estado["bola"]["x"] = 41

            # Rebater na raquete 2 (direita, x ≈ LARGURA-30)
            if bx >= LARGURA - 40 and abs(by - estado["raquete2"]) < TAMANHO_RAQUETE // 2:
                estado["vel_bola"]["x"] *= -1
                estado["bola"]["x"] = LARGURA - 41

            #Ponto
            if bx < 0:
                estado["placar"]["j2"] += 1
                reiniciar_bola(direcao_x=1)
                if estado["placar"]["j2"] >= PONTOS_PARA_VENCER:
                    estado["status"] = "fim"
                    estado["vencedor"] = 2

            if bx > LARGURA:
                estado["placar"]["j1"] += 1
                reiniciar_bola(direcao_x=-1)
                if estado["placar"]["j1"] >= PONTOS_PARA_VENCER:
                    estado["status"] = "fim"
                    estado["vencedor"] = 1

        #Enviar estado para os dois clientes
        mensagem = json.dumps(estado) + "\n"
        for conn, _ in clientes:
            try:
                conn.sendall(mensagem.encode())
            except:
                pass

        time.sleep(1 / 60)  # ~60 FPS


def receber_input(conn, indice_jogador):
    """Recebe os inputs de um jogador em loop."""
    buffer = ""
    while True:
        try:
            dados = conn.recv(1024).decode()
            if not dados:
                break
            buffer += dados
            while "\n" in buffer:
                linha, buffer = buffer.split("\n", 1)
                msg = json.loads(linha)
                with lock:
                    inputs[indice_jogador] = msg.get("direcao", 0)
        except:
            break
    print(f"Jogador {indice_jogador + 1} desconectado.")


def aguardar_conexoes():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(2)
    print(f"Servidor aguardando na porta {PORTA}...")

    while len(clientes) < 2:
        conn, addr = servidor.accept()
        indice = len(clientes)
        clientes.append((conn, addr))
        print(f"Jogador {indice + 1} conectado: {addr}")

        #Informa ao cliente qual jogador ele é (1 ou 2)
        conn.sendall((json.dumps({"seu_numero": indice + 1}) + "\n").encode())

        #Inicia thread de recebimento de input desse jogador
        t = threading.Thread(target=receber_input, args=(conn, indice), daemon=True)
        t.start()

    print("Dois jogadores conectados! Iniciando jogo...")
    with lock:
        estado["status"] = "jogando"


#Main
if __name__ == "__main__":
    threading.Thread(target=atualizar_jogo, daemon=True).start()
    aguardar_conexoes()

    # Mantém o servidor vivo
    while True:
        time.sleep(1)
