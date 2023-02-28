import socket

class SocketTCPCliente:

    def __init__(self, ip_servidor, porta_servidor):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor = ip_servidor
        self.porta = porta_servidor
        self.endereco = (self.servidor, self.porta)
        self.identificador_jogador = self.conectar()

    def conectar(self):
        self.cliente.connect(self.endereco)
        return self.cliente.recv(1024).decode()

    def enviar(self, dado):
        try:
            dados_enviar_bytes = str.encode(dado)
            self.cliente.send(dados_enviar_bytes)
        except socket.error as e:
            raise e

    def receber(self):
        try:
            dados_recebidos_bytes = self.cliente.recv(1024)
            return dados_recebidos_bytes.decode('utf-8')
        except socket.error as e:
            raise e

    def encerrar(self):
        self.cliente.close()
