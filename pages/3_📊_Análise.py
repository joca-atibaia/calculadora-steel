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
# IDENTIFICA MASSAS E TELAS
#
# IMPORTANTE:
# Massas e Telas já estão incluídas em total_materiais.
# Portanto, serão mostradas apenas como composição interna
# dos materiais e NÃO serão somadas novamente ao custo geral.
# ============================================================

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
# PERCENTUAIS CORRETOS
#
# O custo geral é:
#
# MATERIAIS + MÃO DE OBRA
#
# Massas e Telas NÃO entram novamente aqui.
# ============================================================

if total_geral > 0:

    percentual_materiais = (
        total_materiais /
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
    percentual_mao_obra = 0.0


# ============================================================
# CONFERÊNCIA MATEMÁTICA
# ============================================================

total_conferido = (
    total_materiais +
    mao_de_obra
)


diferenca = (
    total_geral -
    total_conferido
)


calculo_ok = (
    abs(diferenca) < 0.01
)


# ============================================================
# INFORMAÇÕES DO PROJETO
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
# DIMENSÕES DA ESTRUTURA
# ============================================================

st.markdown("---")

st.subheader(
    "🏠 Dimensões da estrutura"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        label="Comprimento das paredes",
        value=f"{comprimento_paredes:,.2f} m"
    )


with col2:

    st.metric(
        label="Pé-direito",
        value=f"{pe_direito:,.2f} m"
    )


with col3:

    st.metric(
        label="Área das paredes",
        value=f"{area_total:,.2f} m²"
    )


# ============================================================
# RESUMO FINANCEIRO
# ============================================================

st.markdown("---")

st.subheader(
    "💰 Resumo financeiro"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        label="🧱 Materiais",
        value=f"R$ {total_materiais:,.2f}",
        delta=f"{percentual_materiais:.1f}% do custo geral"
    )


with col2:

    st.metric(
        label="👷 Mão de Obra",
        value=f"R$ {mao_de_obra:,.2f}",
        delta=f"{percentual_mao_obra:.1f}% do custo geral"
    )


with col3:

    st.metric(
        label="💰 Custo Geral",
        value=f"R$ {total_geral:,.2f}"
    )


# ============================================================
# COMPOSIÇÃO INTERNA DOS MATERIAIS
# ============================================================

st.markdown("---")

st.subheader(
    "🧱 Composição dos materiais"
)


st.caption(
    "Massas e Telas fazem parte do custo total de materiais "
    "e, portanto, não são adicionadas novamente ao custo geral."
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        label="🧱 Total de Materiais",
        value=f"R$ {total_materiais:,.2f}"
    )


with col2:

    st.metric(
        label="🪣 Massas e Telas",
        value=f"R$ {massas_telas:,.2f}"
    )


if total_materiais > 0:

    percentual_massas_sobre_materiais = (
        massas_telas /
        total_materiais *
        100
    )

else:

    percentual_massas_sobre_materiais = 0.0


st.progress(
    min(
        max(
            percentual_massas_sobre_materiais / 100,
            0.0
        ),
        1.0
    )
)


st.caption(
    f"Massas e Telas representam "
    f"{percentual_massas_sobre_materiais:.1f}% "
    f"do custo de materiais."
)


# ============================================================
# COMPOSIÇÃO DO CUSTO GERAL
# ============================================================

st.markdown("---")

st.subheader(
    "📊 Composição do custo geral"
)


df_composicao = pd.DataFrame(
    {
        "Categoria": [
            "Materiais",
            "Mão de Obra"
        ],
        "Valor": [
            total_materiais,
            mao_de_obra
        ],
        "Percentual": [
            percentual_materiais,
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
# GRÁFICO
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
        f"**Total conferido:** "
        f"R$ {total_conferido:,.2f}"
    )


if calculo_ok:

    st.success(
        "✅ Cálculo conferido corretamente: "
        "Materiais + Mão de Obra = Custo Geral."
    )

else:

    st.error(
        f"❌ Existe uma diferença de "
        f"R$ {diferenca:,.2f} "
        f"entre o custo geral e a soma dos componentes."
    )


# ============================================================
# STATUS FINAL
# ============================================================

st.markdown("---")

st.success(
    "✅ Projeto calculado e carregado corretamente "
    "a partir da página 📐 Projeto."
)
