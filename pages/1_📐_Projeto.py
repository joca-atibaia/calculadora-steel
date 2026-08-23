import streamlit as st

from core.calculos import calcular_projeto
from core.dados import PRECOS_BASE


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Projeto | Calculadora Steel",
    page_icon="📐",
    layout="wide",
)


# ============================================================
# FUNÇÃO DE FORMATAÇÃO
# ============================================================

def formatar_moeda(valor):
    """
    Formata valores no padrão brasileiro.
    """

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ============================================================
# CABEÇALHO
# ============================================================

st.title("📐 Novo Projeto")
st.caption("Calculadora Steel Framing")

st.divider()


# ============================================================
# DADOS DO PROJETO
# ============================================================

st.subheader("Dados do projeto")

col1, col2, col3 = st.columns(3)


with col1:

    nome_projeto = st.text_input(
        "Nome do projeto",
        placeholder="Ex.: Residência Atibaia",
    )


with col2:

    comprimento = st.number_input(
        "Comprimento (m)",
        min_value=0.01,
        value=30.00,
        step=0.10,
    )


with col3:

    altura = st.number_input(
        "Altura (m)",
        min_value=0.01,
        value=3.00,
        step=0.10,
    )


st.divider()


# ============================================================
# PREÇOS DOS MATERIAIS
# ============================================================

st.subheader("💰 Preços dos materiais")

st.caption(
    "Os preços podem ser ajustados conforme "
    "o fornecedor e a realidade de cada obra."
)


# Inicializa os preços somente uma vez
if "precos" not in st.session_state:

    st.session_state["precos"] = (
        PRECOS_BASE.copy()
    )


# Cria os campos de preço
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

    precos_atualizados[nome] = (
        preco_atual
    )


# Atualiza os preços da sessão
st.session_state["precos"] = (
    precos_atualizados
)


st.divider()


# ============================================================
# BOTÃO CALCULAR
# ============================================================

if st.button(
    "🧮 CALCULAR PROJETO",
    type="primary",
    use_container_width=True,
):

    resultado = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        precos=st.session_state["precos"],
    )

    st.session_state["projeto"] = resultado

    st.session_state["nome_projeto"] = (
        nome_projeto
    )


# ============================================================
# RESULTADO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]


    st.subheader("📊 Resultado")


    col1, col2, col3, col4 = st.columns(4)


    # ========================================================
    # ÁREA
    # ========================================================

    with col1:

        st.metric(
            "Área",
            f'{projeto["area"]:.2f} m²',
        )


    # ========================================================
    # MATERIAIS
    # ========================================================

    with col2:

        st.metric(
            "Materiais",
            formatar_moeda(
                projeto["subtotal_materiais"]
            ),
        )


    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    with col3:

        st.metric(
            "Mão de obra",
            formatar_moeda(
                projeto["mao_de_obra"]["custo"]
            ),
        )


    # ========================================================
    # CUSTO GERAL
    # ========================================================

    with col4:

        st.metric(
            "Custo geral",
            formatar_moeda(
                projeto["custo_geral"]
            ),
        )


    st.divider()


    # ========================================================
    # QUANTITATIVO DE MATERIAIS
    # ========================================================

    st.subheader(
        "📋 Quantitativo de materiais"
    )


    for nome, material in (
        projeto["materiais"].items()
    ):

        col1, col2, col3, col4 = st.columns(
            [4, 2, 2, 2]
        )


        with col1:

            st.write(nome)


        with col2:

            st.write(
                f'{material["quantidade"]:.2f}'
            )


        with col3:

            st.write(
                formatar_moeda(
                    material["preco_unitario"]
                )
            )


        with col4:

            st.write(
                formatar_moeda(
                    material["custo"]
                )
            )


    st.divider()


    # ========================================================
    # MASSAS E TELAS
    # ========================================================

    st.subheader(
        "🧱 Massas e Telas"
    )


    st.write(
        formatar_moeda(
            projeto["massas_telas"]
        )
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
    # CUSTO GERAL
    # ========================================================

    st.success(
        f'💰 CUSTO GERAL: '
        f'{formatar_moeda(projeto["custo_geral"])}'
    )
