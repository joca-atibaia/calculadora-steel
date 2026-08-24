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
# Linkar o manifesto para transformação em App
st.markdown(
    """
    <link rel="manifest" href="https://githubusercontent.com">
    """,
    unsafe_allow_html=True
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

    @import url(
        'https://googleapis.com'
    );


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

    /* Caixa de fundo do cabeçalho */
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

    /* Título principal interno */
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

    /* Subtítulo / Descrição interna */
    div[data-testid="stVerticalBlock"] h1 + p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
        margin: 0 0 16px 0 !important;
        padding: 0 !important;
    }

    /* Versão interna / Caption */
    div[data-testid="stVerticalBlock"] .stCaption  {
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
       ESTILO DE LETRAS DO SUBTOTAL CORRIGIDO
       ======================================================== */
    .total-item-value {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        text-align: right !important;
        display: block !important;
        margin-top: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
