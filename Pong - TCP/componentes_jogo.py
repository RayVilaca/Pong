import pygame
from variaveis_configuracao import BRANCO, PRETO

class Jogador:

    def __init__(self, x_inicial, y_inicial, largura, altura, cor = BRANCO):
        self.x = self.x_partida = x_inicial
        self.y = self.y_partida = y_inicial
        self.largura = largura
        self.altura = altura
        self.velocidade = 4
        self.cor = cor

    def movimento(self, subir=True):
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
    
    VELOCIDADE_MAXIMA = 4

    def __init__(self, x_inicial, y_inicial, raio, cor = BRANCO):
        self.x = self.x_partida = x_inicial
        self.y = self.y_partida = y_inicial
        self.raio = raio
        self.x_velocidade = self.VELOCIDADE_MAXIMA
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


class Canvas:

    def __init__(self, largura, altura, nome = "Nenhum"):
        self.largura = largura
        self.altura = altura
        self.janela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption(nome)

    @staticmethod
    def atualizar():
        pygame.display.update()

    def criar_texto_rederizado(self, texto, tamanho, cor = BRANCO):
        pygame.font.init()
        fonte = pygame.font.SysFont("comicsans", tamanho)
        return fonte.render(texto, 1, cor)

    def desenhar_texto(self, texto_renderizado, x, y, atualiza):
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
        self.desenhar_texto(texto_rederizado_pontuacao_primeiro_jogador, LARGURA // 4 - texto_rederizado_pontuacao_primeiro_jogador.get_width() // 2, 20, False)
        self.desenhar_texto(texto_rederizado_pontuacao_segundo_jogador, LARGURA * (3 / 4) - texto_rederizado_pontuacao_segundo_jogador.get_width() // 2, 20, False)

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