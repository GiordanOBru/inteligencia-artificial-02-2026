# Otimizador de Férias com Algoritmo Genético (AG)

Projeto da disciplina de Inteligência Artificial / Computação Evolutiva — Universidade Federal do Tocantins (UFT).

**Professor:** Alexandre Tadeu Rossini da Silva

**Integrantes:**
- Maria Luiza Pinheiro Higashi
- Giordano Bruno de Moura Fragoso Santos

## Descrição

Aplicação de um **Algoritmo Genético** para resolver um problema de otimização combinatória e agendamento: encontrar o **melhor período de férias** (6, 10 ou 30 dias) dentro do calendário, maximizando o aproveitamento de:

- Feriados municipais e estaduais (maior prioridade — bom potencial para viagens)
- Feriados federais
- Finais de semana
- Sequências contínuas de dias de descanso

## Modelagem

- **Codificação:** cromossomo binário de 365 genes (366 em ano bissexto), um por dia do ano. `0` = dia normal, `1` = dia escolhido para férias.
- **Fitness:** soma pontos por tipo de dia selecionado (feriado municipal/estadual = +3,0; federal = +1,5; fim de semana = +1,0; bônus por sequências contínuas). Se a quantidade de dias de férias não for exatamente a solicitada, fitness = 0.

## Operadores Genéticos

| Operador | Método | Parâmetro |
|---|---|---|
| Seleção | Roleta (proporcional ao fitness) | — |
| Crossover | 1 ponto | Taxa de 65% |
| Mutação | Inversão de bit | Taxa de 1% |
| Substituição | Por inclusão (elitista) | Mantém os N mais aptos |

## Parâmetros do AG

| Parâmetro | Valor |
|---|---|
| Tamanho da população | 100 indivíduos |
| Tamanho do cromossomo | 365 genes |
| Condição de parada | 200 gerações |

## Pré-requisitos

- Python 3.8 ou superior
- Git

```bash
python --version
```

## Como executar

```bash
git clone https://github.com/usuario/otimizador-ferias-ag.git
cd otimizador-ferias-ag
python main.py
```

## Estrutura do projeto

```text
otimizador-ferias-ag/
│
├── main.py
├── calendario.py
├── genetico.py
├── fitness.py
├── operadores.py
├── README.md
└── requirements.txt
```

## Testes

O projeto é validado verificando:

- Quantidade correta de dias selecionados
- Identificação de feriados e finais de semana
- Cálculo correto do fitness
- Funcionamento da seleção, crossover e mutação
- Evolução da população ao longo das gerações
- Qualidade da solução final após 200 gerações

## Divisão de trabalho

| Integrante | Responsabilidades |
|---|---|
| Maria Luiza Pinheiro Higashi | Mapeamento do calendário e estrutura genética; Função de Fitness e regras de pontuação |
| Giordano Bruno de Moura Fragoso Santos | Operadores genéticos: seleção, crossover e mutação ; laço evolutivo principal e substituição por inclusão |