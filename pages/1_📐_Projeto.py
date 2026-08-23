import streamlit as st
import pandas as pd
from datetime import date

from core.calculos import calcular_projeto
from core.dados import PRECOS_BASE


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Calculadora Steel Framing",
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
# CSS — VISUAL PROFISSIONAL 6C
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
    );

    html,
    body,
    [data-testid="stAppViewContainer"],
    .stApp {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;
    }

    .stApp {
        background: #f5f7fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }


    /* ========================================================
       CABEÇALHO
       ======================================================== */

    .sf-header {
        background: linear-gradient(
            135deg,
            #17202a 0%,
            #263746 55%,
            #34495e 100%
        );

        border-radius: 18px;

        padding: 30px 38px 24px 38px;

        margin-bottom: 8px;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.12);
    }


    /* ========================================================
       TÍTULO DO CABEÇALHO
       ======================================================== */

    .sf-header-title {
        font-size: 2.15rem;
        line-height: 1.2;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
        margin: 0;
    }


    /* ========================================================
       SUBTÍTULO
       ======================================================== */

    .sf-subtitle {
        color: #dce3e8;
        font-size: 1rem;
        line-height: 1.6;
        margin-top: 8px;
        margin-bottom: 14px;
    }


    /* ========================================================
       BADGE
       ======================================================== */

    .sf-badge {
        display: inline-block;

        background: rgba(255, 255, 255, 0.12);

        border: 1px solid rgba(255, 255, 255, 0.22);

        border-radius: 999px;

        padding: 7px 14px;

        font-size: 0.75rem;

        font-weight: 700;

        letter-spacing: 0.6px;

        color: #ffffff;
    }


    /* ========================================================
       SEÇÕES
       ======================================================== */

    .sf-section {
        margin-top: 28px;
        margin-bottom: 16px;
    }

    .sf-section h2 {
        margin: 0 0 4px 0;
        padding: 0;

        font-size: 1.35rem;
        line-height: 1.3;
        font-weight: 800;

        color: #17202a;
    }

    .sf-section p {
        margin: 0;

        font-size: 0.9rem;
        line-height: 1.5;

        color: #6b7280;
    }


    /* ========================================================
       CAMPOS
       ======================================================== */

    .stTextInput label,
    .stNumberInput label,
    .stDateInput label,
    .stTextArea label,
    .stSelectbox label {
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: #374151 !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 9px;
    }

    input,
    textarea,
    [data-baseweb="select"] {
        font-family:
            "Inter",
            "Segoe UI",
            sans-serif !important;
    }


    /* ========================================================
       MÉTRICAS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff;

        border: 1px solid #e1e6eb;

        border-radius: 14px;

        padding: 15px;

        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.04);
    }


    /* ========================================================
       BOTÕES
       ======================================================== */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;

        font-weight: 700;

        min-height: 42px;
    }


    /* ========================================================
       TABELAS
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }


    /* ========================================================
       RESPONSIVIDADE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .sf-header {
            padding: 25px 22px 20px 22px;
        }

        .sf-header-title {
            font-size: 1.65rem;
        }

        .sf-subtitle {
            font-size: 0.9rem;
        }

        .sf-section h2 {
            font-size: 1.15rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CABEÇALHO PRINCIPAL
# ============================================================

st.markdown(
    """
    <div class="sf-header">

        <div class="sf-header-title">
            📐 CALCULADORA STEEL FRAMING
        </div>

        <div class="sf-subtitle">
            Sistema profissional para orçamento de
            materiais, quantitativos e mão de obra.
        </div>

        <div class="sf-badge">
            ORÇAMENTO PROFISSIONAL • VERSÃO 6C
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# IDENTIFICAÇÃO DO PROJETO
# ============================================================

st.markdown(
    """
    <div class="sf-section">
        <h2>📋 Identificação do projeto</h2>
        <p>Informe os dados principais do orçamento.</p>
    </div>
    """,
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


observacoes = st.text_area(
    "Observações",
    placeholder="Informações adicionais sobre o orçamento...",
)


st.divider()


# ============================================================
# DIMENSÕES DO PROJETO
# ============================================================

st.markdown(
    """
    <div class="sf-section">
        <h2>📐 Dimensões do projeto</h2>
        <p>Informe as dimensões utilizadas no cálculo.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2, col3 = st.columns(3)


with col1:

    comprimento = st.number_input(
        "Comprimento (m)",
        min_value=0.01,
        value=30.00,
        step=0.10,
        format="%.2f",
    )


with col2:

    altura = st.number_input(
        "Altura (m)",
        min_value=0.01,
        value=3.00,
        step=0.10,
        format="%.2f",
    )


with col3:

    area_preview = comprimento * altura

    st.metric(
        "Área do projeto",
        f"{area_preview:.2f} m²",
    )


st.divider()


# ============================================================
# PREÇOS DOS MATERIAIS
# ============================================================

st.markdown(
    """
    <div class="sf-section">
        <h2>💰 Preços dos materiais</h2>
        <p>
            Altere os preços conforme fornecedor,
            região ou condição de compra.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


if "precos" not in st.session_state:

    st.session_state["precos"] = PRECOS_BASE.copy()


precos_atualizados = {}


for nome, preco_padrao in st.session_state["precos"].items():

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
# QUANTIDADES DOS MATERIAIS
# ============================================================

st.markdown(
    """
    <div class="sf-section">
        <h2>📦 Quantidades dos materiais</h2>
        <p>
            As quantidades são calculadas automaticamente.
            Você pode alterar qualquer quantidade conforme
            a necessidade da obra.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
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


st.session_state["quantidades"] = quantidades_atualizadas


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

    st.session_state["nome_projeto"] = nome_projeto

    st.session_state["cliente"] = cliente

    st.session_state["local_obra"] = local_obra

    st.session_state["responsavel"] = responsavel

    st.session_state["data_orcamento"] = data_orcamento

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


    st.divider()


    # ========================================================
    # RESUMO DO ORÇAMENTO
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
    # QUANTITATIVO DE MATERIAIS
    # ========================================================

    st.subheader(
        "📋 Quantitativo de materiais"
    )


    tabela_materiais = []


    for nome, material in projeto["materiais"].items():

        tabela_materiais.append(
            {
                "Material": nome,

                "Unidade": material["unidade"],

                "Quantidade": (
                    f'{material["quantidade"]:.2f}'
                ),

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
    # OBSERVAÇÕES
    # ========================================================

    observacoes_salvas = st.session_state.get(
        "observacoes",
        "",
    )


    if observacoes_salvas:

        st.subheader(
            "📝 Observações"
        )

        st.write(
            observacoes_salvas
        )

        st.divider()


    # ========================================================
    # TOTAL
    # ========================================================

    st.success(
        f'💰 CUSTO GERAL: '
        f'{formatar_moeda(projeto["custo_geral"])}'
    )
