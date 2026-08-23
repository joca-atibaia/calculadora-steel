import streamlit as st
import pandas as pd
from datetime import date

from core.calculos import calcular_projeto
from core.dados import PRECOS_BASE


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Orçamento | Calculadora Steel",
    page_icon="📐",
    layout="wide",
)


# ============================================================
# FUNÇÕES AUXILIARES
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

st.title("📐 CALCULADORA STEEL FRAMING")
st.caption("Orçamento de materiais e mão de obra")

st.divider()


# ============================================================
# IDENTIFICAÇÃO DO PROJETO
# ============================================================

st.subheader("📋 Identificação do projeto")

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


observacoes = st.text_area(
    "Observações",
    placeholder="Informações adicionais sobre o orçamento...",
)


st.divider()


# ============================================================
# DADOS DO PROJETO
# ============================================================

st.subheader("📐 Dimensões do projeto")

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

    st.session_state["precos"] = (
        PRECOS_BASE.copy()
    )


st.subheader("💰 Preços dos materiais")

st.caption(
    "Altere os preços conforme fornecedor, "
    "região ou condição de compra."
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

st.subheader("📦 Quantidades dos materiais")

st.caption(
    "As quantidades são calculadas automaticamente. "
    "Você pode alterar qualquer quantidade conforme "
    "a necessidade da obra."
)


if "quantidades" not in st.session_state:

    st.session_state["quantidades"] = {}


quantidades_atualizadas = {}


for nome, material in previa["materiais"].items():

    quantidade_automatica = material[
        "quantidade"
    ]

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


    quantidades_atualizadas[nome] = (
        quantidade_atual
    )


st.session_state["quantidades"] = (
    quantidades_atualizadas
)


st.divider()


# ============================================================
# CALCULAR ORÇAMENTO
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

    st.session_state["nome_projeto"] = (
        nome_projeto
    )

    st.session_state["cliente"] = (
        cliente
    )

    st.session_state["local_obra"] = (
        local_obra
    )

    st.session_state["responsavel"] = (
        responsavel
    )

    st.session_state["data_orcamento"] = (
        data_orcamento
    )

    st.session_state["observacoes"] = (
        observacoes
    )


# ============================================================
# RESULTADO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]

    st.divider()

    st.header("📊 Orçamento")


    # ========================================================
    # IDENTIFICAÇÃO
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


    st.divider()


    # ========================================================
    # RESUMO
    # ========================================================

    st.subheader("📊 Resumo do orçamento")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Área",
            f'{projeto["area"]:.2f} m²',
        )


    with col2:

        st.metric(
            "Materiais",
            formatar_moeda(
                projeto["subtotal_materiais"]
            ),
        )


    with col3:

        st.metric(
            "Mão de obra",
            formatar_moeda(
                projeto["mao_de_obra"]["custo"]
            ),
        )


    with col4:

        st.metric(
            "Custo geral",
            formatar_moeda(
                projeto["custo_geral"]
            ),
        )


    st.divider()


    # ========================================================
    # TABELA PROFISSIONAL DE MATERIAIS
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


    mao_de_obra = projeto[
        "mao_de_obra"
    ]


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
    # OBSERVAÇÕES
    # ========================================================

    observacoes_salvas = st.session_state.get(
        "observacoes",
        "",
    )


    if observacoes_salvas:

        st.subheader("📝 Observações")

        st.write(
            observacoes_salvas
        )

        st.divider()


    # ========================================================
    # CUSTO GERAL
    # ========================================================

    st.success(
        f'💰 CUSTO GERAL: '
        f'{formatar_moeda(projeto["custo_geral"])}'
    )
