import streamlit as st
import pandas as pd
from datetime import date

from core.calculos import calcular_projeto
from core.dados import PRECOS_BASE


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Calculadora Steel Framing",
    page_icon="📐",
    layout="wide",
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
# CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');


    /* ========================================================
       CONFIGURAÇÃO GERAL
       ======================================================== */

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
       ESTILIZAÇÃO NATIVA DO CABEÇALHO
       ======================================================== */

    div[data-testid="stVerticalBlock"] > div:has(h1) {
        background: linear-gradient(
            135deg,
            #17202a 0%,
            #263746 55%,
            #34495e 100%
        );
        border-radius: 18px;
        padding: 35px 38px 30px 38px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }


    /* ========================================================
       TÍTULO PRINCIPAL
       ======================================================== */

    div[data-testid="stVerticalBlock"] h1 {
        color: #6fa8c9 !important;
        font-size: 3.5rem !important;
        line-height: 1.2 !important;
        font-weight: 900 !important;
        letter-spacing: -1px !important;
        margin: 0 0 10px 0 !important;
        padding: 0 !important;
        border: none !important;
    }


    /* ========================================================
       SUBTÍTULO
       ======================================================== */

    div[data-testid="stVerticalBlock"] h1 + p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
        margin: 0 0 16px 0 !important;
        padding: 0 !important;
    }


    /* ========================================================
       CAPTION / VERSÃO
       ======================================================== */

    div[data-testid="stVerticalBlock"] .stCaption {
        display: inline-block !important;
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 999px !important;
        padding: 7px 14px !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.6px !important;
        margin: 0 !important;
    }


    /* ========================================================
       SEÇÕES
       ======================================================== */

    .section-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #17202a;
        margin-top: 28px;
        margin-bottom: 4px;
    }

    .section-description {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 16px;
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


    /* ========================================================
       MÉTRICAS
       ======================================================== */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e6eb;
        border-radius: 14px;
        padding: 15px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
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
       VALORES DE SUBTOTAL
       ======================================================== */

    .total-item-value {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif !important;

        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        text-align: right !important;
        display: block !important;
        margin-top: 5px !important;
    }


    /* ========================================================
       RESPONSIVIDADE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        div[data-testid="stVerticalBlock"] h1 {
            font-size: 2.2rem !important;
        }

        div[data-testid="stVerticalBlock"] h1 + p {
            font-size: 1rem !important;
        }

        .section-title {
            font-size: 1.15rem;
        }

        .total-item-value {
            font-size: 1rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CABEÇALHO PRINCIPAL
# ============================================================

st.title("📐 CALCULADORA STEEL FRAMING")

st.markdown(
    "Sistema profissional para orçamento de materiais, "
    "quantitativos e mão de obra."
)

st.caption("ORÇAMENTO PROFISSIONAL • VERSÃO 6C")


# ============================================================
# IDENTIFICAÇÃO DO PROJETO
# ============================================================

st.markdown(
    '<div class="section-title">📋 Identificação do projeto</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Informe os dados principais do orçamento.'
    '</div>',
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
# DIMENSÕES
# ============================================================

st.markdown(
    '<div class="section-title">📐 Dimensões do projeto</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Informe as dimensões utilizadas no cálculo.'
    '</div>',
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
# PREÇOS
# ============================================================

st.markdown(
    '<div class="section-title">💰 Preços dos materiais</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Altere os preços conforme fornecedor, região ou condição de compra.'
    '</div>',
    unsafe_allow_html=True,
)


if "precos" not in st.session_state:
    st.session_state["precos"] = PRECOS_BASE.copy()


precos_atualizados = {}

cols_precos = st.columns(2)

for i, (nome, preco_padrao) in enumerate(
    st.session_state["precos"].items()
):

    with cols_precos[i % 2]:

        precos_atualizados[nome] = st.number_input(
            f"Preço: {nome}",
            min_value=0.0,
            value=float(preco_padrao),
            step=0.5,
            format="%.2f",
            key=f"preco_projeto_{nome}",
        )


st.session_state["precos"] = precos_atualizados
