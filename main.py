from funcoes import (
    carregar_dados,
    mostrar_amostra,
    tratar_categorias,
    tratar_canais,
    contar_correcoes,
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


if __name__ == "__main__":
    main()
    