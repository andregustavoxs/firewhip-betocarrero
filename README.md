# 🎢 Simulação de Sistema de Filas - FireWhip

## Projeto Acadêmico - Beto Carrero World

Uma simulação de eventos discretos do sistema de filas da montanha-russa FireWhip do Beto Carrero World, desenvolvida como projeto da disciplina de **Simulação e Avaliação de Software**.

---

## 👥 Equipe

- **André Gustavo Xavier dos Santos**
- **Eduardo Silva Weba Ferreira**  
- **Marcus Fernando Santos Cuba**
- **Pedro Lucas Pires Lopes**
- **Samuel Victor Avelino Araújo**
- **Lucas Gabriel Pereira Pestana**

---

## 📋 Descrição do Projeto

Este projeto implementa uma simulação computacional para analisar o sistema de filas da **FireWhip**, a única montanha-russa invertida do Brasil, localizada no Beto Carrero World. A simulação compara dois cenários distintos de demanda: **baixa temporada** e **alta temporada**.

### 🎯 Objetivos

- Aplicar conceitos de simulação de eventos discretos em um caso real
- Modelar sistema de filas usando teoria de filas (FIFO)
- Analisar comportamento do sistema em diferentes cenários de demanda
- Gerar métricas e insights para otimização operacional

---

## 🎢 Características da FireWhip

| Especificação | Valor |
|---------------|-------|
| 🏃 **Capacidade** | 20 pessoas por ciclo |
| ⏱️ **Duração do passeio** | 1min 36seg (96 segundos) |
| 🚪 **Tempo embarque/desembarque** | 3 minutos (180 segundos) |
| 🔄 **Ciclo total** | ~5 minutos (276 segundos) |
| 📏 **Percurso** | 700 metros |
| ⚡ **Velocidade máxima** | 80 km/h |
| 📐 **Altura máxima** | 33,3 metros |

---

## 🔬 Metodologia de Simulação

### Modelagem do Sistema

- **Entidades**: Visitantes (clientes) e FireWhip (servidor único)
- **Eventos**: Chegada de visitante na fila e término do atendimento
- **Atributos**: Tempo de chegada, tempo de espera, tempo de atendimento
- **Tipo de Fila**: FIFO (First In, First Out)

### Cenários Analisados

#### 🟢 Baixa Temporada (Março - Junho)
- **Taxa de chegada**: 1 visitante a cada 2 minutos (±30s)
- **Público esperado**: 3.000 - 8.000 visitantes/dia
- **Característica**: Sistema opera abaixo da capacidade

#### 🔴 Alta Temporada (Janeiro, Julho, Dezembro)
- **Taxa de chegada**: 1 visitante a cada 30 segundos (±10s)
- **Público esperado**: 15.000 - 25.000 visitantes/dia
- **Característica**: Sistema opera próximo do limite

---

## 💻 Requisitos Técnicos

### Dependências

```bash
pip install simpy matplotlib pandas numpy
```

### Versões Testadas

- **Python**: 3.8+
- **SimPy**: 4.0+
- **Matplotlib**: 3.5+
- **Pandas**: 1.3+
- **NumPy**: 1.21+

---

## 🚀 Como Executar

### Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/simulacao-firewhip.git
   cd simulacao-firewhip
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a simulação**:
   ```bash
   python firewhip_simulacao.py
   ```

### Execução Personalizada

```python
from firewhip_simulacao import executar_simulacao, imprimir_relatorio

# Executar cenário específico
resultado = executar_simulacao("baixa_temporada", tempo_simulacao_horas=8)
imprimir_relatorio(resultado)
```

---

## 📊 Resultados e Métricas

### Métricas Calculadas

- **Tempo médio de espera** (segundos/minutos)
- **Tempo máximo de espera**
- **Tempo médio no sistema**
- **Tamanho médio da fila**
- **Tamanho máximo da fila**
- **Taxa de atendimento** (clientes/hora)
- **Utilização do sistema** (%)
- **Número de clientes atendidos**

### Saídas Geradas

1. **Relatório em console** com estatísticas detalhadas
2. **Gráficos comparativos** salvos em PNG:
   - Tempo médio de espera por cenário
   - Distribuição dos tempos de espera
   - Evolução do tamanho da fila ao longo do tempo

---

## 📁 Estrutura do Projeto

```
simulacao-firewhip/
│
├── firewhip_simulacao.py      # Código principal da simulação
├── README.md                  # Documentação do projeto
├── requirements.txt           # Dependências Python
├── resultados/               # Pasta para resultados
│   ├── graficos/            # Gráficos gerados
│   └── relatorios/          # Relatórios CSV/Excel
└── docs/                     # Documentação adicional
    ├── apresentacao.html    # Slides da apresentação
    └── relatorio_tecnico.md # Relatório técnico detalhado
```

---

## 🔧 Arquitetura do Código

### Classes Principais

#### `Cliente`
```python
@dataclass
class Cliente:
    id: int
    tempo_chegada: float
    tempo_inicio_servico: float = 0
    tempo_fim_servico: float = 0
```

#### `FireWhipSimulacao`
```python
class FireWhipSimulacao:
    """Simulação principal do sistema de filas."""
    
    def __init__(self, env, cenario)
    def gerar_chegadas(self)
    def processo_firewhip(self, cliente)
    def coletar_estatisticas(self)
```

### Funções Utilitárias

- `executar_simulacao()`: Executa simulação completa
- `imprimir_relatorio()`: Gera relatório formatado
- `gerar_graficos()`: Cria visualizações comparativas
- `main()`: Função principal com execução padrão

---

## 📈 Exemplos de Resultados

### Baixa Temporada
```
📊 RELATÓRIO DE SIMULAÇÃO
Cenário: Baixa Temporada (Mar-Jun): 1 visitante a cada 2 minutos
Tempo de simulação: 8.0 horas

👥 CLIENTES:
  • Chegaram: 245
  • Atendidos: 243
  • Ainda na fila: 2

⏱️  TEMPOS DE ESPERA:
  • Média: 156.3s (2.6 min)
  • Máximo: 420.1s (7.0 min)

📈 PERFORMANCE:
  • Taxa atendimento: 30.4 clientes/hora
  • Utilização sistema: 42.1%
```

### Alta Temporada
```
📊 RELATÓRIO DE SIMULAÇÃO
Cenário: Alta Temporada (Jan,Jul,Dez): 1 visitante a cada 30 segundos
Tempo de simulação: 8.0 horas

👥 CLIENTES:
  • Chegaram: 962
  • Atendidos: 578
  • Ainda na fila: 384

⏱️  TEMPOS DE ESPERA:
  • Média: 1847.2s (30.8 min)
  • Máximo: 5430.6s (90.5 min)

📈 PERFORMANCE:
  • Taxa atendimento: 72.3 clientes/hora
  • Utilização sistema: 98.7%
```

---

## 🧪 Validação e Testes

### Cenários de Teste

1. **Teste de sanidade**: Verificação básica do funcionamento
2. **Teste de cenários extremos**: Verificação de limites
3. **Teste de reprodutibilidade**: Seeds fixas para resultados consistentes
4. **Validação de métricas**: Comparação com cálculos teóricos

### Executar Testes

```bash
python -m pytest tests/
```

---

## 🔍 Interpretação dos Resultados

### Insights Principais

1. **Diferença significativa** entre cenários:
   - Alta temporada: ~28 minutos a mais de espera
   - Sistema próximo da saturação na alta temporada

2. **Gargalo identificado**: 
   - Capacidade limitada (20 pessoas/ciclo)
   - Ciclo fixo de 5 minutos

3. **Oportunidades de otimização**:
   - Implementar sistema de fila virtual
   - Considerar segundo trem para aumentar throughput
   - Otimizar tempo de embarque/desembarque

---

## 🤝 Contribuições

### Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Áreas para Melhoria

- [ ] Implementar interface gráfica (Tkinter/PyQt)
- [ ] Adicionar mais cenários (fins de semana, feriados)
- [ ] Implementar fila virtual/fast pass
- [ ] Adicionar análise de sensibilidade
- [ ] Exportar resultados para Excel/CSV
- [ ] Adicionar testes automatizados

---

## 📚 Referências

1. **Teoria das Filas**: Hillier, F. S., & Lieberman, G. J. (2015). *Introduction to Operations Research*
2. **SimPy Documentation**: https://simpy.readthedocs.io/
3. **Beto Carrero World**: https://www.betocarrero.com.br/
4. **Discrete Event Simulation**: Banks, J. et al. (2010). *Discrete-Event System Simulation*

---

## 📄 Licença

Este projeto é desenvolvido para fins acadêmicos. Todos os direitos sobre a FireWhip e Beto Carrero World pertencem aos seus respectivos proprietários.

---

## 📧 Contato

Para dúvidas sobre o projeto, entre em contato com qualquer membro da equipe através do ambiente acadêmico.

---

**🎢 Desenvolvido com ❤️ para a disciplina de Simulação e Avaliação de Software**