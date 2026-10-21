from funcoes import carregar_dados, mostrar_amostra

CAMINHO_CSV = "halloween_vendas.csv"


def main():
    df = carregar_dados(CAMINHO_CSV)

    print("=== SPRINT 1: INGESTÃO ===")
    print(f"Total de linhas lidas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    print("\nTrês primeiros registros:")
    print(mostrar_amostra(df, 3).to_string())


if __name__ == "__main__":
    main()
    