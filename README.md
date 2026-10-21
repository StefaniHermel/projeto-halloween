# Mini-Projeto Avaliativo: Festa em Cena (Halloween)

Projeto do curso de Machine Learning e Visão Computacional (Turma 05, Módulo 1, Semana 07).

## Descrição do projeto

### O problema

A Festa em Cena é uma rede **fictícia** que vende fantasias e acessórios de Halloween por três canais: **Mercado** (caixas de supermercados parceiros), **Loja física** (lojas próprias) e **Web** (pedidos pelo site). A empresa precisa organizar seus registros e entender como os pedidos variam por canal e período. A base tem problemas intencionais: categorias vazias, pontuação indevida, canais escritos de formas diferentes, quantidades inválidas, preços ausentes e datas inválidas.

### Objetivo do programa

Ler o arquivo `halloween_vendas.csv` com Pandas, validar e padronizar os dados, investigar a regra de entrega sem data e gerar um relatório simples com contagens de pedidos por canal e por ano-mês.

### O que significa uma linha

Cada linha é **um pedido de um único produto**, que pode conter várias unidades. Portanto, a contagem de linhas é uma contagem de **pedidos**, e não de unidades vendidas.

### Quatro colunas

| Coluna | Significado |
|---|---|
| `categoria` | Tipo do produto (fantasia ou acessório). Pode vir vazia ou com pontuação |
| `canal_venda` | Canal do pedido: Mercado, Loja física ou Web, escrito de várias formas |
| `quantidade` | Unidades do produto no pedido (deve ser inteiro maior que zero) |
| `data_venda` | Data e hora do pedido, no formato `2025-10-12 14:35:00` |

### Regras adotadas

**Textos**
- `categoria`: `.strip()`, `.lower()` e `re.sub()` para remover tudo que não é letra ou espaço. Se ficar vazia, vira `sem categoria`.
- `canal_venda`: padronizado para Mercado, Loja física e Web por um dicionário. Canal desconhecido seria marcado como `nao reconhecido`, sem adivinhar.

**Valores**
- `quantidade`: precisa ser inteiro maior que zero.
- `preco_unitario`: precisa estar preenchido e não ser negativo (preço 0 é aceito).
- Registros com problema são **marcados e separados**, sem inventar valores. Preço ausente não vira zero nem média.

**Datas**
- `data_venda` é convertida com `datetime.strptime()`. O texto original é preservado, e são extraídos ano, mês, dia e hora, além da data brasileira com `strftime()`.
- Data vazia ou inválida é marcada e o processamento continua. Nunca é substituída pela data de hoje.

Custos e descontos existem no CSV, mas não foram usados.

## Guia de execução

### Arquivos necessários

- `main.py`: executa a análise e imprime os resultados
- `funcoes.py`: funções de leitura, limpeza, validação e contagem
- `halloween_vendas.csv`: base de dados (na mesma pasta dos scripts)

### Como executar

1. Instale o Python 3 e o pandas: `pip install pandas`
2. Coloque `halloween_vendas.csv` na mesma pasta de `main.py` e `funcoes.py`.
3. Abra o terminal nessa pasta e rode: `python main.py` (no Windows, também funciona `py main.py`).

O arquivo original **não é alterado**. Os campos são lidos como texto (`dtype=str`, vírgula como separador e `encoding="utf-8"`) e convertidos só quando necessário.

## Resultados

| Verificação | Resultado |
|---|---|
| Linhas lidas | 1.500 |
| Categorias vazias preenchidas | 18 |
| Categorias não vazias alteradas | 1.482 (55 com pontuação ou espaços removidos pelo `re.sub`) |
| Canais não reconhecidos | 0 |
| Quantidade com problema | 7 (todas menores ou iguais a zero) |
| Preço com problema | 12 (todos ausentes) |
| Pedidos afetados, sem somar duas vezes | 19 (nenhum com problema nos dois campos) |
| Datas de venda inválidas | 4 |
| Pedidos cancelados | 109 |

### Conclusão sobre entrega sem data

A hipótese "todo pedido sem `data_entrega` está Cancelado" é **falsa nesta base**. Dos 143 pedidos sem entrega, 109 (76,2%) são cancelados e 34 (23,8%) são concluídos. Todos os cancelados estão sem entrega, mas existem 34 contraexemplos. Isso sugere falha de registro ou inconsistência entre status e data, cuja causa a base não permite saber. Nenhum status foi alterado e nenhuma data foi inventada.

### Descoberta 1: pedidos por canal

- **Evidência:** Web 666 (44,4%), Loja física 551 (36,7%), Mercado 283 (18,9%). Nenhum pedido foi excluído.
- **Interpretação:** o site é o canal com mais pedidos registrados.
- **Limitação:** a contagem inclui todos os status (concluídos, cancelados e devolvidos). Não representa receita, unidades vendidas nem vendas concluídas.

### Descoberta 2: pedidos por ano-mês

| Ano-mês | Pedidos | Ano-mês | Pedidos |
|---|---|---|---|
| 2024-08 | 77 | 2025-08 | 62 |
| 2024-09 | 104 | 2025-09 | 94 |
| 2024-10 | 393 | 2025-10 | 410 |
| 2024-11 | 174 | 2025-11 | 182 |

- **Evidência:** outubro tem 393 pedidos em 2024 (52,5% do ano) e 410 em 2025 (54,8%).
- **Interpretação:** os pedidos se concentram em outubro, mês do Halloween (31/10), nos dois anos.
- **Limitação:** 4 pedidos foram excluídos por data inválida. A contagem é por ano-mês, para não misturar 2024 e 2025, e inclui todos os status. A base é fictícia e não vale para o mercado real.

## Reflexão: Machine Learning e qualidade de dados

A qualidade dos dados influencia diretamente os resultados de análises e modelos de Machine Learning. Um modelo treinado com categorias escritas de formas diferentes, preços ausentes ou datas inválidas aprende com ruído e pode produzir conclusões erradas. Por isso, antes de qualquer modelo, é preciso verificar informações ausentes, textos inconsistentes e datas inválidas, sem inventar valores.

Limpar os dados, porém, **não garante sozinho evitar overfitting ou underfitting**. Overfitting acontece quando o modelo decora os dados de treino e falha com dados novos. Underfitting acontece quando ele é simples demais para captar o padrão. Para evitá-los também importam a **representatividade** da base (esta cobre só agosto a novembro de dois anos e é fictícia), a **escolha do modelo** e a **avaliação** com dados que o modelo não viu.

## Organização do versionamento

| Branch | Objetivo |
|---|---|
| `sprint-1-ingestao` | Ler o CSV com Pandas, conferir linhas e mostrar três registros |
| `sprint-2-strings` | Limpar categoria (strip, lower, re.sub) e padronizar canais |
| `sprint-3-validacao` | Validar quantidade e preço, marcar e separar problemas |
| `sprint-4-regras-datas` | Hipótese da entrega sem data, datas com datetime e contagens por canal e ano-mês |
| `sprint-5-documentacao` | README.md e report.md |