import socket

class Rede:

    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor = "192.168.56.1"
        self.porta = 5555
        self.endereco = (self.servidor, self.porta)
        self.identificador_jogador = self.conectar()

    def conectar(self):
        self.cliente.connect(self.endereco)
        return self.cliente.recv(2048).decode()

    def send(self, dado):
        try:
            self.cliente.send(str.encode(dado))
            return self.cliente.recv(4096).decode()
        except socket.error as e:
            return str(e)
