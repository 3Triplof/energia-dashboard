from utils.graficos import (
    estilizar_linha,
    estilizar_pizza
)

from utils.formatacao import (
    converter_valor,
    formatar_moeda,
    formatar_percentual
)

import streamlit as st
import pandas as pd
import plotly.express as px

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
# CARREGAMENTO
# =========================

@st.cache_data(ttl=3600)
def carregar():
    return carregar_dados()

df = carregar()


# =========================
# TRATAMENTO
# =========================

df['data'] = pd.to_datetime(df['data'])

colunas_numericas = [
    'Kwh',
    'valor',
    'pis/confins',
    'icms',
    'iluPublica',
    'tarifa',
    'outros'
]

for coluna in colunas_numericas:
    df[coluna] = df[coluna].apply(converter_valor)


# =========================
# COMPOSIÇÃO FINANCEIRA
# =========================

# Energia consumida
df['energia'] = df['Kwh'] * df['tarifa']

# Impostos
df['impostos'] = (
    df['pis/confins']
    + df['icms']
)

# Taxa iluminação pública
df['taxas_publicas'] = df['iluPublica']

# Outros encargos
df['encargos'] = df['outros']


# =========================
# KPIs
# =========================

total_pago = df['valor'].sum()

total_energia = df['energia'].sum()

total_impostos = df['impostos'].sum()

total_taxas = df['taxas_publicas'].sum()

total_outros = df['encargos'].sum()

percentual_impostos = (
    total_impostos / total_pago
) * 100


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Pago",
    formatar_moeda(total_pago)
)

col2.metric(
    "Energia Consumida",
    formatar_moeda(total_energia)
)

col3.metric(
    "Impostos",
    formatar_moeda(total_impostos)
)

col4.metric(
    "% Impostos",
    formatar_percentual(percentual_impostos)
)


# =========================
# RESUMO
# =========================

st.info(
    f"""
💡 Do total pago em energia:

- {formatar_percentual(percentual_impostos)} corresponde a impostos
- {formatar_moeda(total_taxas)} foram taxas de iluminação pública
- {formatar_moeda(total_outros)} foram outros encargos
"""
)


# =========================
# GRÁFICO PIZZA
# =========================

fig1 = px.pie(
    values=[
        total_energia,
        df['icms'].sum(),
        df['pis/confins'].sum(),
        total_taxas,
        total_outros
    ],

    names=[
        'Energia',
        'ICMS',
        'PIS/COFINS',
        'Iluminação Pública',
        'Outros'
    ],

    title='Composição da Conta de Energia'
)

fig1 = estilizar_pizza(fig1)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# =========================
# EVOLUÇÃO DOS IMPOSTOS
# =========================

fig2 = px.line(
    df,
    x='data',
    y='impostos',
    markers=True,
    title='Evolução dos Impostos'
)

fig2 = estilizar_linha(fig2)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# =========================
# EVOLUÇÃO DO VALOR TOTAL
# =========================

fig3 = px.line(
    df,
    x='data',
    y='valor',
    markers=True,
    title='Evolução da Conta'
)

fig3 = estilizar_linha(fig3)

st.plotly_chart(
    fig3,
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
