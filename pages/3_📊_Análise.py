import streamlit as st
import pandas as pd


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Análise - Calculadora Steel Framing",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    .stApp {
        background: #f5f7fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TÍTULO
# ============================================================

st.title("📊 Análise do Projeto")

st.markdown(
    "Análise financeira, composição de custos e quantitativos "
    "do projeto calculado."
)


# ============================================================
# RECUPERA PROJETO CALCULADO
# ============================================================

projeto = st.session_state.get(
    "projeto_calculado"
)


# ============================================================
# VERIFICAÇÃO
# ============================================================

if not projeto:

    st.warning(
        "⚠️ Ainda não existe um projeto calculado para análise."
    )

    st.info(
        "Vá até a página 📐 Projeto, preencha os dados "
        "e clique em **🧮 CALCULAR PROJETO** antes de acessar "
        "esta página."
    )

    st.stop()


if not projeto.get("calculado", False):

    st.warning(
        "⚠️ O projeto ainda não foi calculado."
    )

    st.info(
        "Vá até a página 📐 Projeto e clique em "
        "**🧮 CALCULAR PROJETO**."
    )

    st.stop()


# ============================================================
# RECUPERAÇÃO DOS DADOS
# ============================================================

cliente = projeto.get(
    "cliente",
    "Não informado"
)


data_projeto = projeto.get(
    "data_projeto",
    None
)


comprimento_paredes = float(
    projeto.get(
        "comprimento_paredes",
        0
    )
)


pe_direito = float(
    projeto.get(
        "pe_direito",
        0
    )
)


area_total = float(
    projeto.get(
        "area_total",
        0
    )
)


dados_atualizados = projeto.get(
    "dados_atualizados",
    []
)


total_materiais = float(
    projeto.get(
        "total_materiais",
        0
    )
)


mao_de_obra = float(
    projeto.get(
        "mao_de_obra",
        0
    )
)


total_geral = float(
    projeto.get(
        "total_geral",
        0
    )
)


# ============================================================
# CUSTO POR M²
# ============================================================

if area_total > 0:

    custo_m2 = (
        total_geral /
        area_total
    )

else:

    custo_m2 = 0.0


# ============================================================
# CABEÇALHO DO PROJETO
# ============================================================

st.markdown("---")

st.subheader(
    "📐 Informações do projeto"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        label="Área",
        value=f"{area_total:,.2f} m²"
    )


with col2:

    st.metric(
        label="Custo geral",
        value=f"R$ {total_geral:,.2f}"
    )


with col3:

    st.metric(
        label="Custo por m²",
        value=f"R$ {custo_m2:,.2f}"
    )


# ============================================================
# DADOS DIMENSIONAIS
# ============================================================

st.markdown("---")

st.subheader(
    "🏠 Dimensões da estrutura"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Comprimento das paredes",
        f"{comprimento_paredes:,.2f} m"
    )


with col2:

    st.metric(
        "Pé-direito",
        f"{pe_direito:,.2f} m"
    )


with col3:

    st.metric(
        "Área das paredes",
        f"{area_total:,.2f} m²"
    )


# ============================================================
# RESUMO FINANCEIRO
# ============================================================

st.markdown("---")

st.subheader(
    "💰 Resumo financeiro"
)


# ------------------------------------------------------------
# LOCALIZA MASSAS E TELAS
# ------------------------------------------------------------

massas_telas = 0.0


for item in dados_atualizados:

    nome_item = str(
        item.get(
            "Item",
            ""
        )
    ).lower()

    if (
        "massa" in nome_item
        or "tela" in nome_item
    ):

        massas_telas += float(
            item.get(
                "Total Item",
                0
            )
        )


# ============================================================
# PERCENTUAIS
# ============================================================

if total_geral > 0:

    percentual_materiais = (
        total_materiais /
        total_geral *
        100
    )

    percentual_massas_telas = (
        massas_telas /
        total_geral *
        100
    )

    percentual_mao_obra = (
        mao_de_obra /
        total_geral *
        100
    )

else:

    percentual_materiais = 0.0
    percentual_massas_telas = 0.0
    percentual_mao_obra = 0.0


# ============================================================
# CARDS FINANCEIROS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="🧱 Materiais",
        value=f"R$ {total_materiais:,.2f}",
        delta=f"{percentual_materiais:.1f}%"
    )


with col2:

    st.metric(
        label="🪣 Massas e Telas",
        value=f"R$ {massas_telas:,.2f}",
        delta=f"{percentual_massas_telas:.1f}%"
    )


with col3:

    st.metric(
        label="👷 Mão de Obra",
        value=f"R$ {mao_de_obra:,.2f}",
        delta=f"{percentual_mao_obra:.1f}%"
    )


with col4:

    st.metric(
        label="💰 Custo Geral",
        value=f"R$ {total_geral:,.2f}"
    )


# ============================================================
# COMPOSIÇÃO DO CUSTO
# ============================================================

st.markdown("---")

st.subheader(
    "📊 Composição do custo"
)


df_composicao = pd.DataFrame(
    {
        "Categoria": [
            "Materiais",
            "Massas e Telas",
            "Mão de Obra"
        ],
        "Valor": [
            total_materiais,
            massas_telas,
            mao_de_obra
        ],
        "Percentual": [
            percentual_materiais,
            percentual_massas_telas,
            percentual_mao_obra
        ]
    }
)


st.dataframe(
    df_composicao.style.format(
        {
            "Valor": "R$ {:.2f}",
            "Percentual": "{:.1f}%"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# GRÁFICO DE COMPOSIÇÃO
# ============================================================

if total_geral > 0:

    st.bar_chart(
        df_composicao.set_index(
            "Categoria"
        )["Valor"]
    )


# ============================================================
# QUANTITATIVO DE MATERIAIS
# ============================================================

st.markdown("---")

st.subheader(
    "📋 Quantitativo de materiais"
)


if dados_atualizados:

    df_materiais = pd.DataFrame(
        dados_atualizados
    )

    st.dataframe(
        df_materiais.style.format(
            {
                "Quantidade": "{:.2f}",
                "Preço Unitário": "R$ {:.2f}",
                "Total Item": "R$ {:.2f}"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Nenhum material calculado foi encontrado."
    )


# ============================================================
# IDENTIFICAÇÃO DO PROJETO
# ============================================================

st.markdown("---")

st.subheader(
    "📋 Identificação"
)


col1, col2 = st.columns(2)


with col1:

    st.write(
        f"**Cliente:** {cliente}"
    )


with col2:

    if data_projeto:

        try:

            data_formatada = (
                data_projeto.strftime(
                    "%d/%m/%Y"
                )
            )

        except Exception:

            data_formatada = str(
                data_projeto
            )

        st.write(
            f"**Data do orçamento:** "
            f"{data_formatada}"
        )


# ============================================================
# CONFERÊNCIA DO CÁLCULO
# ============================================================

st.markdown("---")

st.subheader(
    "✅ Conferência do cálculo"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.write(
        f"**Materiais:** "
        f"R$ {total_materiais:,.2f}"
    )


with col2:

    st.write(
        f"**Mão de obra:** "
        f"R$ {mao_de_obra:,.2f}"
    )


with col3:

    st.write(
        f"**Total geral:** "
        f"R$ {total_geral:,.2f}"
    )


st.success(
    "✅ Projeto calculado e carregado corretamente "
    "a partir da página 📐 Projeto."
)
