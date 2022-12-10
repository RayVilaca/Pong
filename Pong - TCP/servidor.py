import sys
import socket
from _thread import *
from socket_servidor import SocketServidor
from componentes_jogo import Jogador, Bola, Controle
from variaveis_configuracao import PONTUACAO_MAXIMA

class Servidor:

    def __init__(self):
        self.socket = SocketServidor()
        self.controle = None
        self.identificadores = [1, 0]

    def executar(self):

        while True:
            conn, addr = self.socket.aceitar_conexao()
            print("Conectado: ", addr)


            if len(self.identificadores) == 0:
                print("Apenas 2 jogadores por vez")
                conn.close()
                continue

            start_new_thread(self.thread_cliente, (conn, self.identificadores.pop()))




    def thread_cliente(self, conn, identificador_jogador):
        
        
        conn.send(str.encode(str(identificador_jogador)))
        reply = ''
        
        print(len(self.identificadores))
        if len(self.identificadores) == 1:
            self.controle = Controle()

        else:
            self.controle.comecar_partida()
        
        while True:

            #try:

                if self.controle.todos_prontos():
                    self.controle.movimentar_bola()

                if self.controle.pegar_pontuacao_primeiro_jogador() >= PONTUACAO_MAXIMA or self.controle.pegar_pontuacao_segundo_jogador() >= PONTUACAO_MAXIMA:
                    self.controle.recomecar()
                    self.controle.comecar_partida()

                data = conn.recv(4096)
                reply = data.decode('utf-8')

                if not data:
                    break

                subir, descer = map(int, reply.split(','))
                
                print("Recebido: " + reply)
                print(f'{identificador_jogador}: {subir}, {descer}')

                if subir or descer:
                    self.controle.movimentacao_raquete(subir, descer, identificador_jogador)

                self.controle.tratamento_colisao()
                self.controle.atualizacao_placar()
                
                conn.sendall(str.encode(self.controle.posicao_atualizada()))
            #except:
             #   break

        print("Conexão fechada")

        self.identificadores.append(identificador_jogador)
        self.identificadores.sort(reverse = True)
        self.controle.pausar_partida()
        conn.close()


