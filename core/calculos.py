"""
Motor de cálculo da Calculadora Steel Framing.

Este módulo concentra toda a lógica matemática do aplicativo.
A interface gráfica fica nas páginas do Streamlit.
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
    Calcula a área do projeto.

    Fórmula:
        área = comprimento × altura
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
    Calcula a quantidade automática do material.

    Metodologia atual:

        quantidade =
        (área do projeto ÷ área de referência)
        × coeficiente

    A área de referência padrão é 30 m².
    """

    if area <= 0:
        return 0.0

    area_referencia = CONFIGURACAO_PROJETO.get(
        "area_referencia",
        30.00,
    )

    if area_referencia <= 0:
        raise ValueError(
            "A área de referência deve ser maior que zero."
        )

    return (
        area / area_referencia
    ) * coeficiente


def calcular_custo_material(
    quantidade,
    preco_unitario,
):
    """
    Calcula o custo total de um material.

    Fórmula:
        quantidade × preço unitário
    """

    return quantidade * preco_unitario


def calcular_materiais(
    area,
    materiais=None,
    precos=None,
    quantidades=None,
):
    """
    Calcula quantitativo e custo dos materiais.

    O sistema calcula automaticamente a quantidade.

    Se uma quantidade manual for informada,
    ela substitui a quantidade automática.

    Os preços personalizados têm prioridade
    sobre os preços padrão.
    """

    if materiais is None:
        materiais = MATERIAIS

    if quantidades is None:
        quantidades = {}

    resultado = {}

    for nome, dados in materiais.items():

        # ----------------------------------------------------
        # MATERIAL ATIVO
        # ----------------------------------------------------

        if not dados.get("ativo", True):
            continue

        # ----------------------------------------------------
        # COEFICIENTE
        # ----------------------------------------------------

        coeficiente = dados.get(
            "coeficiente",
            0.0,
        )

        # ----------------------------------------------------
        # PREÇO
        # ----------------------------------------------------

        preco = dados.get(
            "preco",
            0.0,
        )

        if precos is not None and nome in precos:
            preco = precos[nome]

        # ----------------------------------------------------
        # QUANTIDADE AUTOMÁTICA
        # ----------------------------------------------------

        quantidade_automatica = (
            calcular_quantidade_material(
                area=area,
                coeficiente=coeficiente,
            )
        )

        # ----------------------------------------------------
        # QUANTIDADE FINAL
        # ----------------------------------------------------

        if nome in quantidades:
            quantidade = float(
                quantidades[nome]
            )
        else:
            quantidade = quantidade_automatica

        # ----------------------------------------------------
        # CUSTO
        # ----------------------------------------------------

        custo = calcular_custo_material(
            quantidade=quantidade,
            preco_unitario=preco,
        )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        resultado[nome] = {
            "quantidade": quantidade,
            "quantidade_automatica": quantidade_automatica,
            "preco_unitario": preco,
            "custo": custo,
            "unidade": dados.get(
                "unidade",
                "un",
            ),
            "categoria": dados.get(
                "categoria",
                "Outros",
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
    Calcula o custo de Massas e Telas.

    Se um valor manual for informado,
    ele será utilizado.

    Caso contrário, utiliza o percentual
    definido em CONFIGURACAO_PROJETO.
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

    O número de dias é proporcional à área.
    """

    if area <= 0:
        return {
            "dias": 0.0,
            "diaria": diaria or 0.0,
            "custo": 0.0,
        }

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

    if area_referencia <= 0:
        raise ValueError(
            "A área de referência deve ser maior que zero."
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
# PROJETO COMPLETO
# ============================================================

def calcular_projeto(
    comprimento,
    altura,
    diaria=None,
    precos=None,
    materiais=None,
    quantidades=None,
    valor_massas_telas=None,
):
    """
    Executa todos os cálculos do projeto.

    Retorna:
        área
        materiais
        subtotal dos materiais
        massas e telas
        mão de obra
        custo geral
    """

    # --------------------------------------------------------
    # ÁREA
    # --------------------------------------------------------

    area = calcular_area(
        comprimento=comprimento,
        altura=altura,
    )

    # --------------------------------------------------------
    # MATERIAIS
    # --------------------------------------------------------

    materiais_calculados = calcular_materiais(
        area=area,
        materiais=materiais,
        precos=precos,
        quantidades=quantidades,
    )

    subtotal_materiais = (
        calcular_subtotal_materiais(
            materiais_calculados
        )
    )

    # --------------------------------------------------------
    # MASSAS E TELAS
    # --------------------------------------------------------

    massas_telas = calcular_massas_telas(
        subtotal_materiais=subtotal_materiais,
        valor_manual=valor_massas_telas,
    )

    # --------------------------------------------------------
    # MÃO DE OBRA
    # --------------------------------------------------------

    mao_de_obra = calcular_mao_de_obra(
        area=area,
        diaria=diaria,
    )

    # --------------------------------------------------------
    # CUSTO GERAL
    # --------------------------------------------------------

    custo_geral = (
        subtotal_materiais
        + massas_telas
        + mao_de_obra["custo"]
    )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

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
    quantidades=None,
    valor_massas_telas=None,
):
    """
    Retorna somente os principais indicadores
    do projeto.
    """

    projeto = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        diaria=diaria,
        precos=precos,
        materiais=materiais,
        quantidades=quantidades,
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
