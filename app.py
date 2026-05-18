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
    df[coluna] = pd.to_numeric(df[coluna])

df['custo_kwh'] = df['valor'] / df['Kwh']

df['impostos'] = df['pis/confins'] + df['icms']

df['ano'] = df['data'].dt.year

df['mes'] = df['data'].dt.month

df['mes_nome'] = df['data'].dt.strftime('%b')

df = df.sort_values('data')

# =========================
# FILTROS
# =========================

st.sidebar.header("Filtros")

anos = sorted(df['ano'].unique())

anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos",
    anos,
    default=anos
)

df_filtrado = df[
    df['ano'].isin(anos_selecionados)
]

# =========================
# KPIs
# =========================

consumo_total = df_filtrado['Kwh'].sum()

valor_total = df_filtrado['valor'].sum()

media_mensal = df_filtrado['Kwh'].mean()

custo_medio = df_filtrado['custo_kwh'].mean()

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
# CONSUMO HISTÓRICO
# =========================

fig1 = px.line(
    df_filtrado,
    x='data',
    y='Kwh',
    color='ano',
    markers=True,
    title='Consumo ao Longo do Tempo'
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================
# COMPARAÇÃO ANUAL
# =========================

comparacao = df_filtrado.groupby('ano')['Kwh'].sum().reset_index()

fig2 = px.bar(
    comparacao,
    x='ano',
    y='Kwh',
    text_auto=True,
    title='Comparação Anual de Consumo'
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================
# HEATMAP
# =========================

heatmap = df_filtrado.pivot_table(
    values='Kwh',
    index='ano',
    columns='mes_nome',
    aggfunc='sum'
)

fig3 = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto",
    title='Heatmap de Consumo'
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =========================
# VALOR DA CONTA
# =========================

fig4 = px.bar(
    df_filtrado,
    x='data',
    y='valor',
    title='Valor da Conta'
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# =========================
# TABELA
# =========================

st.subheader("📋 Dados")

st.dataframe(
    df_filtrado,
    use_container_width=True
)
