import pandas as pd
import numpy as np


# =========================
# CRESCIMENTO DE CONSUMO
# =========================

def crescimento_consumo(df):

    consumo_anual = (
        df.groupby("ano")["Kwh"]
        .sum()
        .sort_index()
    )

    if len(consumo_anual) < 2:
        return None

    primeiro = consumo_anual.iloc[0]
    ultimo = consumo_anual.iloc[-1]

    if primeiro == 0:
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

    tarifa_anual = (
        df.groupby("ano")["tarifa"]
        .mean()
        .sort_index()
    )

    if len(tarifa_anual) < 2:
        return None

    primeira = tarifa_anual.iloc[0]
    ultima = tarifa_anual.iloc[-1]

    if primeira == 0:
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

    media = df["Kwh"].mean()
    desvio = df["Kwh"].std()

    limite_superior = media + (2 * desvio)

    anomalias = df[
        df["Kwh"] > limite_superior
    ]

    return anomalias


# =========================
# TENDÊNCIA
# =========================

def tendencia_consumo(df):

    primeiros = (
        df.sort_values("data")
        .head(6)["Kwh"]
        .mean()
    )

    ultimos = (
        df.sort_values("data")
        .tail(6)["Kwh"]
        .mean()
    )

    if ultimos > primeiros:
        return "alta"

    elif ultimos < primeiros:
        return "queda"

    return "estável"


# =========================
# RESUMO AUTOMÁTICO
# =========================

def gerar_insights(df):

    insights = []

    crescimento = crescimento_consumo(df)

    if crescimento is not None:

        if crescimento > 0:
            insights.append(
                f"📈 Seu consumo aumentou {crescimento:.1f}% desde o início da série histórica."
            )

        elif crescimento < 0:
            insights.append(
                f"📉 Seu consumo caiu {abs(crescimento):.1f}% desde o início da série histórica."
            )

    crescimento_kwh = crescimento_tarifa(df)

    if crescimento_kwh is not None:

        insights.append(
            f"💸 O custo médio da tarifa subiu {crescimento_kwh:.1f}%."
        )

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

    tendencia = tendencia_consumo(df)

    if tendencia == "alta":

        insights.append(
            "⚠ Seu consumo recente está em tendência de alta."
        )

    elif tendencia == "queda":

        insights.append(
            "✅ Seu consumo recente está em tendência de queda."
        )

    anomalias = detectar_anomalias(df)

    if not anomalias.empty:

        insights.append(
            f"🚨 Foram detectados {len(anomalias)} meses com consumo fora do padrão."
        )

    return insights
