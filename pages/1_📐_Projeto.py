```python
import streamlit as st

from core.calculos import calcular_projeto
from core.dados import PRECOS_BASE


st.set_page_config(
    page_title="Projeto | Calculadora Steel",
    page_icon="📐",
    layout="wide",
)


st.title("📐 Novo Projeto")
st.caption("Calculadora Steel Framing")


st.divider()


# ==============================
# DADOS DO PROJETO
# ==============================

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


# ==============================
# CÁLCULO
# ==============================

if st.button(
    "🧮 CALCULAR PROJETO",
    type="primary",
    use_container_width=True,
):

    resultado = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
    )

    st.session_state["projeto"] = resultado
    st.session_state["nome_projeto"] = nome_projeto


# ==============================
# RESULTADO
# ==============================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]

    st.subheader("Resultado")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Área",
            f'{projeto["area"]:.2f} m²',
        )

    with col2:
        st.metric(
            "Materiais",
            f'R$ {projeto["subtotal_materiais"]:,.2f}'
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )

    with col3:
        st.metric(
            "Mão de obra",
            f'R$ {projeto["mao_de_obra"]["custo"]:,.2f}'
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )

    with col4:
        st.metric(
            "Custo geral",
            f'R$ {projeto["custo_geral"]:,.2f}'
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )


    st.divider()


    # ==============================
    # MATERIAIS
    # ==============================

    st.subheader("📋 Quantitativo de materiais")

    for nome, material in projeto["materiais"].items():

        col1, col2, col3 = st.columns([4, 2, 2])

        with col1:
            st.write(nome)

        with col2:
            st.write(
                f'{material["quantidade"]:.2f}'
            )

        with col3:
            custo = material["custo"]

            st.write(
                f'R$ {custo:,.2f}'
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )


    st.divider()


    # ==============================
    # MASSAS E TELAS
    # ==============================

    st.subheader("🧱 Massas e Telas")

    st.write(
        f'R$ {projeto["massas_telas"]:,.2f}'
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


    # ==============================
    # MÃO DE OBRA
    # ==============================

    st.subheader("👷 Mão de obra")

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
            f'R$ {mao_de_obra["diaria"]:,.2f}'
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )

    with col3:
        st.metric(
            "Custo",
            f'R$ {mao_de_obra["custo"]:,.2f}'
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
        )


    st.divider()


    # ==============================
    # TOTAL
    # ==============================

    st.success(
        f'💰 CUSTO GERAL: '
        f'R$ {projeto["custo_geral"]:,.2f}'
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
```
