# 🎃 Relatório e insights: Festa em Cena (Halloween)

Analisei 1.500 pedidos fictícios de agosto a novembro de 2024 e 2025. Antes de interpretar, tratei a qualidade dos dados: 18 categorias vazias viraram "sem categoria", 55 categorias perderam pontuação indevida, 45 canais foram padronizados e 19 pedidos ficaram marcados por quantidade inválida (7, todas com -1) ou preço ausente (12). Também encontrei 4 datas de venda inválidas, que foram excluídas das contagens por período, sem inventar valores.

**🚚 Entrega sem data.** Dos 143 pedidos sem data de entrega, 109 são cancelados, mas 34 estão como Concluído. Logo, a ideia de que todo pedido sem entrega é cancelado é falsa nesta base. Isso sugere falha de registro ou entregas não informadas, e vale investigar antes de usar o status em qualquer modelo.

**🌐 Canal.** A Web lidera com 666 pedidos (44,4%), seguida pela Loja física, com 551 (36,7%), e pelo Mercado, com 283 (18,9%). O site é o principal canal de entrada de pedidos. Como a contagem inclui cancelados e devolvidos, ela mostra pedidos registrados, não receita.

**📅 Período.** Outubro concentra os pedidos: 393 em 2024 e 410 em 2025, cerca de 52,5% e 54,8% dos 748 pedidos com data válida de cada ano. O pico no mês do Halloween se repete e cresce um pouco de um ano para o outro. Agrupei por ano-mês para não misturar 2024 com 2025.

**⚠️ Limitações.** A base é fictícia e não representa o mercado real. As contagens são de pedidos, não de unidades, e cada pedido pode ter várias unidades. Datas inválidas reduzem a amostra por período.

**🤖 Lição para Machine Learning.** Limpar os dados melhora a base, mas não garante um bom modelo: ainda é preciso verificar se a base é representativa, escolher bem o modelo e avaliar com dados novos para evitar overfitting e underfitting.

