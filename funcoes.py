import math
import re
import unicodedata
from datetime import datetime

import pandas as pd

# Mapa dos canais: chave sem acento e em minúsculas -> nome padrão do enunciado
MAPA_CANAIS = {
    "mercado": "Mercado",
    "loja fisica": "Loja física",
    "web": "Web",
}

# Formato do texto de data_venda no CSV, ex.: "2025-10-12 14:35:00"
FORMATO_DATA = "%Y-%m-%d %H:%M:%S"


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


# ---------------------------------------------------------------
# SPRINT 2: transformação de strings
# ---------------------------------------------------------------

def limpar_categoria(valor):
    """Limpa uma categoria e informa o que aconteceu com ela.

    Retorna: (categoria_limpa, foi_vazia_preenchida, foi_alterada,
              limpou_com_regex)
    - foi_alterada: o texto final é diferente do original (inclui maiúscula).
    - limpou_com_regex: o re.sub removeu pontuação ou espaços sobrando.
    """
    original_vazio = valor.strip() == ""

    # Passo 1: tira espaços das pontas e deixa minúscula
    base = valor.strip().lower()

    # Passo 2: re.sub remove tudo que não é letra nem espaço
    texto = re.sub(r"[^a-zà-ÿ\s]", "", base)

    # Passo 3: junta espaços repetidos em um só
    texto = re.sub(r"\s+", " ", texto).strip()

    # O regex mexeu em algo além de maiúscula/minúscula?
    limpou_com_regex = (texto != base) and not original_vazio

    # Passo 4: se ficou vazio, usa "sem categoria" (sem inventar categoria)
    if texto == "":
        texto = "sem categoria"

    if original_vazio:
        # Categoria que já era vazia e foi preenchida
        return texto, True, False, False

    # Categoria que tinha conteúdo e mudou (maiúscula, pontuação, espaço...)
    alterada = texto != valor
    return texto, False, alterada, limpou_com_regex


def tratar_categorias(df):
    """Cria as colunas categoria_limpa e marcadores, mantendo a original."""
    df = df.copy()

    categorias_limpas = []
    vazias_preenchidas = []
    alteradas = []
    limpas_regex = []

    for valor in df["categoria"]:
        nova, foi_vazia, foi_alterada, usou_regex = limpar_categoria(valor)
        categorias_limpas.append(nova)
        vazias_preenchidas.append(foi_vazia)
        alteradas.append(foi_alterada)
        limpas_regex.append(usou_regex)

    df["categoria_limpa"] = categorias_limpas
    df["categoria_vazia_preenchida"] = vazias_preenchidas
    df["categoria_alterada"] = alteradas
    df["categoria_limpa_regex"] = limpas_regex
    return df


def _remover_acentos(texto):
    """Tira acentos para comparar 'Loja física' com 'loja fisica'."""
    decomposto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in decomposto if unicodedata.category(c) != "Mn")


def padronizar_canal(valor):
    """Converte o canal para Mercado, Loja física ou Web.

    Se não for reconhecido, devolve "nao reconhecido" em vez de adivinhar.
    """
    chave = _remover_acentos(valor.strip().lower())
    chave = re.sub(r"\s+", " ", chave)

    if chave in MAPA_CANAIS:
        return MAPA_CANAIS[chave]
    else:
        return "nao reconhecido"


def tratar_canais(df):
    """Cria a coluna canal_padrao, mantendo canal_venda original."""
    df = df.copy()
    df["canal_padrao"] = [padronizar_canal(v) for v in df["canal_venda"]]
    return df


def contar_correcoes(df):
    """Conta as correções de categoria e canal, separadamente."""
    return {
        "categorias vazias preenchidas": int(df["categoria_vazia_preenchida"].sum()),
        "categorias nao vazias alteradas": int(df["categoria_alterada"].sum()),
        "dessas, com pontuacao/espacos removidos pelo re.sub": int(df["categoria_limpa_regex"].sum()),
        "canais nao reconhecidos": int((df["canal_padrao"] == "nao reconhecido").sum()),
    }


# ---------------------------------------------------------------
# SPRINT 3: nulos e validação de quantidade e preço
# ---------------------------------------------------------------

def validar_quantidade(valor):
    """Valida a quantidade: precisa ser inteiro maior que zero.

    Regra: não invento valor. Se tem problema, o número vira None
    e o motivo fica registrado em texto.

    Retorna: (numero_ou_None, motivo_do_problema)
    - motivo vazio ("") significa que a quantidade está válida.
    """
    texto = valor.strip()

    if texto == "":
        return None, "vazia"

    try:
        numero = int(texto)
    except ValueError:
        # Texto que não é número inteiro (ex.: "abc" ou "2.5").
        # O except evita que o programa pare: ele marca e segue.
        return None, "nao e inteiro"

    if numero <= 0:
        return None, "menor ou igual a zero"

    return numero, ""


def validar_preco(valor):
    """Valida o preço unitário: precisa estar preenchido e não ser negativo.

    Regra: preço 0 é aceito (o enunciado diz "não negativo").
    Preço ausente NÃO vira zero: fica marcado como problema.

    Retorna: (numero_ou_None, motivo_do_problema)
    """
    texto = valor.strip()

    if texto == "":
        return None, "ausente"

    try:
        numero = float(texto)
    except ValueError:
        return None, "nao e numero"

    if not math.isfinite(numero):
        return None, "nao e numero"

    if numero < 0:
        return None, "negativo"

    return numero, ""


def validar_numeros(df):
    """Valida quantidade e preço de cada pedido e marca os problemas.

    Cria colunas novas, sem mexer nas originais:
    - quantidade_num / preco_num: valor convertido (vazio se inválido)
    - quantidade_problema / preco_problema: motivo ("" se estiver ok)
    - pedido_com_problema: True se qualquer um dos dois campos falhou
    """
    df = df.copy()

    quantidades = []
    problemas_quantidade = []
    precos = []
    problemas_preco = []

    for q, p in zip(df["quantidade"], df["preco_unitario"]):
        numero_q, problema_q = validar_quantidade(q)
        numero_p, problema_p = validar_preco(p)

        quantidades.append(numero_q)
        problemas_quantidade.append(problema_q)
        precos.append(numero_p)
        problemas_preco.append(problema_p)

    df["quantidade_num"] = quantidades
    df["quantidade_problema"] = problemas_quantidade
    df["preco_num"] = precos
    df["preco_problema"] = problemas_preco

    # O "|" significa OU: basta um dos dois campos ter problema
    df["pedido_com_problema"] = (
        (df["quantidade_problema"] != "") | (df["preco_problema"] != "")
    )
    return df


def contar_problemas_numericos(df):
    """Conta problemas por campo e o total de pedidos afetados.

    O total de pedidos NÃO é a soma dos dois campos, porque um mesmo
    pedido pode ter problema na quantidade e no preço ao mesmo tempo.
    Por isso uso OU (|) para o total e E (&) para a sobreposição.
    """
    q_tem = df["quantidade_problema"] != ""
    p_tem = df["preco_problema"] != ""

    return {
        "quantidade com problema": int(q_tem.sum()),
        "preco_unitario com problema": int(p_tem.sum()),
        "pedidos com problema nos dois campos": int((q_tem & p_tem).sum()),
        "pedidos afetados (sem contar duas vezes)": int((q_tem | p_tem).sum()),
    }


def separar_registros(df):
    """Separa os pedidos válidos dos pedidos com problema numérico.

    Retorna: (df_validos, df_com_problema)
    Nada é apagado nem alterado: só dividimos em dois grupos.
    """
    com_problema = df[df["pedido_com_problema"]]
    validos = df[~df["pedido_com_problema"]]
    return validos, com_problema


# ---------------------------------------------------------------
# SPRINT 4: regras de negócio e datas
# ---------------------------------------------------------------

def investigar_entrega_sem_data(df):
    """Testa a hipótese: todo pedido sem data_entrega está Cancelado.

    Para cada pedido, uso condicionais (if/else) aninhados:
    - se data_entrega está vazia:
        - se o status é Cancelado -> conta no grupo 1
        - senão -> conta no grupo 2 (contraexemplo)
    Não altero o status e não invento datas de entrega.

    Retorna um dicionário com as contagens, até 3 exemplos do grupo 2
    e se a hipótese é verdadeira ou falsa.
    """
    sem_entrega_cancelado = 0
    sem_entrega_outro_status = 0
    total_cancelados = 0
    indices_exemplos = []

    for indice, linha in df.iterrows():
        eh_cancelado = linha["status_pedido"].strip().lower() == "cancelado"

        if eh_cancelado:
            total_cancelados += 1

        if linha["data_entrega"].strip() == "":
            if eh_cancelado:
                sem_entrega_cancelado += 1
            else:
                sem_entrega_outro_status += 1
                if len(indices_exemplos) < 3:
                    indices_exemplos.append(indice)

    colunas = ["pedido_id", "status_pedido", "data_venda", "data_entrega"]
    exemplos = df.loc[indices_exemplos, colunas]

    return {
        "sem_entrega_e_cancelado": sem_entrega_cancelado,
        "sem_entrega_outro_status": sem_entrega_outro_status,
        "total_cancelados": total_cancelados,
        "exemplos": exemplos,
        # Basta UM contraexemplo para a hipótese ser falsa
        "hipotese_verdadeira": sem_entrega_outro_status == 0,
    }


def converter_data_venda(valor):
    """Converte o texto de data_venda para datetime com strptime().

    Se estiver vazia ou inválida, NÃO substituo pela data de hoje:
    devolvo None e o motivo, e o processamento continua.

    Retorna: (datetime_ou_None, motivo_do_problema)
    """
    texto = valor.strip()

    if texto == "":
        return None, "vazia"

    try:
        data = datetime.strptime(texto, FORMATO_DATA)
    except ValueError:
        # Ex.: "2025-13-45 99:99:99" ou "texto qualquer"
        return None, "invalida"

    return data, ""


def tratar_datas(df):
    """Extrai ano, mês, dia e hora e cria a data no formato brasileiro.

    O texto original de data_venda é preservado. Cria colunas novas:
    ano, mes, dia, hora, data_br (dd/mm/aaaa), ano_mes (aaaa-mm),
    data_problema e data_valida.
    """
    df = df.copy()

    anos, meses, dias, horas = [], [], [], []
    datas_br, anos_meses, problemas = [], [], []

    for texto in df["data_venda"]:
        data, problema = converter_data_venda(texto)
        problemas.append(problema)

        if data is None:
            # Data com problema: deixa as partes vazias, sem inventar nada
            anos.append(None)
            meses.append(None)
            dias.append(None)
            horas.append(None)
            datas_br.append(None)
            anos_meses.append(None)
        else:
            anos.append(data.year)
            meses.append(data.month)
            dias.append(data.day)
            horas.append(data.hour)
            datas_br.append(data.strftime("%d/%m/%Y"))
            anos_meses.append(data.strftime("%Y-%m"))

    df["data_problema"] = problemas
    df["data_valida"] = df["data_problema"] == ""
    df["ano"] = pd.array(anos, dtype="Int64")
    df["mes"] = pd.array(meses, dtype="Int64")
    df["dia"] = pd.array(dias, dtype="Int64")
    df["hora"] = pd.array(horas, dtype="Int64")
    df["data_br"] = datas_br
    df["ano_mes"] = anos_meses
    return df


def contar_datas_invalidas(df):
    """Conta datas de venda vazias e inválidas."""
    return {
        "datas vazias": int((df["data_problema"] == "vazia").sum()),
        "datas invalidas": int((df["data_problema"] == "invalida").sum()),
        "total de datas com problema": int((~df["data_valida"]).sum()),
    }


def contar_por_canal(df):
    """Conta pedidos registrados por canal, só com canal reconhecido.

    Inclui todos os status (concluído, cancelado...). Não é receita.
    Retorna: (contagem_por_canal, quantidade_excluida)
    """
    reconhecidos = df[df["canal_padrao"] != "nao reconhecido"]
    contagem = reconhecidos["canal_padrao"].value_counts()
    excluidos = len(df) - len(reconhecidos)
    return contagem, excluidos


def contar_por_ano_mes(df):
    """Conta pedidos registrados por ano-mês, só com data_venda válida.

    Uso ano_mes (ex.: 2025-10) e NÃO só o mês, para não misturar
    2024 com 2025. Inclui todos os status.
    Retorna: (contagem_por_ano_mes, quantidade_excluida)
    """
    validos = df[df["data_valida"]]
    contagem = validos["ano_mes"].value_counts().sort_index()
    excluidos = len(df) - len(validos)
    return contagem, excluidos

def contar_status_sem_entrega(df):
    """Conta os status dos pedidos que estão sem data_entrega.

    Serve para detalhar o grupo dos contraexemplos: quantos dos pedidos
    sem entrega são Cancelado, Concluído ou Devolvido.
    Não altera nenhum dado.
    """
    sem_entrega = df[df["data_entrega"].str.strip() == ""]
    return sem_entrega["status_pedido"].value_counts()