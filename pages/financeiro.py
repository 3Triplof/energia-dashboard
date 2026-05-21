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

    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = df[coluna].fillna(0)

    df = df[df["valor"] > 0]

    df["impostos"] = df["pis/confins"] + df["icms"]
    df["taxas_publicas"] = df["iluPublica"]
    df["encargos"] = df["outros"]
    df["custo_kwh"] = np.where(df["Kwh"] > 0, df["valor"] / df["Kwh"], np.nan)

    df = df.sort_values("data")
    return df


# =========================
# VALIDAÇÃO
# =========================

def validar_consistencia(df: pd.DataFrame) -> dict:
    total_pago = df["valor"].sum()
    total_impostos = df["impostos"].sum()

    percentual_impostos = (total_impostos / total_pago * 100) if total_pago else 0
    inconsistente = total_impostos > total_pago

    return {
        "total_pago": total_pago,
        "total_impostos": total_impostos,
        "percentual_impostos": percentual_impostos,
        "inconsistente": inconsistente,
    }


def exibir_alertas(validacao: dict) -> None:
    if validacao["inconsistente"]:
        st.error(
            "Inconsistência detectada: o total de impostos está maior que o total pago. "
            "Isso indica erro na base, na conversão dos valores ou nas fórmulas."
        )
    elif validacao["percentual_impostos"] > 100:
        st.warning(
            "Atenção: o percentual de impostos está acima de 100%. "
            "Revise os dados de entrada."
        )


# =========================
# KPIS
# =========================

def exibir_kpis(df: pd.DataFrame, validacao: dict) -> None:
    total_pago = validacao["total_pago"]
    total_impostos = validacao["total_impostos"]
    total_taxas = df["taxas_publicas"].sum()
    total_outros = df["encargos"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Pago", formatar_moeda(total_pago))
    col2.metric("Impostos", formatar_moeda(total_impostos))
    col3.metric("% Impostos", formatar_percentual(validacao["percentual_impostos"]))
    col4.metric("Taxas + Outros", formatar_moeda(total_taxas + total_outros))


# =========================
# RESUMO
# =========================

def exibir_resumo(df: pd.DataFrame, validacao: dict) -> None:
    st.info(
        f"""
💡 Do total pago em energia:

- {formatar_percentual(validacao["percentual_impostos"])} corresponde a impostos
- {formatar_moeda(df["taxas_publicas"].sum())} foram taxas de iluminação pública
- {formatar_moeda(df["encargos"].sum())} foram outros encargos
"""
    )


# =========================
# GRAFICOS
# =========================

def grafico_pizza(df: pd.DataFrame) -> None:
    dados = pd.DataFrame({
        "Categoria": [
            "ICMS",
            "PIS/COFINS",
            "Iluminação Pública",
            "Outros"
        ],
        "Valor": [
            df["icms"].sum(),
            df["pis/confins"].sum(),
            df["taxas_publicas"].sum(),
            df["encargos"].sum()
        ]
    })

    dados = dados[dados["Valor"] > 0]

    if dados.empty:
        st.warning("Sem dados válidos para o gráfico de composição.")
        return

    fig = px.pie(
        dados,
        values="Valor",
        names="Categoria",
        title="Composição dos Encargos da Conta"
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
        "data", "Kwh", "valor", "impostos",
        "taxas_publicas", "encargos", "custo_kwh"
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

    validacao = validar_consistencia(df)
    exibir_alertas(validacao)
    exibir_kpis(df, validacao)
    exibir_resumo(df, validacao)
    grafico_pizza(df)
    grafico_evolucao_impostos(df)
    grafico_evolucao_conta(df)
    exibir_tabela(df)


if __name__ == "__main__":
    main()
