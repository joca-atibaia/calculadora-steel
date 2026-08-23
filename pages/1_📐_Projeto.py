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

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        padding: 34px 38px;
        border-radius: 18px;
        border: 1px solid #dfe3e8;
        background:
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #ffffff 55%,
                #f1f5f9 100%
            );
        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.06);
        margin-bottom: 28px;
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #172033;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #64748b;
        line-height: 1.5;
        margin-bottom: 18px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        color: #3730a3;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }

    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-title {
        font-size: 21px;
        font-weight: 800;
        color: #172033;
        margin-top: 12px;
        margin-bottom: 3px;
    }

    .section-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 17px;
    }

    .section-divider {
        height: 1px;
        background: #e5e7eb;
        margin: 28px 0;
    }

    /* ======================================================
       CARDS
       ====================================================== */

    .info-card {
        padding: 20px 22px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.04);
        min-height: 150px;
        margin-bottom: 10px;
    }

    .card-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: #64748b;
        margin-bottom: 4px;
    }

    .card-value {
        font-size: 16px;
        font-weight: 650;
        color: #172033;
    }

    .card-spacing {
        margin-bottom: 16px;
    }

    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        padding: 22px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.04);
        text-align: center;
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 11px;
        font-weight: 800;
        color: #64748b;
        letter-spacing: 0.8px;
        margin-bottom: 7px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 800;
        color: #172033;
    }

    /* ======================================================
       FINANCEIRO
       ====================================================== */

    .finance-card {
        padding: 20px 22px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        box-shadow:
            0 4px 14px rgba(15, 23, 42, 0.04);
        margin-bottom: 12px;
    }

    .finance-label {
        font-size: 13px;
        font-weight: 650;
        color: #475569;
    }

    .finance-value {
        font-size: 21px;
        font-weight: 800;
        color: #172033;
        margin-top: 4px;
    }

    .total-box {
        padding: 28px 30px;
        border-radius: 16px;
        border: 2px solid #16a34a;
        background:
            linear-gradient(
                135deg,
                #f0fdf4,
                #ffffff
            );
        text-align: center;
        margin: 18px 0 25px 0;
        box-shadow:
            0 7px 20px rgba(22, 163, 74, 0.08);
    }

    .total-label {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #166534;
        margin-bottom: 6px;
    }

    .total-value {
        font-size: 38px;
        font-weight: 900;
        color: #14532d;
    }

    /* ======================================================
       OBSERVAÇÕES
       ====================================================== */

    .observation-card {
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
        color: #334155;
        line-height: 1.6;
        margin-bottom: 12px;
    }

    /* ======================================================
       ASSINATURA
       ====================================================== */

    .assinatura {
        margin-top: 50px;
        padding: 25px 20px 10px 20px;
        text-align: center;
    }

    .linha-assinatura {
        border-top: 1px solid #334155;
        width: 55%;
        max-width: 430px;
        min-width: 250px;
        margin: 0 auto 10px auto;
    }

    .assinatura-nome {
        font-size: 14px;
        font-weight: 800;
        color: #172033;
    }

    .assinatura-cargo {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }

    /* ======================================================
       TABELAS
       ====================================================== */

    .table-title {
        font-size: 15px;
        font-weight: 750;
        color: #334155;
        margin-bottom: 10px;
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
            font-size: 27px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        .metric-value {
            font-size: 23px;
        }

        .total-value {
            font-size: 30px;
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
    return (
        f"R$ {float(valor):,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def obter_valor(dicionario, chave, padrao=0):
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
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
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
        0,
    )

    area = obter_valor(
        projeto,
        "area",
    )

    materiais = projeto.get(
        "materiais",
        {},
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

    custo_geral = obter_valor(
        projeto,
        "custo_geral",
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

    azul = "172033"
    cinza = "64748B"
    cinza_claro = "F1F5F9"
    verde = "16A34A"
    verde_claro = "F0FDF4"
    branco = "FFFFFF"
    borda_cor = "CBD5E1"

    thin = Side(
        style="thin",
        color=borda_cor,
    )

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin,
    )

    titulo_fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    secao_fill = PatternFill(
        "solid",
        fgColor=cinza_claro,
    )

    total_fill = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

    moeda_format = (
        '"R$" #,##0.00'
    )

    # --------------------------------------------------------
    # FUNÇÕES INTERNAS DO EXCEL
    # --------------------------------------------------------

    def configurar_larguras(ws):

        larguras = {
            "A": 30,
            "B": 24,
            "C": 22,
            "D": 22,
            "E": 22,
        }

        for coluna, largura in larguras.items():

            ws.column_dimensions[
                coluna
            ].width = largura

    def estilizar_titulo(
        ws,
        celula,
        texto,
    ):

        ws[celula] = texto
        ws[celula].font = Font(
            bold=True,
            size=18,
            color=branco,
        )
        ws[celula].fill = titulo_fill
        ws[celula].alignment = Alignment(
            horizontal="left",
            vertical="center",
        )

    def estilizar_secao(
        ws,
        linha,
        texto,
    ):

        ws.merge_cells(
            start_row=linha,
            start_column=1,
            end_row=linha,
            end_column=5,
        )

        cell = ws.cell(
            linha,
            1,
        )

        cell.value = texto
        cell.font = Font(
            bold=True,
            size=12,
            color=azul,
        )
        cell.fill = secao_fill
        cell.alignment = Alignment(
            horizontal="left"
        )

    def aplicar_bordas(
        ws,
        min_row,
        max_row,
        min_col=1,
        max_col=5,
    ):

        for row in ws.iter_rows(
            min_row=min_row,
            max_row=max_row,
            min_col=min_col,
            max_col=max_col,
        ):

            for cell in row:

                cell.border = border
                cell.alignment = Alignment(
                    vertical="center"
                )

    # --------------------------------------------------------
    # ABA ORÇAMENTO
    # --------------------------------------------------------

    configurar_larguras(
        ws_orcamento
    )

    ws_orcamento.merge_cells(
        "A1:E1"
    )

    estilizar_titulo(
        ws_orcamento,
        "A1",
        "ORÇAMENTO — STEEL FRAMING",
    )

    ws_orcamento.merge_cells(
        "A2:E2"
    )

    ws_orcamento["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws_orcamento["A2"].font = Font(
        italic=True,
        color=cinza,
    )

    # --------------------------------------------------------
    # IDENTIFICAÇÃO
    # --------------------------------------------------------

    estilizar_secao(
        ws_orcamento,
        4,
        "IDENTIFICAÇÃO DO PROJETO",
    )

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

    for rotulo, valor in dados_identificacao:

        ws_orcamento.cell(
            linha,
            1,
        ).value = rotulo

        ws_orcamento.cell(
            linha,
            2,
        ).value = valor

        linha += 1

    aplicar_bordas(
        ws_orcamento,
        5,
        9,
        1,
        2,
    )

    # --------------------------------------------------------
    # DIMENSÕES
    # --------------------------------------------------------

    estilizar_secao(
        ws_orcamento,
        11,
        "DIMENSÕES DO PROJETO",
    )

    dimensoes = [
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
    ]

    linha = 12

    for rotulo, valor in dimensoes:

        ws_orcamento.cell(
            linha,
            1,
        ).value = rotulo

        ws_orcamento.cell(
            linha,
            2,
        ).value = float(valor)

        linha += 1

    aplicar_bordas(
        ws_orcamento,
        12,
        14,
        1,
        2,
    )

    # --------------------------------------------------------
    # RESUMO FINANCEIRO
    # --------------------------------------------------------

    estilizar_secao(
        ws_orcamento,
        16,
        "RESUMO FINANCEIRO",
    )

    ws_orcamento["A17"] = "Materiais"
    ws_orcamento["B17"] = float(
        subtotal_materiais
    )

    ws_orcamento["A18"] = "Massas e telas"
    ws_orcamento["B18"] = float(
        massas_telas
    )

    ws_orcamento["A19"] = "Mão de obra"
    ws_orcamento["B19"] = float(
        custo_mao_de_obra
    )

    for row in range(17, 20):

        ws_orcamento.cell(
            row,
            2,
        ).number_format = moeda_format

    aplicar_bordas(
        ws_orcamento,
        17,
        19,
        1,
        2,
    )

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    ws_orcamento.merge_cells(
        "A21:D21"
    )

    ws_orcamento["A21"] = (
        "VALOR TOTAL DO ORÇAMENTO"
    )

    ws_orcamento["A21"].font = Font(
        bold=True,
        size=14,
        color="14532D",
    )

    ws_orcamento["A21"].fill = total_fill

    ws_orcamento["E21"] = (
        "=B17+B18+B19"
    )

    ws_orcamento["E21"].number_format = (
        moeda_format
    )

    ws_orcamento["E21"].font = Font(
        bold=True,
        size=16,
        color="14532D",
    )

    ws_orcamento["E21"].fill = total_fill

    aplicar_bordas(
        ws_orcamento,
        21,
        21,
        1,
        5,
    )

    # --------------------------------------------------------
    # CONDIÇÕES COMERCIAIS
    # --------------------------------------------------------

    estilizar_secao(
        ws_orcamento,
        23,
        "CONDIÇÕES COMERCIAIS",
    )

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

    linha = 24

    for rotulo, valor in condicoes:

        ws_orcamento.cell(
            linha,
            1,
        ).value = rotulo

        ws_orcamento.cell(
            linha,
            2,
        ).value = valor

        linha += 1

    aplicar_bordas(
        ws_orcamento,
        24,
        27,
        1,
        2,
    )

    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

    estilizar_secao(
        ws_orcamento,
        29,
        "OBSERVAÇÕES COMERCIAIS",
    )

    ws_orcamento.merge_cells(
        "A30:E31"
    )

    ws_orcamento["A30"] = (
        observacoes_comerciais
        or "Não informado"
    )

    ws_orcamento["A30"].alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )

    aplicar_bordas(
        ws_orcamento,
        30,
        31,
        1,
        5,
    )

    estilizar_secao(
        ws_orcamento,
        33,
        "OBSERVAÇÕES TÉCNICAS",
    )

    ws_orcamento.merge_cells(
        "A34:E35"
    )

    ws_orcamento["A34"] = (
        observacoes_tecnicas
        or "Não informado"
    )

    ws_orcamento["A34"].alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )

    aplicar_bordas(
        ws_orcamento,
        34,
        35,
        1,
        5,
    )

    # --------------------------------------------------------
    # ABA MATERIAIS
    # --------------------------------------------------------

    configurar_larguras(
        ws_materiais
    )

    ws_materiais.merge_cells(
        "A1:E1"
    )

    estilizar_titulo(
        ws_materiais,
        "A1",
        "QUANTITATIVO DE MATERIAIS",
    )

    cabecalho = [
        "Material",
        "Unidade",
        "Quantidade",
        "Preço unitário",
        "Total",
    ]

    for coluna, valor in enumerate(
        cabecalho,
        start=1,
    ):

        cell = ws_materiais.cell(
            3,
            coluna,
        )

        cell.value = valor
        cell.font = Font(
            bold=True,
            color=branco,
        )
        cell.fill = titulo_fill
        cell.alignment = Alignment(
            horizontal="center"
        )

    linha = 4

    for nome, material in materiais.items():

        ws_materiais.cell(
            linha,
            1,
        ).value = str(nome)

        ws_materiais.cell(
            linha,
            2,
        ).value = material.get(
            "unidade",
            "",
        )

        ws_materiais.cell(
            linha,
            3,
        ).value = float(
            material.get(
                "quantidade",
                0,
            )
        )

        ws_materiais.cell(
            linha,
            4,
        ).value = float(
            material.get(
                "preco_unitario",
                0,
            )
        )

        # Fórmula simples e compatível
        ws_materiais.cell(
            linha,
            5,
        ).value = (
            f"=C{linha}*D{linha}"
        )

        ws_materiais.cell(
            linha,
            4,
        ).number_format = moeda_format

        ws_materiais.cell(
            linha,
            5,
        ).number_format = moeda_format

        linha += 1

    ultima_linha_materiais = (
        linha - 1
    )

    aplicar_bordas(
        ws_materiais,
        3,
        ultima_linha_materiais,
        1,
        5,
    )

    # Total de materiais
    ws_materiais.cell(
        linha + 1,
        4,
    ).value = "TOTAL"

    ws_materiais.cell(
        linha + 1,
        4,
    ).font = Font(
        bold=True
    )

    ws_materiais.cell(
        linha + 1,
        5,
    ).value = (
        f"=SUM(E4:E{ultima_linha_materiais})"
    )

    ws_materiais.cell(
        linha + 1,
        5,
    ).number_format = moeda_format

    ws_materiais.cell(
        linha + 1,
        5,
    ).font = Font(
        bold=True
    )

    aplicar_bordas(
        ws_materiais,
        linha + 1,
        linha + 1,
        4,
        5,
    )

    ws_materiais.freeze_panes = "A4"

    # --------------------------------------------------------
    # ABA MÃO DE OBRA
    # --------------------------------------------------------

    configurar_larguras(
        ws_mao
    )

    ws_mao.merge_cells(
        "A1:C1"
    )

    estilizar_titulo(
        ws_mao,
        "A1",
        "MÃO DE OBRA",
    )

    ws_mao["A3"] = "Descrição"
    ws_mao["B3"] = "Valor"
    ws_mao["C3"] = "Resultado"

    for cell in ws_mao[3]:

        cell.font = Font(
            bold=True,
            color=branco,
        )

        cell.fill = titulo_fill
        cell.alignment = Alignment(
            horizontal="center"
        )

    ws_mao["A4"] = "Dias estimados"
    ws_mao["B4"] = float(dias)
    ws_mao["C4"] = float(dias)

    ws_mao["A5"] = "Valor da diária"
    ws_mao["B5"] = float(diaria)
    ws_mao["C5"] = float(diaria)

    ws_mao["A6"] = "Custo da mão de obra"

    # Fórmula básica: dias x diária
    ws_mao["C6"] = "=C4*C5"

    ws_mao["B5"].number_format = moeda_format
    ws_mao["C5"].number_format = moeda_format
    ws_mao["C6"].number_format = moeda_format

    aplicar_bordas(
        ws_mao,
        3,
        6,
        1,
        3,
    )

    ws_mao["A6"].font = Font(
        bold=True
    )

    ws_mao["C6"].font = Font(
        bold=True
    )

    # --------------------------------------------------------
    # ABA DADOS
    # --------------------------------------------------------

    configurar_larguras(
        ws_dados
    )

    ws_dados.merge_cells(
        "A1:B1"
    )

    estilizar_titulo(
        ws_dados,
        "A1",
        "DADOS DO ORÇAMENTO",
    )

    dados = [
        ("Projeto", nome_projeto),
        ("Cliente", cliente),
        ("Local da obra", local_obra),
        ("Responsável", responsavel),
        (
            "Data",
            data_orcamento.strftime(
                "%d/%m/%Y"
            ),
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
        (
            "Comprimento (m)",
            float(comprimento),
        ),
        (
            "Altura (m)",
            float(altura),
        ),
        (
            "Área (m²)",
            float(area),
        ),
        (
            "Observações comerciais",
            observacoes_comerciais
            or "Não informado",
        ),
        (
            "Observações técnicas",
            observacoes_tecnicas
            or "Não informado",
        ),
    ]

    linha = 3

    for rotulo, valor in dados:

        ws_dados.cell(
            linha,
            1,
        ).value = rotulo

        ws_dados.cell(
            linha,
            2,
        ).value = valor

        linha += 1

    aplicar_bordas(
        ws_dados,
        3,
        linha - 1,
        1,
        2,
    )

    # --------------------------------------------------------
    # FORMATAÇÃO GERAL
    # --------------------------------------------------------

    for ws in wb.worksheets:

        ws.sheet_view.showGridLines = False

        ws.freeze_panes = (
            "A3"
            if ws.title != "ORÇAMENTO"
            else None
        )

        for row in ws.iter_rows():

            for cell in row:

                cell.alignment = Alignment(
                    vertical="center",
                    wrap_text=True,
                )

    # --------------------------------------------------------
    # SALVAR NA MEMÓRIA
    # --------------------------------------------------------

    buffer = BytesIO()

    wb.save(
        buffer
    )

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# GERAÇÃO DO PDF
# ============================================================

def gerar_pdf(projeto):

    try:

        from reportlab.lib import colors
        from reportlab.lib.enums import (
            TA_CENTER,
            TA_RIGHT,
        )
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
        author=responsavel
        or "Calculadora Steel Framing",
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
    # 1. DADOS
    # ========================================================

    elementos.append(
        Paragraph(
            "1. DADOS DO ORÇAMENTO",
            estilo_secao,
        )
    )

    data_formatada = data_orcamento.strftime(
        "%d/%m/%Y"
    )

    dados_orcamento = [
        [
            Paragraph(
                f"<b>Projeto:</b><br/>{escape(nome_projeto) or 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Cliente:</b><br/>{escape(cliente) or 'Não informado'}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra:</b><br/>{escape(local_obra) or 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Responsável:</b><br/>{escape(responsavel) or 'Não informado'}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Data:</b><br/>{data_formatada}",
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

    elementos.append(
        tabela_dados
    )

    elementos.append(
        Spacer(1, 8)
    )

    # ========================================================
    # 2. RESUMO DO PROJETO
    # ========================================================

    elementos.append(
        Paragraph(
            "2. RESUMO DO PROJETO",
            estilo_secao,
        )
    )

    resumo = [
        [
            Paragraph(
                "<b>Área</b>",
                estilo_normal,
            ),
            Paragraph(
                f"{float(area):.2f} m²",
                estilo_direita,
            ),
        ],
        [
            Paragraph(
                "<b>Comprimento</b>",
                estilo_normal,
            ),
            Paragraph(
                f"{float(comprimento):.2f} m",
                estilo_direita,
            ),
        ],
        [
            Paragraph(
                "<b>Altura</b>",
                estilo_normal,
            ),
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
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
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
        tabela_resumo
    )

    elementos.append(
        Spacer(1, 10)
    )

    # ========================================================
    # 3. MATERIAIS
    # ========================================================

    elementos.append(
        Paragraph(
            "3. QUANTITATIVO DE MATERIAIS",
            estilo_secao,
        )
    )

    tabela_materiais = [
        [
            Paragraph(
                "<b>Material</b>",
                estilo_pequeno,
            ),
            Paragraph(
                "<b>Un.</b>",
                estilo_pequeno,
            ),
            Paragraph(
                "<b>Quantidade</b>",
                estilo_pequeno,
            ),
            Paragraph(
                "<b>Preço unitário</b>",
                estilo_pequeno,
            ),
            Paragraph(
                "<b>Total</b>",
                estilo_pequeno,
            ),
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

    elementos.append(
        tabela_material_pdf
    )

    elementos.append(
        Spacer(1, 10)
    )

    # ========================================================
    # 4. RESUMO FINANCEIRO
    # ========================================================

    elementos.append(
        Paragraph(
            "4. RESUMO FINANCEIRO",
            estilo_secao,
        )
    )

    financeiro = [
        [
            Paragraph(
                "Materiais",
                estilo_normal,
            ),
            Paragraph(
                formatar_moeda(
                    subtotal_materiais
                ),
                estilo_direita,
            ),
        ],
        [
            Paragraph(
                "Massas e telas",
                estilo_normal,
            ),
            Paragraph(
                formatar_moeda(
                    massas_telas
                ),
                estilo_direita,
            ),
        ],
        [
            Paragraph(
                "Mão de obra",
                estilo_normal,
            ),
            Paragraph(
                formatar_moeda(
                    custo_mao_de_obra
                ),
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

    elementos.append(
        tabela_financeiro
    )

    elementos.append(
        Spacer(1, 10)
    )

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

    elementos.append(
        total_tabela
    )

    # ========================================================
    # 5. MÃO DE OBRA
    # ========================================================

    elementos.append(
        Spacer(1, 10)
    )

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
    # 6. CONDIÇÕES COMERCIAIS
    # ========================================================

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(
        Paragraph(
            "6. CONDIÇÕES COMERCIAIS",
            estilo_secao,
        )
    )

    condicoes = [
        [
            Paragraph(
                "<b>Validade</b>",
                estilo_normal,
            ),
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
                escape(
                    prazo_execucao
                    or "Não informado"
                ),
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                "<b>Condição de pagamento</b>",
                estilo_normal,
            ),
            Paragraph(
                escape(
                    condicao_pagamento
                    or "Não informado"
                ),
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                "<b>Forma de pagamento</b>",
                estilo_normal,
            ),
            Paragraph(
                escape(
                    forma_pagamento
                    or "Não informado"
                ),
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
    # 7. OBSERVAÇÕES
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

    # --------------------------------------------------------
    # RESPONSÁVEL — UMA ÚNICA VEZ
    # --------------------------------------------------------

    responsavel_pdf = (
        responsavel.strip()
        if responsavel
        and responsavel.strip()
        else "Responsável pelo orçamento"
    )

    elementos.append(
        Paragraph(
            f"<b>{escape(responsavel_pdf)}</b>",
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
    # GERAR
    # ========================================================

    doc.build(
        elementos,
        onFirstPage=adicionar_rodape,
        onLaterPages=adicionar_rodape,
    )

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# HERO PRINCIPAL — FASE 6C
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
    <div class="section-title">
        📋 Identificação do projeto
    </div>

    <div class="section-subtitle">
        Informe os dados principais do orçamento.
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
    <div class="section-title">
        💼 Condições comerciais
    </div>

    <div class="section-subtitle">
        Defina validade, prazo e condições de pagamento.
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
    <div class="section-title">
        📐 Dimensões do projeto
    </div>

    <div class="section-subtitle">
        Informe as dimensões utilizadas no cálculo.
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
    )

with col2:

    altura = st.number_input(
        "Altura (m)",
        min_value=0.01,
        value=3.00,
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

st.session_state["comprimento"] = (
    comprimento
)

st.session_state["altura"] = (
    altura
)


# ============================================================
# PREÇOS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        💰 Preços dos materiais
    </div>

    <div class="section-subtitle">
        Altere os preços conforme fornecedor,
        região ou condição de compra.
    </div>
    """,
    unsafe_allow_html=True,
)

if "precos" not in st.session_state:

    st.session_state["precos"] = (
        PRECOS_BASE.copy()
    )

precos_atualizados = {}

for nome, preco_padrao in (
    st.session_state["precos"].items()
):

    preco_atual = st.number_input(
        nome,
        min_value=0.00,
        value=float(preco_padrao),
        step=0.01,
        format="%.2f",
        key=f"preco_{nome}",
    )

    precos_atualizados[nome] = (
        preco_atual
    )

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
    <div class="section-title">
        📦 Quantidades dos materiais
    </div>

    <div class="section-subtitle">
        As quantidades são calculadas automaticamente,
        mas podem ser ajustadas.
    </div>
    """,
    unsafe_allow_html=True,
)

if "quantidades" not in st.session_state:

    st.session_state["quantidades"] = {}

quantidades_atualizadas = {}

for nome, material in previa["materiais"].items():

    quantidade_automatica = material[
        "quantidade"
    ]

    if nome not in st.session_state[
        "quantidades"
    ]:

        st.session_state[
            "quantidades"
        ][nome] = quantidade_automatica

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

    quantidades_atualizadas[nome] = (
        quantidade_atual
    )

st.session_state["quantidades"] = (
    quantidades_atualizadas
)


# ============================================================
# OBSERVAÇÕES TÉCNICAS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        📝 Observações técnicas
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
# BOTÃO CALCULAR
# ============================================================

if st.button(
    "🧮 CALCULAR / ATUALIZAR ORÇAMENTO",
    type="primary",
    use_container_width=True,
):

    resultado = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        precos=st.session_state["precos"],
        quantidades=st.session_state[
            "quantidades"
        ],
    )

    st.session_state["projeto"] = (
        resultado
    )

    st.session_state["nome_projeto"] = (
        nome_projeto
    )

    st.session_state["cliente"] = (
        cliente
    )

    st.session_state["local_obra"] = (
        local_obra
    )

    st.session_state["responsavel"] = (
        responsavel
    )

    st.session_state["data_orcamento"] = (
        data_orcamento
    )

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
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    # ========================================================
    # HERO DO ORÇAMENTO
    # ========================================================

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
    # DADOS DO ORÇAMENTO
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            📋 Dados do orçamento
        </div>
        """,
        unsafe_allow_html=True,
    )

    data_salva = st.session_state.get(
        "data_orcamento",
        date.today(),
    )

    projeto_nome = (
        st.session_state.get(
            "nome_projeto",
            "",
        )
        or "Não informado"
    )

    cliente_nome = (
        st.session_state.get(
            "cliente",
            "",
        )
        or "Não informado"
    )

    local_nome = (
        st.session_state.get(
            "local_obra",
            "",
        )
        or "Não informado"
    )

    responsavel_nome = (
        st.session_state.get(
            "responsavel",
            "",
        )
        or "Não informado"
    )

    validade_salva = st.session_state.get(
        "validade_orcamento",
        10,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Projeto
                </div>

                <div class="card-value">
                    {escape(projeto_nome)}
                </div>

                <div class="card-spacing"></div>

                <div class="card-label">
                    Cliente
                </div>

                <div class="card-value">
                    {escape(cliente_nome)}
                </div>

                <div class="card-spacing"></div>

                <div class="card-label">
                    Local da obra
                </div>

                <div class="card-value">
                    {escape(local_nome)}
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
                    {escape(responsavel_nome)}
                </div>

                <div class="card-spacing"></div>

                <div class="card-label">
                    Data
                </div>

                <div class="card-value">
                    {data_salva.strftime("%d/%m/%Y")}
                </div>

                <div class="card-spacing"></div>

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
        <div class="section-title">
            📐 Resumo do projeto
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
        <div class="section-title">
            📦 Quantitativo de materiais
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
                "Preço unitário": formatar_moeda(
                    material[
                        "preco_unitario"
                    ]
                ),
                "Total": formatar_moeda(
                    material[
                        "custo"
                    ]
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
        column_config={
            "Quantidade":
                st.column_config.NumberColumn(
                    "Quantidade",
                    format="%.2f",
                ),
        },
    )

    # ========================================================
    # FINANCEIRO
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            💰 Resumo financeiro
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
            <div class="finance-card">

                <div class="finance-label">
                    Materiais
                </div>

                <div class="finance-value">
                    {formatar_moeda(subtotal_materiais)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="finance-card">

                <div class="finance-label">
                    Massas e telas
                </div>

                <div class="finance-value">
                    {formatar_moeda(massas_telas)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="finance-card">

                <div class="finance-label">
                    Mão de obra
                </div>

                <div class="finance-value">
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
        <div class="section-title">
            👷 Mão de obra
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
    # CONDIÇÕES COMERCIAIS
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            💼 Condições comerciais
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

    forma_pagamento_salva = (
        st.session_state.get(
            "forma_pagamento",
            "",
        )
    )

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
                {escape(prazo_salvo or "Não informado")}
            </div>

            <br>

            <div class="card-label">
                Condição de pagamento
            </div>

            <div class="card-value">
                {escape(pagamento_salvo or "Não informado")}
            </div>

            <br>

            <div class="card-label">
                Forma de pagamento
            </div>

            <div class="card-value">
                {escape(
                    forma_pagamento_salva
                    or "Não informado"
                )}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    observacoes_comerciais_salvas = (
        st.session_state.get(
            "observacoes_comerciais",
            "",
        )
    )

    if observacoes_comerciais_salvas:

        st.markdown(
            f"""
            <div class="observation-card">

                <div class="card-label">
                    Inclusões / observações comerciais
                </div>

                {escape(
                    observacoes_comerciais_salvas
                ).replace(chr(10), "<br>")}

            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # OBSERVAÇÕES TÉCNICAS
    # ========================================================

    observacoes_tecnicas_salvas = (
        st.session_state.get(
            "observacoes_tecnicas",
            "",
        )
    )

    if observacoes_tecnicas_salvas:

        st.markdown(
            """
            <div class="section-title">
                📝 Observações técnicas
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="observation-card">
                {escape(
                    observacoes_tecnicas_salvas
                ).replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # VALOR FINAL
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            💵 Valor final
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="total-box">

            <div class="total-label">
                CUSTO GERAL
            </div>

            <div class="total-value">
                {formatar_moeda(custo_geral)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # ASSINATURA — CORREÇÃO 6C
    # ========================================================

    responsavel_assinatura = (
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
                {escape(responsavel_assinatura)}
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
        <div class="section-title">
            📤 Exportação do orçamento
        </div>

        <div class="section-subtitle">
            Gere os documentos profissionais do orçamento.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    # ========================================================
    # PDF
    # ========================================================

    with col1:

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

                nome_arquivo = (
                    nome_arquivo_orcamento()
                )

                st.download_button(
                    label="⬇️ BAIXAR PDF",
                    data=pdf_bytes,
                    file_name=(
                        f"{nome_arquivo}.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

                st.success(
                    "PDF gerado com sucesso."
                )

    # ========================================================
    # EXCEL
    # ========================================================

    with col2:

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

                nome_arquivo = (
                    nome_arquivo_orcamento()
                )

                st.download_button(
                    label="⬇️ BAIXAR EXCEL",
                    data=excel_bytes,
                    file_name=(
                        f"{nome_arquivo}.xlsx"
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
        "O Excel mantém os valores do orçamento e "
        "permite edição dos quantitativos e preços."
    )
