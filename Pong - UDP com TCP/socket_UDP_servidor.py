import socket

class SocketUDPServidor:

    def __init__(self, ip, porta):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.porta = porta
        self.endereco = (self.ip, self.porta)
        self.escutar()

    def receber(self):
        try:
            dados_recebidos_bytes, endereco = self.servidor.recvfrom(1024)
            dados_recebidos= dados_recebidos_bytes.decode('utf-8')
            return dados_recebidos, endereco
        except socket.error as e:
            raise e

    def enviar(self, dados_enviar, endereco):
        try:
            dados_enviar_bytes = str.encode(dados_enviar)
            return self.servidor.sendto(dados_enviar_bytes, endereco)
        except socket.error as e:
            raise e

    def escutar(self):
        try:
            self.servidor.bind(self.endereco)
        except socket.error as e:
            raise e

        print(f"Esperando por uma conexão em {self.endereco}")

    def encerrar(self):
        self.servidor.close()