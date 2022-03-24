import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 32016
        self.addr = (self.server, self.port)
        self.p = self.connect()
        self.qty = 0

    def getP(self):
        return self.p

    def decrement(self):
        self.qty -= 1
        if self.qty == 0:
            self.client.close()

    def connect(self):
        try:
            self.client.connect(self.addr)
            print('antes de aumentar: ', self.qty)
            self.qty += 1
            print('aumentando saporra ', self.qty)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            print('data: ', data)
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print('error: ', e)
            print(e)

    def receive(self, nickname):
        while True:  # making valid connection
            try:
                message = self.client.recv(1024).decode('ascii')

                if message == 'QUIT':
                    print('Desconectando do server...')
                    self.client.close()
                    break

                if message == 'NICKNAME':
                    self.client.send(nickname.encode('ascii'))
                else:
                    print(message)
            except:  # case on wrong ip/port details
                print("An error occured!")
                self.client.close()
                break

    def write(self, nickname):
        while True:  # message layout
            message = '{}: {}'.format(nickname, input(''))

            if message == 'QUIT':
                print('Desconectando do server...')
                self.client.close()
                break

            self.client.send(message.encode('ascii'))
