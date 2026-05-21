import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.estatisticas import media_mensal, media_anual, custo_medio_kwh
from utils.graficos import estilizar_linha, estilizar_barra, estilizar_heatmap
from utils.formatacao import converter_valor, formatar_moeda, formatar_kwh
from services.sheets import carregar_dados


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Dashboard Energia",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Dashboard de Energia")


# =========================
# CONSTANTES
# =========================

COLUNAS_OBRIGATORIAS = [
    "data", "Kwh", "valor", "pis/confins",
    "icms", "iluPublica", "tarifa", "outros"
]

COLUNAS_NUMERICAS = [
    "Kwh", "valor", "pis/confins",
    "icms", "iluPublica", "tarifa", "outros"
]

MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
    5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
}

MESES_ORDEM = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
]


# =========================
# DADOS
# =========================

@st.cache_data(ttl=3600, max_entries=10)
def carregar():
    return carregar_dados()


def validar_colunas(df: pd.DataFrame) -> None:
    faltantes = [col for col in COLUNAS_OBRIGATORIAS if col not in df.columns]
    if faltantes:
        st.error(f"Colunas ausentes na base: {', '.join(faltantes)}")
        st.stop()


def preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    validar_colunas(df)

    df["data"] = pd.to_datetime(df["data"], format="%Y-%m", errors="coerce")
    df = df[df["data"].notna()]

    for coluna in COLUNAS_NUMERICAS:

    df[coluna] = (
        df[coluna]
        .astype(str)
        .str.replace('.', '', regex=False)
        .str.replace(',', '.', regex=False)
    )

    df[coluna] = pd.to_numeric(
        df[coluna],
        errors='coerce'
    )

def filtrar_dados(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")
    anos = sorted(df["ano"].dropna().unique().tolist())

    anos_selecionados = st.sidebar.multiselect(
        "Selecione os anos",
        anos,
        default=anos
    )

    df_filtrado = df[df["ano"].isin(anos_selecionados)].copy()

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    return df_filtrado


# =========================
# KPIS
# =========================

def exibir_kpis(df: pd.DataFrame) -> None:
    consumo_total = df["Kwh"].sum()
    valor_total = df["valor"].sum()
    media_mensal_kwh = media_mensal(df)
    media_anual_kwh = media_anual(df)
    custo_medio = custo_medio_kwh(df)
    maior_consumo = df["Kwh"].max()
    menor_consumo = df["Kwh"].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("Consumo Total", formatar_kwh(consumo_total))
    col2.metric("Valor Total", formatar_moeda(valor_total))
    col3.metric("Custo Médio / kWh", formatar_moeda(custo_medio))

    col4, col5, col6 = st.columns(3)
    col4.metric("Média Mensal", formatar_kwh(media_mensal_kwh))
    col5.metric("Média Anual", formatar_kwh(media_anual_kwh))
    col6.metric("Maior Consumo", formatar_kwh(maior_consumo))

    st.caption(f"Menor consumo no período: {formatar_kwh(menor_consumo)}")


# =========================
# GRAFICOS
# =========================

def grafico_consumo_historico(df: pd.DataFrame) -> None:
    fig = px.line(
        df,
        x="data",
        y="Kwh",
        color="ano",
        markers=True,
        title="Consumo ao Longo do Tempo"
    )
    fig = estilizar_linha(fig)
    st.plotly_chart(fig, use_container_width=True)


def grafico_comparacao_anual(df: pd.DataFrame) -> None:
    comparacao = df.groupby("ano", as_index=False)["Kwh"].sum()

    fig = px.bar(
        comparacao,
        x="ano",
        y="Kwh",
        text_auto=True,
        title="Comparação Anual de Consumo"
    )
    fig = estilizar_barra(fig)
    st.plotly_chart(fig, use_container_width=True)


def grafico_heatmap(df: pd.DataFrame) -> None:
    heatmap = (
        df.pivot_table(
            values="Kwh",
            index="ano",
            columns="mes_nome",
            aggfunc="sum"
        )
        .reindex(columns=MESES_ORDEM)
        .fillna(0)
    )

    fig = px.imshow(
        heatmap,
        text_auto=True,
        aspect="auto",
        title="Heatmap de Consumo"
    )
    fig = estilizar_heatmap(fig)
    st.plotly_chart(fig, use_container_width=True)


def grafico_valor_conta(df: pd.DataFrame) -> None:
    fig = px.bar(
        df,
        x="data",
        y="valor",
        title="Valor da Conta"
    )
    fig = estilizar_barra(fig)
    st.plotly_chart(fig, use_container_width=True)


def grafico_custo_kwh(df: pd.DataFrame) -> None:
    fig = px.line(
        df,
        x="data",
        y="custo_kwh",
        markers=True,
        title="Evolução do Custo do kWh"
    )
    fig = estilizar_linha(fig)
    st.plotly_chart(fig, use_container_width=True)


# =========================
# TABELA
# =========================

def exibir_tabela(df: pd.DataFrame) -> None:
    st.subheader("📋 Dados")

    colunas_exibir = [
        "data", "ano", "mes_nome",
        "Kwh", "valor", "custo_kwh",
        "tarifa", "impostos"
    ]

    st.dataframe(
        df[colunas_exibir].sort_values("data"),
        use_container_width=True
    )


# =========================
# MAIN
# =========================

def main():
    df = carregar()
    df = preparar_dados(df)
    df_filtrado = filtrar_dados(df)

    exibir_kpis(df_filtrado)
    grafico_consumo_historico(df_filtrado)
    grafico_comparacao_anual(df_filtrado)
    grafico_heatmap(df_filtrado)
    grafico_valor_conta(df_filtrado)
    grafico_custo_kwh(df_filtrado)
    exibir_tabela(df_filtrado)


if __name__ == "__main__":
    main()
