#Alunas:
#Jully Manuele Dias Lima - 10420556
#Karina da Cunha Alves - 10420180

import socket
import threading
import json
import pygame
import sys

# Configurações
HOST = '127.0.0.1'     
PORTA = 12345          

LARGURA, ALTURA = 800, 600
TAMANHO_RAQUETE = 100
ESPESSURA_RAQUETE = 15
TAMANHO_BOLA = 15

# Cores
PRETO  = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA  = (100, 100, 100)
VERDE  = (0, 255, 100)
VERMELHO = (255, 60, 60)

# - Estado recebido do servidor -
estado = {}
estado_lock = threading.Lock()
meu_numero = None   # 1 ou 2


def receber_estado(conn):
    """Thread que fica ouvindo o servidor e atualiza o estado."""
    global meu_numero, estado
    buffer = ""
    while True:
        try:
            dados = conn.recv(4096).decode()
            if not dados:
                break
            buffer += dados
            while "\n" in buffer:
                linha, buffer = buffer.split("\n", 1)
                msg = json.loads(linha)

                # Primeira mensagem: servidor informa nosso número
                if "seu_numero" in msg:
                    meu_numero = msg["seu_numero"]
                else:
                    with estado_lock:
                        estado.update(msg)
        except:
            break


def enviar_input(conn, direcao):
    try:
        msg = json.dumps({"direcao": direcao}) + "\n"
        conn.sendall(msg.encode())
    except:
        pass


def desenhar(tela, fonte, fonte_grande):
    with estado_lock:
        if not estado:
            return
        bola      = estado.get("bola", {"x": 400, "y": 300})
        r1        = estado.get("raquete1", 300)
        r2        = estado.get("raquete2", 300)
        placar    = estado.get("placar", {"j1": 0, "j2": 0})
        status    = estado.get("status", "aguardando")
        vencedor  = estado.get("vencedor")

    tela.fill(PRETO)

    # Linha central
    pygame.draw.aaline(tela, CINZA, (LARGURA // 2, 0), (LARGURA // 2, ALTURA))

    # Raquetes
    cor_r1 = VERDE   if meu_numero == 1 else BRANCO
    cor_r2 = VERDE   if meu_numero == 2 else BRANCO

    pygame.draw.rect(tela, cor_r1,
                     (20, r1 - TAMANHO_RAQUETE // 2, ESPESSURA_RAQUETE, TAMANHO_RAQUETE))
    pygame.draw.rect(tela, cor_r2,
                     (LARGURA - 20 - ESPESSURA_RAQUETE, r2 - TAMANHO_RAQUETE // 2,
                      ESPESSURA_RAQUETE, TAMANHO_RAQUETE))

    # Bola
    pygame.draw.circle(tela, BRANCO,
                       (int(bola["x"]), int(bola["y"])), TAMANHO_BOLA)

    # Placar
    txt_p = fonte.render(f"{placar['j1']}  x  {placar['j2']}", True, BRANCO)
    tela.blit(txt_p, (LARGURA // 2 - txt_p.get_width() // 2, 20))

    # Tela de aguardando
    if status == "aguardando":
        txt = fonte.render("Aguardando o segundo jogador...", True, CINZA)
        tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, ALTURA // 2 - 20))

    # Tela de fim
    if status == "fim":
        if vencedor == meu_numero:
            txt = fonte_grande.render("Você venceu! 🏆", True, VERDE)
        else:
            txt = fonte_grande.render("Você perdeu!", True, VERMELHO)
        tela.blit(txt, (LARGURA // 2 - txt.get_width() // 2, ALTURA // 2 - 40))

    pygame.display.flip()


def main():
    # Conectar ao servidor 
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((HOST, PORTA))
        print("Conectado ao servidor!")
    except ConnectionRefusedError:
        print("Servidor não encontrado. Certifique-se de que o servidor está rodando.")
        sys.exit(1)

    # Thread para receber estado
    t = threading.Thread(target=receber_estado, args=(conn,), daemon=True)
    t.start()

    # Pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Pong Multiplayer")
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("monospace", 28, bold=True)
    fonte_grande = pygame.font.SysFont("monospace", 48, bold=True)

    # Aguarda receber o número do jogador
    print("Aguardando identificação do servidor...")
    while meu_numero is None:
        clock.tick(10)

    print(f"Você é o Jogador {meu_numero}!")
    pygame.display.set_caption(f"Pong Multiplayer — Jogador {meu_numero}")

    # Loop principal
    while True:
        direcao = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            direcao = -1
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            direcao = 1

        enviar_input(conn, direcao)
        desenhar(tela, fonte, fonte_grande)
        clock.tick(60)


if __name__ == "__main__":
    main()
