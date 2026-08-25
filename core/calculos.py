import math

# Preços base padrão do sistema
PRECOS_BASE = {
    "perfil": 50.0, "guia": 50.0, "plywood": 80.0, "placa_st": 40.0,
    "placa_cimenticia": 140.0, "la_pet": 200.0, "parafusos": 35.0,
    "massas": 500.0, "telas": 500.0, "adesivo": 150.0, "telha": 400.0, "manta": 1000.0
}

def _numero(valor, padrao=0.0):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return float(padrao)

def validar_positivo(valor, nome):
    val = _numero(valor)
    if val < 0:
        raise ValueError(f"{nome} deve ser maior que zero.")
    return val

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ============================================================
# FUNÇÃO DE SUBTOTAL PURIFICADA (SEM ERROS DE SPAN)
# ============================================================
def calcular_subtotal_materiais(quantidade, preco_unitario):
    qtd = _numero(quantidade)
    prc = _numero(preco_unitario)
    subtotal = qtd * prc
    # RETORNO LIMPO E AUMENTADO: Texto direto formatado sem tags que quebram o celular
    return formatar_moeda(subtotal)

def quantidade_de_material(area_total, pe_direito):
    area = validar_positivo(area_total, "Área")
    alt = validar_positivo(pe_direito, "Pé Direito")
    
    qtd_perfil = math.ceil((area * 3.5) / 3.0)
    qtd_guia = math.ceil(area * 0.8)
    qtd_plywood = math.ceil(area / 2.2)
    qtd_placa_st = math.ceil(area / 2.4)
    qtd_cimenticia = math.ceil(area / 2.4)
    qtd_la = math.ceil(area / 10.0)
    
    return {
        "perfil": qtd_perfil, "guia": qtd_guia, "plywood": qtd_plywood,
        "placa_st": qtd_placa_st, "placa_cimenticia": qtd_cimenticia, "la_pet": qtd_la
    }

def calcular_massas_telas(area_total):
    area = validar_positivo(area_total, "Área")
    return {
        "parafusos": math.ceil(area * 0.5), "massas": math.ceil(area / 30.0),
        "telas": math.ceil(area / 40.0), "adesivo": math.ceil(area / 15.0)
    }

def projeto_sina(area_cobertura):
    cobertura = validar_positivo(area_cobertura, "Área de Cobertura")
    return {
        "telha": math.ceil(cobertura * 1.15), "manta": math.ceil(cobertura / 50.0)
    }

def calcular_projeto(area_total, pe_direito, area_cobertura):
    estrutura = quantidade_de_material(area_total, pe_direito)
    acabamento = calcular_massas_telas(area_total)
    telhado = projeto_sina(area_cobertura)
    
    resultado = {}
    resultado.update(estrutura)
    resultado.update(acabamento)
    resultado.update(telhado)
    return resultado
def calcular_indicadores_projeto(projeto):
    """Calcula os indicadores usados pela página de Análise."""
    area = _numero(projeto.get("area", 0.0))
    subtotal_materiais = _numero(
        projeto.get("subtotal_materiais", 0.0)
    )
    massas_telas = _numero(
        projeto.get("massas_telas", 0.0)
    )

    mao_de_obra = projeto.get("mao_de_obra", {})

    if not isinstance(mao_de_obra, dict):
        mao_de_obra = {}

    custo_mao_de_obra = _numero(
        mao_de_obra.get("custo", 0.0)
    )

    custo_geral = _numero(
        projeto.get("custo_geral", 0.0)
    )

    custo_por_m2 = (
        custo_geral / area
        if area > 0
        else 0.0
    )

    if custo_geral > 0:
        percentual_materiais = (
            subtotal_materiais / custo_geral
        ) * 100

        percentual_massas_telas = (
            massas_telas / custo_geral
        ) * 100

        percentual_mao_de_obra = (
            custo_mao_de_obra / custo_geral
        ) * 100
    else:
        percentual_materiais = 0.0
        percentual_massas_telas = 0.0
        percentual_mao_de_obra = 0.0

    return {
        "custo_por_m2": custo_por_m2,
        "percentual_materiais": percentual_materiais,
        "percentual_massas_telas": percentual_massas_telas,
        "percentual_mao_de_obra": percentual_mao_de_obra,
    }
