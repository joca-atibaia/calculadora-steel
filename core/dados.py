# Catálogo padrão de materiais da Calculadora Steel
#
# "base" define sobre qual dimensão o consumo é calculado:
# - comprimento: materiais relacionados ao comprimento do projeto
# - area: materiais relacionados à área do projeto
#
# "consumo_referencia" representa a quantidade utilizada
# na dimensão indicada em "referencia".

MATERIAIS = {
    "Perfil 90x0,80": {
        "base": "comprimento",
        "consumo_referencia": 113.0,
        "referencia": 30.0,
        "unidade": "un",
        "preco": 60.0,
    },
    "Guia Perimetral": {
        "base": "comprimento",
        "consumo_referencia": 20.0,
        "referencia": 30.0,
        "unidade": "m",
        "preco": 50.0,
    },
    "Plywood 8mm": {
        "base": "area",
        "consumo_referencia": 20.0,
        "referencia": 90.0,
        "unidade": "chapa",
        "preco": 80.0,
    },
    "Placa ST 12.5mm": {
        "base": "area",
        "consumo_referencia": 12.0,
        "referencia": 90.0,
        "unidade": "chapa",
        "preco": 40.0,
    },
    "Placa Cimentícia 12mm": {
        "base": "area",
        "consumo_referencia": 12.0,
        "referencia": 90.0,
        "unidade": "chapa",
        "preco": 140.0,
    },
    "Lã PET": {
        "base": "area",
        "consumo_referencia": 2.0,
        "referencia": 90.0,
        "unidade": "pacote",
        "preco": 200.0,
    },
    "Parafusos": {
        "base": "area",
        "consumo_referencia": 2400.0,
        "referencia": 90.0,
        "unidade": "un",
        "preco": 0.07,
    },
    "Cola PU 40": {
        "base": "area",
        "consumo_referencia": 12.0,
        "referencia": 90.0,
        "unidade": "un",
        "preco": 40.0,
    },
    "Manta Hidrófuga": {
        "base": "area",
        "consumo_referencia": 1.0,
        "referencia": 90.0,
        "unidade": "rolo",
        "preco": 500.0,
    },
}


# Compatibilidade com a interface atual.
# A página Materiais ainda utiliza estes dicionários.
COEFICIENTES = {
    nome: dados["consumo_referencia"] / dados["referencia"]
    for nome, dados in MATERIAIS.items()
}


PRECOS_BASE = {
    nome: dados["preco"]
    for nome, dados in MATERIAIS.items()
}


CONFIGURACAO_PROJETO = {
    "comprimento_padrao": 30.00,
    "altura_padrao": 3.00,
    "diaria_mao_de_obra": 755.0,
    "coeficiente_dias_mao_de_obra": 30.0,
    "area_referencia_mao_de_obra": 90.0,
    "percentual_massas_telas": 0.05,
}


def obter_materiais():
    return {
        nome: dados.copy()
        for nome, dados in MATERIAIS.items()
    }


def obter_coeficientes():
    return COEFICIENTES.copy()


def obter_precos():
    return PRECOS_BASE.copy()


def obter_configuracao():
    return CONFIGURACAO_PROJETO.copy()
