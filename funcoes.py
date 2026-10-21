import re
import unicodedata

import pandas as pd

# Mapa dos canais: chave sem acento e em minúsculas -> nome padrão do enunciado
MAPA_CANAIS = {
    "mercado": "Mercado",
    "loja fisica": "Loja física",
    "web": "Web",
}


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
