# Relatório e insights: Festa em Cena (Halloween)

## Resumo

Analisei 1.500 pedidos fictícios da Festa em Cena (agosto a novembro de 2024 e 2025) com Python e Pandas. Cada linha é um pedido de um único produto, que pode ter várias unidades. Os números abaixo contam pedidos registrados, não receita nem vendas concluídas.

## Qualidade dos dados

- **Categoria:** 18 estavam vazias e viraram "sem categoria". Outras 1.482 mudaram de escrita, e em 55 o re.sub removeu pontuação ou espaços sobrando, como "FANTASIA!!!".
- **Canal:** todos os 1.500 pedidos foram padronizados para Mercado, Loja física ou Web, sem nenhum canal não reconhecido.
- **Números:** 19 pedidos (1,27%) têm problema, sendo 7 com quantidade menor ou igual a zero e 12 com preço ausente. Nenhum valor foi inventado: os registros foram marcados e separados.
- **Datas:** 4 datas de venda são inválidas e ficaram fora da contagem por período.

## Entrega sem data

A hipótese de que todo pedido sem data de entrega está cancelado é falsa. Dos 143 pedidos sem entrega, 109 são cancelados e 34 são concluídos. Esses 34 são contraexemplos e sugerem falha de registro. Nenhum status ou data foi alterado.

## Descobertas

**Por canal:** a Web lidera com 666 pedidos (44,4%), seguida da Loja física com 551 (36,7%) e do Mercado com 283 (18,9%). Limitação: entram todos os status, inclusive cancelados e devolvidos.

**Por período:** outubro concentra 393 pedidos em 2024 e 410 em 2025, mais de metade de cada ano, o que combina com o Halloween em 31 de outubro. Limitação: são 748 pedidos válidos em cada ano e 4 foram excluídos por data inválida.

## Lição sobre Machine Learning

Limpar os dados é necessário, mas não basta para evitar overfitting ou underfitting. Também importam a representatividade da base, a escolha do modelo e a avaliação. Como esta base é fictícia, as conclusões não valem para o mercado real.

