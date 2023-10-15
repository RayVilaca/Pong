import sys
import pygame
import socket
import time
import threading
from _thread import *
from socket_servidor import SocketServidor
from componentes_jogo import Jogador, Bola, Controle_Servidor
from variaveis_configuracao import PONTUACAO_MAXIMA, FPS

class Servidor:

    def __init__(self):
        self.socket = SocketServidor("192.168.56.1", 5555)
        self.socket_placar = SocketServidor("192.168.56.1", 6666)
        self.controle = Controle_Servidor()
        self.identificadores = [1, 0]
        self.jogadores = {}
        self.enderecos_placar = {}
        self.lock = threading.Lock()
        self.evento = threading.Event()

    def associar_identificador(self, endereco_jogador):
        self.lock.acquire()
        try:
            self.jogadores[endereco_jogador] = self.identificadores.pop()
        finally:
            self.lock.release()  

    def desassociar_identificador(self, endereco_jogador):
        self.lock.acquire()
        try:
            self.identificadores.append(self.jogadores[endereco_jogador])
            self.identificadores.sort(reverse = True)
            self.jogadores.pop(endereco_jogador)
        finally:
            self.lock.release()

    def thread_movimentar_bola(self):
        while True:
            time.sleep(0.003)
            self.lock.acquire()
            try:
                if self.controle.todos_prontos():
                    self.controle.movimentar_bola()

                self.controle.tratamento_colisao()
                self.controle.atualizacao_placar(self.evento)
            except:
                break
            finally:
                self.lock.release()
        print("Thread para movimentar a bola encerrada...")

    def thread_enviar_placar(self):
        while True:
            self.evento.wait()

            self.lock.acquire()
            try:
                if self.controle.pegar_pontuacao_primeiro_jogador() >= PONTUACAO_MAXIMA or self.controle.pegar_pontuacao_segundo_jogador() >= PONTUACAO_MAXIMA:
                    self.controle.recomecar()
                    self.controle.comecar_partida()

                for endereco in list(self.enderecos_placar.values()):
                    print(endereco)
                    self.socket_placar.enviar(self.controle.placar_atualizado(), endereco)
            except:
                break
            finally:
                self.lock.release()

            self.evento.clear()
        
        print("Thread para enviar o placar encerrada...")         

    def executar(self):

        threading.Thread(target=self.thread_enviar_placar).start()
        threading.Thread(target=self.thread_movimentar_bola).start()

        while True:

            try:

                dados_recebidos, endereco_jogador = self.socket.receber()

                if not dados_recebidos:
                    continue

                if endereco_jogador not in self.jogadores and len(self.identificadores) == 0:
                    print("Apenas 2 jogadores por vez")
                    continue

                elif endereco_jogador not in self.jogadores:
                    print(f"Novo jogador: {endereco_jogador}")
                    self.associar_identificador(endereco_jogador)
                    if len(self.identificadores) == 0:
                        self.controle.comecar_partida()
                
                identificador_jogador = self.jogadores[endereco_jogador]

                if dados_recebidos == "ID":  
                    self.socket.enviar(f'{identificador_jogador}', endereco_jogador)
                    dados_placar_recebidos, endereco_placar_jogador = self.socket_placar.receber()
                    self.socket_placar.enviar(f'{identificador_jogador}', endereco_placar_jogador)
                    self.enderecos_placar[endereco_jogador] = endereco_placar_jogador
                    continue

                if dados_recebidos == "SAIR":
                    if len(self.identificadores) < 2:
                        print(f"O jogador de id {identificador_jogador} saiu...")
                        self.desassociar_identificador(endereco_jogador)
                        self.controle.pausar_partida()

                    if len(self.identificadores) == 2:
                        self.controle.recomecar()
                        print("Esperando uma nova dupla ...")

                    continue

                subir, descer = map(int, dados_recebidos.split(','))

                self.lock.acquire()
                try:
                    if subir or descer:
                        self.controle.movimentacao_raquete(subir, descer, identificador_jogador)

                    self.socket.enviar(self.controle.posicao_atualizada(), endereco_jogador)
                except:
                    break
                finally:
                    self.lock.release()
            
            except socket.timeout:
                continue
            except:
                break

        self.socket.encerrar()
        self.socket_placar.encerrar()
        self.parar_threads = True
        self.evento.set()
        print("Encerrando o jogo...")
