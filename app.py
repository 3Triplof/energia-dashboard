from utils.estatisticas import (
    media_mensal,
    media_anual,
    custo_medio_kwh
)
from utils.graficos import (
    estilizar_linha,
    estilizar_barra,
    estilizar_heatmap
)
from utils.formatacao import (
    converter_valor,
    formatar_moeda,
    formatar_kwh,
    formatar_percentual
)
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
    df[coluna] = df[coluna].apply(converter_valor)

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

media_mensal_kwh = media_mensal(df_filtrado)

media_anual_kwh = media_anual(df_filtrado)

custo_medio = custo_medio_kwh(df_filtrado)

custo_medio = df_filtrado['custo_kwh'].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Consumo Total",
    formatar_kwh(consumo_total)
)

col2.metric(
    "Valor Total",
    formatar_moeda(valor_total)
)

col3.metric(
    "Média Mensal",
    formatar_kwh(media_mensal_kwh)
)

col4.metric(
    "Custo Médio kWh",
    formatar_moeda(custo_medio)
)
col5.metric(
    "Média Anual",
    formatar_kwh(media_anual_kwh)
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

fig1 = estilizar_linha(fig1)

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

fig2 = estilizar_barra(fig2)

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

fig3 = estilizar_heatmap(fig3)

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

fig4 = estilizar_barra(fig4)

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
