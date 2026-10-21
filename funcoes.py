import pandas as pd


def carregar_dados(caminho):
    """Lê o CSV preservando o arquivo original.

    Decisões:
    - dtype=str: todos os campos entram como texto e só viram número
      ou data quando eu converter de propósito (como o enunciado pede).
    - keep_default_na=False: célula vazia fica como "" e não vira NaN,
      assim eu mesma decido o que é vazio em cada campo.
    """
    df = pd.read_csv(
        caminho,
        sep=",",
        encoding="utf-8",
        dtype=str,
        keep_default_na=False,
    )
    return df


def mostrar_amostra(df, n=3):
    """Devolve os n primeiros registros para conferência."""
    return df.head(n)