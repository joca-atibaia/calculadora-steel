import streamlit as st
import pandas as pd
from datetime import date

from core.calculos import calcular_projeto
from core.dados import PRECOS_BASE


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Orçamento | Calculadora Steel",
    page_icon="📐",
    layout="wide",
)


# ============================================================
# ESTILO PROFISSIONAL
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        color: #666;
        font-size: 1.05rem;
        margin-top: 0;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 10px;
    }

    .total-box {
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #d9d9d9;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .total-label {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 4px;
    }

    .total-value {
        font-size: 2rem;
        font-weight: 800;
    }

    .info-box {
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #e2e2e2;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES
# ============================================================

def formatar_moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="main-title">📐 CALCULADORA STEEL FRAMING</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Sistema profissional para orçamento de materiais e mão de obra'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()


# ============================================================
# IDENTIFICAÇÃO
# ============================================================

st.markdown(
    '<div class="section-title">📋 Identificação do projeto</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:

    nome_projeto = st.text_input(
        "Nome do projeto",
        placeholder="Ex.: Residência Atibaia",
    )

    cliente = st.text_input(
        "Cliente",
        placeholder="Nome do cliente",
    )


with col2:

    local_obra = st.text_input(
        "Local da obra",
        placeholder="Ex.: Atibaia - SP",
    )

    responsavel = st.text_input(
        "Responsável pelo orçamento",
        placeholder="Nome do profissional",
    )


data_orcamento = st.date_input(
    "Data do orçamento",
    value=date.today(),
)


st.divider()


# ============================================================
# CONDIÇÕES COMERCIAIS
# ============================================================

st.markdown(
    '<div class="section-title">💼 Condições comerciais</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:

    validade = st.number_input(
        "Validade do orçamento (dias)",
        min_value=1,
        value=10,
        step=1,
    )

    prazo_execucao = st.text_input(
        "Prazo estimado de execução",
        placeholder="Ex.: 30 dias",
    )


with col2:

    condicao_pagamento = st.text_input(
        "Condição de pagamento",
        placeholder="Ex.: 50% entrada + 50% conclusão",
    )

    inclusao = st.text_input(
        "Inclusões / observações comerciais",
        placeholder="Ex.: Materiais e mão de obra",
    )


observacoes = st.text_area(
    "Observações",
    placeholder=(
        "Informações adicionais sobre o orçamento, "
        "condições da obra, especificações ou ressalvas..."
    ),
)


st.divider()


# ============================================================
# DIMENSÕES
# ============================================================

st.markdown(
    '<div class="section-title">📐 Dimensões do projeto</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:

    comprimento = st.number_input(
        "Comprimento (m)",
        min_value=0.01,
        value=30.00,
        step=0.10,
    )


with col2:

    altura = st.number_input(
        "Altura (m)",
        min_value=0.01,
        value=3.00,
        step=0.10,
    )


with col3:

    area_preview = comprimento * altura

    st.metric(
        "Área do projeto",
        f"{area_preview:.2f} m²",
    )


st.divider()


# ============================================================
# PREÇOS
# ============================================================

if "precos" not in st.session_state:

    st.session_state["precos"] = PRECOS_BASE.copy()


st.markdown(
    '<div class="section-title">💰 Preços dos materiais</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Altere os preços conforme fornecedor, região "
    "ou condição de compra."
)


precos_atualizados = {}


for nome, preco_padrao in (
    st.session_state["precos"].items()
):

    preco_atual = st.number_input(
        nome,
        min_value=0.00,
        value=float(preco_padrao),
        step=0.01,
        format="%.2f",
        key=f"preco_{nome}",
    )

    precos_atualizados[nome] = preco_atual


st.session_state["precos"] = precos_atualizados


st.divider()


# ============================================================
# PRÉ-CÁLCULO
# ============================================================

previa = calcular_projeto(
    comprimento=comprimento,
    altura=altura,
    precos=st.session_state["precos"],
)


# ============================================================
# QUANTIDADES
# ============================================================

st.markdown(
    '<div class="section-title">📦 Quantidades dos materiais</div>',
    unsafe_allow_html=True,
)

st.caption(
    "As quantidades são calculadas automaticamente. "
    "Você pode ajustar conforme a necessidade da obra."
)


if "quantidades" not in st.session_state:

    st.session_state["quantidades"] = {}


quantidades_atualizadas = {}


for nome, material in previa["materiais"].items():

    quantidade_automatica = material["quantidade"]

    if nome not in st.session_state["quantidades"]:

        st.session_state["quantidades"][nome] = (
            quantidade_automatica
        )


    quantidade_atual = st.number_input(
        nome,
        min_value=0.0,
        value=float(
            st.session_state["quantidades"][nome]
        ),
        step=1.0,
        format="%.2f",
        key=f"quantidade_{nome}",
    )


    quantidades_atualizadas[nome] = quantidade_atual


st.session_state["quantidades"] = (
    quantidades_atualizadas
)


st.divider()


# ============================================================
# BOTÃO CALCULAR
# ============================================================

if st.button(
    "🧮 CALCULAR ORÇAMENTO",
    type="primary",
    use_container_width=True,
):

    resultado = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        precos=st.session_state["precos"],
        quantidades=st.session_state["quantidades"],
    )

    st.session_state["projeto"] = resultado

    st.session_state["nome_projeto"] = nome_projeto
    st.session_state["cliente"] = cliente
    st.session_state["local_obra"] = local_obra
    st.session_state["responsavel"] = responsavel
    st.session_state["data_orcamento"] = data_orcamento

    st.session_state["validade"] = validade
    st.session_state["prazo_execucao"] = prazo_execucao
    st.session_state["condicao_pagamento"] = condicao_pagamento
    st.session_state["inclusao"] = inclusao
    st.session_state["observacoes"] = observacoes


# ============================================================
# RESULTADO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]

    st.divider()

    st.header("📊 Orçamento")


    # ========================================================
    # IDENTIFICAÇÃO DO ORÇAMENTO
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Projeto:** "
            f"{st.session_state.get('nome_projeto', '')}"
        )

        st.write(
            f"**Cliente:** "
            f"{st.session_state.get('cliente', '')}"
        )

        st.write(
            f"**Local da obra:** "
            f"{st.session_state.get('local_obra', '')}"
        )


    with col2:

        st.write(
            f"**Responsável:** "
            f"{st.session_state.get('responsavel', '')}"
        )

        data_salva = st.session_state.get(
            "data_orcamento",
            data_orcamento,
        )

        st.write(
            f"**Data:** "
            f"{data_salva.strftime('%d/%m/%Y')}"
        )

        st.write(
            f"**Validade:** "
            f"{st.session_state.get('validade', 10)} dias"
        )


    st.divider()


    # ========================================================
    # RESUMO FINANCEIRO
    # ========================================================

    st.subheader("💰 Resumo financeiro")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Materiais",
            formatar_moeda(
                projeto["subtotal_materiais"]
            ),
        )

    with col2:

        st.metric(
            "Mão de obra",
            formatar_moeda(
                projeto["mao_de_obra"]["custo"]
            ),
        )

    with col3:

        st.metric(
            "Área",
            f'{projeto["area"]:.2f} m²',
        )


    st.markdown(
        f"""
        <div class="total-box">
            <div class="total-label">
                CUSTO GERAL DO ORÇAMENTO
            </div>
            <div class="total-value">
                {formatar_moeda(projeto["custo_geral"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.divider()


    # ========================================================
    # MATERIAIS
    # ========================================================

    st.subheader(
        "📋 Quantitativo de materiais"
    )


    tabela_materiais = []


    for nome, material in (
        projeto["materiais"].items()
    ):

        tabela_materiais.append(
            {
                "Material": nome,
                "Unidade": material["unidade"],
                "Quantidade": f'{material["quantidade"]:.2f}',
                "Preço unitário": formatar_moeda(
                    material["preco_unitario"]
                ),
                "Total": formatar_moeda(
                    material["custo"]
                ),
            }
        )


    df_materiais = pd.DataFrame(
        tabela_materiais
    )


    st.dataframe(
        df_materiais,
        use_container_width=True,
        hide_index=True,
    )


    st.divider()


    # ========================================================
    # MASSAS E TELAS
    # ========================================================

    st.subheader(
        "🧱 Massas e Telas"
    )

    st.metric(
        "Custo",
        formatar_moeda(
            projeto["massas_telas"]
        ),
    )


    st.divider()


    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    st.subheader(
        "👷 Mão de obra"
    )

    mao_de_obra = projeto["mao_de_obra"]

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Dias estimados",
            f'{mao_de_obra["dias"]:.1f}',
        )

    with col2:

        st.metric(
            "Diária",
            formatar_moeda(
                mao_de_obra["diaria"]
            ),
        )

    with col3:

        st.metric(
            "Custo da mão de obra",
            formatar_moeda(
                mao_de_obra["custo"]
            ),
        )


    st.divider()


    # ========================================================
    # CONDIÇÕES COMERCIAIS
    # ========================================================

    st.subheader(
        "💼 Condições comerciais"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Prazo estimado:** "
            f"{st.session_state.get('prazo_execucao', '')}"
        )

        st.write(
            f"**Condição de pagamento:** "
            f"{st.session_state.get('condicao_pagamento', '')}"
        )


    with col2:

        st.write(
            f"**Validade:** "
            f"{st.session_state.get('validade', 10)} dias"
        )

        st.write(
            f"**Inclusões:** "
            f"{st.session_state.get('inclusao', '')}"
        )


    # ========================================================
    # OBSERVAÇÕES
    # ========================================================

    observacoes_salvas = st.session_state.get(
        "observacoes",
        "",
    )


    if observacoes_salvas:

        st.divider()

        st.subheader(
            "📝 Observações"
        )

        st.info(
            observacoes_salvas
        )


    st.divider()


    # ========================================================
    # TOTAL FINAL
    # ========================================================

    st.markdown(
        f"""
        <div class="total-box">
            <div class="total-label">
                VALOR TOTAL DO ORÇAMENTO
            </div>
            <div class="total-value">
                {formatar_moeda(projeto["custo_geral"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.caption(
        "Orçamento elaborado pela Calculadora Steel Framing."
    )
