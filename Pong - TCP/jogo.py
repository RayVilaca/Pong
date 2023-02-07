import pygame
from socket_cliente import SocketCliente
from componentes_jogo import Jogador, Bola, Canvas, Controle_Cliente
from variaveis_configuracao import FPS

class Jogo:

    def __init__(self):
        self.lock = threading.Lock()
        self.socket = SocketCliente("192.168.56.1", 5555)     
        self.socket_placar = SocketCliente("192.168.56.1", 6666)
        self.controle = Controle_Cliente()

    def finalizar_sockets(self):
        self.socket.encerrar()
        self.socket_placar.encerrar()

    def enviar_teclas(self, teclas):
        if self.socket.identificador_jogador == '0':
            dado =  (f'{0 if teclas == "Nenhuma" else int(teclas[pygame.K_w])},{0 if teclas == "Nenhuma" else int(teclas[pygame.K_s])}')
        else:
            dado = f'{0 if teclas == "Nenhuma" else int(teclas[pygame.K_UP])},{0 if teclas == "Nenhuma" else int(teclas[pygame.K_DOWN])}'

        return self.socket.enviar(dado)

    def thread_receber_placar(self):
        while True:
            try:
                dados_placar = self.socket_placar.receber()

                self.lock.acquire()
                try:
                    self.controle.descompactar_dados_placar(dados_placar)
                finally:
                    self.lock.release()
                print(dados_placar)
            except:
                break

    def executar(self):
        clock = pygame.time.Clock()

        teclas = "Nenhuma"
        executa = True

        threading.Thread(target=self.thread_receber_placar).start()
        
        while executa:
            try:
                clock.tick(FPS)

                teclas = pygame.key.get_pressed()

                self.enviar_teclas(teclas)
                dados_recebidos = self.socket.receber()
                self.controle.descompactar_dados_movimento(dados_recebidos)

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        executa = False

                    if evento.type == pygame.K_ESCAPE:
                        executa = False

                self.lock.acquire()
                try:
                    self.controle.desenhar()
                except:
                    break
                finally:
                    self.lock.release()
            except:
                break
                

        self.finalizar_sockets()
        pygame.quit()
        print("Encerrando a partida...")

    



