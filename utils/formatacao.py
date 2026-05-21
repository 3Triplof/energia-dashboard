import pandas as pd


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
    # Ex:
    # 1.234,56
    # =========================

    if ',' in valor and '.' in valor:

        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')

    # =========================
    # FORMATO BR SIMPLES
    # Ex:
    # 34,56
    # =========================

    elif ',' in valor:

        valor = valor.replace(',', '.')

    # =========================
    # IMPORTANTE:
    # NÃO remove ponto
    # se já estiver correto:
    # 34.03
    # =========================

    try:
        return float(valor)

    except:
        return 0
