"""
Mini-Projeto Avaliativo - Módulo 1 - Festa em Cena (Halloween)

Lê halloween_vendas.csv com Pandas, valida e padroniza os dados e imprime
um relatório de status. O arquivo original NUNCA é alterado: todo o
tratamento acontece em colunas novas do DataFrame.

Como executar:
    1. Coloque halloween_vendas.csv na mesma pasta deste arquivo.
    2. Instale o Pandas (pip install pandas).
    3. Rode: python main.py
"""

import re
from datetime import datetime

import pandas as pd

ARQUIVO_CSV = "halloween_vendas.csv"
FORMATO_DATA = "%Y-%m-%d %H:%M:%S"

# Dicionário que liga o texto limpo (minúsculo, sem espaços nas pontas)
# ao nome oficial do canal.
CANAIS_VALIDOS = {
    "mercado": "Mercado",
    "loja física": "Loja física",
    "web": "Web",
}


# ----------------------------------------------------------------------
# 1. Leitura
# ----------------------------------------------------------------------
def carregar_dados(caminho):
    """Lê o CSV com Pandas. Tudo entra como texto (dtype=str) para que a
    conversão para número/data seja feita de forma controlada por nós.
    keep_default_na=False mantém células vazias como '' (sem virar NaN)."""
    return pd.read_csv(
        caminho, sep=",", encoding="utf-8", dtype=str, keep_default_na=False
    )


# ----------------------------------------------------------------------
# 2. Strings e Regex
# ----------------------------------------------------------------------
def padronizar_categoria(valor):
    """Limpa uma categoria. Retorna (texto_final, estava_vazia).

    Passos: strip + lower, depois re.sub para tirar tudo que não for
    letra ou espaço (as categorias deste CSV não têm acento, então
    a-z basta). Espaços repetidos viram um só. Se sobrar nada, o
    registro vira 'sem categoria'."""
    estava_vazia = valor.strip() == ""
    texto = valor.strip().lower()
    texto = re.sub(r"[^a-z\s]", "", texto)  # remove pontuações indevidas
    texto = re.sub(r"\s+", " ", texto).strip()  # junta espaços repetidos
    if texto == "":
        texto = "sem categoria"
    return texto, estava_vazia


def padronizar_canal(valor):
    """Retorna o canal oficial (Mercado, Loja física, Web) ou None se o
    texto não for reconhecido (não inventamos um canal)."""
    return CANAIS_VALIDOS.get(valor.strip().lower())


# ----------------------------------------------------------------------
# 3. Validação numérica
# ----------------------------------------------------------------------
def quantidade_valida(valor):
    """Quantidade válida = número inteiro maior que zero."""
    texto = valor.strip()
    return bool(re.fullmatch(r"\d+", texto)) and int(texto) > 0


def preco_valido(valor):
    """Preço válido = preenchido, numérico e não negativo.
    Zero é aceito (só negativo e vazio são problemas)."""
    texto = valor.strip()
    if texto == "":
        return False
    try:
        return float(texto) >= 0
    except ValueError:
        return False


# ----------------------------------------------------------------------
# 4. Datas
# ----------------------------------------------------------------------
def converter_data(valor):
    """Converte 'AAAA-MM-DD HH:MM:SS' com strptime. Se estiver vazia ou
    inválida (ex.: 2025-02-30), devolve None em vez de parar o programa e
    sem trocar por outra data."""
    try:
        return datetime.strptime(valor.strip(), FORMATO_DATA)
    except ValueError:
        return None


def formatar_data_br(data):
    """Apresentação brasileira, ex.: 12/10/2025. None continua None."""
    return data.strftime("%d/%m/%Y") if data else None


# ----------------------------------------------------------------------
# 5. Tratamento geral (cria colunas novas, preserva as originais)
# ----------------------------------------------------------------------
def tratar_dataframe(df):
    """Aplica as regras e devolve o DataFrame com colunas de apoio."""
    df = df.copy()

    # Categoria
    resultado = df["categoria"].apply(padronizar_categoria)
    df["categoria_limpa"] = resultado.apply(lambda r: r[0])
    df["categoria_estava_vazia"] = resultado.apply(lambda r: r[1])

    # Canal (None = não reconhecido)
    df["canal_padrao"] = df["canal_venda"].apply(padronizar_canal)

    # Problemas numéricos: só MARCAMOS, não corrigimos nem inventamos valor
    df["qtd_invalida"] = ~df["quantidade"].apply(quantidade_valida)
    df["preco_invalido"] = ~df["preco_unitario"].apply(preco_valido)
    df["problema_numerico"] = df["qtd_invalida"] | df["preco_invalido"]

    # Datas
    # dtype=object evita que o Pandas troque None por NaT (que não tem strftime)
    datas = pd.Series(
        [converter_data(v) for v in df["data_venda"]], index=df.index, dtype=object
    )
    df["data_valida"] = datas.notna()
    df["ano"] = datas.apply(lambda d: d.year if d else None)
    df["mes"] = datas.apply(lambda d: d.month if d else None)
    df["dia"] = datas.apply(lambda d: d.day if d else None)
    df["hora"] = datas.apply(lambda d: d.hour if d else None)
    df["data_br"] = datas.apply(formatar_data_br)
    df["ano_mes"] = datas.apply(lambda d: d.strftime("%Y-%m") if d else None)

    # Entrega
    df["sem_entrega"] = df["data_entrega"].str.strip() == ""
    return df


# ----------------------------------------------------------------------
# 6. Análises
# ----------------------------------------------------------------------
def investigar_entrega(df):
    """Hipótese: todo pedido sem data_entrega tem status Cancelado.
    Retorna (sem_entrega_cancelado, sem_entrega_outros, exemplos)."""
    sem_entrega = df[df["sem_entrega"]]
    cancelados = sem_entrega[sem_entrega["status_pedido"] == "Cancelado"]
    outros = sem_entrega[sem_entrega["status_pedido"] != "Cancelado"]
    exemplos = outros.head(3)[["pedido_id", "status_pedido", "data_venda"]]
    return len(cancelados), len(outros), exemplos


def contar_por_canal(df):
    """Pedidos por canal reconhecido (todos os status incluídos).
    Retorna (contagem, quantidade_excluida)."""
    reconhecidos = df[df["canal_padrao"].notna()]
    contagem = reconhecidos["canal_padrao"].value_counts()
    return contagem, len(df) - len(reconhecidos)


def contar_por_ano_mes(df):
    """Pedidos por ano-mês, só com data_venda válida (todos os status).
    Agrupar só por mês misturaria 2024 e 2025."""
    validos = df[df["data_valida"]]
    contagem = validos["ano_mes"].value_counts().sort_index()
    return contagem, len(df) - len(validos)


# ----------------------------------------------------------------------
# 7. Relatório
# ----------------------------------------------------------------------
def exibir_relatorio(df):
    total = len(df)
    print("=" * 60)
    print("RELATÓRIO - FESTA EM CENA (HALLOWEEN)")
    print("=" * 60)
    print(f"Total de linhas lidas: {total}")
    print("\nTrês primeiros registros (originais):")
    print(df[["pedido_id", "data_venda", "categoria", "canal_venda"]].head(3))

    # Categorias
    vazias = int(df["categoria_estava_vazia"].sum())
    nao_vazias = df[~df["categoria_estava_vazia"]]
    alteradas = int((nao_vazias["categoria"] != nao_vazias["categoria_limpa"]).sum())
    com_pontuacao = int(
        nao_vazias["categoria"].apply(lambda c: bool(re.search(r"[^A-Za-z\s]", c))).sum()
    )
    print("\n--- Categorias ---")
    print(f"Vazias preenchidas com 'sem categoria': {vazias}")
    print(f"Não vazias alteradas (espaços, caixa ou pontuação): {alteradas}")
    print(f"  das quais tinham pontuação indevida removida: {com_pontuacao}")
    print("Categorias após a limpeza:")
    print(df["categoria_limpa"].value_counts().to_string())

    # Canais
    canal_alterado = int((df["canal_venda"] != df["canal_padrao"]).sum())
    print("\n--- Canais ---")
    print(f"Canais com texto ajustado na padronização: {canal_alterado}")

    # Problemas numéricos
    print("\n--- Problemas numéricos (marcados, sem inventar valores) ---")
    print(f"quantidade inválida: {int(df['qtd_invalida'].sum())}")
    print(f"preco_unitario inválido: {int(df['preco_invalido'].sum())}")
    print(
        "Total de pedidos afetados (sem somar sobreposição): "
        f"{int(df['problema_numerico'].sum())}"
    )

    # Datas
    print("\n--- Datas de venda ---")
    print(f"Datas inválidas ou vazias: {int((~df['data_valida']).sum())}")
    validas = df[df["data_valida"]].head(3)
    print("Exemplo de conversão (original -> formato brasileiro):")
    for _, linha in validas.iterrows():
        print(f"  {linha['data_venda']} -> {linha['data_br']} (hora {int(linha['hora'])})")

    # Cancelados e entrega
    cancel_ent, outros_ent, exemplos = investigar_entrega(df)
    print("\n--- Status e entrega ---")
    print(f"Total de pedidos cancelados: {int((df['status_pedido'] == 'Cancelado').sum())}")
    print(f"Sem data de entrega e Cancelado: {cancel_ent}")
    print(f"Sem data de entrega e outro status: {outros_ent}")
    if outros_ent > 0:
        print("Hipótese FALSA na base. Exemplos (até 3):")
        print(exemplos.to_string(index=False))
    else:
        print("Hipótese confirmada: todo pedido sem entrega está cancelado.")

    # Contagens exploratórias
    por_canal, excl_canal = contar_por_canal(df)
    print("\n--- Pedidos por canal (todos os status) ---")
    print(por_canal.to_string())
    print(f"Registros excluídos (canal não reconhecido): {excl_canal}")

    por_periodo, excl_data = contar_por_ano_mes(df)
    print("\n--- Pedidos por ano-mês (todos os status) ---")
    print(por_periodo.to_string())
    print(f"Registros excluídos (data de venda inválida/vazia): {excl_data}")
    print("\nObs.: são pedidos registrados, não receita nem vendas concluídas.")


def main():
    df = carregar_dados(ARQUIVO_CSV)
    df = tratar_dataframe(df)
    exibir_relatorio(df)


if __name__ == "__main__":
    main()
