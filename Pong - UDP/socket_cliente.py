import socket

class SocketCliente:

    def __init__(self, ip_servidor, porta_servidor):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor = ip_servidor
        self.porta = porta_servidor
        self.endereco = (self.servidor, self.porta)
        self.identificador_jogador = self.enviar("ID")

    def enviar(self, dados_enviar):
        try:
            dados_enviar_codificados = str.encode(dados_enviar)
            self.cliente.sendto(dados_enviar_codificados, self.endereco)
            dados_recebidos, endereco = self.cliente.recvfrom(4096)
            return dados_recebidos.decode()
        except socket.error as e:
            return str(e)
