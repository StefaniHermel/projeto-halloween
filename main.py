from funcoes import (
    carregar_dados,
    mostrar_amostra,
    tratar_categorias,
    tratar_canais,
    contar_correcoes,
    validar_numeros,
    contar_problemas_numericos,
    separar_registros,
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


if __name__ == "__main__":
    main()

    