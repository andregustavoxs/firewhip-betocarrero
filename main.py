"""
Simulação de Sistema de Filas - FireWhip (Beto Carrero World)
===========================================================

Este módulo implementa uma simulação de eventos discretos para modelar
o sistema de filas da montanha-russa FireWhip do Beto Carrero World.

Autores: André Gustavo, Eduardo Silva, Marcus Fernando, Pedro Lucas,
         Samuel Victor, Lucas Gabriel
Disciplina: Simulação e Avaliação de Software
"""

import simpy
import random
import matplotlib.pyplot as plt
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Tuple
import numpy as np
from statistics import mean, stdev


@dataclass
class Cliente:
    """Representa um visitante na fila da FireWhip."""
    id: int
    tempo_chegada: float
    tempo_inicio_servico: float = 0
    tempo_fim_servico: float = 0

    @property
    def tempo_espera(self) -> float:
        """Calcula o tempo de espera na fila."""
        return self.tempo_inicio_servico - self.tempo_chegada

    @property
    def tempo_sistema(self) -> float:
        """Calcula o tempo total no sistema."""
        return self.tempo_fim_servico - self.tempo_chegada


class FireWhipSimulacao:
    """
    Simulação do sistema de filas da montanha-russa FireWhip.

    Características da FireWhip:
    - Capacidade: 20 pessoas por ciclo
    - Duração do passeio: 1min 36seg (96 segundos)
    - Tempo de embarque/desembarque: 3 minutos (180 segundos)
    - Ciclo total: 5 minutos (300 segundos)
    """

    # Constantes da FireWhip
    CAPACIDADE_FIREWHIP = 20
    TEMPO_PASSEIO = 96  # segundos (1min 36seg)
    TEMPO_EMBARQUE = 180  # segundos (3 minutos)
    CICLO_TOTAL = TEMPO_PASSEIO + TEMPO_EMBARQUE  # 276 segundos ≈ 5 minutos

    def __init__(self, env: simpy.Environment, cenario: str = "baixa_temporada"):
        """
        Inicializa a simulação.

        Args:
            env: Ambiente SimPy
            cenario: "baixa_temporada" ou "alta_temporada"
        """
        self.env = env
        self.cenario = cenario
        self.firewhip = simpy.Resource(env, capacity=1)  # Uma montanha-russa
        self.clientes_atendidos: List[Cliente] = []
        self.clientes_sistema: List[Cliente] = []
        self.contador_clientes = 0
        self.historico_fila: List[Tuple[float, int]] = []

        # Configurações por cenário
        self.config_cenario = self._configurar_cenario(cenario)

    def _configurar_cenario(self, cenario: str) -> Dict:
        """Configura parâmetros específicos do cenário."""
        configuracoes = {
            "baixa_temporada": {
                "intervalo_chegada": 120,  # 2 minutos entre chegadas
                "desvio_chegada": 30,  # Variação de ±30 segundos
                "descricao": "Baixa Temporada (Mar-Jun): 1 visitante a cada 2 minutos"
            },
            "alta_temporada": {
                "intervalo_chegada": 30,  # 30 segundos entre chegadas
                "desvio_chegada": 10,  # Variação de ±10 segundos
                "descricao": "Alta Temporada (Jan,Jul,Dez): 1 visitante a cada 30 segundos"
            }
        }
        return configuracoes[cenario]

    def gerar_chegadas(self):
        """Processo gerador de chegadas de clientes."""
        while True:
            # Tempo até próxima chegada (distribuição normal)
            intervalo = max(1, random.normalvariate(
                self.config_cenario["intervalo_chegada"],
                self.config_cenario["desvio_chegada"]
            ))

            yield self.env.timeout(intervalo)

            # Criar novo cliente
            self.contador_clientes += 1
            cliente = Cliente(
                id=self.contador_clientes,
                tempo_chegada=self.env.now
            )

            # Registrar tamanho atual da fila
            tamanho_fila = len(self.firewhip.queue) + len(self.firewhip.users)
            self.historico_fila.append((self.env.now, tamanho_fila))

            # Iniciar processo de atendimento
            self.env.process(self.processo_firewhip(cliente))

    def processo_firewhip(self, cliente: Cliente):
        """
        Processo de atendimento na FireWhip.

        Args:
            cliente: Cliente a ser atendido
        """
        # Aguardar vez na fila (até 20 pessoas)
        with self.firewhip.request() as request:
            yield request

            # Cliente inicia atendimento
            cliente.tempo_inicio_servico = self.env.now
            self.clientes_sistema.append(cliente)

            print(f"[{self.env.now:6.1f}s] Cliente {cliente.id:3d} iniciou atendimento "
                  f"(esperou {cliente.tempo_espera:5.1f}s)")

            # Aguardar até completar grupo de 20 pessoas ou timeout
            yield self.env.timeout(self.TEMPO_EMBARQUE)  # Embarque
            yield self.env.timeout(self.TEMPO_PASSEIO)  # Passeio

            # Cliente finaliza atendimento
            cliente.tempo_fim_servico = self.env.now
            self.clientes_atendidos.append(cliente)

            print(f"[{self.env.now:6.1f}s] Cliente {cliente.id:3d} finalizou atendimento "
                  f"(tempo total: {cliente.tempo_sistema:5.1f}s)")

    def coletar_estatisticas(self) -> Dict:
        """Coleta e calcula estatísticas da simulação."""
        if not self.clientes_atendidos:
            return {"erro": "Nenhum cliente foi atendido"}

        # Tempos de espera
        tempos_espera = [c.tempo_espera for c in self.clientes_atendidos]
        tempos_sistema = [c.tempo_sistema for c in self.clientes_atendidos]

        # Análise da fila
        if self.historico_fila:
            tamanhos_fila = [tamanho for _, tamanho in self.historico_fila]
            fila_max = max(tamanhos_fila)
            fila_media = mean(tamanhos_fila)
        else:
            fila_max = fila_media = 0

        # Taxa de atendimento
        tempo_total_simulacao = self.env.now
        taxa_atendimento = len(self.clientes_atendidos) / (tempo_total_simulacao / 3600)  # clientes/hora

        # Utilização do sistema
        tempo_ocupado = len(self.clientes_atendidos) * self.CICLO_TOTAL
        utilizacao = (tempo_ocupado / tempo_total_simulacao) * 100

        estatisticas = {
            "cenario": self.cenario,
            "descricao": self.config_cenario["descricao"],
            "tempo_simulacao_horas": tempo_total_simulacao / 3600,
            "clientes_chegaram": self.contador_clientes,
            "clientes_atendidos": len(self.clientes_atendidos),
            "clientes_na_fila": len(self.clientes_sistema) - len(self.clientes_atendidos),

            # Tempos de espera
            "tempo_espera_medio": mean(tempos_espera),
            "tempo_espera_min": min(tempos_espera),
            "tempo_espera_max": max(tempos_espera),
            "tempo_espera_desvio": stdev(tempos_espera) if len(tempos_espera) > 1 else 0,

            # Tempos no sistema
            "tempo_sistema_medio": mean(tempos_sistema),
            "tempo_sistema_max": max(tempos_sistema),

            # Análise da fila
            "fila_tamanho_max": fila_max,
            "fila_tamanho_medio": fila_media,

            # Performance
            "taxa_atendimento_hora": taxa_atendimento,
            "utilizacao_sistema_percent": utilizacao,

            # Dados brutos
            "tempos_espera": tempos_espera,
            "historico_fila": self.historico_fila
        }

        return estatisticas


def executar_simulacao(cenario: str, tempo_simulacao_horas: float = 8) -> Dict:
    """
    Executa uma simulação completa para um cenário específico.

    Args:
        cenario: "baixa_temporada" ou "alta_temporada"
        tempo_simulacao_horas: Duração da simulação em horas

    Returns:
        Dicionário com estatísticas da simulação
    """
    print(f"\n{'=' * 60}")
    print(f"INICIANDO SIMULAÇÃO - {cenario.upper()}")
    print(f"{'=' * 60}")

    # Configurar ambiente SimPy
    random.seed(42)  # Para reprodutibilidade
    env = simpy.Environment()

    # Criar simulação
    simulacao = FireWhipSimulacao(env, cenario)

    # Iniciar processo de chegadas
    env.process(simulacao.gerar_chegadas())

    # Executar simulação
    tempo_simulacao_segundos = tempo_simulacao_horas * 3600
    env.run(until=tempo_simulacao_segundos)

    # Coletar resultados
    estatisticas = simulacao.coletar_estatisticas()

    print(f"\nSIMULAÇÃO CONCLUÍDA - {cenario.upper()}")
    print(f"{'=' * 60}")

    return estatisticas


def imprimir_relatorio(stats: Dict):
    """Imprime relatório formatado das estatísticas."""
    print(f"\n📊 RELATÓRIO DE SIMULAÇÃO")
    print(f"{'=' * 50}")
    print(f"Cenário: {stats['descricao']}")
    print(f"Tempo de simulação: {stats['tempo_simulacao_horas']:.1f} horas")
    print(f"\n👥 CLIENTES:")
    print(f"  • Chegaram: {stats['clientes_chegaram']}")
    print(f"  • Atendidos: {stats['clientes_atendidos']}")
    print(f"  • Ainda na fila: {stats['clientes_na_fila']}")
    print(f"\n⏱️  TEMPOS DE ESPERA:")
    print(f"  • Média: {stats['tempo_espera_medio']:.1f}s ({stats['tempo_espera_medio'] / 60:.1f} min)")
    print(f"  • Mínimo: {stats['tempo_espera_min']:.1f}s")
    print(f"  • Máximo: {stats['tempo_espera_max']:.1f}s ({stats['tempo_espera_max'] / 60:.1f} min)")
    print(f"  • Desvio padrão: {stats['tempo_espera_desvio']:.1f}s")
    print(f"\n🏁 TEMPO NO SISTEMA:")
    print(f"  • Média: {stats['tempo_sistema_medio']:.1f}s ({stats['tempo_sistema_medio'] / 60:.1f} min)")
    print(f"  • Máximo: {stats['tempo_sistema_max']:.1f}s ({stats['tempo_sistema_max'] / 60:.1f} min)")
    print(f"\n📋 ANÁLISE DA FILA:")
    print(f"  • Tamanho máximo: {stats['fila_tamanho_max']} pessoas")
    print(f"  • Tamanho médio: {stats['fila_tamanho_medio']:.1f} pessoas")
    print(f"\n📈 PERFORMANCE:")
    print(f"  • Taxa atendimento: {stats['taxa_atendimento_hora']:.1f} clientes/hora")
    print(f"  • Utilização sistema: {stats['utilizacao_sistema_percent']:.1f}%")


def gerar_graficos(stats_baixa: Dict, stats_alta: Dict):
    """Gera gráficos comparativos dos resultados."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    # Gráfico 1: Comparação de tempos médios de espera
    cenarios = ['Baixa Temporada', 'Alta Temporada']
    tempos_espera = [stats_baixa['tempo_espera_medio'] / 60, stats_alta['tempo_espera_medio'] / 60]

    ax1.bar(cenarios, tempos_espera, color=['green', 'red'], alpha=0.7)
    ax1.set_title('Tempo Médio de Espera por Cenário')
    ax1.set_ylabel('Tempo (minutos)')
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Distribuição dos tempos de espera
    ax2.hist(np.array(stats_baixa['tempos_espera']) / 60, bins=20, alpha=0.7,
             label='Baixa Temporada', color='green')
    ax2.hist(np.array(stats_alta['tempos_espera']) / 60, bins=20, alpha=0.7,
             label='Alta Temporada', color='red')
    ax2.set_title('Distribuição dos Tempos de Espera')
    ax2.set_xlabel('Tempo de Espera (minutos)')
    ax2.set_ylabel('Frequência')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Gráfico 3: Evolução do tamanho da fila (Baixa Temporada)
    if stats_baixa['historico_fila']:
        tempos_b, tamanhos_b = zip(*stats_baixa['historico_fila'][:100])  # Primeiras 100 observações
        ax3.plot(np.array(tempos_b) / 3600, tamanhos_b, 'g-', alpha=0.7)
        ax3.set_title('Evolução da Fila - Baixa Temporada')
        ax3.set_xlabel('Tempo (horas)')
        ax3.set_ylabel('Pessoas na Fila')
        ax3.grid(True, alpha=0.3)

    # Gráfico 4: Evolução do tamanho da fila (Alta Temporada)
    if stats_alta['historico_fila']:
        tempos_a, tamanhos_a = zip(*stats_alta['historico_fila'][:100])  # Primeiras 100 observações
        ax4.plot(np.array(tempos_a) / 3600, tamanhos_a, 'r-', alpha=0.7)
        ax4.set_title('Evolução da Fila - Alta Temporada')
        ax4.set_xlabel('Tempo (horas)')
        ax4.set_ylabel('Pessoas na Fila')
        ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('resultados_simulacao_firewhip.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """Função principal - executa simulação completa."""
    print("🎢 SIMULAÇÃO DO SISTEMA DE FILAS - FIREWHIP")
    print("Beto Carrero World - Análise Comparativa de Cenários")
    print("=" * 60)

    # Executar simulações
    resultado_baixa = executar_simulacao("baixa_temporada", tempo_simulacao_horas=8)
    resultado_alta = executar_simulacao("alta_temporada", tempo_simulacao_horas=8)

    # Gerar relatórios
    print("\n" + "=" * 60)
    print("📋 RELATÓRIOS DETALHADOS")
    print("=" * 60)

    imprimir_relatorio(resultado_baixa)
    print("\n" + "-" * 50)
    imprimir_relatorio(resultado_alta)

    # Comparação final
    print(f"\n🎯 COMPARAÇÃO FINAL:")
    print(f"{'=' * 50}")
    melhoria_espera = (resultado_alta['tempo_espera_medio'] - resultado_baixa['tempo_espera_medio']) / 60
    print(f"Diferença no tempo de espera: +{melhoria_espera:.1f} minutos na alta temporada")

    diferenca_atendimento = resultado_alta['taxa_atendimento_hora'] - resultado_baixa['taxa_atendimento_hora']
    print(f"Diferença na taxa de atendimento: {diferenca_atendimento:+.1f} clientes/hora")

    # Gerar gráficos
    print(f"\n📊 Gerando gráficos comparativos...")
    gerar_graficos(resultado_baixa, resultado_alta)

    print(f"\n✅ Simulação concluída! Gráficos salvos em 'resultados_simulacao_firewhip.png'")


if __name__ == "__main__":
    main()