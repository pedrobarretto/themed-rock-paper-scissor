import socket
import threading
from _thread import *
import pickle
from game import Game

server = socket.gethostbyname(socket.gethostname())
port = 32016

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients = []
nicknames = []

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Servidor iniciado na porta: ", 32016)

connected = set()
games = {}
idCount = 0


# def broadcast(message):
#     for client in clients:
#         client.send(message)


# def chat_thread(conn, p, gameId):
#     while True:
#         try:
#             data = conn.recv(4096).decode()

#             if gameId in games:
#                 game = games[gameId]

#                 if not data:
#                     break
#                 else:
#                     if data == "reset":
#                         clients.remove(p)
#                     elif data != "get":
#                         clients.append(p)

#                     conn.sendall(pickle.dumps(game))
#             else:
#                 break
#         except:
#             break

#     conn.close()
#     while True:
#         try:
#             message = conn.recv(2048).decode()
#             if message:
#                 broadcast(message)
#         except:
#             break

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = s.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            print('antes do if gameId')
            if gameId in games:
                game = games[gameId]
                print('game: ', game)

                if not data:
                    break
                else:
                    if data == "reset":
                        print('data = reset')
                        game.resetWent()
                    elif data != "get":
                        print('data != get')
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Perda de conexao")
    try:
        del games[gameId]
        print("Fechando joguinho", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Conectado em:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Criando novo jogo...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
    receive()
