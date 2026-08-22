import streamlit as st

from core.dados import COEFICIENTES, PRECOS_BASE


st.set_page_config(
    page_title="Materiais | Calculadora Steel",
    page_icon="📋",
    layout="wide",
)


st.title("📋 Materiais")
st.caption("Coeficientes e preços utilizados nos cálculos")

st.divider()


if "coeficientes" not in st.session_state:
    st.session_state["coeficientes"] = COEFICIENTES.copy()


if "precos" not in st.session_state:
    st.session_state["precos"] = PRECOS_BASE.copy()


st.subheader("⚙️ Configuração dos materiais")

st.info(
    "Altere os coeficientes e preços dos materiais. "
    "As alterações serão utilizadas nos próximos cálculos."
)


for nome in COEFICIENTES:

    col1, col2 = st.columns(2)

    with col1:

        st.session_state["coeficientes"][nome] = st.number_input(
            f"{nome} — Coeficiente",
            min_value=0.0,
            value=float(
                st.session_state["coeficientes"].get(
                    nome,
                    COEFICIENTES[nome]
                )
            ),
            step=0.01,
            key=f"coeficiente_{nome}",
        )

    with col2:

        st.session_state["precos"][nome] = st.number_input(
            f"{nome} — Preço unitário (R$)",
            min_value=0.0,
            value=float(
                st.session_state["precos"].get(
                    nome,
                    PRECOS_BASE[nome]
                )
            ),
            step=0.01,
            key=f"preco_{nome}",
        )

    st.divider()


st.subheader("📊 Resumo atual")


resumo = []

for nome in COEFICIENTES:

    resumo.append(
        {
            "Material": nome,
            "Coeficiente": st.session_state["coeficientes"][nome],
            "Preço unitário": (
                f'R$ {st.session_state["precos"][nome]:,.2f}'
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            ),
        }
    )


st.dataframe(
    resumo,
    use_container_width=True,
    hide_index=True,
)


st.success(
    "✅ Os valores acima estão carregados na sessão atual. "
    "Volte para 📐 Novo Projeto e faça um novo cálculo."
)
