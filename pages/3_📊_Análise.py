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

    /* ========================================================
       CONFIGURAÇÃO GERAL
       ======================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    .stApp {
        font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        background-color: #f5f7fa !important;
        color: #17202a !important;
    }


    .block-container {
        max-width: 1400px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }


    /* ========================================================
       TEXTOS GERAIS
       ======================================================== */

    p,
    span,
    div,
    label,
    small {
        opacity: 1 !important;
    }


    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #17202a !important;
        opacity: 1 !important;
        visibility: visible !important;
    }


    /* ========================================================
       TÍTULOS
       ======================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #17202a !important;
        opacity: 1 !important;
        visibility: visible !important;
        -webkit-text-fill-color: #17202a !important;
    }


    /* ========================================================
       MÉTRICAS
       ======================================================== */

    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #d8e0e7 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05) !important;
    }


    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] span {
        color: #566573 !important;
        -webkit-text-fill-color: #566573 !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 700 !important;
    }


    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div,
    [data-testid="stMetricValue"] p {
        color: #17202a !important;
        -webkit-text-fill-color: #17202a !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 800 !important;
    }


    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] div,
    [data-testid="stMetricDelta"] p,
    [data-testid="stMetricDelta"] span {
        opacity: 1 !important;
        visibility: visible !important;
    }


    /* ========================================================
       AVISOS
       ======================================================== */

    [data-testid="stAlert"] {
        opacity: 1 !important;
        visibility: visible !important;
        border-radius: 10px !important;
    }


    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] div {
        opacity: 1 !important;
        visibility: visible !important;
        color: #17202a !important;
        -webkit-text-fill-color: #17202a !important;
    }


    /* ========================================================
       CAPTION
       ======================================================== */

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #566573 !important;
        -webkit-text-fill-color: #566573 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }


    /* ========================================================
       DATAFRAME / TABELAS
       ======================================================== */

    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border-radius: 10px !important;
        opacity: 1 !important;
        visibility: visible !important;
    }


    [data-testid="stDataFrame"] * {
        opacity: 1 !important;
    }


    /* ========================================================
       PROGRESS
       ======================================================== */

    [data-testid="stProgress"] {
        opacity: 1 !important;
        visibility: visible !important;
    }


    /* ========================================================
       GRÁFICOS
       ======================================================== */

    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stVegaLiteChart"],
    [data-testid="stGraphVizChart"],
    [data-testid="stPydeckChart"] {
        opacity: 1 !important;
        visibility: visible !important;
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }


    /* ========================================================
       SEPARADORES
       ======================================================== */

    hr {
        border: none !important;
        border-top: 1px solid #d8e0e7 !important;
        opacity: 1 !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-top: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 3rem !important;
        }


        h1 {
            font-size: 2rem !important;
            line-height: 1.2 !important;
        }


        h2 {
            font-size: 1.55rem !important;
        }


        h3 {
            font-size: 1.25rem !important;
        }


        [data-testid="stMetric"] {
            padding: 13px !important;
            margin-bottom: 10px !important;
        }


        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p {
            font-size: 0.85rem !important;
        }


        [data-testid="stMetricValue"] {
            font-size: 1.45rem !important;
        }


        [data-testid="stMetricDelta"] {
            font-size: 0.78rem !important;
        }


        [data-testid="stDataFrame"] {
            width: 100% !important;
            overflow-x: auto !important;
        }


        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {
            font-size: 0.85rem !important;
            line-height: 1.4 !important;
        }
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
# PERCENTUAIS
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
