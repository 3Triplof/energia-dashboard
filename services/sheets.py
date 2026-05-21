import streamlit as st
import gspread
import pandas as pd

from oauth2client.service_account import (
    ServiceAccountCredentials
)


# =========================
# CARREGAR DADOS
# =========================

def carregar_dados():

    creds_dict = dict(
        st.secrets["gcp_service_account"]
    )

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = (
        ServiceAccountCredentials
        .from_json_keyfile_dict(
            creds_dict,
            scope
        )
    )

    client = gspread.authorize(creds)

    planilha = client.open(
        "Energia"
    )

    aba = planilha.sheet1

    # =========================
    # PEGA VALORES FORMATADOS
    # =========================

    dados = aba.get_all_values()

    # Cabeçalho
    colunas = dados[0]

    # Dados
    linhas = dados[1:]

    # DataFrame
    df = pd.DataFrame(
        linhas,
        columns=colunas
    )

    return df
