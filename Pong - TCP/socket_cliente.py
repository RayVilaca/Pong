import socket

class SocketCliente:

    def __init__(self, ip_servidor, porta_servidor):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor = ip_servidor
        self.porta = porta_servidor
        self.endereco = (self.servidor, self.porta)
        self.identificador_jogador = self.conectar()

    def conectar(self):
        self.cliente.connect(self.endereco)
        return self.cliente.recv(4096).decode()

    def enviar(self, dado):
        try:
            self.cliente.send(str.encode(dado))
            return self.cliente.recv(4096).decode()
        except socket.error as e:
            return str(e)

    def receber(self):
        try:
            return self.cliente.recv(4096).decode()
        except socket.error as e:
            return str(e)
