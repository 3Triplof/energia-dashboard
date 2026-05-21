import pandas as pd
import numpy as np


# =========================
# BASE VÁLIDA
# =========================

def base_valida(df):

    df = df.copy()

    df = df[
        (df["Kwh"] > 0)
    ]

    df = df[
        (df["valor"] > 0)
    ]

    df = df[
        (df["tarifa"] > 0)
    ]

    return df


# =========================
# CRESCIMENTO CONSUMO
# =========================

def crescimento_consumo(df):

    df = base_valida(df)

    consumo_anual = (
        df.groupby("ano")["Kwh"]
        .mean()
        .sort_index()
    )

    if len(consumo_anual) < 2:
        return None

    primeiro = consumo_anual.iloc[0]
    ultimo = consumo_anual.iloc[-1]

    if primeiro <= 0:
        return None

    crescimento = (
        (ultimo - primeiro)
        / primeiro
    ) * 100

    return round(crescimento, 1)


# =========================
# CRESCIMENTO TARIFA
# =========================

def crescimento_tarifa(df):

    df = base_valida(df)

    tarifa_anual = (
        df.groupby("ano")["tarifa"]
        .mean()
        .sort_index()
    )

    if len(tarifa_anual) < 2:
        return None

    primeira = tarifa_anual.iloc[0]
    ultima = tarifa_anual.iloc[-1]

    if primeira <= 0:
        return None

    crescimento = (
        (ultima - primeira)
        / primeira
    ) * 100

    return round(crescimento, 1)


# =========================
# MÊS MAIOR CONSUMO
# =========================

def mes_maior_consumo(df):

    df = base_valida(df)

    agrupado = (
        df.groupby("mes_nome")["Kwh"]
        .mean()
        .sort_values(ascending=False)
    )

    if agrupado.empty:
        return None

    return agrupado.index[0]


# =========================
# MÊS MENOR CONSUMO
# =========================

def mes_menor_consumo(df):

    df = base_valida(df)

    agrupado = (
        df.groupby("mes_nome")["Kwh"]
        .mean()
        .sort_values()
    )

    if agrupado.empty:
        return None

    return agrupado.index[0]


# =========================
# MAIOR CONTA
# =========================

def maior_conta(df):

    df = base_valida(df)

    linha = df.loc[
        df["valor"].idxmax()
    ]

    return {
        "valor": linha["valor"],
        "data": linha["data"]
    }


# =========================
# MENOR CONTA
# =========================

def menor_conta(df):

    df = base_valida(df)

    linha = df.loc[
        df["valor"].idxmin()
    ]

    return {
        "valor": linha["valor"],
        "data": linha["data"]
    }


# =========================
# ANOMALIAS
# =========================

def detectar_anomalias(df):

    df = base_valida(df)

    media = df["Kwh"].mean()

    desvio = df["Kwh"].std()

    limite_superior = (
        media + (2 * desvio)
    )

    anomalias = df[
        df["Kwh"] > limite_superior
    ]

    return anomalias


# =========================
# TENDÊNCIA
# =========================

def tendencia_consumo(df):

    df = base_valida(df)

    df = (
        df.sort_values("data")
    )

    if len(df) < 12:
        return "estável"

    primeiros = (
        df.head(6)["Kwh"]
        .mean()
    )

    ultimos = (
        df.tail(6)["Kwh"]
        .mean()
    )

    variacao = (
        (ultimos - primeiros)
        / primeiros
    ) * 100

    if variacao > 5:
        return "alta"

    elif variacao < -5:
        return "queda"

    return "estável"


# =========================
# INSIGHTS
# =========================

def gerar_insights(df):

    df = base_valida(df)

    insights = []

    # =========================
    # CONSUMO
    # =========================

    crescimento = crescimento_consumo(df)

    if crescimento is not None:

        if crescimento > 5:

            insights.append(
                f"📈 Seu consumo médio aumentou {crescimento:.1f}% desde o início da série histórica."
            )

        elif crescimento < -5:

            insights.append(
                f"📉 Seu consumo médio caiu {abs(crescimento):.1f}% desde o início da série histórica."
            )

        else:

            insights.append(
                "⚖ Seu consumo médio permaneceu estável ao longo dos anos."
            )

    # =========================
    # TARIFA
    # =========================

    crescimento_kwh = crescimento_tarifa(df)

    if crescimento_kwh is not None:

        if crescimento_kwh > 0:

            insights.append(
                f"💸 O custo médio da tarifa subiu {crescimento_kwh:.1f}%."
            )

        else:

            insights.append(
                f"💰 O custo médio da tarifa caiu {abs(crescimento_kwh):.1f}%."
            )

    # =========================
    # MESES
    # =========================

    maior_mes = mes_maior_consumo(df)

    if maior_mes:

        insights.append(
            f"🔥 {maior_mes} é historicamente seu mês de maior consumo."
        )

    menor_mes = mes_menor_consumo(df)

    if menor_mes:

        insights.append(
            f"❄ {menor_mes} é historicamente seu mês de menor consumo."
        )

    # =========================
    # TENDÊNCIA
    # =========================

    tendencia = tendencia_consumo(df)

    if tendencia == "alta":

        insights.append(
            "⚠ Seu consumo recente está em tendência de alta."
        )

    elif tendencia == "queda":

        insights.append(
            "✅ Seu consumo recente está em tendência de queda."
        )

    else:

        insights.append(
            "⚖ Seu consumo recente está estável."
        )

    # =========================
    # ANOMALIAS
    # =========================

    anomalias = detectar_anomalias(df)

    if not anomalias.empty:

        insights.append(
            f"🚨 Foram detectados {len(anomalias)} meses com consumo fora do padrão."
        )

    return insights
