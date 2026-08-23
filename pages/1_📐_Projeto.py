# ============================================================
# 📐 CALCULADORA STEEL FRAMING — VERSÃO 6B
# LOCO 1 — IMPORTS + CONFIGURAÇÃO + CSS + FUNÇÕES + ESTADO
# ============================================================

import streamlit as st
import pandas as pd

from datetime import date
from io import BytesIO
from html import escape


# ============================================================
# IMPORTAÇÕES DO PROJETO
# ============================================================

from core.calculos import (
    calcular_projeto,
    calcular_indicadores_projeto,
)

from core.dados import (
    PRECOS_BASE,
    MATERIAIS,
    CONFIGURACAO_PROJETO,
)


# ============================================================
# CONFIGURAÇÃO DO STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Calculadora Steel Framing",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS — VISUAL PROFISSIONAL 6B
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       BASE
       ====================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
    );

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] *,
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


    /* ======================================================
       REMOVE EXCESSOS VISUAIS DO STREAMLIT
       ====================================================== */

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        right: 1rem;
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

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.12);

        color: #ffffff;
    }

    .hero-title {
        font-size: 2.15rem;

        font-weight: 800;

        letter-spacing: -0.5px;

        line-height: 1.2;

        margin-bottom: 10px;

        color: #ffffff;
    }

    .hero-subtitle {
        font-size: 1rem;

        font-weight: 400;

        color: #dce3e8;

        line-height: 1.6;

        margin-bottom: 18px;
    }

    .hero-badge {
        display: inline-block;

        background:
            rgba(255, 255, 255, 0.12);

        border:
            1px solid rgba(255, 255, 255, 0.22);

        border-radius: 999px;

        padding: 7px 14px;

        font-size: 0.75rem;

        font-weight: 700;

        letter-spacing: 0.6px;

        color: #ffffff;
    }


    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-header {
        margin-top: 28px;

        margin-bottom: 16px;
    }

    .section-title {
        font-size: 1.35rem;

        font-weight: 800;

        color: #17202a;

        margin-bottom: 3px;

        line-height: 1.3;
    }

    .section-subtitle {
        color: #6b7280;

        font-size: 0.9rem;

        margin-bottom: 18px;

        line-height: 1.5;
    }


    /* ======================================================
       CARDS
       ====================================================== */

    .info-card {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 14px;

        padding: 18px 20px;

        margin-bottom: 14px;

        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.04);
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

        line-height: 1.45;
    }


    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 14px;

        padding: 20px;

        text-align: center;

        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.04);
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

        line-height: 1.2;
    }


    /* ======================================================
       TOTAL
       ====================================================== */

    .total-card {
        background:
            linear-gradient(
                135deg,
                #ecfdf3,
                #f6fff9
            );

        border:
            2px solid #28a745;

        border-radius: 16px;

        padding: 25px;

        text-align: center;

        margin: 22px 0;

        box-shadow:
            0 5px 18px rgba(40, 167, 69, 0.10);
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
       AVISOS
       ====================================================== */

    .notice-card {
        background: #ffffff;

        border-left:
            4px solid #34495e;

        border-radius: 10px;

        padding: 15px 18px;

        margin: 12px 0;

        color: #374151;

        line-height: 1.6;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.03);
    }


    /* ======================================================
       CAMPOS
       ====================================================== */

    .stTextInput label,
    .stNumberInput label,
    .stDateInput label,
    .stTextArea label,
    .stSelectbox label,
    .stCheckbox label {
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


    /* ======================================================
       BOTÕES
       ====================================================== */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;

        font-weight: 700;

        min-height: 42px;
    }


    /* ======================================================
       TABELAS
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;

        overflow: hidden;
    }


    /* ======================================================
       RESPONSIVIDADE
       ====================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 25px 22px;
        }

        .hero-title {
            font-size: 1.65rem;
        }

        .hero-subtitle {
            font-size: 0.9rem;
        }

        .section-title {
            font-size: 1.15rem;
        }

        .metric-value {
            font-size: 1.35rem;
        }

        .total-value {
            font-size: 1.8rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def numero(valor, padrao=0.0):
    """
    Converte um valor para float com segurança.
    """

    try:

        if valor is None:
            return float(padrao)

        return float(valor)

    except (TypeError, ValueError):

        return float(padrao)


def formatar_moeda(valor):
    """
    Formata valores no padrão monetário brasileiro.

    Exemplo:
        11958.50
        -> R$ 11.958,50
    """

    valor = numero(valor)

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def obter_valor(dicionario, chave, padrao=0):
    """
    Obtém um valor de dicionário sem gerar erro
    caso o dicionário ou a chave não existam.
    """

    if not isinstance(dicionario, dict):
        return padrao

    valor = dicionario.get(chave, padrao)

    if valor is None:
        return padrao

    return valor


def texto_seguro(valor, padrao=""):
    """
    Converte qualquer valor para texto seguro.
    """

    if valor is None:
        return padrao

    return str(valor).strip()


def nome_arquivo_seguro(nome, padrao="Orcamento_Steel_Framing"):
    """
    Prepara o nome do projeto para utilização
    como nome de arquivo.
    """

    nome = texto_seguro(nome)

    if not nome:
        return padrao

    caracteres_invalidos = [
        "/",
        "\\",
        ":",
        "*",
        "?",
        '"',
        "<",
        ">",
        "|",
    ]

    for caractere in caracteres_invalidos:
        nome = nome.replace(
            caractere,
            "_",
        )

    nome = nome.replace(
        " ",
        "_",
    )

    return nome[:120]


# ============================================================
# INICIALIZAÇÃO DO ESTADO
# ============================================================

def inicializar_estado():

    defaults = {

        # ----------------------------------------------------
        # IDENTIFICAÇÃO
        # ----------------------------------------------------

        "nome_projeto": "",

        "cliente": "",

        "local_obra": "",

        "responsavel": "",

        "data_orcamento": date.today(),


        # ----------------------------------------------------
        # CONDIÇÕES COMERCIAIS
        # ----------------------------------------------------

        "validade_orcamento": 10,

        "prazo_execucao": "",

        "condicao_pagamento": "",

        "forma_pagamento": "Pix",

        "observacoes_comerciais": "",

        "observacoes_tecnicas": "",


        # ----------------------------------------------------
        # DIMENSÕES
        # ----------------------------------------------------

        "comprimento": 30.00,

        "altura": 3.00,


        # ----------------------------------------------------
        # MÃO DE OBRA
        # ----------------------------------------------------

        "diaria_mao_obra":
            numero(
                CONFIGURACAO_PROJETO.get(
                    "diaria_mao_de_obra",
                    755.00,
                ),
                755.00,
            ),


        # ----------------------------------------------------
        # PREÇOS
        # ----------------------------------------------------

        "precos":
            dict(PRECOS_BASE),


        # ----------------------------------------------------
        # QUANTIDADES MANUAIS
        # ----------------------------------------------------

        "quantidades": {},


        # ----------------------------------------------------
        # RESULTADO DO PROJETO
        # ----------------------------------------------------

        "projeto": None,


        # ----------------------------------------------------
        # MASSAS E TELAS
        # ----------------------------------------------------

        "massas_telas_manual": None,

        "usar_massas_manual": False,
    }


    for chave, valor in defaults.items():

        if chave not in st.session_state:

            st.session_state[chave] = valor


# Executa a inicialização
inicializar_estado()


# ============================================================
# FIM DO LOCO 1
# ============================================================
