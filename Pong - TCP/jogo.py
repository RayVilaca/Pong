import pygame
from socket_cliente import SocketCliente
from componentes_jogo import Jogador, Bola, Canvas
from variaveis_configuracao import ALTURA_RAQUETE, LARGURA_RAQUETE, VERMELHO, AZUL, RAIO_BOLA, BRANCO, FPS, ALTURA_JANELA, LARGURA_JANELA

class Jogo:

    def __init__(self):
        self.socket = SocketCliente()        
        self.canvas = Canvas("Pong")
        self.prontos = 0
        self.pontuacao_primeiro_jogador = 0
        self.pontuacao_segundo_jogador = 0

    def executar(self):
        clock = pygame.time.Clock()

        self.primeiro_jogador = Jogador(10, ALTURA_JANELA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, VERMELHO)
        self.segundo_jogador = Jogador(LARGURA_JANELA - 10 - LARGURA_RAQUETE, ALTURA_JANELA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, AZUL)    
        self.bola = Bola(LARGURA_JANELA // 2, ALTURA_JANELA//2, RAIO_BOLA, BRANCO)

        teclas = "Nenhuma"
        executa = True
        
        while executa:

            clock.tick(FPS)

            teclas = pygame.key.get_pressed()

            dados_recebidos = self.enviar_teclas(teclas)
            self.descompactar_dados(dados_recebidos)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executa = False

                if evento.type == pygame.K_ESCAPE:
                    executa = False


            if not self.prontos:
                texto_rederizado = self.canvas.criar_texto_rederizado("Esperando por jogador...", 50, VERMELHO)
                self.canvas.desenhar_texto(texto_rederizado, LARGURA_JANELA / 2 - texto_rederizado.get_width() / 2, ALTURA_JANELA / 2 - texto_rederizado.get_height() / 2, True)
            else: 
                self.canvas.desenhar_componentes(ALTURA_JANELA, LARGURA_JANELA, self.primeiro_jogador, self.segundo_jogador, self.bola, self.pontuacao_primeiro_jogador, self.pontuacao_segundo_jogador)
                

        pygame.quit()

    def enviar_teclas(self, teclas):

        #Envia ao servidor se a tecla que o jogador acionou é de subida ou descida
        
        if self.socket.identificador_jogador == '0':
            dado =  (f'{0 if teclas == "Nenhuma" else int(teclas[pygame.K_w])},{0 if teclas == "Nenhuma" else int(teclas[pygame.K_s])}')
        else:
            dado = f'{0 if teclas == "Nenhuma" else int(teclas[pygame.K_UP])},{0 if teclas == "Nenhuma" else int(teclas[pygame.K_DOWN])}'

        return self.socket.send(dado)

    def descompactar_dados(self, dado):
        d = dado.split(",")
        self.prontos = int(float(d[0]))
        self.primeiro_jogador.x = int(float(d[1]))
        self.primeiro_jogador.y = int(float(d[2]))
        self.segundo_jogador.x = int(float(d[3]))
        self.segundo_jogador.y = int(float(d[4]))
        self.bola.x = int(float(d[5]))
        self.bola.y = int(float(d[6]))
        self.bola.x_velocidade = int(float(d[7]))
        self.bola.y_velocidade = int(float(d[8]))
        self.pontuacao_primeiro_jogador = int(float(d[9]))
        self.pontuacao_segundo_jogador = int(float(d[10]))



