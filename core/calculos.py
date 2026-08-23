"""
Motor de cálculo da Calculadora Profissional de Steel Frame.

Este módulo contém somente as regras matemáticas do aplicativo.
A interface fica nas páginas do Streamlit.
"""

from .dados import (
    MATERIAIS,
    CONFIGURACAO_PROJETO,
)


# ============================================================
# PROJETO
# ============================================================

def calcular_area(comprimento, altura):
    """
    Calcula a área da parede.

    Área = comprimento × altura
    """
    if comprimento <= 0 or altura <= 0:
        raise ValueError(
            "Comprimento e altura devem ser maiores que zero."
        )

    return comprimento * altura


# ============================================================
# MATERIAIS
# ============================================================

def calcular_quantidade_material(
    area,
    coeficiente,
):
    """
    Calcula a quantidade do material com base
    na área e no coeficiente cadastrado.

    A metodologia atual da calculadora é preservada:
    
        quantidade = área × coeficiente
    """
    if area <= 0:
        return 0.0

    return area * coeficiente


def calcular_custo_material(
    quantidade,
    preco_unitario,
):
    """
    Calcula o custo de um material.
    """
    return quantidade * preco_unitario


def calcular_materiais(
    area,
    materiais=None,
    precos=None,
):
    """
    Calcula quantitativo e custo de todos os materiais ativos.

    Permite receber preços personalizados sem alterar
    o catálogo padrão.
    """

    if materiais is None:
        materiais = MATERIAIS

    resultado = {}

    for nome, dados in materiais.items():

        # Ignora materiais desativados
        if not dados.get("ativo", True):
            continue

        coeficiente = dados.get(
            "coeficiente",
            0.0
        )

        preco = dados.get(
            "preco",
            0.0
        )

        # Se a interface enviar preços personalizados,
        # eles têm prioridade.
        if precos and nome in precos:
            preco = precos[nome]

        quantidade = calcular_quantidade_material(
            area=area,
            coeficiente=coeficiente,
        )

        custo = calcular_custo_material(
            quantidade=quantidade,
            preco_unitario=preco,
        )

        resultado[nome] = {
            "quantidade": quantidade,
            "preco_unitario": preco,
            "custo": custo,
            "unidade": dados.get(
                "unidade",
                "un"
            ),
            "categoria": dados.get(
                "categoria",
                "Outros"
            ),
        }

    return resultado


def calcular_subtotal_materiais(materiais):
    """
    Soma o custo de todos os materiais.
    """
    return sum(
        item["custo"]
        for item in materiais.values()
    )


# ============================================================
# MASSAS E TELAS
# ============================================================

def calcular_massas_telas(
    subtotal_materiais,
    valor_manual=None,
):
    """
    Calcula Massas e Telas.

    Por padrão utiliza o percentual configurado.
    Se o profissional informar um valor manual,
    esse valor prevalece.
    """

    if valor_manual is not None:
        return float(valor_manual)

    percentual = CONFIGURACAO_PROJETO.get(
        "percentual_massas_telas",
        0.05,
    )

    return subtotal_materiais * percentual


# ============================================================
# MÃO DE OBRA
# ============================================================

def calcular_mao_de_obra(
    area,
    diaria=None,
):
    """
    Calcula a mão de obra.

    A quantidade de dias permanece proporcional
    à área do projeto.
    """

    if diaria is None:
        diaria = CONFIGURACAO_PROJETO.get(
            "diaria_mao_de_obra",
            755.00,
        )

    area_referencia = CONFIGURACAO_PROJETO.get(
        "area_referencia",
        30.00,
    )

    dias_referencia = CONFIGURACAO_PROJETO.get(
        "dias_mao_de_obra_referencia",
        10.00,
    )

    dias = (
        area / area_referencia
    ) * dias_referencia

    custo = dias * diaria

    return {
        "dias": dias,
        "diaria": diaria,
        "custo": custo,
    }


# ============================================================
# CÁLCULO COMPLETO DO PROJETO
# ============================================================

def calcular_projeto(
    comprimento,
    altura,
    diaria=None,
    precos=None,
    materiais=None,
    valor_massas_telas=None,
):
    """
    Executa todos os cálculos do projeto.
    """

    area = calcular_area(
        comprimento,
        altura,
    )

    materiais_calculados = calcular_materiais(
        area=area,
        materiais=materiais,
        precos=precos,
    )

    subtotal_materiais = (
        calcular_subtotal_materiais(
            materiais_calculados
        )
    )

    massas_telas = calcular_massas_telas(
        subtotal_materiais=subtotal_materiais,
        valor_manual=valor_massas_telas,
    )

    mao_de_obra = calcular_mao_de_obra(
        area=area,
        diaria=diaria,
    )

    custo_geral = (
        subtotal_materiais
        + massas_telas
        + mao_de_obra["custo"]
    )

    return {
        "comprimento": comprimento,
        "altura": altura,
        "area": area,
        "materiais": materiais_calculados,
        "subtotal_materiais": subtotal_materiais,
        "massas_telas": massas_telas,
        "mao_de_obra": mao_de_obra,
        "custo_geral": custo_geral,
    }


# ============================================================
# RESUMO
# ============================================================

def calcular_resumo(
    comprimento,
    altura,
    diaria=None,
    precos=None,
    materiais=None,
    valor_massas_telas=None,
):
    """
    Retorna apenas os principais valores
    para apresentação no dashboard.
    """

    projeto = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        diaria=diaria,
        precos=precos,
        materiais=materiais,
        valor_massas_telas=valor_massas_telas,
    )

    return {
        "Área": projeto["area"],
        "Materiais": projeto[
            "subtotal_materiais"
        ],
        "Massas e Telas": projeto[
            "massas_telas"
        ],
        "Mão de Obra": projeto[
            "mao_de_obra"
        ]["custo"],
        "Custo Geral": projeto[
            "custo_geral"
        ],
    }
