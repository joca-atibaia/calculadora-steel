import streamlit as st

from core.dados import (
    COEFICIENTES,
    PRECOS_BASE,
)


st.set_page_config(
    page_title="Materiais | Calculadora Steel",
    page_icon="📋",
    layout="wide",
)


st.title("📋 Materiais")
st.caption("Coeficientes e preços utilizados nos cálculos")

st.divider()


st.subheader("⚙️ Configuração dos materiais")

st.info(
    "Altere os coeficientes e preços abaixo. "
    "As alterações ficam disponíveis durante a sessão "
    "atual do aplicativo."
)


if "coeficientes" not in st.session_state:

    st.session_state["coeficientes"] = (
        COEFICIENTES.copy()
    )


if "precos" not in st.session_state:

    st.session_state["precos"] = (
        PRECOS_BASE.copy()
    )


coeficientes = st.session_state["coeficientes"]
precos = st.session_state["precos"]


for nome in coeficientes:

    st.markdown(f"### {nome}")

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:

        novo_coeficiente = st.number_input(
            "Coeficiente",
            min_value=0.0,
            value=float(coeficientes[nome]),
            step=0.01,
            key=f"coef_{nome}",
        )

    with col2:

        novo_preco = st.number_input(
            "Preço unitário (R$)",
            min_value=0.0,
            value=float(precos.get(nome, 0.0)),
            step=0.01,
            key=f"preco_{nome}",
        )

    with col3:

        st.write("")

        st.write("Atual")

        st.write(
            f"R$ {precos.get(nome, 0.0):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    coeficientes[nome] = novo_coeficiente
    precos[nome] = novo_preco

    st.divider()


if st.button(
    "💾 SALVAR ALTERAÇÕES",
    type="primary",
    use_container_width=True,
):

    st.session_state["coeficientes"] = (
        coeficientes.copy()
    )

    st.session_state["precos"] = (
        precos.copy()
    )

    st.success(
        "Alterações salvas nesta sessão."
    )


st.divider()


st.subheader("📊 Resumo dos parâmetros")


dados = []

for nome in coeficientes:

    dados.append(
        {
            "Material": nome,
            "Coeficiente": coeficientes[nome],
            "Preço unitário": (
                f'R$ {precos[nome]:,.2f}'
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            ),
        }
    )


st.dataframe(
    dados,
    use_container_width=True,
    hide_index=True,
)
