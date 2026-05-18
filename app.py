import streamlit as st
import pandas as pd
import plotly.express as px

from services.sheets import carregar_dados

st.set_page_config(
    page_title="Dashboard Energia",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Dashboard de Energia")

# CACHE
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
    df[coluna] = pd.to_numeric(df[coluna])

# NOVAS MÉTRICAS
df['custo_kwh'] = df['valor'] / df['Kwh']

df['impostos'] = df['pis/confins'] + df['icms']

# ORDENA
df = df.sort_values('data')

# =========================
# KPIs
# =========================

consumo_total = df['Kwh'].sum()

valor_total = df['valor'].sum()

media_mensal = df['Kwh'].mean()

custo_medio = df['custo_kwh'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Consumo Total",
    f"{consumo_total:.0f} kWh"
)

col2.metric(
    "Valor Total",
    f"R$ {valor_total:.2f}"
)

col3.metric(
    "Média Mensal",
    f"{media_mensal:.0f} kWh"
)

col4.metric(
    "Custo Médio kWh",
    f"R$ {custo_medio:.2f}"
)

# =========================
# GRÁFICO CONSUMO
# =========================

fig1 = px.line(
    df,
    x='data',
    y='Kwh',
    title='Consumo ao Longo do Tempo',
    markers=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================
# GRÁFICO VALOR
# =========================

fig2 = px.bar(
    df,
    x='data',
    y='valor',
    title='Valor da Conta'
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================
# IMPOSTOS
# =========================

fig3 = px.pie(
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
    title='Distribuição de Taxas'
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================
# TABELA
# =========================

st.subheader("📋 Dados")

st.dataframe(
    df,
    use_container_width=True
)
