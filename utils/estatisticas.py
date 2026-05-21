import pandas as pd


# =========================
# MÉDIA MENSAL REAL
# =========================

def media_mensal(df, coluna='Kwh'):

    meses_unicos = (
        df['data']
        .dt.to_period('M')
        .nunique()
    )

    if meses_unicos == 0:
        return 0

    return df[coluna].sum() / meses_unicos


# =========================
# MÉDIA ANUAL
# =========================

def media_anual(df, coluna='Kwh'):

    anual = (
        df.groupby(
            df['data'].dt.year
        )[coluna]
        .sum()
    )

    if len(anual) == 0:
        return 0

    return anual.mean()


# =========================
# TOTAL ANUAL
# =========================

def total_por_ano(df, coluna='Kwh'):

    return (
        df.groupby(
            df['data'].dt.year
        )[coluna]
        .sum()
        .reset_index()
    )


# =========================
# CRESCIMENTO ANUAL %
# =========================

def crescimento_anual(df, coluna='Kwh'):

    anual = (
        df.groupby(
            df['data'].dt.year
        )[coluna]
        .sum()
        .pct_change()
        * 100
    )

    return anual.reset_index(
        name='crescimento'
    )


# =========================
# IDENTIFICAR ANOS COMPLETOS
# =========================

def anos_completos(df):

    meses_por_ano = (
        df.groupby(
            df['data'].dt.year
        )['data']
        .nunique()
    )

    completos = (
        meses_por_ano[
            meses_por_ano >= 12
        ]
        .index
        .tolist()
    )

    return completos


# =========================
# MAIOR CONSUMO
# =========================

def maior_consumo(df):

    idx = df['Kwh'].idxmax()

    return df.loc[idx]


# =========================
# MENOR CONSUMO
# =========================

def menor_consumo(df):

    idx = df['Kwh'].idxmin()

    return df.loc[idx]


# =========================
# CUSTO MÉDIO REAL KWH
# =========================

def custo_medio_kwh(df):

    total_kwh = df['Kwh'].sum()

    if total_kwh == 0:
        return 0

    return (
        df['valor'].sum()
        / total_kwh
    )
