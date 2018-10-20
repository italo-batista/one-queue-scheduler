# coding: utf-8
import time
from servidor import Servidor
from fregues import Fregues
from escalonador import Escalonador
from util.time_helper import current_time
from util.file_helper import write_results
from tipo_distribuicao import TipoDistribuicao, Distribuicao


class Simulador(object):

    def __init__(self, tipo_distribuicao_chegada, params_distribuicao, tempo_medio_servico, duracao_simulacao, qnt_repeticoes):
        """
        Construtor.

        Args:
                tipo_distribuicao_chegada (TipoDistribuicao): Tipo de distribuição de propabilidade para chegada de clientes.			
                params_distribuicao (list): Lista com parâmetros da distribuição. Consulte doc de tipo_distribuicao.
                tempo_medio_servico (int): Tempo médio que um cliente dura no serviço, em segundos.
                duracao_simulacao (int): Tempo que uma simulação deve durar, em segundos.
                qnt_repeticoes (int): Quantidade de repetições de uma simulação.
        """

        self.qnt_repeticoes = qnt_repeticoes
        self.duracao_simulacao = duracao_simulacao
        self.tempo_medio_servico = tempo_medio_servico
        self.params_distribuicao = params_distribuicao
        self.tipo_distribuicao_chegada = tipo_distribuicao_chegada
        self.distribuicao = Distribuicao(
            self.tipo_distribuicao_chegada, self.params_distribuicao)

    def run(self):

        for repeticao in xrange(self.qnt_repeticoes):

            servidor = Servidor()
            escalonador = Escalonador(self.tempo_medio_servico, servidor)

            self.requisicoes_recebidas = 0
            self.tempo_inicio = current_time()
            proxima_chegada = int(current_time() + self.distribuicao.sample())
            proximo_termino = 0

            while(not self.fim_execucao(self.tempo_inicio)):

                # se o servidor está livre.
                            # se tem fregues na fila, atende fregues, escalonando seu termino
                            # se chega freguês, escala o termino do fregues
                                    # pega chegada de próximo cliente
                                    # enquanto termino n ocorrer, servidor está ocupado. sleep do tempo para o termino
                # se não está livre
                            # se chegou freguês, coloca na fila

                if (current_time() >= proximo_termino):
                    servidor.liberar()

                if (servidor.is_livre()):
                    if (not escalonador.is_fila_vazia()):
                        proximo_termino = int(
                            escalonador.atender_fregues_em_fila())

                    elif (self.chegou_fregues(proxima_chegada)):
                        fregues = Fregues()
                        proxima_chegada = int(
                            current_time() + self.distribuicao.sample())
                        proximo_termino = int(escalonador.escalonar(fregues))

                else:
                    if (self.chegou_fregues(proxima_chegada)):
                        fregues = Fregues()
                        escalonador.enfileirar(fregues)

                escalonador.update_qnt_media_elems_na_fila(self.get_momento())
                time.sleep(0.9)

            write_results(
                self.tipo_distribuicao_chegada,
                self.params_distribuicao,
                self.tempo_medio_servico,
                self.duracao_simulacao,
                self.requisicoes_recebidas,
                escalonador.get_qnt_requisicoes_atendidas(),
                escalonador.get_tempo_medio_atendendo(),
                escalonador.get_qnt_media_elems_na_fila()
            )

    def fim_execucao(self, tempo_inicio):
        delta = current_time() - self.tempo_inicio
        return delta > self.duracao_simulacao

    def chegou_fregues(self, proxima_chegada):
        if current_time() >= proxima_chegada:
            self.requisicoes_recebidas += 1
            return True
        return False

    def get_momento(self):
        return current_time() - self.tempo_inicio

sim = Simulador(TipoDistribuicao.UNIFORME, [0, 1], 1, 10, 30)
sim.run()

sim = Simulador(TipoDistribuicao.NORMAL, [0.5, 0.4], 1, 10, 30)
sim.run()

sim = Simulador(TipoDistribuicao.EXPONENCIAL, [1], 1, 10, 30)
sim.run()
