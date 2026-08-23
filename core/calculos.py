"""
Motor de cálculo da Calculadora Profissional de Steel Framing.

Versão 6B

Responsável por:
- cálculo da área;
- cálculo automático dos materiais;
- alteração manual das quantidades;
- alteração dos preços;
- cálculo de massas e telas;
- cálculo de mão de obra;
- custo total;
- indicadores financeiros.

A interface gráfica fica nas páginas do Streamlit.
"""

from .dados import (
    MATERIAIS,
    CONFIGURACAO_PROJETO,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def _numero(valor, padrao=0.0):
    """
    Converte um valor para float com segurança.
    """

    if valor is None:
        return float(padrao)

    try:
        return float(valor)

    except (TypeError, ValueError):
        return float(padrao)


def _validar_positivo(valor, nome):
    """
    Valida se um valor é maior que zero.
    """

    valor = _numero(valor)

    if valor <= 0:
        raise ValueError(
            f"{nome} deve ser maior que zero."
        )

    return valor


# ============================================================
# ÁREA DO PROJETO
# ============================================================

def calcular_area(comprimento, altura):
    """
    Calcula a área do projeto.

    Fórmula:

        área = comprimento × altura
    """

    comprimento = _validar_positivo(
        comprimento,
        "Comprimento",
    )

    altura = _validar_positivo(
        altura,
        "Altura",
    )

    return comprimento * altura


# ============================================================
# QUANTIDADE AUTOMÁTICA DE MATERIAL
# ============================================================

def calcular_quantidade_material(
    area,
    coeficiente,
):
    """
    Calcula a quantidade automática de um material.

    Fórmula:

        quantidade =
            (área ÷ área de referência)
            × coeficiente

    A área de referência vem de:

        CONFIGURACAO_PROJETO["area_referencia"]
    """

    area = _numero(area)

    coeficiente = _numero(
        coeficiente
    )

    if area <= 0:
        return 0.0

    if coeficiente < 0:
        raise ValueError(
            "O coeficiente do material "
            "não pode ser negativo."
        )

    area_referencia = _numero(
        CONFIGURACAO_PROJETO.get(
            "area_referencia",
            30.00,
        )
    )

    if area_referencia <= 0:
        raise ValueError(
            "A área de referência "
            "deve ser maior que zero."
        )

    return (
        area / area_referencia
    ) * coeficiente


# ============================================================
# CUSTO DE MATERIAL
# ============================================================

def calcular_custo_material(
    quantidade,
    preco_unitario,
):
    """
    Calcula:

        custo = quantidade × preço unitário
    """

    quantidade = _numero(
        quantidade
    )

    preco_unitario = _numero(
        preco_unitario
    )

    if quantidade < 0:
        raise ValueError(
            "A quantidade não pode ser negativa."
        )

    if preco_unitario < 0:
        raise ValueError(
            "O preço unitário não pode ser negativo."
        )

    return (
        quantidade *
        preco_unitario
    )


# ============================================================
# MATERIAIS
# ============================================================

def calcular_materiais(
    area,
    materiais=None,
    precos=None,
    quantidades=None,
):
    """
    Calcula quantitativo e custo dos materiais.

    Regras:

    1. Materiais inativos não entram.

    2. O coeficiente cadastrado em dados.py
       determina a quantidade automática.

    3. Se houver quantidade manual,
       ela substitui a automática.

    4. Se houver preço personalizado,
       ele substitui o preço padrão.

    5. O resultado mantém informações
       necessárias para a interface,
       PDF e Excel.
    """

    area = _numero(area)

    if materiais is None:
        materiais = MATERIAIS

    if precos is None:
        precos = {}

    if quantidades is None:
        quantidades = {}

    resultado = {}

    for nome, dados in materiais.items():

        # ----------------------------------------------------
        # SEGURANÇA
        # ----------------------------------------------------

        if not isinstance(
            dados,
            dict,
        ):
            continue

        # ----------------------------------------------------
        # MATERIAL ATIVO
        # ----------------------------------------------------

        if not dados.get(
            "ativo",
            True,
        ):
            continue

        # ----------------------------------------------------
        # COEFICIENTE
        # ----------------------------------------------------

        coeficiente = _numero(
            dados.get(
                "coeficiente",
                0.0,
            )
        )

        # ----------------------------------------------------
        # PREÇO PADRÃO
        # ----------------------------------------------------

        preco_padrao = _numero(
            dados.get(
                "preco",
                0.0,
            )
        )

        # ----------------------------------------------------
        # PREÇO FINAL
        # ----------------------------------------------------

        if nome in precos:

            preco = _numero(
                precos[nome],
                preco_padrao,
            )

        else:

            preco = preco_padrao

        if preco < 0:
            raise ValueError(
                f"O preço do material "
                f"'{nome}' não pode ser negativo."
            )

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

        possui_quantidade_manual = (
            nome in quantidades
        )

        if possui_quantidade_manual:

            quantidade = _numero(
                quantidades[nome],
                quantidade_automatica,
            )

            if quantidade < 0:
                raise ValueError(
                    f"A quantidade do material "
                    f"'{nome}' não pode ser negativa."
                )

            origem_quantidade = "manual"

        else:

            quantidade = (
                quantidade_automatica
            )

            origem_quantidade = "automática"

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

            "quantidade":
                quantidade,

            "quantidade_automatica":
                quantidade_automatica,

            "quantidade_manual":
                possui_quantidade_manual,

            "origem_quantidade":
                origem_quantidade,

            "coeficiente":
                coeficiente,

            "preco_unitario":
                preco,

            "preco_padrao":
                preco_padrao,

            "preco_personalizado":
                nome in precos,

            "custo":
                custo,

            "unidade":
                dados.get(
                    "unidade",
                    "un",
                ),

            "categoria":
                dados.get(
                    "categoria",
                    "Outros",
                ),
        }

    return resultado


# ============================================================
# SUBTOTAL DOS MATERIAIS
# ============================================================

def calcular_subtotal_materiais(
    materiais,
):
    """
    Soma o custo de todos os materiais.
    """

    if not materiais:
        return 0.0

    subtotal = 0.0

    for item in materiais.values():

        if not isinstance(
            item,
            dict,
        ):
            continue

        subtotal += _numero(
            item.get(
                "custo",
                0.0,
            )
        )

    return subtotal


# ============================================================
# MASSAS E TELAS
# ============================================================

def calcular_massas_telas(
    subtotal_materiais,
    valor_manual=None,
):
    """
    Calcula o custo de Massas e Telas.

    Se valor_manual for informado,
    utiliza esse valor.

    Caso contrário:

        subtotal × percentual
    """

    subtotal_materiais = _numero(
        subtotal_materiais
    )

    # --------------------------------------------------------
    # VALOR MANUAL
    # --------------------------------------------------------

    if valor_manual is not None:

        valor = _numero(
            valor_manual
        )

        if valor < 0:
            raise ValueError(
                "O valor de Massas e Telas "
                "não pode ser negativo."
            )

        return valor

    # --------------------------------------------------------
    # PERCENTUAL
    # --------------------------------------------------------

    percentual = _numero(
        CONFIGURACAO_PROJETO.get(
            "percentual_massas_telas",
            0.05,
        )
    )

    if percentual < 0:
        raise ValueError(
            "O percentual de Massas e Telas "
            "não pode ser negativo."
        )

    return (
        subtotal_materiais *
        percentual
    )


# ============================================================
# MÃO DE OBRA
# ============================================================

def calcular_mao_de_obra(
    area,
    diaria=None,
):
    """
    Calcula a mão de obra.

    Fórmula:

        dias =
            (área ÷ área de referência)
            × dias de referência

        custo =
            dias × diária
    """

    area = _numero(area)

    # --------------------------------------------------------
    # DIÁRIA
    # --------------------------------------------------------

    if diaria is None:

        diaria_final = _numero(
            CONFIGURACAO_PROJETO.get(
                "diaria_mao_de_obra",
                755.00,
            )
        )

    else:

        diaria_final = _numero(
            diaria
        )

    if diaria_final < 0:
        raise ValueError(
            "A diária de mão de obra "
            "não pode ser negativa."
        )

    # --------------------------------------------------------
    # SEM ÁREA
    # --------------------------------------------------------

    if area <= 0:

        return {
            "dias": 0.0,
            "diaria": diaria_final,
            "custo": 0.0,
        }

    # --------------------------------------------------------
    # ÁREA DE REFERÊNCIA
    # --------------------------------------------------------

    area_referencia = _numero(
        CONFIGURACAO_PROJETO.get(
            "area_referencia",
            30.00,
        )
    )

    if area_referencia <= 0:
        raise ValueError(
            "A área de referência "
            "deve ser maior que zero."
        )

    # --------------------------------------------------------
    # DIAS DE REFERÊNCIA
    # --------------------------------------------------------

    dias_referencia = _numero(
        CONFIGURACAO_PROJETO.get(
            "dias_mao_de_obra_referencia",
            10.00,
        )
    )

    if dias_referencia < 0:
        raise ValueError(
            "Os dias de mão de obra "
            "não podem ser negativos."
        )

    # --------------------------------------------------------
    # DIAS CALCULADOS
    # --------------------------------------------------------

    dias = (
        area /
        area_referencia
    ) * dias_referencia

    # --------------------------------------------------------
    # CUSTO
    # --------------------------------------------------------

    custo = (
        dias *
        diaria_final
    )

    return {
        "dias": dias,
        "diaria": diaria_final,
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

        comprimento
        altura
        área
        materiais
        subtotal_materiais
        massas_telas
        mão_de_obra
        custo_geral
    """

    # ========================================================
    # ÁREA
    # ========================================================

    area = calcular_area(
        comprimento=comprimento,
        altura=altura,
    )

    # ========================================================
    # MATERIAIS
    # ========================================================

    materiais_calculados = (
        calcular_materiais(
            area=area,
            materiais=materiais,
            precos=precos,
            quantidades=quantidades,
        )
    )

    # ========================================================
    # SUBTOTAL
    # ========================================================

    subtotal_materiais = (
        calcular_subtotal_materiais(
            materiais_calculados
        )
    )

    # ========================================================
    # MASSAS E TELAS
    # ========================================================

    massas_telas = (
        calcular_massas_telas(
            subtotal_materiais=
                subtotal_materiais,
            valor_manual=
                valor_massas_telas,
        )
    )

    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    mao_de_obra = (
        calcular_mao_de_obra(
            area=area,
            diaria=diaria,
        )
    )

    # ========================================================
    # CUSTO GERAL
    # ========================================================

    custo_geral = (
        subtotal_materiais
        + massas_telas
        + mao_de_obra["custo"]
    )

    # ========================================================
    # RESULTADO
    # ========================================================

    return {

        "comprimento":
            _numero(comprimento),

        "altura":
            _numero(altura),

        "area":
            area,

        "materiais":
            materiais_calculados,

        "subtotal_materiais":
            subtotal_materiais,

        "massas_telas":
            massas_telas,

        "mao_de_obra":
            mao_de_obra,

        "custo_geral":
            custo_geral,
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
    Retorna os principais indicadores
    financeiros do projeto.
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

        "Área":
            projeto["area"],

        "Materiais":
            projeto["subtotal_materiais"],

        "Massas e Telas":
            projeto["massas_telas"],

        "Mão de Obra":
            projeto[
                "mao_de_obra"
            ]["custo"],

        "Custo Geral":
            projeto["custo_geral"],
    }


# ============================================================
# INDICADORES
# ============================================================

def calcular_custo_por_m2(
    custo_total,
    area,
):
    """
    Calcula custo total por metro quadrado.
    """

    custo_total = _numero(
        custo_total
    )

    area = _numero(
        area
    )

    if area <= 0:
        return 0.0

    return (
        custo_total /
        area
    )


def calcular_percentual(
    valor,
    total,
):
    """
    Calcula a participação percentual
    de um valor em relação ao total.
    """

    valor = _numero(
        valor
    )

    total = _numero(
        total
    )

    if total <= 0:
        return 0.0

    return (
        valor /
        total
    ) * 100.0


def calcular_indicadores_projeto(
    projeto,
):
    """
    Calcula indicadores complementares.

    Retorna:

        custo_por_m2
        percentual_materiais
        percentual_massas_telas
        percentual_mao_de_obra
    """

    if not projeto:

        return {
            "custo_por_m2": 0.0,
            "percentual_materiais": 0.0,
            "percentual_massas_telas": 0.0,
            "percentual_mao_de_obra": 0.0,
        }

    area = _numero(
        projeto.get(
            "area",
            0.0,
        )
    )

    subtotal_materiais = _numero(
        projeto.get(
            "subtotal_materiais",
            0.0,
        )
    )

    massas_telas = _numero(
        projeto.get(
            "massas_telas",
            0.0,
        )
    )

    mao_de_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    if isinstance(
        mao_de_obra,
        dict,
    ):

        custo_mao_de_obra = _numero(
            mao_de_obra.get(
                "custo",
                0.0,
            )
        )

    else:

        custo_mao_de_obra = 0.0

    custo_geral = _numero(
        projeto.get(
            "custo_geral",
            0.0,
        )
    )

    return {

        "custo_por_m2":
            calcular_custo_por_m2(
                custo_total=custo_geral,
                area=area,
            ),

        "percentual_materiais":
            calcular_percentual(
                valor=subtotal_materiais,
                total=custo_geral,
            ),

        "percentual_massas_telas":
            calcular_percentual(
                valor=massas_telas,
                total=custo_geral,
            ),

        "percentual_mao_de_obra":
            calcular_percentual(
                valor=custo_mao_de_obra,
                total=custo_geral,
            ),
    }
