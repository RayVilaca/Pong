import socket

class SocketTCPServidor:

    def __init__(self, ip, porta):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.porta = porta
        self.endereco = (self.ip, self.porta)
        self.escutar()
        self.servidor.settimeout(60) 

    def aceitar_conexao(self):
        return self.servidor.accept()

    def escutar(self):
        try:
            self.servidor.bind(self.endereco)
        except socket.error as e:
            print(str(e))

        self.servidor.listen(2)
        print(f"Esperando por uma conexão em {self.endereco}")
