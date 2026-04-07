# Projeto Redes N1-05

## Visão geral

Este repositório contém dois exercícios de redes em Python:

- `chatTCP/` — cliente e servidor TCP para troca de mensagens texto.
- `questão 3/` — jogo Pong multiplayer com servidor e clientes usando sockets e `pygame`.

## Autoras

- Jully Manuele Dias Lima — 10420556
- Karina da Cunha Alves — 10420180

## Estrutura do projeto

- `chatTCP/ClientTCP.py` — cliente TCP de chat.
- `chatTCP/serverTCP.py` — servidor TCP de chat.
- `questão 3/cliente.py` — cliente multiplayer do jogo Pong.
- `questão 3/servidor.py` — servidor do jogo Pong.

## Requisitos

- Python 3
- `pygame` (para o jogo Pong)

Instale o `pygame` com:

```bash
python3 -m pip install pygame
```

## Como executar

### Chat TCP

1. Abra um terminal e execute o servidor:

```bash
python3 chatTCP/serverTCP.py
```

2. Em outro terminal, execute o cliente:

```bash
python3 chatTCP/ClientTCP.py
```

3. Digite mensagens no cliente e o servidor poderá responder no terminal do servidor.

4. Para encerrar, digite `QUIT` no cliente ou no servidor.

### Jogo Pong Multiplayer

1. Abra um terminal e execute o servidor do jogo:

```bash
python3 "questão 3/servidor.py"
```

2. Abra dois terminais diferentes para os jogadores e execute o cliente em cada um:

```bash
python3 "questão 3/cliente.py"
```

3. Cada jogador deve conectar-se ao servidor e controlar sua raquete com as teclas:

- `W` / `Up` — mover para cima
- `S` / `Down` — mover para baixo

4. O jogo termina quando um jogador alcança 5 pontos.

## Observações

- O servidor do Pong escuta em `127.0.0.1:12345`.
- O cliente do Pong também tenta se conectar em `127.0.0.1:12345`.
- Ajuste os endereços IP e portas nos scripts se desejar usar outra configuração de rede.
