import pandas as pd


def converter_valor(valor):
    if pd.isna(valor):
        return 0.0

    if isinstance(valor, (int, float)):
        return float(valor)

    texto = str(valor).strip()
    if not texto:
        return 0.0

    texto = texto.replace("R$", "").strip()

    try:
        if "," in texto and "." in texto:
            texto = texto.replace(".", "").replace(",", ".")
        elif "," in texto:
            texto = texto.replace(",", ".")
        return float(texto)
    except (ValueError, TypeError):
        return 0.0


def formatar_moeda(valor):
    if pd.isna(valor):
        return "R$ 0,00"

    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"


def formatar_kwh(valor):
    if pd.isna(valor):
        return "0 kWh"

    try:
        return f"{float(valor):,.0f} kWh".replace(",", ".")
    except (ValueError, TypeError):
        return "0 kWh"


def formatar_percentual(valor):
    if pd.isna(valor):
        return "0,0%"

    try:
        return f"{float(valor):.1f}%".replace(".", ",")
    except (ValueError, TypeError):
        return "0,0%"
