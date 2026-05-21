import pandas as pd


# =========================
# CONVERSÃO
# =========================

import pandas as pd
import re


def converter_valor(valor):

    # =========================
    # NULO
    # =========================

    if pd.isna(valor):
        return 0

    # =========================
    # JÁ NUMÉRICO
    # =========================

    if isinstance(valor, (int, float)):
        return float(valor)

    valor = str(valor).strip()

    if valor == '':
        return 0

    # Remove moeda/espaços
    valor = (
        valor
        .replace('R$', '')
        .replace(' ', '')
    )

    # =========================
    # CASO:
    # 1.234,56
    # (milhar BR)
    # =========================

    if re.match(r'^\d{1,3}(\.\d{3})*,\d+$', valor):

        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')

    # =========================
    # CASO:
    # 17,23
    # decimal BR
    # =========================

    elif ',' in valor and '.' not in valor:

        valor = valor.replace(',', '.')

    # =========================
    # CASO:
    # 17.23
    # decimal correto
    # NÃO FAZ NADA
    # =========================

    try:
        return float(valor)

    except:
        return 0

# =========================
# FORMATAÇÕES
# =========================

def formatar_moeda(valor):

    return (
        f'R$ {valor:,.2f}'
        .replace(',', 'X')
        .replace('.', ',')
        .replace('X', '.')
    )


def formatar_kwh(valor):

    return (
        f'{valor:,.0f} kWh'
        .replace(',', '.')
    )


def formatar_percentual(valor):

    return f'{valor:.1f}%'
