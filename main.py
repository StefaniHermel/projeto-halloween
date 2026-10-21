from funcoes import (
    carregar_dados,
    mostrar_amostra,
    tratar_categorias,
    tratar_canais,
    contar_correcoes,
    validar_numeros,
    contar_problemas_numericos,
    separar_registros,
    investigar_entrega_sem_data,
    tratar_datas,
    contar_datas_invalidas,
    contar_por_canal,
    contar_por_ano_mes,
    contar_status_sem_entrega,
)

CAMINHO_CSV = "halloween_vendas.csv"


def main():
    df = carregar_dados(CAMINHO_CSV)

    print("=== SPRINT 1: INGESTÃO ===")
    print(f"Total de linhas lidas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    print("\nTrês primeiros registros:")
    print(mostrar_amostra(df, 3).to_string())

    print("\n=== SPRINT 2: TRANSFORMAÇÃO DE STRINGS ===")
    df = tratar_categorias(df)
    df = tratar_canais(df)

    print("\nValores de categoria ANTES:")
    print(sorted(df["categoria"].unique()))
    print("\nValores de categoria DEPOIS:")
    print(sorted(df["categoria_limpa"].unique()))

    print("\nExemplos de antes e depois (categoria):")
    mudou = df[df["categoria_vazia_preenchida"] | df["categoria_alterada"]]
    exemplos = mudou[["categoria", "categoria_limpa"]].drop_duplicates().head(10)
    print(exemplos.to_string(index=False))

    print("\nCanais ANTES:")
    print(sorted(df["canal_venda"].unique()))
    print("\nCanais DEPOIS:")
    print(df["canal_padrao"].value_counts().to_string())

    print("\nContagens de correções:")
    for nome, total in contar_correcoes(df).items():
        print(f"- {nome}: {total}")

    print("\n=== SPRINT 3: NULOS E VALIDAÇÃO ===")
    df = validar_numeros(df)

    print("\nTipos de problema em quantidade:")
    problemas_q = df[df["quantidade_problema"] != ""]["quantidade_problema"]
    print(problemas_q.value_counts().to_string())

    print("\nTipos de problema em preco_unitario:")
    problemas_p = df[df["preco_problema"] != ""]["preco_problema"]
    print(problemas_p.value_counts().to_string())

    print("\nContagens de problemas:")
    for nome, total in contar_problemas_numericos(df).items():
        print(f"- {nome}: {total}")

    validos, com_problema = separar_registros(df)
    print(f"\nPedidos válidos: {len(validos)}")
    print(f"Pedidos separados com problema: {len(com_problema)}")

    print("\nExemplos de pedidos com problema:")
    colunas = [
        "pedido_id", "quantidade", "preco_unitario",
        "quantidade_problema", "preco_problema",
    ]
    print(com_problema[colunas].head(5).to_string(index=False))

    print("\n=== SPRINT 4: REGRAS DE NEGÓCIO E DATAS ===")

    print("\nValores de status_pedido:")
    print(df["status_pedido"].value_counts().to_string())

    resultado = investigar_entrega_sem_data(df)
    print("\nHipótese: todo pedido sem data_entrega está Cancelado")
    print(f"- sem entrega e cancelados: {resultado['sem_entrega_e_cancelado']}")
    print(f"- sem entrega com outro status: {resultado['sem_entrega_outro_status']}")
    print(f"- total de cancelados na base: {resultado['total_cancelados']}")

    if resultado["hipotese_verdadeira"]:
        print("Conclusão: hipótese VERDADEIRA, não há contraexemplo.")
    else:
        print("Conclusão: hipótese FALSA, existe contraexemplo.")
        print("\nAté 3 exemplos de pedidos sem entrega e com outro status:")
        print(resultado["exemplos"].to_string(index=False))

    print("\nStatus dos pedidos sem data_entrega:")
    print(contar_status_sem_entrega(df).to_string())

    df = tratar_datas(df)
    print("\nExemplos de conversão de data_venda:")
    colunas_data = ["data_venda", "ano", "mes", "dia", "hora", "data_br"]
    print(df[colunas_data].head(5).to_string(index=False))

    print("\nDatas de venda com problema:")
    for nome, total in contar_datas_invalidas(df).items():
        print(f"- {nome}: {total}")

    contagem_canal, excluidos_canal = contar_por_canal(df)
    print("\nPedidos registrados por canal (todos os status):")
    print(contagem_canal.to_string())
    print(f"Excluídos por canal não reconhecido: {excluidos_canal}")

    contagem_periodo, excluidos_periodo = contar_por_ano_mes(df)
    print("\nPedidos registrados por ano-mês (todos os status):")
    print(contagem_periodo.to_string())
    print(f"Excluídos por data_venda inválida ou vazia: {excluidos_periodo}")


if __name__ == "__main__":
    main()
    