import pygame
from variaveis_configuracao import BRANCO, VERMELHO, AZUL, PRETO, VELOCIDADE_MAXIMA_BOLA, ALTURA_JANELA, LARGURA_JANELA, RAIO_BOLA, ALTURA_RAQUETE, LARGURA_RAQUETE

class Jogador:

    def __init__(self, x_inicial, y_inicial, largura, altura, cor = BRANCO):
        self.x = self.x_partida = x_inicial
        self.y = self.y_partida = y_inicial
        self.largura = largura
        self.altura = altura
        self.velocidade = 4
        self.cor = cor

    def movimento(self, subir = True):
        if subir:
            self.y -= self.velocidade
        else:
            self.y += self.velocidade

    def recomecar(self):
        self.x = self.x_partida
        self.y = self.y_partida

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, (self.x, self.y, self.largura, self.altura))

class Bola:

    def __init__(self, x_inicial, y_inicial, raio, cor = BRANCO):
        self.x = self.x_partida = x_inicial
        self.y = self.y_partida = y_inicial
        self.raio = raio
        self.x_velocidade = VELOCIDADE_MAXIMA_BOLA
        self.y_velocidade = 0
        self.cor = cor

    def movimento(self):
        self.x += self.x_velocidade
        self.y += self.y_velocidade

    def recomecar(self):
        self.x = self.x_partida
        self.y = self.y_partida
        self.y_velocidade = 0
        self.x_velocidade *= -1

    def desenhar(self, janela):
        pygame.draw.circle(janela, self.cor, (self.x, self.y), self.raio)

class Controle_Cliente:

    def __init__(self):
        self.prontos = 0
        self.canvas = Canvas("Pong")
        self.pontuacao_primeiro_jogador = 0
        self.pontuacao_segundo_jogador = 0
        self.primeiro_jogador = Jogador(10, ALTURA_JANELA//2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, VERMELHO)
        self.segundo_jogador = Jogador(LARGURA_JANELA - 10 - LARGURA_RAQUETE, ALTURA_JANELA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, AZUL)
        self.bola = Bola(LARGURA_JANELA // 2, ALTURA_JANELA // 2, RAIO_BOLA)

    def desenhar(self):
        if not self.prontos:
            texto_rederizado = self.canvas.criar_texto_rederizado("Esperando por jogador...", 50, VERMELHO)
            self.canvas.desenhar_texto(texto_rederizado, LARGURA_JANELA / 2 - texto_rederizado.get_width() / 2, ALTURA_JANELA / 2 - texto_rederizado.get_height() / 2, True)
        else: 
            self.canvas.desenhar_componentes(ALTURA_JANELA, LARGURA_JANELA, self.primeiro_jogador, self.segundo_jogador, self.bola, self.pontuacao_primeiro_jogador, self.pontuacao_segundo_jogador)

    def descompactar_dados_placar(self, dado):
        d = dado.split(",")
        self.pontuacao_primeiro_jogador = int(float(d[0]))
        self.pontuacao_segundo_jogador = int(float(d[1]))

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

class Controle_Servidor:

    def __init__(self):
        self.prontos = 0
        self.pontuacao_primeiro_jogador = 0
        self.pontuacao_segundo_jogador = 0
        self.primeiro_jogador = Jogador(10, ALTURA_JANELA//2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE)
        self.segundo_jogador = Jogador(LARGURA_JANELA - 10 - LARGURA_RAQUETE, ALTURA_JANELA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE)
        self.bola = Bola(LARGURA_JANELA // 2, ALTURA_JANELA // 2, RAIO_BOLA)

    def pegar_primeiro_jogador(self):
        return self.primeiro_jogador

    def pegar_segundo_jogador(self):
        return self.segundo_jogador

    def pegar_pontuacao_primeiro_jogador(self):
        return self.pontuacao_primeiro_jogador

    def pegar_pontuacao_segundo_jogador(self):
        return self.pontuacao_segundo_jogador

    def movimentar_bola(self):
        self.bola.movimento()

    def todos_prontos(self):
        return self.prontos

    def pausar_partida(self):
        self.prontos = 0

    def comecar_partida(self):
        self.prontos = 1

    def recomecar(self):
        self.prontos = self.pontuacao_primeiro_jogador = self.pontuacao_segundo_jogador = 0
        self.bola.recomecar()
        self.primeiro_jogador.recomecar()
        self.segundo_jogador.recomecar()

    def atualizacao_placar(self):
        if self.bola.x < 0:
            self.pontuacao_segundo_jogador += 1
            self.bola.recomecar()

        elif self.bola.x > LARGURA_JANELA:
            self.pontuacao_primeiro_jogador += 1
            self.bola.recomecar()

    def placar_atualizado(self):
        return f'{self.pontuacao_primeiro_jogador},{self.pontuacao_segundo_jogador}'

    def posicao_atualizada(self):
        return f'{self.prontos},{self.primeiro_jogador.x},{self.primeiro_jogador.y},{self.segundo_jogador.x},{self.segundo_jogador.y},{self.bola.x},{self.bola.y},{self.bola.x_velocidade},{self.bola.y_velocidade}'
    
    def tratamento_colisao(self):
        
        if self.bola.y + self.bola.raio >= ALTURA_JANELA:
            self.bola.y_velocidade *= -1
        elif self.bola.y - self.bola.raio <= 0:
            self.bola.y_velocidade *= -1

        if self.bola.x_velocidade < 0:
            if self.bola.y >= self.primeiro_jogador.y and self.bola.y <= self.primeiro_jogador.y + self.primeiro_jogador.altura:
                
                if self.bola.x - self.bola.raio <= self.primeiro_jogador.x + self.primeiro_jogador.largura:
                    self.bola.x_velocidade *= -1

                    meio_y = self.primeiro_jogador.y + self.primeiro_jogador.altura / 2
                    diferenca_em_y = meio_y - self.bola.y
                    fator_reducao = (self.primeiro_jogador.altura / 2) / VELOCIDADE_MAXIMA_BOLA
                    y_velocidade = diferenca_em_y / fator_reducao
                    self.bola.y_velocidade = -1 * y_velocidade

        else:
            if self.bola.y >= self.segundo_jogador.y and self.bola.y <= self.segundo_jogador.y + self.segundo_jogador.altura:
                if self.bola.x + self.bola.raio >= self.segundo_jogador.x:
                    self.bola.x_velocidade *= -1

                    meio_y = self.segundo_jogador.y + self.segundo_jogador.altura / 2
                    diferenca_em_y = meio_y - self.bola.y
                    fator_reducao = (self.segundo_jogador.altura / 2) / VELOCIDADE_MAXIMA_BOLA
                    y_velocidade = diferenca_em_y / fator_reducao
                    self.bola.y_velocidade = -1 * y_velocidade

    def identificar_jogador(self, identificador_jogador):
        return self.segundo_jogador if identificador_jogador else self.primeiro_jogador

    def movimentacao_raquete(self, subir, descer, identificador_jogador):

        jogador = self.identificar_jogador(identificador_jogador)
        
        if subir and jogador.y - jogador.velocidade >= 0:
            jogador.movimento(subir = True)

        elif descer and jogador.y + jogador.velocidade + jogador.altura <= ALTURA_JANELA:
            jogador.movimento(subir = False)

    

class Canvas:

    def __init__(self, nome = "Nenhum"):
        self.janela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
        pygame.display.set_caption(nome)

    @staticmethod
    def atualizar():
        pygame.display.update()

    def criar_texto_rederizado(self, texto, tamanho, cor = BRANCO):
        pygame.font.init()
        fonte = pygame.font.SysFont("comicsans", tamanho)
        return fonte.render(texto, 1, cor)

    def desenhar_texto(self, texto_renderizado, x, y, atualiza = False):
        self.janela.blit(texto_renderizado, (x, y))
        if atualiza:
            self.atualizar()

    def preencher_fundo(self, cor = PRETO):
        self.janela.fill(cor)

    def desenhar_componentes(self, ALTURA, LARGURA, primeiro_jogador, segundo_jogador, bola, pontuacao_primeiro_jogador, pontuacao_segundo_jogador):

        #Preencher o fundo
        self.preencher_fundo()

        texto_rederizado_pontuacao_primeiro_jogador = self.criar_texto_rederizado(f"{pontuacao_primeiro_jogador}", 50)
        texto_rederizado_pontuacao_segundo_jogador = self.criar_texto_rederizado(f"{pontuacao_segundo_jogador}", 50)

        #Desenha o placar
        self.desenhar_texto(texto_rederizado_pontuacao_primeiro_jogador, LARGURA // 4 - texto_rederizado_pontuacao_primeiro_jogador.get_width() // 2, 20)
        self.desenhar_texto(texto_rederizado_pontuacao_segundo_jogador, LARGURA * (3 / 4) - texto_rederizado_pontuacao_segundo_jogador.get_width() // 2, 20)

        #Desenha a linha que divide a janela ao meio
        for i in range(10, ALTURA, ALTURA // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(self.janela, BRANCO, (LARGURA // 2 - 5, i, 10, ALTURA // 20))

        #Desenha as entidades ativas do jogo
        bola.desenhar(self.janela)
        primeiro_jogador.desenhar(self.janela)
        segundo_jogador.desenhar(self.janela)
        
        #Atualiza a janela
        self.atualizar()