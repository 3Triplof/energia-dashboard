import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.graficos import estilizar_linha, estilizar_pizza
from utils.formatacao import converter_valor, formatar_moeda, formatar_percentual
from services.sheets import carregar_dados


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="Financeiro",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Análise Financeira")


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

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df[df["data"].notna()]

    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(df[coluna].map(converter_valor), errors="coerce")

    df["Kwh"] = df["Kwh"].fillna(0)
    df["valor"] = df["valor"].fillna(0)
    df["pis/confins"] = df["pis/confins"].fillna(0)
    df["icms"] = df["icms"].fillna(0)
    df["iluPublica"] = df["iluPublica"].fillna(0)
    df["tarifa"] = df["tarifa"].fillna(0)
    df["outros"] = df["outros"].fillna(0)

    df = df[df["Kwh"] > 0]

    df["energia"] = df["Kwh"] * df["tarifa"]
    df["impostos"] = df["pis/confins"] + df["icms"]
    df["taxas_publicas"] = df["iluPublica"]
    df["encargos"] = df["outros"]
    df["custo_kwh"] = np.where(df["Kwh"] > 0, df["valor"] / df["Kwh"], np.nan)

    df = df.sort_values("data")
    return df


# =========================
# KPIS
# =========================

def calcular_kpis(df: pd.DataFrame) -> dict:
    total_pago = df["valor"].sum()
    total_energia = df["energia"].sum()
    total_impostos = df["impostos"].sum()
    total_taxas = df["taxas_publicas"].sum()
    total_outros = df["encargos"].sum()

    percentual_impostos = (total_impostos / total_pago * 100) if total_pago else 0

    return {
        "total_pago": total_pago,
        "total_energia": total_energia,
        "total_impostos": total_impostos,
        "total_taxas": total_taxas,
        "total_outros": total_outros,
        "percentual_impostos": percentual_impostos,
    }


def exibir_kpis(kpis: dict) -> None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Pago", formatar_moeda(kpis["total_pago"]))
    col2.metric("Energia Consumida", formatar_moeda(kpis["total_energia"]))
    col3.metric("Impostos", formatar_moeda(kpis["total_impostos"]))
    col4.metric("% Impostos", formatar_percentual(kpis["percentual_impostos"]))


# =========================
# RESUMO
# =========================

def exibir_resumo(kpis: dict) -> None:
    st.info(
        f"""
💡 Do total pago em energia:

- {formatar_percentual(kpis["percentual_impostos"])} corresponde a impostos
- {formatar_moeda(kpis["total_taxas"])} foram taxas de iluminação pública
- {formatar_moeda(kpis["total_outros"])} foram outros encargos
"""
    )


# =========================
# GRAFICOS
# =========================

def grafico_pizza(df: pd.DataFrame) -> None:
    dados = pd.DataFrame({
        "Categoria": [
            "Energia",
            "ICMS",
            "PIS/COFINS",
            "Iluminação Pública",
            "Outros"
        ],
        "Valor": [
            df["energia"].sum(),
            df["icms"].sum(),
            df["pis/confins"].sum(),
            df["taxas_publicas"].sum(),
            df["encargos"].sum()
        ]
    })

    fig = px.pie(
        dados,
        values="Valor",
        names="Categoria",
        title="Composição da Conta de Energia"
    )
    fig = estilizar_pizza(fig)
    st.plotly_chart(fig, use_container_width=True)


def grafico_evolucao_impostos(df: pd.DataFrame) -> None:
    fig = px.line(
        df,
        x="data",
        y="impostos",
        markers=True,
        title="Evolução dos Impostos"
    )
    fig = estilizar_linha(fig)
    st.plotly_chart(fig, use_container_width=True)


def grafico_evolucao_conta(df: pd.DataFrame) -> None:
    fig = px.line(
        df,
        x="data",
        y="valor",
        markers=True,
        title="Evolução da Conta"
    )
    fig = estilizar_linha(fig)
    st.plotly_chart(fig, use_container_width=True)


# =========================
# TABELA
# =========================

def exibir_tabela(df: pd.DataFrame) -> None:
    st.subheader("📋 Dados Financeiros")

    colunas_exibir = [
        "data", "Kwh", "valor", "energia",
        "impostos", "taxas_publicas", "encargos", "custo_kwh"
    ]

    st.dataframe(
        df[colunas_exibir].copy(),
        use_container_width=True
    )


# =========================
# MAIN
# =========================

def main():
    df = carregar()
    df = preparar_dados(df)

    if df.empty:
        st.warning("Nenhum dado válido encontrado.")
        st.stop()

    kpis = calcular_kpis(df)

    exibir_kpis(kpis)
    exibir_resumo(kpis)
    grafico_pizza(df)
    grafico_evolucao_impostos(df)
    grafico_evolucao_conta(df)
    exibir_tabela(df)


if __name__ == "__main__":
    main()
