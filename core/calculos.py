```python
"""
Motor de cálculo da Calculadora Steel Framing.

As fórmulas deste módulo ficam separadas da interface do Streamlit.
Isso permite futuramente utilizar o mesmo motor em:
- aplicativo Android;
- aplicativo desktop;
- API;
- versão web;
- geração de orçamento.
"""

import math

from .dados import (
    COEFICIENTES,
    PRECOS_BASE,
    CONFIGURACAO_PROJETO,
)


def calcular_area(comprimento, altura):
    """
    Calcula a área da parede.

    Fórmula:
        área = comprimento × altura
    """
    if comprimento <= 0 or altura <= 0:
        raise ValueError("Comprimento e altura devem ser maiores que zero.")

    return comprimento * altura


def calcular_quantidade_material(area, coeficiente):
    """
    Calcula a quantidade de material com base na área.

    quantidade = área × coeficiente
    """
    if area <= 0:
        return 0.0

    return area * coeficiente


def calcular_custo_material(quantidade, preco_unitario):
    """
    Calcula o custo individual de um material.
    """
    return quantidade * preco_unitario


def calcular_materiais(area, coeficientes=None, precos=None):
    """
    Calcula quantidades e custos de todos os materiais.

    Retorna um dicionário contendo:
        material
        quantidade
        preço unitário
        custo total
    """

    if coeficientes is None:
        coeficientes = COEFICIENTES

    if precos is None:
        precos = PRECOS_BASE

    materiais = {}

    for nome, coeficiente in coeficientes.items():

        preco = precos.get(nome, 0.0)

        quantidade = calcular_quantidade_material(
            area,
            coeficiente
        )

        custo = calcular_custo_material(
            quantidade,
            preco
        )

        materiais[nome] = {
            "quantidade": quantidade,
            "preco_unitario": preco,
            "custo": custo,
        }

    return materiais


def calcular_subtotal_materiais(materiais):
    """
    Soma o custo de todos os materiais.
    """

    return sum(
        item["custo"]
        for item in materiais.values()
    )


def calcular_massas_telas(subtotal_materiais):
    """
    Calcula massas e telas.

    Regra atual:
        5% do subtotal dos materiais.
    """

    percentual = CONFIGURACAO_PROJETO[
        "percentual_massas_telas"
    ]

    return subtotal_materiais * percentual


def calcular_mao_de_obra(area, diaria=None):
    """
    Calcula a mão de obra.

    Regra atual:

        dias = área ÷ 90 × 30

        custo = dias × diária
    """

    if diaria is None:
        diaria = CONFIGURACAO_PROJETO[
            "diaria_mao_de_obra"
        ]

    area_referencia = CONFIGURACAO_PROJETO[
        "area_referencia_mao_de_obra"
    ]

    coeficiente_dias = CONFIGURACAO_PROJETO[
        "coeficiente_dias_mao_de_obra"
    ]

    dias = (
        area / area_referencia
    ) * coeficiente_dias

    custo = dias * diaria

    return {
        "dias": dias,
        "diaria": diaria,
        "custo": custo,
    }


def calcular_projeto(
    comprimento,
    altura,
    diaria=None,
    coeficientes=None,
    precos=None,
):
    """
    Executa o cálculo completo do projeto.
    """

    area = calcular_area(
        comprimento,
        altura
    )

    materiais = calcular_materiais(
        area,
        coeficientes=coeficientes,
        precos=precos,
    )

    subtotal_materiais = calcular_subtotal_materiais(
        materiais
    )

    massas_telas = calcular_massas_telas(
        subtotal_materiais
    )

    mao_de_obra = calcular_mao_de_obra(
        area,
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
        "materiais": materiais,
        "subtotal_materiais": subtotal_materiais,
        "massas_telas": massas_telas,
        "mao_de_obra": mao_de_obra,
        "custo_geral": custo_geral,
    }


def calcular_resumo(
    comprimento,
    altura,
    diaria=None,
    coeficientes=None,
    precos=None,
):
    """
    Retorna somente os principais resultados
    para utilização em telas de resumo.
    """

    projeto = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        diaria=diaria,
        coeficientes=coeficientes,
        precos=precos,
    )

    return {
        "Área": projeto["area"],
        "Materiais": projeto["subtotal_materiais"],
        "Massas e Telas": projeto["massas_telas"],
        "Mão de Obra": projeto["mao_de_obra"]["custo"],
        "Custo Geral": projeto["custo_geral"],
    }
```
