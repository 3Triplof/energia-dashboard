import pandas as pd

# =========================
# CONVERSÃO BR
# =========================

def converter_valor(valor):

    if pd.isna(valor):
        return 0

    valor = str(valor).strip()

    if valor == '':
        return 0

    valor = valor.replace('.', '')

    valor = valor.replace(',', '.')

    try:
        return float(valor)
    except:
        return 0


# =========================
# FORMATAÇÃO MOEDA
# =========================

def formatar_moeda(valor):

    return f"R$ {valor:,.2f}"\
        .replace(",", "X")\
        .replace(".", ",")\
        .replace("X", ".")


# =========================
# FORMATAÇÃO KWH
# =========================

def formatar_kwh(valor):

    return f"{valor:,.0f} kWh"\
        .replace(",", ".")


# =========================
# FORMATAÇÃO %
# =========================

def formatar_percentual(valor):

    return f"{valor:.1f}%"
