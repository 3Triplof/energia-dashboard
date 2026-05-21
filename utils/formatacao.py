import pandas as pd


# =========================
# CONVERSÃO
# =========================

def converter_valor(valor):

    # Nulo
    if pd.isna(valor):
        return 0

    # Já numérico
    if isinstance(valor, (int, float)):
        return float(valor)

    valor = str(valor).strip()

    if valor == '':
        return 0

    # Remove moeda e espaços
    valor = (
        valor
        .replace('R$', '')
        .replace(' ', '')
    )

    # =========================
    # FORMATO BR
    # 1.234,56
    # =========================

    if ',' in valor and '.' in valor:

        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')

    # =========================
    # FORMATO:
    # 34,56
    # =========================

    elif ',' in valor:

        valor = valor.replace(',', '.')

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
