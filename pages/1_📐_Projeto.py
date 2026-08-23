import streamlit as st
import pandas as pd

from datetime import date
from io import BytesIO
from html import escape

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
# CSS — APARÊNCIA 6C
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f5f7fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ======================================================
       TIPOGRAFIA GERAL — VISUAL PROFISSIONAL 6C
       ====================================================== */

    html,
    body,
    [class*="css"] {
        font-family:
            "Inter",
            "Segoe UI",
            Roboto,
            Helvetica,
            Arial,
            sans-serif;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        background:
            linear-gradient(
                135deg,
                #17202a 0%,
                #263746 55%,
                #34495e 100%
            );
        border-radius: 18px;
        padding: 34px 38px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        color: white;
    }

    .hero-title {
        font-family:
            "Inter",
            "Segoe UI",
            sans-serif;
        font-size: 2.15rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-family:
            "Inter",
            "Segoe UI",
            sans-serif;
        font-size: 1rem;
        font-weight: 400;
        color: #dce3e8;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 999px;
        padding: 7px 14px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.6px;
    }

    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-header {
        margin-top: 28px;
        margin-bottom: 16px;
    }

    .section-title {
        font-family:
            "Inter",
            "Segoe UI",
            sans-serif;
        font-size: 1.35rem;
        font-weight: 800;
        color: #17202a;
        margin-bottom: 3px;
        letter-spacing: -0.2px;
    }

    .section-subtitle {
        font-family:
            "Inter",
            "Segoe UI",
            sans-serif;
        color: #6b7280;
        font-size: 0.9rem;
        font-weight: 400;
        margin-bottom: 18px;
    }

    /* ======================================================
       CARDS
       ====================================================== */

    .info-card {
        background: white;
        border: 1px solid #e1e6eb;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 14px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .card-label {
        color: #7b8794;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 5px;
    }

    .card-value {
        color: #17202a;
        font-size: 1rem;
        font-weight: 600;
    }

    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        background: white;
        border: 1px solid #e1e6eb;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .metric-label {
        color: #7b8794;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.8px;
        margin-bottom: 7px;
    }

    .metric-value {
        color: #17202a;
        font-size: 1.65rem;
        font-weight: 800;
    }

    /* ======================================================
       TOTAL
       ====================================================== */

    .total-card {
        background: linear-gradient(
            135deg,
            #ecfdf3,
            #f6fff9
        );
        border: 2px solid #28a745;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        margin: 22px 0;
        box-shadow: 0 5px 18px rgba(40,167,69,0.10);
    }

    .total-label {
        color: #36734a;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .total-value {
        color: #176b35;
        font-size: 2.2rem;
        font-weight: 900;
        margin-top: 5px;
    }

    /* ======================================================
       ASSINATURA
       ====================================================== */

    .assinatura {
        margin: 55px auto 25px auto;
        max-width: 520px;
        text-align: center;
    }

    .linha-assinatura {
        border-top: 1px solid #333;
        width: 85%;
        margin: 0 auto 10px auto;
    }

    .assinatura-nome {
        font-weight: 700;
        color: #17202a;
        font-size: 0.95rem;
    }

    .assinatura-cargo {
        color: #777;
        font-size: 0.8rem;
        margin-top: 5px;
    }

    /* ======================================================
       TABELAS / CAIXAS
       ====================================================== */

    .table-card {
        background: white;
        border: 1px solid #e1e6eb;
        border-radius: 14px;
        padding: 8px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .notice-card {
        background: #fff;
        border-left: 4px solid #34495e;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 12px 0;
        color: #374151;
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 9px;
    }

    .stTextInput label,
    .stNumberInput label,
    .stDateInput label,
    .stTextArea label,
    .stSelectbox label {
        font-weight: 600;
        color: #374151;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
        min-height: 42px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e1e6eb;
        border-radius: 12px;
        padding: 12px;
    }

    /* ======================================================
       DATAFRAME
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
