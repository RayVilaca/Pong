import sys
import socket
from _thread import *
from socket_servidor import SocketServidor
from componentes_jogo import Jogador, Bola, Controle_Servidor
from variaveis_configuracao import PONTUACAO_MAXIMA

class Servidor:

    def __init__(self):
        self.socket = SocketServidor("192.168.56.1", 5555)
        self.socket_placar = SocketServidor("192.168.56.1", 6666)
        self.controle = Controle_Servidor()
        self.identificadores = [1, 0]
        self.jogadores = {}
        self.enderecos_placar = {}

    def associar_identificador(self, endereco_jogador):
        self.jogadores[endereco_jogador] = self.identificadores.pop()

    def desassociar_identificador(self, endereco_jogador):
        self.identificadores.append(self.jogadores[endereco_jogador])
        self.identificadores.sort(reverse = True)
        self.jogadores.pop(endereco_jogador)

    def executar(self):

        while True:

            #try:
                print("Esperando dados ...")
                dados_recebidos, endereco_jogador = self.socket.receber()
                dados_recebidos_decodificados = dados_recebidos.decode('utf-8')
                print(f"Dados recebidos: {dados_recebidos_decodificados}, {endereco_jogador}")
                if not dados_recebidos_decodificados:
                    break

                if endereco_jogador not in self.jogadores and len(self.identificadores) == 0:
                    print("Apenas 2 jogadores por vez")
                    break

                elif endereco_jogador not in self.jogadores:
                    self.associar_identificador(endereco_jogador)
                    if len(self.identificadores) == 0:
                        self.controle.comecar_partida()
                
                identificador_jogador = self.jogadores[endereco_jogador]

                if dados_recebidos_decodificados == "ID":  
                    self.socket.enviar(f'{identificador_jogador}', endereco_jogador)
                    dados_placar_recebidos, endereco_placar_jogador = self.socket_placar.receber()
                    print(f"Placar: {dados_recebidos.decode()}, {endereco_placar_jogador}")
                    self.socket_placar.enviar(f'{identificador_jogador}', endereco_placar_jogador)
                    self.enderecos_placar[endereco_jogador] = endereco_placar_jogador
                    continue

                if dados_recebidos_decodificados == "SAIR":
                    if len(self.identificadores) < 2:
                        print("Conexão fechada")
                        self.desassociar_identificador(endereco_jogador)
                        self.controle.pausar_partida()
                    
                    self.socket.enviar("Ok", endereco_jogador)
                        
                    if len(self.identificadores) == 2:
                        self.controle.recomecar()
                        print("Esperando uma nova dupla ...")

                    continue

                print(f'Posição:{identificador_jogador}:{self.controle.posicao_atualizada()}')

                if identificador_jogador == 0:
                    if self.controle.todos_prontos():
                        self.controle.movimentar_bola()

                    if self.controle.pegar_pontuacao_primeiro_jogador() >= PONTUACAO_MAXIMA or self.controle.pegar_pontuacao_segundo_jogador() >= PONTUACAO_MAXIMA:
                        self.controle.recomecar()
                        self.controle.comecar_partida()

                subir, descer = map(int, dados_recebidos_decodificados.split(','))

                print(f"Identificador[{identificador_jogador}]: subir({'X' if subir else ''}), descer({'X' if descer else ''})")

                if subir or descer:
                    self.controle.movimentacao_raquete(subir, descer, identificador_jogador)

                if identificador_jogador == 0:
                    self.controle.tratamento_colisao()
                    self.controle.atualizacao_placar()
                
                self.socket.enviar(self.controle.posicao_atualizada(), endereco_jogador)
                self.socket_placar.enviar(self.controle.placar_atualizado(), self.enderecos_placar[endereco_jogador])
            #except:
                #break

        



