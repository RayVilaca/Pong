import socket
import pickle

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = "192.168.1.5"
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = self.connect()

    def connect(self):
        data = "ID"
        self.client.sendto(str.encode(data), self.addr)
        data, addr = self.client.recvfrom(2048)
        data = data.decode()
        data = data.split(',')
        return int(float(data[0]))

    def send(self, data):
        try:
            self.client.sendto(str.encode(data), self.addr)
            data, addr = self.client.recvfrom(4096)
            return data.decode()
        except socket.error as e:
            return str(e)
