"""
Motor de cálculo da Calculadora Profissional de Steel Framing.

Versão: 6B

Responsabilidades deste módulo:
- calcular área do projeto;
- calcular quantitativos automáticos;
- aceitar quantidades manuais;
- aceitar preços personalizados;
- calcular custos dos materiais;
- calcular subtotal de materiais;
- calcular Massas e Telas separadamente;
- calcular mão de obra;
- calcular custo geral;
- fornecer indicadores para a interface.

A interface do Streamlit fica fora deste módulo.
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

    Aceita:
        - int
        - float
        - strings numéricas
        - None

    Retorna:
        float
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
# PROJETO
# ============================================================

def calcular_area(comprimento, altura):
    """
    Calcula a área do projeto.

    Fórmula:

        área = comprimento × altura

    Parâmetros:
        comprimento: dimensão horizontal em metros
        altura: dimensão vertical em metros

    Retorna:
        área em m²
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
    coeficiente = _numero(coeficiente)

    if area <= 0:
        return 0.0

    if coeficiente < 0:
        raise ValueError(
            "O coeficiente do material não pode ser negativo."
        )

    area_referencia = _numero(
        CONFIGURACAO_PROJETO.get(
            "area_referencia",
            30.00,
        )
    )

    if area_referencia <= 0:
        raise ValueError(
            "A área de referência deve ser maior que zero."
        )

    quantidade = (
        area / area_referencia
    ) * coeficiente

    return quantidade


# ============================================================
# CUSTO DE MATERIAL
# ============================================================

def calcular_custo_material(
    quantidade,
    preco_unitario,
):
    """
    Calcula o custo total de um material.

    Fórmula:

        custo = quantidade × preço unitário
    """

    quantidade = _numero(quantidade)
    preco_unitario = _numero(preco_unitario)

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

    1. Materiais inativos não entram no cálculo.

    2. O coeficiente cadastrado em dados.py
       determina a quantidade automática.

    3. Se existir uma quantidade manual,
       ela substitui a quantidade automática.

    4. Se não existir quantidade manual,
       permanece a quantidade automática.

    5. Se existir preço personalizado,
       ele substitui o preço padrão.

    6. O resultado registra:
       - quantidade final;
       - quantidade automática;
       - se houve alteração manual;
       - origem da quantidade;
       - coeficiente;
       - preço unitário;
       - preço padrão;
       - se houve preço personalizado;
       - custo;
       - unidade;
       - categoria.
    """

    area = _numero(area)

    if materiais is None:
        materiais = MATERIAIS

    if precos is None:
        precos = {}

    if quantidades is None:
        quantidades = {}

    if not isinstance(materiais, dict):
        raise ValueError(
            "O catálogo de materiais deve ser um dicionário."
        )

    if not isinstance(precos, dict):
        raise ValueError(
            "Os preços devem ser informados como dicionário."
        )

    if not isinstance(quantidades, dict):
        raise ValueError(
            "As quantidades devem ser informadas como dicionário."
        )

    resultado = {}

    for nome, dados in materiais.items():

        # ----------------------------------------------------
        # SEGURANÇA
        # ----------------------------------------------------

        if not isinstance(dados, dict):
            continue

        # ----------------------------------------------------
        # MATERIAL ATIVO
        # ----------------------------------------------------

        if not dados.get("ativo", True):
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

        if coeficiente < 0:
            raise ValueError(
                f"O coeficiente do material '{nome}' "
                "não pode ser negativo."
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

        if preco_padrao < 0:
            raise ValueError(
                f"O preço padrão do material '{nome}' "
                "não pode ser negativo."
            )

        # ----------------------------------------------------
        # PREÇO FINAL
        # ----------------------------------------------------

        preco_personalizado = (
            nome in precos
        )

        if preco_personalizado:

            preco = _numero(
                precos[nome],
                preco_padrao,
            )

        else:

            preco = preco_padrao

        if preco < 0:
            raise ValueError(
                f"O preço do material '{nome}' "
                "não pode ser negativo."
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

        quantidade_manual = (
            nome in quantidades
        )

        if quantidade_manual:

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
                quantidade_manual,

            "origem_quantidade":
                origem_quantidade,

            "coeficiente":
                coeficiente,

            "preco_unitario":
                preco,

            "preco_padrao":
                preco_padrao,

            "preco_personalizado":
                preco_personalizado,

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

def calcular_subtotal_materiais(materiais):
    """
    Soma o custo de todos os materiais calculados.
    """

    if not materiais:
        return 0.0

    subtotal = 0.0

    for item in materiais.values():

        if not isinstance(item, dict):
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

    IMPORTANTE:

    Massas e Telas continuam separadas do
    quantitativo de materiais, conforme definido
    na versão 6B.

    Se valor_manual for informado:

        utiliza o valor manual.

    Caso contrário:

        subtotal_materiais × percentual

    O percentual padrão vem de:

        CONFIGURACAO_PROJETO[
            "percentual_massas_telas"
        ]
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
    # PROJETO SEM ÁREA
    # --------------------------------------------------------

    if area <= 0:

        diaria_final = (
            _numero(diaria)
            if diaria is not None
            else _numero(
                CONFIGURACAO_PROJETO.get(
                    "diaria_mao_de_obra",
                    755.00,
                )
            )
        )

        return {
            "dias": 0.0,
            "diaria": diaria_final,
            "custo": 0.0,
        }

    # --------------------------------------------------------
    # DIÁRIA
    # --------------------------------------------------------

    if diaria is None:

        diaria = _numero(
            CONFIGURACAO_PROJETO.get(
                "diaria_mao_de_obra",
                755.00,
            )
        )

    else:

        diaria = _numero(
            diaria
        )

    if diaria < 0:
        raise ValueError(
            "A diária de mão de obra "
            "não pode ser negativa."
        )

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
            "A área de referência deve "
            "ser maior que zero."
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
        diaria
    )

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

    Parâmetros:

        comprimento:
            comprimento do projeto em metros.

        altura:
            altura do projeto em metros.

        diaria:
            valor personalizado da diária
            de mão de obra.

        precos:
            dicionário com preços personalizados.

        materiais:
            catálogo alternativo de materiais.

        quantidades:
            dicionário com quantidades manuais.

        valor_massas_telas:
            permite substituir o cálculo percentual
            por um valor manual.

    Retorna:

        {
            "comprimento": ...,
            "altura": ...,
            "area": ...,
            "materiais": ...,
            "subtotal_materiais": ...,
            "massas_telas": ...,
            "mao_de_obra": ...,
            "custo_geral": ...
        }
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
    # SUBTOTAL MATERIAIS
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
            comprimento,

        "altura":
            altura,

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
    Retorna somente os principais indicadores
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
            projeto["mao_de_obra"]["custo"],

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
    Calcula o custo total por metro quadrado.

    Fórmula:

        custo por m² =
            custo total ÷ área
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
    Calcula indicadores complementares
    para apresentação na interface.

    Retorna:

        custo por m²
        percentual de materiais
        percentual de Massas e Telas
        percentual de mão de obra
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

    custo_mao_de_obra = _numero(
        mao_de_obra.get(
            "custo",
            0.0,
        )
        if isinstance(
            mao_de_obra,
            dict,
        )
        else 0.0
    )

    custo_geral = _numero(
        projeto.get(
            "custo_geral",
            0.0,
        )
    )

    return {

        "custo_por_m2":
            calcular_custo_por_m2(
                custo_total=
                    custo_geral,
                area=
                    area,
            ),

        "percentual_materiais":
            calcular_percentual(
                valor=
                    subtotal_materiais,
                total=
                    custo_geral,
            ),

        "percentual_massas_telas":
            calcular_percentual(
                valor=
                    massas_telas,
                total=
                    custo_geral,
            ),

        "percentual_mao_de_obra":
            calcular_percentual(
                valor=
                    custo_mao_de_obra,
                total=
                    custo_geral,
            ),
    }
