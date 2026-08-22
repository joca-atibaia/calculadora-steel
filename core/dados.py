"""
Dados padrão da Calculadora Steel Framing.

Os valores abaixo são apenas valores iniciais.
Depois vamos transferir para cá os valores reais
que já existem na sua calculadora atual.
"""

MATERIAIS_PADRAO = {
    "Perfil Montante": {
        "unidade": "barra",
        "comprimento": 3.00,
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Perfil Guia": {
        "unidade": "barra",
        "comprimento": 3.00,
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Placa de Drywall": {
        "unidade": "un",
        "largura": 1.20,
        "altura": 1.80,
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Plywood": {
        "unidade": "un",
        "largura": 1.22,
        "altura": 2.44,
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Lã Mineral": {
        "unidade": "m²",
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Manta": {
        "unidade": "m²",
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Parafusos": {
        "unidade": "un",
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Massa": {
        "unidade": "kg",
        "coeficiente": 0.0,
        "preco": 0.0,
    },

    "Tela": {
        "unidade": "m",
        "coeficiente": 0.0,
        "preco": 0.0,
    },
}


def obter_materiais():
    """Retorna uma cópia dos materiais padrão."""
    return MATERIAIS_PADRAO.copy()
