import streamlit as st
import pandas as pd
import plotly.express as px

from services.sheets import carregar_dados

st.set_page_config(
    page_title="Financeiro",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Análise Financeira")

@st.cache_data(ttl=3600)
def carregar():
    return carregar_dados()

df = carregar()

# =========================
# TRATAMENTO
# =========================

df['data'] = pd.to_datetime(df['data'])

colunas_numericas = [
    'valor',
    'pis/confins',
    'icms',
    'iluPublica',
    'outros'
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna])

df['impostos'] = df['pis/confins'] + df['icms']

# =========================
# KPIs
# =========================

total_impostos = df['impostos'].sum()

total_iluminacao = df['iluPublica'].sum()

valor_total = df['valor'].sum()

percentual_impostos = (
    total_impostos / valor_total
) * 100

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Pago",
    f"R$ {valor_total:.2f}"
)

col2.metric(
    "Impostos",
    f"R$ {total_impostos:.2f}"
)

col3.metric(
    "% Impostos",
    f"{percentual_impostos:.1f}%"
)

# =========================
# PIZZA
# =========================

fig1 = px.pie(
    values=[
        df['icms'].sum(),
        df['pis/confins'].sum(),
        df['iluPublica'].sum(),
        df['outros'].sum()
    ],
    names=[
        'ICMS',
        'PIS/COFINS',
        'Iluminação Pública',
        'Outros'
    ],
    title='Distribuição Financeira'
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================
# EVOLUÇÃO IMPOSTOS
# =========================

fig2 = px.line(
    df,
    x='data',
    y='impostos',
    markers=True,
    title='Evolução dos Impostos'
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================
# TABELA
# =========================

st.subheader("📋 Dados Financeiros")

st.dataframe(
    df,
    use_container_width=True
)
