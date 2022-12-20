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
        self.controle = None
        self.identificadores = [1, 0]

    def executar(self):

        while True:
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

            start_new_thread(self.thread_cliente, (conn_movimento, conn_placar, identificador_jogador))


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

    def thread_cliente(self, conn_movimento, conn_placar, identificador_jogador): 
        reply = ''
        
        if len(self.identificadores) == 1:
            self.controle = Controle_Servidor()

        else:
            self.controle.comecar_partida()
        
        while True:
            try:
                if identificador_jogador == 0:
                    if self.controle.todos_prontos():
                        self.controle.movimentar_bola()

                    if self.controle.pegar_pontuacao_primeiro_jogador() >= PONTUACAO_MAXIMA or self.controle.pegar_pontuacao_segundo_jogador() >= PONTUACAO_MAXIMA:
                        self.controle.recomecar()
                        self.controle.comecar_partida()

                subir, descer = self.receber_dados(conn_movimento)

                if subir == None and descer == None:
                    break
                
                print(f"Identificador[{identificador_jogador}]: subir({'X' if subir else ''}), descer({'X' if descer else ''})")

                if subir or descer:
                    self.controle.movimentacao_raquete(subir, descer, identificador_jogador)

                if identificador_jogador == 0:
                    self.controle.tratamento_colisao()
                    self.controle.atualizacao_placar()
                
                conn_movimento.sendall(str.encode(self.controle.posicao_atualizada()))
                conn_placar.sendall(str.encode(self.controle.placar_atualizado()))
            except:
                break

        print("Conexão fechada")

        self.devolver_identificador(identificador_jogador)
        self.controle.pausar_partida()
        conn_movimento.close()
        conn_placar.close()


