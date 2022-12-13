import socket

class SocketServidor:

    def __init__(self):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = "192.168.56.1"
        self.porta = 5555
        self.endereco = (self.ip, self.porta)
        self.escutar()

    def aceitar_conexao(self):
        return self.servidor.accept()

    def escutar(self):
        try:
            self.servidor.bind(self.endereco)
        except socket.error as e:
            print(str(e))

        self.servidor.listen(2)
        print("Esperando por uma conexão...")