# **Inteligência Artificial - 02_2026**

# **Universidade Federal do Tocantins (UFT)**

**Professor:** Alexandre Tadeu Rossini da Silva

**Integrantes:**

* Maria Luiza Pinheiro Higashi
* Giordano Bruno de Moura Fragoso Santos

---

## **Atividade 1 - 02/09/2026**

## **Algoritmo Genético (AG) para resolver um problema prático**

---

# **1. Descrição do Problema**

O objetivo deste projeto é resolver um problema prático de **otimização combinatória e agendamento (*scheduling*)** utilizando um **Algoritmo Genético (AG)**.

A aplicação busca encontrar o **período ideal para o usuário tirar férias**, considerando períodos de:

* **6 dias**
* **10 dias**
* **30 dias**

O algoritmo analisa o calendário de **feriados municipais, estaduais e federais**, buscando maximizar o aproveitamento dos dias de férias.

A estratégia prioriza:

* **Feriados municipais e estaduais**, por proporcionarem maior potencial de aproveitamento em viagens para outros estados, onde esses dias podem ser úteis normalmente;
* **Feriados federais**;
* **Finais de semana**;
* **Sequências contínuas de dias de descanso**, buscando ampliar o período de folga obtido.

Dessa forma, o Algoritmo Genético procura encontrar uma combinação de dias de férias que maximize a quantidade e a qualidade dos períodos de descanso.

---

# **2. Divisão de Trabalho da Dupla**

| Integrante                                 | Módulos e Responsabilidades                                                                                                                                                        |
| :----------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maria Luiza Pinheiro Higashi**           | • Mapeamento do calendário e estrutura genética (**Módulo 1**).<br>• Formulação da Função de Avaliação (*Fitness*) e regras de pontuação (**Módulo 2**).                           |
| **Giordano Bruno de Moura Fragoso Santos** | • Operadores genéticos: Seleção por Roleta, Crossover de 1 ponto e Mutação (**Módulo 3**).<br>• Laço evolutivo principal e Estratégia de Substituição por Inclusão (**Módulo 4**). |

---

# **3. Modelagem da Solução Genética**

## **3.1 Codificação Genética**

A solução utiliza **codificação binária**, em que cada gene representa um dia do ano:

| Valor | Significado               |
| :---: | :------------------------ |
|  `0`  | Dia normal                |
|  `1`  | Dia escolhido para férias |

Cada indivíduo da população é representado por um **cromossomo contendo 365 genes**, correspondentes aos dias de um ano civil.

### **Exemplo**

```text
[0, 0, 1, 1, 1, 0, 0, ...]
```

Nesse exemplo, os valores `1` representam os dias selecionados para férias.

> **Observação:** para anos bissextos, a representação deverá considerar os 366 dias do ano.

---

## **3.2 Função de Avaliação (*Fitness*)**

A função de avaliação determina a qualidade de cada cromossomo.

São atribuídas pontuações diferentes de acordo com o tipo de dia selecionado:

| Tipo de dia                |           Pontuação |
| :------------------------- | ------------------: |
| Feriado municipal/estadual |            **+3,0** |
| Feriado federal            |            **+1,5** |
| Final de semana            |            **+1,0** |
| Sequências contínuas       | **Bônus adicional** |

O algoritmo também verifica se o cromossomo possui **exatamente a quantidade de dias de férias estipulada**.

Caso a quantidade de dias seja diferente da solicitada, o indivíduo recebe:

```text
fitness = 0
```

Dessa forma, somente soluções que respeitam a quantidade de dias definida podem apresentar uma boa aptidão.

---

# **4. Operadores Genéticos**

## **4.1 Seleção por Roleta**

A seleção dos indivíduos será realizada por meio da **amostragem estocástica por roleta**.

Nesse método, indivíduos com maior *fitness* possuem maior probabilidade de serem selecionados para reprodução.

A probabilidade de seleção é determinada proporcionalmente à aptidão de cada indivíduo:

```text
P(indivíduo) = fitness(indivíduo) / fitness_total
```

---

## **4.2 Crossover de Um Ponto**

O cruzamento utilizado será o **crossover de um ponto**.

O operador possui uma **taxa de cruzamento de 65%**.

Um ponto de corte é escolhido aleatoriamente no cromossomo e os segmentos dos pais são combinados para gerar os descendentes.

### **Exemplo simplificado**

```text
Pai 1:  00000 | 11111
Pai 2:  11111 | 00000

Filho 1: 00000 | 00000
Filho 2: 11111 | 11111
```

---

## **4.3 Mutação**

A mutação consiste na **inversão aleatória de um bit** do cromossomo.

A taxa de mutação definida é de **1%**.

### **Exemplo**

```text
Antes:  0 0 1 0 1
Depois: 0 1 1 0 1
          ↑
       bit mutado
```

A mutação contribui para manter a diversidade genética da população e permite explorar novas possibilidades de solução.

---

# **5. Estratégia de Substituição**

Será utilizada a estratégia de **substituição por inclusão** (*elitist replacement*).

Nesse processo:

1. Os indivíduos da população atual são combinados com os descendentes gerados;
2. Todos os indivíduos são avaliados;
3. Os indivíduos são ordenados de acordo com o *fitness*;
4. Os **N indivíduos mais aptos** são mantidos para formar a próxima geração.

Considerando uma população de tamanho `N = 100`:

```text
Pais + Descendentes
        ↓
    Avaliação
        ↓
 Ordenação por Fitness
        ↓
  Seleção dos 100
    mais aptos
        ↓
 Próxima geração
```

---

# **6. Parâmetros Genéticos**

Os principais parâmetros utilizados no algoritmo são:

| Parâmetro             |               Valor |
| :-------------------- | ------------------: |
| Tamanho da população  |  **100 indivíduos** |
| Tamanho do cromossomo |       **365 genes** |
| Seleção               |          **Roleta** |
| Crossover             |         **1 ponto** |
| Taxa de crossover     |             **65%** |
| Mutação               | **Inversão de bit** |
| Taxa de mutação       |              **1%** |
| Substituição          |    **Por inclusão** |
| Geração inicial       |           **t = 0** |
| Condição de parada    |    **200 gerações** |

---

# **7. Como Executar o Código**

## **Pré-requisitos**

Para executar o projeto, é necessário possuir:

* **Python 3.8 ou superior**
* **Git**

### **Verificar a versão do Python**

```bash
python --version
```

---

## **Clonar o Repositório**

```bash
git clone https://github.com/usuario/otimizador-ferias-ag.git
```

Entrar na pasta do projeto:

```bash
cd otimizador-ferias-ag
```

---

## **Executar o Algoritmo**

```bash
python main.py
```

---

# **8. Estrutura do Projeto**

Uma possível organização dos arquivos é:

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

A estrutura pode ser adaptada conforme a implementação final do projeto.

---

# **9. Testes**

Serão realizados testes simulados para verificar o funcionamento do algoritmo, observando principalmente:

* Quantidade correta de dias selecionados;
* Identificação dos feriados;
* Identificação dos finais de semana;
* Cálculo correto do *fitness*;
* Funcionamento da seleção por roleta;
* Funcionamento do crossover;
* Funcionamento da mutação;
* Evolução da população ao longo das gerações;
* Soluções encontradas ao final das 200 gerações.

---

# **10. Resumo da Solução**

O projeto utiliza um **Algoritmo Genético** para buscar períodos de férias que maximizem o aproveitamento dos dias de descanso.

A solução é representada por cromossomos binários de 365 genes, nos quais cada gene representa a escolha ou não de um determinado dia para férias.

O processo evolutivo utiliza:

* **População de 100 indivíduos**;
* **Seleção por roleta**;
* **Crossover de um ponto com taxa de 65%**;
* **Mutação de bits com taxa de 1%**;
* **Substituição por inclusão**;
* **Limite de 200 gerações**.

A função de *fitness* considera feriados municipais e estaduais, feriados federais, finais de semana e sequências contínuas de dias de descanso, buscando encontrar uma configuração de férias com maior aproveitamento.
