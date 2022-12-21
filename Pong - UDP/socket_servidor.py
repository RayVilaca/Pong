import socket

class SocketServidor:

    def __init__(self, ip, porta):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.porta = porta
        self.endereco = (self.ip, self.porta)
        self.escutar()

    def receber(self):
        return self.servidor.recvfrom(4096)

    def enviar(self, dados_enviar, endereco):
        try:
            dados_enviar_codificados = str.encode(dados_enviar)
            return self.servidor.sendto(dados_enviar_codificados, endereco)
        except socket.error as e:
            print(str(e))

    def escutar(self):
        try:
            self.servidor.bind(self.endereco)
        except socket.error as e:
            print(str(e))

        print(f"Esperando por uma conexão em {self.endereco}")