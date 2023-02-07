import socket

class SocketCliente:

    def __init__(self, ip_servidor, porta_servidor):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.servidor = ip_servidor
        self.porta = porta_servidor
        self.endereco = (self.servidor, self.porta)
        print("Tentando me conectar ao servidor...")
        self.identificador_jogador = self.pegar_identificador()
        print(f"Recebimento de identificacao: {self.identificador_jogador}")

    def pegar_identificador(self):
        print("Enviando...")
        self.enviar("ID")
        print("Recebido...")
        return self.receber()

    def enviar(self, dados_enviar):
        try:
            dados_enviar_bytes = str.encode(dados_enviar)
            self.cliente.sendto(dados_enviar_bytes, self.endereco)
        except socket.error as e:
            raise e

    def receber(self):
        try:
            dados_recebidos_bytes, endereco = self.cliente.recvfrom(1024)
            return dados_recebidos_bytes.decode('utf-8')
        except socket.error as e:
            raise e


    def encerrar(self):
        self.cliente.close()

