import sys
import time
import socket
import threading
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
        self.lock = threading.Lock()
        self.evento = threading.Event()
        self.parar_threads = False
        self.conn_placares = []

    def receber_dados(self, conn_movimento):
        
        data = conn_movimento.recv(4096)
        reply = data.decode('utf-8')

        if not data:
            return None, None

        return map(int, reply.split(','))

    def pegar_identificador(self):
        return self.identificadores.pop()

    def devolver_identificador(self, identificador_jogador):
        self.identificadores.append(identificador_jogador)
        self.identificadores.sort(reverse = True)

    def thread_movimentar_bola(self):
        while not self.parar_threads:
            time.sleep(0.001)
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

            if self.parar_threads:
                break

            self.lock.acquire()
            try:
                if self.controle.pegar_pontuacao_primeiro_jogador() >= PONTUACAO_MAXIMA or self.controle.pegar_pontuacao_segundo_jogador() >= PONTUACAO_MAXIMA:
                    self.controle.recomecar()
                    self.controle.comecar_partida()

                for conn in list(self.conn_placares):
                    conn.sendall(str.encode(self.controle.placar_atualizado()))
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
                conn_movimento, addr_movimento = self.socket.aceitar_conexao()
                print("Conectado: ", addr_movimento)

                if len(self.identificadores) == 0:
                    print("Apenas 2 jogadores por vez")
                    conn_movimento.close()
                    continue

                #Enviar ao cliente o identificador correspondente a raquete associada a ele
                identificador_jogador = self.pegar_identificador()
                conn_movimento.send(str.encode(str(identificador_jogador)))

                conn_placar, addr_placar = self.socket_placar.aceitar_conexao()
                print("Conectado2: ", addr_placar)
                
                #Enviar ao cliente o identificador correspondente a raquete associada a ele
                conn_placar.send(str.encode(str(identificador_jogador)))

                self.conn_placares.append(conn_placar)


                start_new_thread(self.thread_cliente, (conn_movimento, conn_placar, identificador_jogador))
            except:
                print("Encerrando o jogo...")
                self.parar_threads = True
                evento.set()


    def thread_cliente(self, conn_movimento, conn_placar, identificador_jogador): 
        
        if len(self.identificadores) == 1:
            self.controle.recomecar()
        else:
            self.controle.comecar_partida()
        
        while True:
            try:

                subir, descer = self.receber_dados(conn_movimento)

                if subir == None and descer == None:
                    break
                
                print(f"Identificador[{identificador_jogador}]: subir({'X' if subir else ''}), descer({'X' if descer else ''})")

                self.lock.acquire()
                try:
                    if subir or descer:
                        self.controle.movimentacao_raquete(subir, descer, identificador_jogador)
                
                    conn_movimento.sendall(str.encode(self.controle.posicao_atualizada()))
                except:
                    break
                finally:
                    self.lock.release()
            except:
                break

        self.devolver_identificador(identificador_jogador)
        self.controle.pausar_partida()
        print(f"O jogador de id {identificador_jogador} saiu...")
        conn_movimento.close()
        conn_placar.close()

        if len(self.identificadores) == 2:
            raise Exceptio()


