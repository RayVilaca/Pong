import pygame
from socket_cliente import SocketCliente
from componentes_jogo import Jogador, Bola, Canvas, Controle_Cliente
from variaveis_configuracao import FPS

class Jogo:

    def __init__(self):
        self.socket = SocketCliente("192.168.56.1", 5555)     
        self.socket_placar = SocketCliente("192.168.56.1", 6666)
        self.controle = Controle_Cliente()

    def enviar_teclas(self, teclas):
        #Envia ao servidor se a tecla que o jogador acionou é de subida ou descida
        if self.socket.identificador_jogador == '0':
            dado =  (f'{0 if teclas == "Nenhuma" else int(teclas[pygame.K_w])},{0 if teclas == "Nenhuma" else int(teclas[pygame.K_s])}')
        else:
            dado = f'{0 if teclas == "Nenhuma" else int(teclas[pygame.K_UP])},{0 if teclas == "Nenhuma" else int(teclas[pygame.K_DOWN])}'

        return self.socket.enviar(dado)

    def executar(self):
        clock = pygame.time.Clock()

        teclas = "Nenhuma"
        executa = True
        
        while executa:
            clock.tick(FPS)

            teclas = pygame.key.get_pressed()

            dados_recebidos = self.enviar_teclas(teclas)
            self.controle.descompactar_dados(dados_recebidos)

            dados_placar = self.socket_placar.receber()
            self.controle.descompactar_dados_placar(dados_placar)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executa = False

                if evento.type == pygame.K_ESCAPE:
                    executa = False


            self.controle.desenhar()
                

        pygame.quit()

    



