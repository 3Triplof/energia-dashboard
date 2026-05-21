import pandas as pd


def _validar_base(df, coluna="Kwh"):
    if df is None or df.empty:
        return False
    if "data" not in df.columns or coluna not in df.columns:
        return False
    return True


def media_mensal(df, coluna="Kwh"):
    if not _validar_base(df, coluna):
        return 0

    df_valido = df[df[coluna].fillna(0) > 0].copy()
    if df_valido.empty:
        return 0

    meses_unicos = df_valido["data"].dt.to_period("M").nunique()
    if meses_unicos == 0:
        return 0

    return df_valido[coluna].sum() / meses_unicos


def media_anual(df, coluna="Kwh"):
    if not _validar_base(df, coluna):
        return 0

    df_valido = df[df[coluna].fillna(0) > 0].copy()
    if df_valido.empty:
        return 0

    anual = df_valido.groupby(df_valido["data"].dt.year)[coluna].sum()
    if anual.empty:
        return 0

    return anual.mean()


def total_por_ano(df, coluna="Kwh"):
    if not _validar_base(df, coluna):
        return pd.DataFrame(columns=["ano", coluna])

    return (
        df.groupby(df["data"].dt.year, as_index=False)[coluna]
        .sum()
        .rename(columns={"data": "ano"})
    )


def crescimento_anual(df, coluna="Kwh"):
    if not _validar_base(df, coluna):
        return pd.DataFrame(columns=["ano", "crescimento"])

    serie = (
        df.groupby(df["data"].dt.year)[coluna]
        .sum()
        .sort_index()
    )

    return (
        serie.pct_change()
        .mul(100)
        .reset_index(name="crescimento")
        .rename(columns={"data": "ano"})
    )


def anos_completos(df):
    if df is None or df.empty or "data" not in df.columns:
        return []

    meses_por_ano = df.groupby(df["data"].dt.year)["data"].nunique()
    return meses_por_ano[meses_por_ano >= 12].index.tolist()


def maior_consumo(df, coluna="Kwh"):
    if not _validar_base(df, coluna):
        return None

    df_valido = df[df[coluna].fillna(0) > 0].copy()
    if df_valido.empty:
        return None

    idx = df_valido[coluna].idxmax()
    return df_valido.loc[idx]


def menor_consumo(df, coluna="Kwh"):
    if not _validar_base(df, coluna):
        return None

    df_valido = df[df[coluna].fillna(0) > 0].copy()
    if df_valido.empty:
        return None

    idx = df_valido[coluna].idxmin()
    return df_valido.loc[idx]


def custo_medio_kwh(df):
    if df is None or df.empty or "Kwh" not in df.columns or "valor" not in df.columns:
        return 0

    total_kwh = df["Kwh"].fillna(0).sum()
    if total_kwh == 0:
        return 0

    return df["valor"].fillna(0).sum() / total_kwh
