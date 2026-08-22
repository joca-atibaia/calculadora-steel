"""
Motor de cálculos da Calculadora Steel Framing.

Este arquivo contém somente regras de cálculo.
A interface do Streamlit fica separada.
"""

import math


def calcular_area(comprimento: float, altura: float) -> float:
    """Calcula a área da parede."""
    return comprimento * altura


def calcular_perfis(
    comprimento: float,
    altura: float,
    espacamento: float = 0.40,
) -> dict:
    """
    Calcula quantidade aproximada de montantes e guias.

    comprimento e altura em metros.
    espacamento em metros.
    """

    if comprimento <= 0 or altura <= 0:
        raise ValueError("Comprimento e altura devem ser maiores que zero.")

    if espacamento <= 0:
        raise ValueError("O espaçamento deve ser maior que zero.")

    montantes = math.ceil(comprimento / espacamento) + 1

    guias = math.ceil(comprimento / 3.0) * 2

    return {
        "montantes": montantes,
        "guias": guias,
    }


def calcular_placas(
    area: float,
    largura_placa: float = 1.20,
    altura_placa: float = 1.80,
) -> int:
    """Calcula quantidade de placas necessárias."""

    if area <= 0:
        return 0

    area_placa = largura_placa * altura_placa

    return math.ceil(area / area_placa)


def calcular_material(
    quantidade: float,
    preco_unitario: float,
) -> float:
    """Calcula o custo de um material."""

    return quantidade * preco_unitario


def calcular_custo_total(
    materiais: list,
    mao_de_obra: float = 0.0,
) -> float:
    """
    Soma os custos dos materiais e da mão de obra.

    Cada item de materiais deve possuir:
        quantidade
        preco
    """

    total_materiais = 0.0

    for material in materiais:
        quantidade = float(material.get("quantidade", 0))
        preco = float(material.get("preco", 0))

        total_materiais += quantidade * preco

    return total_materiais + float(mao_de_obra)


def calcular_projeto(
    comprimento: float,
    altura: float,
    espacamento: float = 0.40,
) -> dict:
    """
    Executa os principais cálculos de um projeto.
    """

    area = calcular_area(comprimento, altura)

    perfis = calcular_perfis(
        comprimento,
        altura,
        espacamento,
    )

    placas = calcular_placas(area)

    return {
        "comprimento": comprimento,
        "altura": altura,
        "area": area,
        "montantes": perfis["montantes"],
        "guias": perfis["guias"],
        "placas": placas,
    }
