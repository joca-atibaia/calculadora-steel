COEFICIENTES = {
    "Perfil 90x0,80": 113.0 / 30.0,
    "Guia Perimetral": 20.0 / 30.0,
    "Plywood 8mm": 60.0 / 90.0,
    "Placa ST 12.5mm": 36.0 / 90.0,
    "Placa Cimentícia 12mm": 36.0 / 90.0,
    "Lã PET": 6.0 / 90.0,
    "Parafusos": 80.0,
    "Cola PU 40": 36.0 / 90.0,
    "Manta Hidrófuga": 3.0 / 90.0,
}


PRECOS_BASE = {
    "Perfil 90x0,80": 50.0,
    "Guia Perimetral": 50.0,
    "Plywood 8mm": 80.0,
    "Placa ST 12.5mm": 40.0,
    "Placa Cimentícia 12mm": 140.0,
    "Lã PET": 200.0,
    "Parafusos": 0.07,
    "Cola PU 40": 40.0,
    "Manta Hidrófuga": 500.0,
}


CONFIGURACAO_PROJETO = {
    "comprimento_padrao": 30.00,
    "altura_padrao": 3.00,
    "diaria_mao_de_obra": 755.0,
    "coeficiente_dias_mao_de_obra": 30.0,
    "area_referencia_mao_de_obra": 90.0,
    "percentual_massas_telas": 0.05,
}


def obter_coeficientes():
    return COEFICIENTES.copy()


def obter_precos():
    return PRECOS_BASE.copy()


def obter_configuracao():
    return CONFIGURACAO_PROJETO.copy()
