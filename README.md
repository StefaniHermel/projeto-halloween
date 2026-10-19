# 🎃 projeto-halloween

Mini-projeto avaliativo de Machine Learning e Visão Computacional (Módulo 1): análise exploratória e limpeza de dados de vendas da **Festa em Cena** 👻

## 📋 Descrição do projeto

A Festa em Cena é uma rede fictícia que vende fantasias e acessórios de Halloween pelos canais **Mercado** 🛒, **Loja física** 🏬 e **Web** 🌐. A base `halloween_vendas.csv` tem problemas intencionais (categorias vazias, pontuação indevida, canais escritos de formas diferentes, quantidades inválidas, preços ausentes e datas inválidas).

🎯 O objetivo do programa (`main.py`) é ler o CSV com Pandas, validar e padronizar os dados e gerar um relatório simples antes de comparar os períodos de venda. O arquivo original nunca é alterado: o tratamento cria colunas novas no DataFrame.

### 🔎 Significado dos dados

- 🧾 **Uma linha:** um pedido de um único produto, que pode ter várias unidades.
- 🔢 `pedido_id`: número que identifica o pedido.
- 📅 `data_venda`: data e hora do pedido (horário local de São Paulo).
- 🏪 `canal_venda`: onde o pedido foi feito (Mercado, Loja física ou Web).
- 📦 `status_pedido`: situação do pedido (Concluído, Cancelado ou Devolvido).

### ⚙️ Regras adotadas

- 🔤 **Textos:** categoria passa por `.strip()`, `.lower()` e `re.sub()` para remover pontuação (ex.: `FANTASIA!!!` vira `fantasia`). Categoria vazia vira `sem categoria`. O canal é padronizado para Mercado, Loja física ou Web; textos não reconhecidos ficam fora das contagens por canal, sem inventar valor.
- 💰 **Valores:** `quantidade` é válida se for inteiro maior que zero; `preco_unitario` é válido se estiver preenchido e não for negativo. Registros com problema são apenas **marcados**, sem corrigir nem inventar valores. Isso evita distorcer a análise com dados que não existem.
- 🕒 **Datas:** `data_venda` é convertida com `datetime.strptime()`. Datas vazias ou inválidas são marcadas e o programa continua, sem trocar pela data de hoje. A apresentação brasileira usa `strftime()` (ex.: `12/10/2025`).

## 🚀 Guia de execução

1. 🐍 Instale o Python e o Pandas (`py -m pip install pandas`).
2. 📁 Deixe `main.py` e `halloween_vendas.csv` na mesma pasta.
3. ▶️ Execute no terminal: `py main.py` (ou `python main.py`).

📌 Arquivos necessários: `main.py` e `halloween_vendas.csv`.

## 📊 Resultados

| Verificação | Resultado |
| --- | --- |
| 📄 Linhas lidas | 1.500 |
| 🏷️ Categorias vazias preenchidas | 18 |
| ✏️ Categorias não vazias alteradas | 1.482 (55 com pontuação removida) |
| ❌ Quantidade inválida | 7 (todas com valor -1) |
| 💸 Preço unitário ausente | 12 |
| ⚠️ Pedidos com problema numérico (sem sobreposição) | 19 |
| 📆 Datas de venda inválidas | 4 |
| 🚫 Pedidos cancelados | 109 |

### 🚚 Conclusão sobre entrega sem data

Há 143 pedidos sem `data_entrega`: 109 são Cancelados e 34 têm status **Concluído**. Portanto, a hipótese de que todo pedido sem entrega é cancelado é **falsa nesta base** ❗ Não alteramos o status nem inventamos datas.

### 💡 Descoberta 1: canal

- 📈 **Evidência:** Web 666 pedidos (44,4%), Loja física 551 (36,7%) e Mercado 283 (18,9%), sem registros excluídos.
- 🧠 **Interpretação:** o site concentra a maior parte dos pedidos registrados.
- ⚠️ **Limitação:** são pedidos, não receita; incluem cancelados e devolvidos. A base é fictícia e não representa o mercado real.

### 💡 Descoberta 2: período

- 📈 **Evidência:** outubro teve 393 pedidos em 2024 e 410 em 2025, cerca de 52,5% e 54,8% dos 748 pedidos com data válida em cada ano.
- 🧠 **Interpretação:** as vendas se concentram no mês do Halloween 🎃, e o padrão se repete nos dois anos.
- ⚠️ **Limitação:** 4 registros foram excluídos por data inválida; a contagem é de pedidos registrados, não de vendas concluídas.

## 🤖 Reflexão: qualidade de dados e Machine Learning

Dados com nulos, textos inconsistentes e datas inválidas prejudicam análises e modelos: o mesmo canal escrito de três formas viraria três categorias diferentes. Limpar os dados é necessário, mas **não basta** para evitar overfitting (o modelo decora os dados de treino) ou underfitting (o modelo é simples demais para aprender o padrão). Para isso também importam a representatividade da base, a escolha do modelo e a avaliação com dados que ele não viu no treino.

# 🎃 projeto-halloween

Mini-projeto avaliativo de Machine Learning e Visão Computacional (Módulo 1): análise exploratória e limpeza de dados de vendas da **Festa em Cena** 👻

## 📋 Descrição do projeto

A Festa em Cena é uma rede fictícia que vende fantasias e acessórios de Halloween pelos canais **Mercado** 🛒, **Loja física** 🏬 e **Web** 🌐. A base `halloween_vendas.csv` tem problemas intencionais (categorias vazias, pontuação indevida, canais escritos de formas diferentes, quantidades inválidas, preços ausentes e datas inválidas).

🎯 O objetivo do programa (`main.py`) é ler o CSV com Pandas, validar e padronizar os dados e gerar um relatório simples antes de comparar os períodos de venda. O arquivo original nunca é alterado: o tratamento cria colunas novas no DataFrame.

### 🔎 Significado dos dados

- 🧾 **Uma linha:** um pedido de um único produto, que pode ter várias unidades.
- 🔢 `pedido_id`: número que identifica o pedido.
- 📅 `data_venda`: data e hora do pedido (horário local de São Paulo).
- 🏪 `canal_venda`: onde o pedido foi feito (Mercado, Loja física ou Web).
- 📦 `status_pedido`: situação do pedido (Concluído, Cancelado ou Devolvido).

### ⚙️ Regras adotadas

- 🔤 **Textos:** categoria passa por `.strip()`, `.lower()` e `re.sub()` para remover pontuação (ex.: `FANTASIA!!!` vira `fantasia`). Categoria vazia vira `sem categoria`. O canal é padronizado para Mercado, Loja física ou Web; textos não reconhecidos ficam fora das contagens por canal, sem inventar valor.
- 💰 **Valores:** `quantidade` é válida se for inteiro maior que zero; `preco_unitario` é válido se estiver preenchido e não for negativo. Registros com problema são apenas **marcados**, sem corrigir nem inventar valores. Isso evita distorcer a análise com dados que não existem.
- 🕒 **Datas:** `data_venda` é convertida com `datetime.strptime()`. Datas vazias ou inválidas são marcadas e o programa continua, sem trocar pela data de hoje. A apresentação brasileira usa `strftime()` (ex.: `12/10/2025`).

## 🚀 Guia de execução

1. 🐍 Instale o Python e o Pandas (`py -m pip install pandas`).
2. 📁 Deixe `main.py` e `halloween_vendas.csv` na mesma pasta.
3. ▶️ Execute no terminal: `py main.py` (ou `python main.py`).

📌 Arquivos necessários: `main.py` e `halloween_vendas.csv`.

## 📊 Resultados

| Verificação | Resultado |
| --- | --- |
| 📄 Linhas lidas | 1.500 |
| 🏷️ Categorias vazias preenchidas | 18 |
| ✏️ Categorias não vazias alteradas | 1.482 (55 com pontuação removida) |
| ❌ Quantidade inválida | 7 (todas com valor -1) |
| 💸 Preço unitário ausente | 12 |
| ⚠️ Pedidos com problema numérico (sem sobreposição) | 19 |
| 📆 Datas de venda inválidas | 4 |
| 🚫 Pedidos cancelados | 109 |

### 🚚 Conclusão sobre entrega sem data

Há 143 pedidos sem `data_entrega`: 109 são Cancelados e 34 têm status **Concluído**. Portanto, a hipótese de que todo pedido sem entrega é cancelado é **falsa nesta base** ❗ Não alteramos o status nem inventamos datas.

### 💡 Descoberta 1: canal

- 📈 **Evidência:** Web 666 pedidos (44,4%), Loja física 551 (36,7%) e Mercado 283 (18,9%), sem registros excluídos.
- 🧠 **Interpretação:** o site concentra a maior parte dos pedidos registrados.
- ⚠️ **Limitação:** são pedidos, não receita; incluem cancelados e devolvidos. A base é fictícia e não representa o mercado real.

### 💡 Descoberta 2: período

- 📈 **Evidência:** outubro teve 393 pedidos em 2024 e 410 em 2025, cerca de 52,5% e 54,8% dos 748 pedidos com data válida em cada ano.
- 🧠 **Interpretação:** as vendas se concentram no mês do Halloween 🎃, e o padrão se repete nos dois anos.
- ⚠️ **Limitação:** 4 registros foram excluídos por data inválida; a contagem é de pedidos registrados, não de vendas concluídas.

## 🤖 Reflexão: qualidade de dados e Machine Learning

Dados com nulos, textos inconsistentes e datas inválidas prejudicam análises e modelos: o mesmo canal escrito de três formas viraria três categorias diferentes. Limpar os dados é necessário, mas **não basta** para evitar overfitting (o modelo decora os dados de treino) ou underfitting (o modelo é simples demais para aprender o padrão). Para isso também importam a representatividade da base, a escolha do modelo e a avaliação com dados que ele não viu no treino.
