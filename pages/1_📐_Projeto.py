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
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS — FASE 6C
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       BASE
       ====================================================== */

    .stApp {
        background:
            linear-gradient(
                180deg,
                #f7f9fc 0%,
                #ffffff 45%,
                #f7f9fc 100%
            );
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    html,
    body,
    [class*="css"] {
        font-family:
            -apple-system,
            BlinkMacSystemFont,
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
        position: relative;
        padding: 34px 38px 30px 38px;
        margin-bottom: 30px;

        border-radius: 20px;

        background:
            linear-gradient(
                135deg,
                #172033 0%,
                #263653 55%,
                #30466b 100%
            );

        box-shadow:
            0 14px 35px rgba(15, 23, 42, 0.14);

        overflow: hidden;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        right: -80px;
        top: -120px;

        border-radius: 50%;

        background: rgba(255,255,255,0.06);
    }

    .hero-title {
        position: relative;
        z-index: 2;

        color: #ffffff;

        font-size: 34px;
        line-height: 1.15;
        font-weight: 800;

        letter-spacing: -0.8px;

        margin-bottom: 10px;
    }

    .hero-subtitle {
        position: relative;
        z-index: 2;

        color: rgba(255,255,255,0.78);

        font-size: 16px;
        line-height: 1.5;

        font-weight: 400;

        max-width: 720px;
    }

    .hero-badge {
        position: relative;
        z-index: 2;

        display: inline-block;

        margin-top: 18px;
        padding: 7px 13px;

        border-radius: 999px;

        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);

        color: rgba(255,255,255,0.90);

        font-size: 11px;
        font-weight: 700;

        letter-spacing: 0.8px;
    }


    /* ======================================================
       TÍTULOS DAS SEÇÕES
       ====================================================== */

    .section-header {
        margin-top: 30px;
        margin-bottom: 16px;
    }

    .section-title {
        color: #172033;

        font-size: 21px;
        line-height: 1.25;

        font-weight: 750;

        letter-spacing: -0.25px;

        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #6b7280;

        font-size: 13px;
        line-height: 1.5;

        margin-bottom: 15px;
    }

    .section-line {
        height: 1px;

        background:
            linear-gradient(
                90deg,
                #dce2ea 0%,
                transparent 100%
            );

        margin: 5px 0 22px 0;
    }


    /* ======================================================
       CARDS
       ====================================================== */

    .info-card {
        background: #ffffff;

        border: 1px solid #e5e9ef;

        border-radius: 14px;

        padding: 18px 20px;

        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.045);

        height: 100%;

        margin-bottom: 12px;
    }

    .card-label {
        color: #7a8494;

        font-size: 11px;
        line-height: 1.3;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.7px;

        margin-bottom: 5px;
    }

    .card-value {
        color: #172033;

        font-size: 15px;
        line-height: 1.45;

        font-weight: 600;
    }

    .card-value-muted {
        color: #8a93a1;

        font-size: 14px;
        font-weight: 500;
    }


    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        background: #ffffff;

        border: 1px solid #e5e9ef;

        border-radius: 14px;

        padding: 20px 22px;

        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.045);

        min-height: 105px;
    }

    .metric-label {
        color: #7a8494;

        font-size: 11px;

        font-weight: 750;

        letter-spacing: 0.8px;

        text-transform: uppercase;

        margin-bottom: 7px;
    }

    .metric-value {
        color: #172033;

        font-size: 26px;

        line-height: 1.15;

        font-weight: 800;

        letter-spacing: -0.5px;
    }


    /* ======================================================
       RESUMO FINANCEIRO
       ====================================================== */

    .financial-card {
        background: #ffffff;

        border: 1px solid #e5e9ef;

        border-radius: 14px;

        padding: 20px 22px;

        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.045);

        height: 100%;
    }

    .financial-label {
        color: #70798a;

        font-size: 12px;

        font-weight: 650;

        margin-bottom: 8px;
    }

    .financial-value {
        color: #172033;

        font-size: 23px;

        font-weight: 800;

        letter-spacing: -0.3px;
    }


    /* ======================================================
       TOTAL
       ====================================================== */

    .total-box {
        position: relative;

        margin: 24px 0 26px 0;

        padding: 27px 30px;

        border-radius: 17px;

        border: 1px solid #b8dfc0;

        background:
            linear-gradient(
                135deg,
                #f3fff5 0%,
                #ffffff 100%
            );

        box-shadow:
            0 8px 25px rgba(22, 101, 52, 0.07);
    }

    .total-label {
        color: #4b6752;

        font-size: 12px;

        font-weight: 750;

        letter-spacing: 1px;

        margin-bottom: 6px;
    }

    .total-value {
        color: #17652b;

        font-size: 35px;

        line-height: 1.1;

        font-weight: 850;

        letter-spacing: -1px;
    }


    /* ======================================================
       OBSERVAÇÕES
       ====================================================== */

    .note-box {
        background: #ffffff;

        border: 1px solid #e5e9ef;

        border-left: 4px solid #526b91;

        border-radius: 10px;

        padding: 15px 18px;

        color: #4b5563;

        font-size: 14px;

        line-height: 1.6;

        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.035);
    }


    /* ======================================================
       ASSINATURA
       ====================================================== */

    .assinatura {
        margin: 55px auto 15px auto;

        max-width: 420px;

        text-align: center;

        color: #172033;
    }

    .linha-assinatura {
        border-top: 1px solid #475569;

        width: 100%;

        margin: 0 auto 10px auto;
    }

    .assinatura-nome {
        font-size: 14px;

        font-weight: 750;

        line-height: 1.4;
    }

    .assinatura-cargo {
        margin-top: 4px;

        color: #7a8494;

        font-size: 12px;

        font-weight: 500;
    }


    /* ======================================================
       EXPORTAÇÃO
       ====================================================== */

    .export-card {
        background: #ffffff;

        border: 1px solid #e5e9ef;

        border-radius: 14px;

        padding: 20px;

        box-shadow:
            0 5px 18px rgba(15, 23, 42, 0.045);

        height: 100%;
    }

    .export-title {
        color: #172033;

        font-size: 15px;

        font-weight: 750;

        margin-bottom: 5px;
    }

    .export-description {
        color: #7a8494;

        font-size: 12px;

        line-height: 1.5;

        margin-bottom: 14px;
    }


    /* ======================================================
       STREAMLIT INPUTS
       ====================================================== */

    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] {
        border-radius: 9px;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        border-color: #dfe4eb;
        background: #ffffff;
    }

    label[data-testid="stWidgetLabel"] p {
        color: #374151;

        font-size: 13px;

        font-weight: 650;
    }

    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {
        font-size: 14px;
    }


    /* ======================================================
       BOTÕES
       ====================================================== */

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;

        font-weight: 700;

        min-height: 42px;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 5px 14px rgba(15, 23, 42, 0.10);
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #e3e7ed;

        border-radius: 12px;

        overflow: hidden;

        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.035);
    }


    /* ======================================================
       DIVISORES
       ====================================================== */

    hr {
        border-color: #e7ebf0 !important;
        margin: 25px 0 !important;
    }


    /* ======================================================
       RESPONSIVO
       ====================================================== */

    @media (max-width: 768px) {

        .hero {
            padding: 26px 22px;
            border-radius: 16px;
        }

        .hero-title {
            font-size: 27px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        .total-value {
            font-size: 29px;
        }

        .metric-value {
            font-size: 23px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_moeda(valor):
    try:
        valor = float(valor or 0)
    except (TypeError, ValueError):
        valor = 0.0

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def obter_valor(dicionario, chave, padrao=0):
    if not isinstance(dicionario, dict):
        return padrao

    valor = dicionario.get(chave, padrao)

    if valor is None:
        return padrao

    return valor


def nome_arquivo_orcamento():
    nome = st.session_state.get(
        "nome_projeto",
        "",
    )

    nome = str(nome).strip()

    if not nome:
        return "Orcamento_Steel_Framing"

    nome = (
        nome
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
    )

    return nome


# ============================================================
# GERAÇÃO DO EXCEL
# ============================================================

def gerar_excel(projeto):

    try:
        from openpyxl import Workbook
        from openpyxl.styles import (
            Font,
            PatternFill,
            Border,
            Side,
            Alignment,
        )
        from openpyxl.utils import get_column_letter

    except ImportError:

        st.error(
            "A biblioteca 'openpyxl' não está instalada. "
            "Adicione 'openpyxl' ao arquivo requirements.txt "
            "e faça o deploy novamente."
        )

        return None

    # --------------------------------------------------------
    # DADOS
    # --------------------------------------------------------

    nome_projeto = st.session_state.get(
        "nome_projeto",
        "",
    )

    cliente = st.session_state.get(
        "cliente",
        "",
    )

    local_obra = st.session_state.get(
        "local_obra",
        "",
    )

    responsavel = st.session_state.get(
        "responsavel",
        "",
    )

    data_orcamento = st.session_state.get(
        "data_orcamento",
        date.today(),
    )

    validade = st.session_state.get(
        "validade_orcamento",
        10,
    )

    prazo_execucao = st.session_state.get(
        "prazo_execucao",
        "",
    )

    condicao_pagamento = st.session_state.get(
        "condicao_pagamento",
        "",
    )

    forma_pagamento = st.session_state.get(
        "forma_pagamento",
        "",
    )

    observacoes_comerciais = st.session_state.get(
        "observacoes_comerciais",
        "",
    )

    observacoes_tecnicas = st.session_state.get(
        "observacoes_tecnicas",
        "",
    )

    comprimento = st.session_state.get(
        "comprimento",
        projeto.get("area", 0),
    )

    altura = st.session_state.get(
        "altura",
        "",
    )

    area = obter_valor(
        projeto,
        "area",
    )

    subtotal_materiais = obter_valor(
        projeto,
        "subtotal_materiais",
    )

    massas_telas = obter_valor(
        projeto,
        "massas_telas",
    )

    custo_geral = obter_valor(
        projeto,
        "custo_geral",
    )

    materiais = projeto.get(
        "materiais",
        {},
    )

    mao_de_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    dias = obter_valor(
        mao_de_obra,
        "dias",
    )

    diaria = obter_valor(
        mao_de_obra,
        "diaria",
    )

    custo_mao_de_obra = obter_valor(
        mao_de_obra,
        "custo",
    )

    # --------------------------------------------------------
    # WORKBOOK
    # --------------------------------------------------------

    wb = Workbook()

    ws_orcamento = wb.active
    ws_orcamento.title = "ORÇAMENTO"

    ws_materiais = wb.create_sheet(
        "MATERIAIS"
    )

    ws_mao = wb.create_sheet(
        "MÃO DE OBRA"
    )

    ws_dados = wb.create_sheet(
        "DADOS"
    )

    # --------------------------------------------------------
    # ESTILOS
    # --------------------------------------------------------

    cor_azul = "172033"
    cor_azul_claro = "EAF0F8"
    cor_cinza = "F4F6F8"
    cor_borda = "D9E0E8"
    cor_verde = "17652B"
    cor_verde_claro = "F3FFF5"
    branco = "FFFFFF"

    fonte_titulo = Font(
        name="Aptos Display",
        size=20,
        bold=True,
        color=branco,
    )

    fonte_secao = Font(
        name="Aptos",
        size=12,
        bold=True,
        color=cor_azul,
    )

    fonte_normal = Font(
        name="Aptos",
        size=10,
        color="374151",
    )

    fonte_bold = Font(
        name="Aptos",
        size=10,
        bold=True,
        color=cor_azul,
    )

    fonte_total = Font(
        name="Aptos Display",
        size=18,
        bold=True,
        color=cor_verde,
    )

    preenchimento_titulo = PatternFill(
        "solid",
        fgColor=cor_azul,
    )

    preenchimento_secao = PatternFill(
        "solid",
        fgColor=cor_azul_claro,
    )

    preenchimento_cinza = PatternFill(
        "solid",
        fgColor=cor_cinza,
    )

    preenchimento_total = PatternFill(
        "solid",
        fgColor=cor_verde_claro,
    )

    linha_fina = Side(
        style="thin",
        color=cor_borda,
    )

    borda = Border(
        left=linha_fina,
        right=linha_fina,
        top=linha_fina,
        bottom=linha_fina,
    )

    alinhamento_centro = Alignment(
        horizontal="center",
        vertical="center",
    )

    alinhamento_direita = Alignment(
        horizontal="right",
        vertical="center",
    )

    alinhamento_esquerda = Alignment(
        horizontal="left",
        vertical="center",
    )

    formato_moeda = (
        '"R$" #,##0.00'
    )

    # --------------------------------------------------------
    # ABA ORÇAMENTO
    # --------------------------------------------------------

    ws = ws_orcamento

    ws.merge_cells(
        "A1:F1"
    )

    ws["A1"] = (
        "ORÇAMENTO — STEEL FRAMING"
    )

    ws["A1"].font = fonte_titulo
    ws["A1"].fill = preenchimento_titulo
    ws["A1"].alignment = alinhamento_centro

    ws.row_dimensions[1].height = 34

    ws.merge_cells(
        "A2:F2"
    )

    ws["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws["A2"].font = Font(
        name="Aptos",
        size=10,
        italic=True,
        color="6B7280",
    )

    ws["A2"].alignment = alinhamento_centro

    # --------------------------------------------------------
    # IDENTIFICAÇÃO
    # --------------------------------------------------------

    ws.merge_cells("A4:F4")

    ws["A4"] = (
        "IDENTIFICAÇÃO DO PROJETO"
    )

    ws["A4"].font = fonte_secao
    ws["A4"].fill = preenchimento_secao

    dados_identificacao = [
        ("Projeto", nome_projeto or "Não informado"),
        ("Cliente", cliente or "Não informado"),
        ("Local da obra", local_obra or "Não informado"),
        ("Responsável", responsavel or "Não informado"),
        (
            "Data",
            data_orcamento.strftime("%d/%m/%Y"),
        ),
    ]

    linha = 5

    for chave, valor in dados_identificacao:

        ws.cell(
            linha,
            1,
            chave,
        )

        ws.cell(
            linha,
            1,
        ).font = fonte_bold

        ws.cell(
            linha,
            2,
            valor,
        )

        ws.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=6,
        )

        ws.cell(
            linha,
            2,
        ).font = fonte_normal

        for col in range(1, 7):
            ws.cell(
                linha,
                col,
            ).border = borda

        linha += 1

    # --------------------------------------------------------
    # DIMENSÕES
    # --------------------------------------------------------

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=6,
    )

    ws.cell(
        linha,
        1,
        "DIMENSÕES DO PROJETO",
    )

    ws.cell(
        linha,
        1,
    ).font = fonte_secao

    ws.cell(
        linha,
        1,
    ).fill = preenchimento_secao

    linha += 1

    dimensoes = [
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
    ]

    for chave, valor in dimensoes:

        ws.cell(
            linha,
            1,
            chave,
        ).font = fonte_bold

        ws.cell(
            linha,
            2,
            float(valor or 0),
        )

        ws.cell(
            linha,
            2,
        ).number_format = '0.00'

        ws.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=6,
        )

        for col in range(1, 7):
            ws.cell(
                linha,
                col,
            ).border = borda

        linha += 1

    # --------------------------------------------------------
    # RESUMO FINANCEIRO
    # --------------------------------------------------------

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=6,
    )

    ws.cell(
        linha,
        1,
        "RESUMO FINANCEIRO",
    )

    ws.cell(
        linha,
        1,
    ).font = fonte_secao

    ws.cell(
        linha,
        1,
    ).fill = preenchimento_secao

    linha += 1

    financeiro_inicio = linha

    financeiro = [
        (
            "Materiais",
            float(subtotal_materiais),
        ),
        (
            "Massas e telas",
            float(massas_telas),
        ),
        (
            "Mão de obra",
            float(custo_mao_de_obra),
        ),
    ]

    for chave, valor in financeiro:

        ws.cell(
            linha,
            1,
            chave,
        ).font = fonte_bold

        ws.cell(
            linha,
            2,
            valor,
        ).number_format = formato_moeda

        ws.cell(
            linha,
            2,
        ).alignment = alinhamento_direita

        ws.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=6,
        )

        for col in range(1, 7):
            ws.cell(
                linha,
                col,
            ).border = borda

        linha += 1

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=3,
    )

    ws.cell(
        linha,
        1,
        "VALOR TOTAL DO ORÇAMENTO",
    )

    ws.cell(
        linha,
        1,
    ).font = fonte_total

    ws.cell(
        linha,
        1,
    ).fill = preenchimento_total

    ws.merge_cells(
        start_row=linha,
        start_column=4,
        end_row=linha,
        end_column=6,
    )

    ws.cell(
        linha,
        4,
        custo_geral,
    )

    ws.cell(
        linha,
        4,
    ).font = fonte_total

    ws.cell(
        linha,
        4,
    ).number_format = formato_moeda

    ws.cell(
        linha,
        4,
    ).alignment = alinhamento_direita

    for col in range(1, 7):
        ws.cell(
            linha,
            col,
        ).fill = preenchimento_total

        ws.cell(
            linha,
            col,
        ).border = borda

    linha += 2

    # --------------------------------------------------------
    # CONDIÇÕES
    # --------------------------------------------------------

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=6,
    )

    ws.cell(
        linha,
        1,
        "CONDIÇÕES COMERCIAIS",
    )

    ws.cell(
        linha,
        1,
    ).font = fonte_secao

    ws.cell(
        linha,
        1,
    ).fill = preenchimento_secao

    linha += 1

    condicoes = [
        (
            "Validade",
            f"{validade} dias",
        ),
        (
            "Prazo de execução",
            prazo_execucao or "Não informado",
        ),
        (
            "Condição de pagamento",
            condicao_pagamento or "Não informado",
        ),
        (
            "Forma de pagamento",
            forma_pagamento or "Não informado",
        ),
    ]

    for chave, valor in condicoes:

        ws.cell(
            linha,
            1,
            chave,
        ).font = fonte_bold

        ws.cell(
            linha,
            2,
            valor,
        ).font = fonte_normal

        ws.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=6,
        )

        for col in range(1, 7):
            ws.cell(
                linha,
                col,
            ).border = borda

        linha += 1

    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=6,
    )

    ws.cell(
        linha,
        1,
        "OBSERVAÇÕES COMERCIAIS",
    )

    ws.cell(
        linha,
        1,
    ).font = fonte_secao

    ws.cell(
        linha,
        1,
    ).fill = preenchimento_secao

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha + 2,
        end_column=6,
    )

    ws.cell(
        linha,
        1,
        observacoes_comerciais or "Não informado",
    )

    ws.cell(
        linha,
        1,
    ).alignment = Alignment(
        vertical="top",
        wrap_text=True,
    )

    for r in range(linha, linha + 3):
        for c in range(1, 7):
            ws.cell(
                r,
                c,
            ).border = borda

    linha += 4

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=6,
    )

    ws.cell(
        linha,
        1,
        "OBSERVAÇÕES TÉCNICAS",
    )

    ws.cell(
        linha,
        1,
    ).font = fonte_secao

    ws.cell(
        linha,
        1,
    ).fill = preenchimento_secao

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha + 2,
        end_column=6,
    )

    ws.cell(
        linha,
        1,
        observacoes_tecnicas or "Não informado",
    )

    ws.cell(
        linha,
        1,
    ).alignment = Alignment(
        vertical="top",
        wrap_text=True,
    )

    for r in range(linha, linha + 3):
        for c in range(1, 7):
            ws.cell(
                r,
                c,
            ).border = borda

    # --------------------------------------------------------
    # ABA MATERIAIS
    # --------------------------------------------------------

    ws = ws_materiais

    headers = [
        "Material",
        "Unidade",
        "Quantidade",
        "Preço unitário",
        "Total",
    ]

    for col, header in enumerate(
        headers,
        start=1,
    ):

        cell = ws.cell(
            1,
            col,
            header,
        )

        cell.font = Font(
            name="Aptos",
            size=10,
            bold=True,
            color=branco,
        )

        cell.fill = preenchimento_titulo
        cell.alignment = alinhamento_centro
        cell.border = borda

    for row, (nome, material) in enumerate(
        materiais.items(),
        start=2,
    ):

        quantidade = float(
            material.get(
                "quantidade",
                0,
            )
            or 0
        )

        preco = float(
            material.get(
                "preco_unitario",
                0,
            )
            or 0
        )

        custo = float(
            material.get(
                "custo",
                quantidade * preco,
            )
            or 0
        )

        ws.cell(
            row,
            1,
            nome,
        )

        ws.cell(
            row,
            2,
            material.get(
                "unidade",
                "",
            ),
        )

        ws.cell(
            row,
            3,
            quantidade,
        )

        ws.cell(
            row,
            4,
            preco,
        )

        ws.cell(
            row,
            5,
            f"=C{row}*D{row}",
        )

        ws.cell(
            row,
            3,
        ).number_format = "0.00"

        ws.cell(
            row,
            4,
        ).number_format = formato_moeda

        ws.cell(
            row,
            5,
        ).number_format = formato_moeda

        for col in range(1, 6):

            ws.cell(
                row,
                col,
            ).font = fonte_normal

            ws.cell(
                row,
                col,
            ).border = borda

    linha_total = len(materiais) + 2

    ws.cell(
        linha_total,
        1,
        "TOTAL MATERIAIS",
    )

    ws.cell(
        linha_total,
        1,
    ).font = fonte_bold

    ws.merge_cells(
        start_row=linha_total,
        start_column=1,
        end_row=linha_total,
        end_column=4,
    )

    ws.cell(
        linha_total,
        5,
        f"=SUM(E2:E{linha_total - 1})",
    )

    ws.cell(
        linha_total,
        5,
    ).font = fonte_bold

    ws.cell(
        linha_total,
        5,
    ).number_format = formato_moeda

    for col in range(1, 6):

        ws.cell(
            linha_total,
            col,
        ).fill = preenchimento_total

        ws.cell(
            linha_total,
            col,
        ).border = borda

    # --------------------------------------------------------
    # ABA MÃO DE OBRA
    # --------------------------------------------------------

    ws = ws_mao

    ws.merge_cells(
        "A1:D1"
    )

    ws["A1"] = (
        "MÃO DE OBRA"
    )

    ws["A1"].font = fonte_titulo
    ws["A1"].fill = preenchimento_titulo
    ws["A1"].alignment = alinhamento_centro

    dados_mao = [
        (
            "Dias estimados",
            float(dias),
        ),
        (
            "Valor da diária",
            float(diaria),
        ),
        (
            "Custo da mão de obra",
            float(custo_mao_de_obra),
        ),
    ]

    linha = 3

    for chave, valor in dados_mao:

        ws.cell(
            linha,
            1,
            chave,
        ).font = fonte_bold

        ws.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=4,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        if chave == "Dias estimados":
            ws.cell(
                linha,
                2,
            ).number_format = "0.0"
        else:
            ws.cell(
                linha,
                2,
            ).number_format = formato_moeda

        for col in range(1, 5):

            ws.cell(
                linha,
                col,
            ).border = borda

        linha += 1

    # --------------------------------------------------------
    # ABA DADOS
    # --------------------------------------------------------

    ws = ws_dados

    ws.merge_cells(
        "A1:B1"
    )

    ws["A1"] = (
        "DADOS DO ORÇAMENTO"
    )

    ws["A1"].font = fonte_titulo
    ws["A1"].fill = preenchimento_titulo
    ws["A1"].alignment = alinhamento_centro

    dados = [
        ("Projeto", nome_projeto),
        ("Cliente", cliente),
        ("Local da obra", local_obra),
        ("Responsável", responsavel),
        (
            "Data",
            data_orcamento.strftime("%d/%m/%Y"),
        ),
        ("Validade", f"{validade} dias"),
        (
            "Prazo de execução",
            prazo_execucao or "Não informado",
        ),
        (
            "Condição de pagamento",
            condicao_pagamento or "Não informado",
        ),
        (
            "Forma de pagamento",
            forma_pagamento or "Não informado",
        ),
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
        (
            "Observações comerciais",
            observacoes_comerciais or "Não informado",
        ),
        (
            "Observações técnicas",
            observacoes_tecnicas or "Não informado",
        ),
    ]

    linha = 3

    for chave, valor in dados:

        ws.cell(
            linha,
            1,
            chave,
        ).font = fonte_bold

        ws.cell(
            linha,
            2,
            valor,
        ).font = fonte_normal

        ws.cell(
            linha,
            1,
        ).border = borda

        ws.cell(
            linha,
            2,
        ).border = borda

        linha += 1

    # --------------------------------------------------------
    # LARGURAS
    # --------------------------------------------------------

    for ws in wb.worksheets:

        larguras = {}

        for row in ws.iter_rows():

            for cell in row:

                if cell.value is None:
                    continue

                valor = str(
                    cell.value
                )

                largura = len(valor) + 2

                if largura > 45:
                    largura = 45

                if (
                    cell.column
                    not in larguras
                    or largura
                    > larguras[cell.column]
                ):
                    larguras[cell.column] = largura

        for coluna, largura in larguras.items():

            ws.column_dimensions[
                get_column_letter(coluna)
            ].width = max(
                12,
                largura,
            )

        ws.freeze_panes = "A2"

    # --------------------------------------------------------
    # SALVAR
    # --------------------------------------------------------

    buffer = BytesIO()

    wb.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# GERAÇÃO DO PDF
# ============================================================

def gerar_pdf(projeto):

    try:

        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle,
        )
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
        )

    except ImportError:

        st.error(
            "A biblioteca 'reportlab' não está instalada. "
            "Adicione 'reportlab' ao arquivo requirements.txt "
            "e faça o deploy novamente."
        )

        return None

    # ========================================================
    # DADOS
    # ========================================================

    nome_projeto = st.session_state.get(
        "nome_projeto",
        "",
    )

    cliente = st.session_state.get(
        "cliente",
        "",
    )

    local_obra = st.session_state.get(
        "local_obra",
        "",
    )

    responsavel = st.session_state.get(
        "responsavel",
        "",
    )

    data_orcamento = st.session_state.get(
        "data_orcamento",
        date.today(),
    )

    validade = st.session_state.get(
        "validade_orcamento",
        10,
    )

    prazo_execucao = st.session_state.get(
        "prazo_execucao",
        "",
    )

    condicao_pagamento = st.session_state.get(
        "condicao_pagamento",
        "",
    )

    forma_pagamento = st.session_state.get(
        "forma_pagamento",
        "",
    )

    observacoes_comerciais = st.session_state.get(
        "observacoes_comerciais",
        "",
    )

    observacoes_tecnicas = st.session_state.get(
        "observacoes_tecnicas",
        "",
    )

    area = obter_valor(
        projeto,
        "area",
    )

    subtotal_materiais = obter_valor(
        projeto,
        "subtotal_materiais",
    )

    massas_telas = obter_valor(
        projeto,
        "massas_telas",
    )

    custo_geral = obter_valor(
        projeto,
        "custo_geral",
    )

    materiais = projeto.get(
        "materiais",
        {},
    )

    mao_de_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    dias = obter_valor(
        mao_de_obra,
        "dias",
    )

    diaria = obter_valor(
        mao_de_obra,
        "diaria",
    )

    custo_mao_de_obra = obter_valor(
        mao_de_obra,
        "custo",
    )

    comprimento = st.session_state.get(
        "comprimento",
        area,
    )

    altura = st.session_state.get(
        "altura",
        "",
    )

    # ========================================================
    # DOCUMENTO
    # ========================================================

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
        title="Orçamento Steel Framing",
        author=responsavel or "Calculadora Steel Framing",
    )

    styles = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloOrcamento",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=23,
        alignment=TA_CENTER,
        spaceAfter=5,
    )

    estilo_subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=15,
    )

    estilo_secao = ParagraphStyle(
        "Secao",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=8,
        spaceAfter=8,
    )

    estilo_normal = ParagraphStyle(
        "NormalOrcamento",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )

    estilo_pequeno = ParagraphStyle(
        "Pequeno",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
    )

    estilo_direita = ParagraphStyle(
        "Direita",
        parent=estilo_normal,
        alignment=TA_RIGHT,
    )

    estilo_centralizado = ParagraphStyle(
        "Centralizado",
        parent=estilo_normal,
        alignment=TA_CENTER,
    )

    estilo_total = ParagraphStyle(
        "Total",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        alignment=TA_RIGHT,
    )

    estilo_assinatura_nome = ParagraphStyle(
        "AssinaturaNome",
        parent=estilo_normal,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        spaceBefore=5,
        spaceAfter=2,
    )

    estilo_assinatura_cargo = ParagraphStyle(
        "AssinaturaCargo",
        parent=estilo_pequeno,
        alignment=TA_CENTER,
        textColor=colors.grey,
        fontSize=8,
        leading=10,
    )

    elementos = []

    # ========================================================
    # CABEÇALHO
    # ========================================================

    elementos.append(
        Paragraph(
            "ORÇAMENTO — STEEL FRAMING",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Quantitativo de materiais e mão de obra",
            estilo_subtitulo,
        )
    )

    # ========================================================
    # DADOS
    # ========================================================

    elementos.append(
        Paragraph(
            "1. DADOS DO ORÇAMENTO",
            estilo_secao,
        )
    )

    dados_orcamento = [
        [
            Paragraph(
                f"<b>Projeto:</b><br/>{escape(nome_projeto) if nome_projeto else 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Cliente:</b><br/>{escape(cliente) if cliente else 'Não informado'}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra:</b><br/>{escape(local_obra) if local_obra else 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Responsável:</b><br/>{escape(responsavel) if responsavel else 'Não informado'}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Data:</b><br/>{data_orcamento.strftime('%d/%m/%Y')}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Validade:</b><br/>{validade} dias",
                estilo_normal,
            ),
        ],
    ]

    tabela_dados = Table(
        dados_orcamento,
        colWidths=[
            88 * mm,
            88 * mm,
        ],
    )

    tabela_dados.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cccccc"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dddddd"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    elementos.append(tabela_dados)

    # ========================================================
    # RESUMO
    # ========================================================

    elementos.append(
        Paragraph(
            "2. RESUMO DO PROJETO",
            estilo_secao,
        )
    )

    resumo = [
        [
            Paragraph("<b>Área</b>", estilo_normal),
            Paragraph(
                f"{float(area):.2f} m²",
                estilo_direita,
            ),
        ],
        [
            Paragraph("<b>Comprimento</b>", estilo_normal),
            Paragraph(
                f"{float(comprimento):.2f} m",
                estilo_direita,
            ),
        ],
        [
            Paragraph("<b>Altura</b>", estilo_normal),
            Paragraph(
                f"{float(altura):.2f} m",
                estilo_direita,
            ),
        ],
    ]

    tabela_resumo = Table(
        resumo,
        colWidths=[
            88 * mm,
            88 * mm,
        ],
    )

    tabela_resumo.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cccccc"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dddddd"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f5f5f5"),
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elementos.append(tabela_resumo)

    # ========================================================
    # MATERIAIS
    # ========================================================

    elementos.append(
        Paragraph(
            "3. QUANTITATIVO DE MATERIAIS",
            estilo_secao,
        )
    )

    tabela_materiais = [
        [
            Paragraph("<b>Material</b>", estilo_pequeno),
            Paragraph("<b>Un.</b>", estilo_pequeno),
            Paragraph("<b>Quantidade</b>", estilo_pequeno),
            Paragraph("<b>Preço unitário</b>", estilo_pequeno),
            Paragraph("<b>Total</b>", estilo_pequeno),
        ]
    ]

    for nome, material in materiais.items():

        tabela_materiais.append(
            [
                Paragraph(
                    escape(str(nome)),
                    estilo_pequeno,
                ),
                Paragraph(
                    str(
                        material.get(
                            "unidade",
                            "",
                        )
                    ),
                    estilo_centralizado,
                ),
                Paragraph(
                    f'{float(material.get("quantidade", 0)):.2f}',
                    estilo_direita,
                ),
                Paragraph(
                    formatar_moeda(
                        material.get(
                            "preco_unitario",
                            0,
                        )
                    ),
                    estilo_direita,
                ),
                Paragraph(
                    formatar_moeda(
                        material.get(
                            "custo",
                            0,
                        )
                    ),
                    estilo_direita,
                ),
            ]
        )

    tabela_material_pdf = Table(
        tabela_materiais,
        colWidths=[
            61 * mm,
            16 * mm,
            28 * mm,
            35 * mm,
            36 * mm,
        ],
        repeatRows=1,
        splitByRow=1,
        hAlign="CENTER",
    )

    tabela_material_pdf.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#eeeeee"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#bbbbbb"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dddddd"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER",
                ),
                (
                    "ALIGN",
                    (2, 1),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elementos.append(tabela_material_pdf)

    # ========================================================
    # FINANCEIRO
    # ========================================================

    elementos.append(
        Paragraph(
            "4. RESUMO FINANCEIRO",
            estilo_secao,
        )
    )

    financeiro = [
        [
            Paragraph("Materiais", estilo_normal),
            Paragraph(
                formatar_moeda(subtotal_materiais),
                estilo_direita,
            ),
        ],
        [
            Paragraph("Massas e telas", estilo_normal),
            Paragraph(
                formatar_moeda(massas_telas),
                estilo_direita,
            ),
        ],
        [
            Paragraph("Mão de obra", estilo_normal),
            Paragraph(
                formatar_moeda(custo_mao_de_obra),
                estilo_direita,
            ),
        ],
    ]

    tabela_financeiro = Table(
        financeiro,
        colWidths=[
            110 * mm,
            66 * mm,
        ],
    )

    tabela_financeiro.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cccccc"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dddddd"),
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    elementos.append(tabela_financeiro)

    # ========================================================
    # TOTAL
    # ========================================================

    total_tabela = Table(
        [
            [
                Paragraph(
                    "<b>VALOR TOTAL DO ORÇAMENTO</b>",
                    estilo_normal,
                ),
                Paragraph(
                    f"<b>{formatar_moeda(custo_geral)}</b>",
                    estilo_total,
                ),
            ]
        ],
        colWidths=[
            90 * mm,
            86 * mm,
        ],
    )

    total_tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1.2,
                    colors.HexColor("#1f7a1f"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#f3fff3"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
            ]
        )
    )

    elementos.append(total_tabela)

    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    elementos.append(
        Paragraph(
            "5. MÃO DE OBRA",
            estilo_secao,
        )
    )

    mao_obra_tabela = Table(
        [
            [
                Paragraph(
                    "<b>Dias estimados</b>",
                    estilo_normal,
                ),
                Paragraph(
                    f"{float(dias):.1f}",
                    estilo_direita,
                ),
            ],
            [
                Paragraph(
                    "<b>Valor da diária</b>",
                    estilo_normal,
                ),
                Paragraph(
                    formatar_moeda(diaria),
                    estilo_direita,
                ),
            ],
            [
                Paragraph(
                    "<b>Custo da mão de obra</b>",
                    estilo_normal,
                ),
                Paragraph(
                    formatar_moeda(
                        custo_mao_de_obra
                    ),
                    estilo_direita,
                ),
            ],
        ],
        colWidths=[
            110 * mm,
            66 * mm,
        ],
    )

    mao_obra_tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cccccc"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dddddd"),
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elementos.append(
        mao_obra_tabela
    )

    # ========================================================
    # CONDIÇÕES
    # ========================================================

    elementos.append(
        Paragraph(
            "6. CONDIÇÕES COMERCIAIS",
            estilo_secao,
        )
    )

    condicoes = [
        [
            Paragraph("<b>Validade</b>", estilo_normal),
            Paragraph(
                f"{validade} dias",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                "<b>Prazo de execução</b>",
                estilo_normal,
            ),
            Paragraph(
                escape(prazo_execucao)
                if prazo_execucao
                else "Não informado",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                "<b>Condição de pagamento</b>",
                estilo_normal,
            ),
            Paragraph(
                escape(condicao_pagamento)
                if condicao_pagamento
                else "Não informado",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                "<b>Forma de pagamento</b>",
                estilo_normal,
            ),
            Paragraph(
                escape(forma_pagamento)
                if forma_pagamento
                else "Não informado",
                estilo_normal,
            ),
        ],
    ]

    tabela_condicoes = Table(
        condicoes,
        colWidths=[
            55 * mm,
            121 * mm,
        ],
    )

    tabela_condicoes.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cccccc"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dddddd"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f5f5f5"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    elementos.append(
        tabela_condicoes
    )

    # ========================================================
    # OBSERVAÇÕES
    # ========================================================

    if observacoes_comerciais:

        elementos.append(
            Paragraph(
                "7. OBSERVAÇÕES COMERCIAIS",
                estilo_secao,
            )
        )

        elementos.append(
            Paragraph(
                escape(
                    observacoes_comerciais
                ).replace(
                    "\n",
                    "<br/>",
                ),
                estilo_normal,
            )
        )

    if observacoes_tecnicas:

        elementos.append(
            Paragraph(
                "8. OBSERVAÇÕES TÉCNICAS",
                estilo_secao,
            )
        )

        elementos.append(
            Paragraph(
                escape(
                    observacoes_tecnicas
                ).replace(
                    "\n",
                    "<br/>",
                ),
                estilo_normal,
            )
        )

    # ========================================================
    # ASSINATURA — CORRIGIDA
    # ========================================================

    elementos.append(
        Spacer(1, 28)
    )

    assinatura = Table(
        [
            [
                Paragraph(
                    " ",
                    estilo_normal,
                )
            ]
        ],
        colWidths=[
            100 * mm,
        ],
        rowHeights=[
            12 * mm,
        ],
    )

    assinatura.setStyle(
        TableStyle(
            [
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.HexColor("#333333"),
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "BOTTOM",
                ),
            ]
        )
    )

    elementos.append(
        assinatura
    )

    nome_assinatura = (
        responsavel.strip()
        if responsavel
        and responsavel.strip()
        else "Responsável pelo orçamento"
    )

    elementos.append(
        Paragraph(
            f"<b>{escape(nome_assinatura)}</b>",
            estilo_assinatura_nome,
        )
    )

    elementos.append(
        Paragraph(
            "Responsável pelo orçamento",
            estilo_assinatura_cargo,
        )
    )

    # ========================================================
    # RODAPÉ
    # ========================================================

    def adicionar_rodape(
        canvas,
        documento,
    ):

        canvas.saveState()

        largura, altura = A4

        canvas.setFont(
            "Helvetica",
            7,
        )

        canvas.setFillColor(
            colors.grey
        )

        canvas.drawCentredString(
            largura / 2,
            8 * mm,
            (
                "Orçamento Steel Framing • "
                f"Página {documento.page}"
            ),
        )

        canvas.restoreState()

    # ========================================================
    # BUILD
    # ========================================================

    doc.build(
        elementos,
        onFirstPage=adicionar_rodape,
        onLaterPages=adicionar_rodape,
    )

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# HERO PRINCIPAL
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            📐 CALCULADORA STEEL FRAMING
        </div>

        <div class="hero-subtitle">
            Sistema profissional para orçamento de materiais,
            quantitativos e mão de obra.
        </div>

        <div class="hero-badge">
            ORÇAMENTO PROFISSIONAL • FASE 6C
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# IDENTIFICAÇÃO
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            📋 Identificação do projeto
        </div>

        <div class="section-subtitle">
            Informe os dados principais do orçamento.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:

    nome_projeto = st.text_input(
        "Nome do projeto",
        placeholder="Ex.: Residência Atibaia",
        value=st.session_state.get(
            "nome_projeto",
            "",
        ),
    )

    cliente = st.text_input(
        "Cliente",
        placeholder="Nome do cliente",
        value=st.session_state.get(
            "cliente",
            "",
        ),
    )

with col2:

    local_obra = st.text_input(
        "Local da obra",
        placeholder="Ex.: Atibaia - SP",
        value=st.session_state.get(
            "local_obra",
            "",
        ),
    )

    responsavel = st.text_input(
        "Responsável pelo orçamento",
        placeholder="Nome do profissional",
        value=st.session_state.get(
            "responsavel",
            "",
        ),
    )

data_orcamento = st.date_input(
    "Data do orçamento",
    value=st.session_state.get(
        "data_orcamento",
        date.today(),
    ),
)


# ============================================================
# CONDIÇÕES COMERCIAIS
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            💼 Condições comerciais
        </div>

        <div class="section-subtitle">
            Defina validade, prazo e condições de pagamento.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:

    validade_orcamento = st.number_input(
        "Validade do orçamento (dias)",
        min_value=1,
        value=st.session_state.get(
            "validade_orcamento",
            10,
        ),
        step=1,
    )

    prazo_execucao = st.text_input(
        "Prazo estimado de execução",
        placeholder="Ex.: 30 dias úteis",
        value=st.session_state.get(
            "prazo_execucao",
            "",
        ),
    )

with col2:

    condicao_pagamento = st.text_input(
        "Condição de pagamento",
        placeholder="Ex.: 50% entrada + 50% na entrega",
        value=st.session_state.get(
            "condicao_pagamento",
            "",
        ),
    )

    forma_pagamento = st.text_input(
        "Forma de pagamento",
        placeholder="Ex.: Pix, transferência ou boleto",
        value=st.session_state.get(
            "forma_pagamento",
            "",
        ),
    )

observacoes_comerciais = st.text_area(
    "Inclusões / observações comerciais",
    placeholder=(
        "Descreva inclusões, exclusões, transporte, "
        "prazo, condições de fornecimento etc."
    ),
    value=st.session_state.get(
        "observacoes_comerciais",
        "",
    ),
)


# ============================================================
# DIMENSÕES
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            📐 Dimensões do projeto
        </div>

        <div class="section-subtitle">
            Informe as dimensões utilizadas no orçamento.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)

with col1:

    comprimento = st.number_input(
        "Comprimento (m)",
        min_value=0.01,
        value=float(
            st.session_state.get(
                "comprimento",
                30.00,
            )
        ),
        step=0.10,
    )

with col2:

    altura = st.number_input(
        "Altura (m)",
        min_value=0.01,
        value=float(
            st.session_state.get(
                "altura",
                3.00,
            )
        ),
        step=0.10,
    )

with col3:

    area_preview = (
        comprimento * altura
    )

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ÁREA DO PROJETO
            </div>

            <div class="metric-value">
                {area_preview:.2f} m²
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

st.session_state["comprimento"] = comprimento
st.session_state["altura"] = altura


# ============================================================
# PREÇOS
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            💰 Preços dos materiais
        </div>

        <div class="section-subtitle">
            Altere os preços conforme fornecedor, região
            ou condição de compra.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

if "precos" not in st.session_state:

    st.session_state["precos"] = (
        PRECOS_BASE.copy()
    )

precos_atualizados = {}

colunas_precos = st.columns(3)

for indice, (
    nome,
    preco_padrao,
) in enumerate(
    st.session_state["precos"].items()
):

    with colunas_precos[
        indice % 3
    ]:

        preco_atual = st.number_input(
            nome,
            min_value=0.00,
            value=float(preco_padrao),
            step=0.01,
            format="%.2f",
            key=f"preco_{nome}",
        )

        precos_atualizados[
            nome
        ] = preco_atual

st.session_state["precos"] = (
    precos_atualizados
)


# ============================================================
# PRÉ-CÁLCULO
# ============================================================

previa = calcular_projeto(
    comprimento=comprimento,
    altura=altura,
    precos=st.session_state["precos"],
)


# ============================================================
# QUANTIDADES
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            📦 Quantidades dos materiais
        </div>

        <div class="section-subtitle">
            As quantidades são calculadas automaticamente,
            mas podem ser ajustadas.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

if "quantidades" not in st.session_state:

    st.session_state["quantidades"] = {}

quantidades_atualizadas = {}

colunas_quantidades = st.columns(3)

for indice, (
    nome,
    material,
) in enumerate(
    previa["materiais"].items()
):

    quantidade_automatica = material[
        "quantidade"
    ]

    if (
        nome
        not in st.session_state["quantidades"]
    ):

        st.session_state[
            "quantidades"
        ][nome] = quantidade_automatica

    with colunas_quantidades[
        indice % 3
    ]:

        quantidade_atual = st.number_input(
            nome,
            min_value=0.0,
            value=float(
                st.session_state[
                    "quantidades"
                ][nome]
            ),
            step=1.0,
            format="%.2f",
            key=f"quantidade_{nome}",
        )

        quantidades_atualizadas[
            nome
        ] = quantidade_atual

st.session_state["quantidades"] = (
    quantidades_atualizadas
)


# ============================================================
# OBSERVAÇÕES TÉCNICAS
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            📝 Observações técnicas
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

observacoes_tecnicas = st.text_area(
    "Observações técnicas",
    placeholder=(
        "Ex.: medidas finais deverão ser conferidas "
        "antes da fabricação."
    ),
    value=st.session_state.get(
        "observacoes_tecnicas",
        "",
    ),
)


# ============================================================
# CALCULAR
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)

if st.button(
    "🧮 CALCULAR / ATUALIZAR ORÇAMENTO",
    type="primary",
    use_container_width=True,
):

    resultado = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        precos=st.session_state[
            "precos"
        ],
        quantidades=st.session_state[
            "quantidades"
        ],
    )

    st.session_state["projeto"] = (
        resultado
    )

    st.session_state[
        "nome_projeto"
    ] = nome_projeto

    st.session_state[
        "cliente"
    ] = cliente

    st.session_state[
        "local_obra"
    ] = local_obra

    st.session_state[
        "responsavel"
    ] = responsavel

    st.session_state[
        "data_orcamento"
    ] = data_orcamento

    st.session_state[
        "validade_orcamento"
    ] = validade_orcamento

    st.session_state[
        "prazo_execucao"
    ] = prazo_execucao

    st.session_state[
        "condicao_pagamento"
    ] = condicao_pagamento

    st.session_state[
        "forma_pagamento"
    ] = forma_pagamento

    st.session_state[
        "observacoes_comerciais"
    ] = observacoes_comerciais

    st.session_state[
        "observacoes_tecnicas"
    ] = observacoes_tecnicas

    st.success(
        "Orçamento atualizado com sucesso."
    )


# ============================================================
# DOCUMENTO DO ORÇAMENTO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state[
        "projeto"
    ]

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                📄 ORÇAMENTO PROFISSIONAL
            </div>

            <div class="hero-subtitle">
                Quantitativo de materiais e mão de obra
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # DADOS
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                📋 Dados do orçamento
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    nome_exibicao = (
        st.session_state.get(
            "nome_projeto",
            "",
        )
        or "Não informado"
    )

    cliente_exibicao = (
        st.session_state.get(
            "cliente",
            "",
        )
        or "Não informado"
    )

    local_exibicao = (
        st.session_state.get(
            "local_obra",
            "",
        )
        or "Não informado"
    )

    responsavel_exibicao = (
        st.session_state.get(
            "responsavel",
            "",
        )
        or "Não informado"
    )

    data_salva = st.session_state.get(
        "data_orcamento",
        date.today(),
    )

    validade_salva = st.session_state.get(
        "validade_orcamento",
        10,
    )

    with col1:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Projeto
                </div>

                <div class="card-value">
                    {escape(nome_exibicao)}
                </div>

                <br>

                <div class="card-label">
                    Cliente
                </div>

                <div class="card-value">
                    {escape(cliente_exibicao)}
                </div>

                <br>

                <div class="card-label">
                    Local da obra
                </div>

                <div class="card-value">
                    {escape(local_exibicao)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Responsável
                </div>

                <div class="card-value">
                    {escape(responsavel_exibicao)}
                </div>

                <br>

                <div class="card-label">
                    Data
                </div>

                <div class="card-value">
                    {data_salva.strftime("%d/%m/%Y")}
                </div>

                <br>

                <div class="card-label">
                    Validade
                </div>

                <div class="card-value">
                    {validade_salva} dias
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # RESUMO DO PROJETO
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                📐 Resumo do projeto
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    ÁREA
                </div>

                <div class="metric-value">
                    {projeto["area"]:.2f} m²
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    COMPRIMENTO
                </div>

                <div class="metric-value">
                    {comprimento:.2f} m
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    ALTURA
                </div>

                <div class="metric-value">
                    {altura:.2f} m
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # MATERIAIS
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                📦 Quantitativo de materiais
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    tabela_materiais = []

    for nome, material in (
        projeto["materiais"].items()
    ):

        tabela_materiais.append(
            {
                "Material": nome,
                "Unidade": material[
                    "unidade"
                ],
                "Quantidade": material[
                    "quantidade"
                ],
                "Preço unitário": (
                    material[
                        "preco_unitario"
                    ]
                ),
                "Total": material[
                    "custo"
                ],
            }
        )

    df_materiais = pd.DataFrame(
        tabela_materiais
    )

    st.dataframe(
        df_materiais,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Material": st.column_config.TextColumn(
                "Material",
            ),
            "Unidade": st.column_config.TextColumn(
                "Unidade",
            ),
            "Quantidade": st.column_config.NumberColumn(
                "Quantidade",
                format="%.2f",
            ),
            "Preço unitário": st.column_config.NumberColumn(
                "Preço unitário",
                format="R$ %.2f",
            ),
            "Total": st.column_config.NumberColumn(
                "Total",
                format="R$ %.2f",
            ),
        },
    )


    # ========================================================
    # FINANCEIRO
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                💰 Resumo financeiro
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    subtotal_materiais = obter_valor(
        projeto,
        "subtotal_materiais",
    )

    massas_telas = obter_valor(
        projeto,
        "massas_telas",
    )

    mao_de_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    custo_mao_de_obra = obter_valor(
        mao_de_obra,
        "custo",
    )

    custo_geral = obter_valor(
        projeto,
        "custo_geral",
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="financial-card">

                <div class="financial-label">
                    MATERIAIS
                </div>

                <div class="financial-value">
                    {formatar_moeda(subtotal_materiais)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="financial-card">

                <div class="financial-label">
                    MASSAS E TELAS
                </div>

                <div class="financial-value">
                    {formatar_moeda(massas_telas)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="financial-card">

                <div class="financial-label">
                    MÃO DE OBRA
                </div>

                <div class="financial-value">
                    {formatar_moeda(custo_mao_de_obra)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown(
        f"""
        <div class="total-box">

            <div class="total-label">
                VALOR TOTAL DO ORÇAMENTO
            </div>

            <div class="total-value">
                {formatar_moeda(custo_geral)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                👷 Mão de obra
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    dias = obter_valor(
        mao_de_obra,
        "dias",
    )

    diaria = obter_valor(
        mao_de_obra,
        "diaria",
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    DIAS ESTIMADOS
                </div>

                <div class="metric-value">
                    {dias:.1f}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    VALOR DA DIÁRIA
                </div>

                <div class="metric-value">
                    {formatar_moeda(diaria)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    CUSTO DA MÃO DE OBRA
                </div>

                <div class="metric-value">
                    {formatar_moeda(custo_mao_de_obra)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # CONDIÇÕES
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                💼 Condições comerciais
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    prazo_salvo = st.session_state.get(
        "prazo_execucao",
        "",
    )

    pagamento_salvo = st.session_state.get(
        "condicao_pagamento",
        "",
    )

    forma_pagamento_salva = st.session_state.get(
        "forma_pagamento",
        "",
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Validade
                </div>

                <div class="card-value">
                    {validade_salva} dias
                </div>

                <br>

                <div class="card-label">
                    Prazo estimado de execução
                </div>

                <div class="card-value">
                    {escape(prazo_salvo) if prazo_salvo else "Não informado"}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Condição de pagamento
                </div>

                <div class="card-value">
                    {escape(pagamento_salvo) if pagamento_salvo else "Não informado"}
                </div>

                <br>

                <div class="card-label">
                    Forma de pagamento
                </div>

                <div class="card-value">
                    {escape(forma_pagamento_salva) if forma_pagamento_salva else "Não informado"}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # OBSERVAÇÕES
    # ========================================================

    observacoes_comerciais_salvas = (
        st.session_state.get(
            "observacoes_comerciais",
            "",
        )
    )

    if observacoes_comerciais_salvas:

        st.markdown(
            """
            <div class="section-header">

                <div class="section-title">
                    📝 Observações comerciais
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="note-box">
                {escape(observacoes_comerciais_salvas).replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )


    observacoes_tecnicas_salvas = (
        st.session_state.get(
            "observacoes_tecnicas",
            "",
        )
    )

    if observacoes_tecnicas_salvas:

        st.markdown(
            """
            <div class="section-header">

                <div class="section-title">
                    📝 Observações técnicas
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="note-box">
                {escape(observacoes_tecnicas_salvas).replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # ASSINATURA — UMA ÚNICA VEZ
    # ========================================================

    nome_assinatura = (
        st.session_state.get(
            "responsavel",
            "",
        )
        or "Responsável pelo orçamento"
    )

    st.markdown(
        f"""
        <div class="assinatura">

            <div class="linha-assinatura"></div>

            <div class="assinatura-nome">
                {escape(nome_assinatura)}
            </div>

            <div class="assinatura-cargo">
                Responsável pelo orçamento
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # EXPORTAÇÃO
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                📤 Exportação do orçamento
            </div>

            <div class="section-subtitle">
                Gere os documentos profissionais do orçamento.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    with col1:

        st.markdown(
            """
            <div class="export-card">

                <div class="export-title">
                    📄 Documento PDF
                </div>

                <div class="export-description">
                    Gera o orçamento em formato PDF,
                    mantendo a apresentação profissional
                    e a assinatura.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📄 GERAR PDF",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                "Gerando orçamento em PDF..."
            ):

                pdf_bytes = gerar_pdf(
                    projeto
                )

            if pdf_bytes:

                st.download_button(
                    label="⬇️ BAIXAR PDF",
                    data=pdf_bytes,
                    file_name=(
                        f"{nome_arquivo_orcamento()}.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

                st.success(
                    "PDF gerado com sucesso."
                )


    # --------------------------------------------------------
    # EXCEL
    # --------------------------------------------------------

    with col2:

        st.markdown(
            """
            <div class="export-card">

                <div class="export-title">
                    📊 Planilha Excel
                </div>

                <div class="export-description">
                    Exporta materiais, mão de obra,
                    dados do projeto e resumo financeiro
                    para uma planilha editável.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "📊 EXPORTAR EXCEL",
            type="primary",
            use_container_width=True,
        ):

            with st.spinner(
                "Gerando orçamento em Excel..."
            ):

                excel_bytes = gerar_excel(
                    projeto
                )

            if excel_bytes:

                st.download_button(
                    label="⬇️ BAIXAR EXCEL",
                    data=excel_bytes,
                    file_name=(
                        f"{nome_arquivo_orcamento()}.xlsx"
                    ),
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    use_container_width=True,
                )

                st.success(
                    "Excel gerado com sucesso."
                )


    st.caption(
        "PDF e Excel disponíveis para exportação. "
        "O Excel mantém os valores validados pelo orçamento "
        "e permite edição dos quantitativos e preços."
    )
