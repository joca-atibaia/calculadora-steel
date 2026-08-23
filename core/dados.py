"""
Catálogo de materiais e parâmetros padrão
da Calculadora Profissional de Steel Frame.

IMPORTANTE:
Os valores abaixo são parâmetros padrão.
O usuário poderá alterá-los na interface
conforme sua realidade de obra.
"""

# ============================================================
# CONFIGURAÇÕES GERAIS
# ============================================================

CONFIGURACAO_PROJETO = {
    "diaria_mao_de_obra": 755.00,
    "dias_mao_de_obra_referencia": 10.00,
    "area_referencia": 30.00,
    "percentual_massas_telas": 0.05,
}


# ============================================================
# CATÁLOGO DE MATERIAIS
# ============================================================

MATERIAIS = {

    "Perfil 90x0,80": {
        "categoria": "Estrutura",
        "unidade": "un",
        "coeficiente": 113.00,
        "preco": 60.00,
        "ativo": True,
    },

    "Guia Perimetral": {
        "categoria": "Estrutura",
        "unidade": "m",
        "coeficiente": 20.00,
        "preco": 50.00,
        "ativo": True,
    },

    "Plywood 8mm": {
        "categoria": "Fechamento",
        "unidade": "chapa",
        "coeficiente": 20.00,
        "preco": 80.00,
        "ativo": True,
    },

    "Placa ST 12.5mm": {
        "categoria": "Drywall",
        "unidade": "chapa",
        "coeficiente": 12.00,
        "preco": 40.00,
        "ativo": True,
    },

    "Placa Cimentícia 12mm": {
        "categoria": "Fechamento",
        "unidade": "chapa",
        "coeficiente": 12.00,
        "preco": 140.00,
        "ativo": True,
    },

    "Lã PET": {
        "categoria": "Isolamento",
        "unidade": "pacote",
        "coeficiente": 2.00,
        "preco": 200.00,
        "ativo": True,
    },

    "Parafusos": {
        "categoria": "Fixação",
        "unidade": "un",
        "coeficiente": 2400.00,
        "preco": 0.07,
        "ativo": True,
    },

    "Cola PU 40": {
        "categoria": "Fixação",
        "unidade": "un",
        "coeficiente": 12.00,
        "preco": 40.00,
        "ativo": True,
    },

    "Manta Hidrófuga": {
        "categoria": "Impermeabilização",
        "unidade": "rolo",
        "coeficiente": 1.00,
        "preco": 500.00,
        "ativo": True,
    },
}


# ============================================================
# COMPATIBILIDADE COM A VERSÃO ATUAL DO APLICATIVO
# ============================================================

COEFICIENTES = {
    nome: dados["coeficiente"]
    for nome, dados in MATERIAIS.items()
}


PRECOS_BASE = {
    nome: dados["preco"]
    for nome, dados in MATERIAIS.items()
}


# ============================================================
# FUNÇÕES DE ACESSO
# ============================================================

def obter_materiais():
    """
    Retorna uma cópia do catálogo de materiais.
    """
    return {
        nome: dados.copy()
        for nome, dados in MATERIAIS.items()
    }


def obter_materiais_ativos():
    """
    Retorna somente os materiais ativos.
    """
    return {
        nome: dados.copy()
        for nome, dados in MATERIAIS.items()
        if dados.get("ativo", True)
    }


def obter_coeficientes():
    """
    Retorna os coeficientes padrão.
    """
    return COEFICIENTES.copy()


def obter_precos():
    """
    Retorna os preços padrão.
    """
    return PRECOS_BASE.copy()


def obter_configuracao():
    """
    Retorna as configurações gerais do projeto.
    """
    return CONFIGURACAO_PROJETO.copy()
