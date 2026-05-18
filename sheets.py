import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def carregar_dados():

    creds_dict = dict(st.secrets["gcp_service_account"])

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict,
        scope
    )

    client = gspread.authorize(creds)

    planilha = client.open("NOME_DA_SUA_PLANILHA")

    aba = planilha.sheet1

    dados = aba.get_all_records()

    df = pd.DataFrame(dados)

    return df
