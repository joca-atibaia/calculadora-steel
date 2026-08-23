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
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_moeda(valor):
    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def titulo_secao(titulo, subtitulo=None):
    # Renderiza o título principal de forma limpa
    st.markdown(
        f"""
        <div style="
            margin-top: 28px;
            margin-bottom: 4px;
            font-size: 1.35rem;
            font-weight: 800;
            color: #17202a;
            line-height: 1.3;
        ">
            {titulo}
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Renderiza o subtítulo de forma nativa e sem bugs usando st.caption
    if subtitulo:
        st.caption(subtitulo)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://googleapis.com'
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
    <div style="
        background: linear-gradient(
            135deg,
            #17202a 0%,
            #263746 55%,
            #34495e 100%
        );
        border-radius: 18px;
        padding: 34px 38px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
        color: white;
    ">

        <div style="
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            line-height: 1.2;
            margin-bottom: 10px;
            color: white;
        ">
            📐 CALCULADORA STEEL FRAMING
        </div>

        <div style="
            font-size: 1rem;
            font-weight: 400;
            color: #dce3e8;
            line-height: 1.6;
            margin-bottom: 18px;
        ">
            Sistema profissional para orçamento de
            materiais, quantitativos e mão de obra.
        </div>

        <div style="
            display: inline-block;
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: 999px;
            padding: 7px 14px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.6px;
            color: white;
        ">
            ORÇAMENTO PROFISSIONAL • VERSÃO 6C
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# IDENTIFICAÇÃO DO PROJETO
# ============================================================

titulo_secao(
    "📋 Identificação do projeto",
    "Informe os dados principais do orçamento.",
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

titulo_secao(
    "📐 Dimensões do projeto",
    "Informe as dimensões utilizadas no cálculo.",
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

titulo_secao(
    "💰 Preços dos materiais",
    "Altere os preços conforme fornecedor, região ou condição de compra.",
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

# Salva as alterações feitas pelo usuário de volta no estado da sessão
st.session_state["precos"] = precos_atualizados
