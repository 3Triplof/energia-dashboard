import streamlit as st
import pandas as pd
import plotly.express as px

from services.sheets import carregar_dados

from utils.insights import (
    gerar_insights,
    detectar_anomalias,
    maior_conta,
    menor_conta
)

from utils.formatacao import (
    formatar_moeda,
    formatar_kwh
)

from utils.graficos import (
    estilizar_barra,
    estilizar_linha
)


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Insights",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Insights Inteligentes")


# =========================
# CONSTANTES
# =========================

COLUNAS_NUMERICAS = [
    "Kwh",
    "valor",
    "pis/confins",
    "icms",
    "iluPublica",
    "tarifa",
    "outros"
]

MESES_PT = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez"
}


# =========================
# DADOS
# =========================

@st.cache_data(ttl=3600)
def carregar():

    return carregar_dados()


def preparar_dados(df):

    df = df.copy()

    # =========================
    # DATA
    # =========================

    df["data"] = pd.to_datetime(
        df["data"],
        format="%Y-%m",
        errors="coerce"
    )

    df = df[
        df["data"].notna()
    ]

    # =========================
    # NUMÉRICOS
    # =========================

    for coluna in COLUNAS_NUMERICAS:

        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.strip()
            .str.replace("R$", "", regex=False)
            .str.replace(" ", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    for coluna in COLUNAS_NUMERICAS:

        df[coluna] = (
            df[coluna]
            .fillna(0)
        )

    # =========================
    # CAMPOS AUXILIARES
    # =========================

    df["ano"] = (
        df["data"]
        .dt.year
    )

    df["mes"] = (
        df["data"]
        .dt.month
    )

    df["mes_nome"] = (
        df["mes"]
        .map(MESES_PT)
    )

    df["impostos"] = (
        df["pis/confins"]
        + df["icms"]
    )

    df["custo_kwh"] = (
        df["valor"] / df["Kwh"]
    )

    df = df.sort_values("data")

    return df


# =========================
# CARREGA
# =========================

df = carregar()

df = preparar_dados(df)


# =========================
# FILTROS
# =========================

st.sidebar.header("Filtros")

anos = sorted(
    df["ano"]
    .dropna()
    .unique()
)

anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos",
    anos,
    default=anos
)

df = df[
    df["ano"]
    .isin(anos_selecionados)
]


# =========================
# INSIGHTS
# =========================

st.subheader("💡 Insights Automáticos")

insights = gerar_insights(df)

for insight in insights:

    st.info(insight)


# =========================
# KPIS
# =========================

maior = maior_conta(df)

menor = menor_conta(df)

col1, col2 = st.columns(2)

col1.metric(
    "Maior Conta",
    formatar_moeda(maior["valor"])
)

col1.caption(
    f"Mês: {maior['data'].strftime('%m/%Y')}"
)

col2.metric(
    "Menor Conta",
    formatar_moeda(menor["valor"])
)

col2.caption(
    f"Mês: {menor['data'].strftime('%m/%Y')}"
)


# =========================
# ANOMALIAS
# =========================

st.subheader("🚨 Detecção de Anomalias")

anomalias = detectar_anomalias(df)

if anomalias.empty:

    st.success(
        "Nenhuma anomalia detectada."
    )

else:

    st.warning(
        f"{len(anomalias)} anomalias encontradas."
    )

    st.dataframe(
        anomalias[
            [
                "data",
                "Kwh",
                "valor"
            ]
        ],
        use_container_width=True
    )


# =========================
# EVOLUÇÃO CONSUMO
# =========================

fig1 = px.line(
    df,
    x="data",
    y="Kwh",
    markers=True,
    title="Evolução do Consumo"
)

fig1 = estilizar_linha(fig1)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# =========================
# EVOLUÇÃO TARIFA
# =========================

fig2 = px.line(
    df,
    x="data",
    y="tarifa",
    markers=True,
    title="Evolução da Tarifa"
)

fig2 = estilizar_linha(fig2)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# =========================
# CONSUMO MÉDIO POR MÊS
# =========================

media_mes = (
    df.groupby("mes_nome")["Kwh"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    media_mes,
    x="mes_nome",
    y="Kwh",
    text_auto=True,
    title="Consumo Médio por Mês"
)

fig3 = estilizar_barra(fig3)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# =========================
# TABELA
# =========================

st.subheader("📋 Dados Analisados")

st.dataframe(
    df,
    use_container_width=True
)
