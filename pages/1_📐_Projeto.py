import streamlit as st
import pandas as pd

from datetime import date
from io import BytesIO
from html import escape

from core.calculos import calcular_projeto
from core.dados import PRECOS_BASE


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Orçamento | Calculadora Steel",
    page_icon="📐",
    layout="wide",
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
        padding-bottom: 3rem;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        padding: 32px 36px;
        border-radius: 18px;
        border: 1px solid #dfe3e8;
        background:
            linear-gradient(
                135deg,
                #f7f9fc 0%,
                #ffffff 55%,
                #eef5ff 100%
            );
        margin-bottom: 30px;
        box-shadow: 0 6px 22px rgba(0, 0, 0, 0.05);
    }

    .hero-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #182230;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #667085;
        line-height: 1.5;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 16px;
        padding: 7px 14px;
        border-radius: 999px;
        background: #e8f1ff;
        color: #175cd3;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.4px;
    }


    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #182230;
        margin-top: 10px;
        margin-bottom: 3px;
    }

    .section-subtitle {
        font-size: 14px;
        color: #667085;
        margin-bottom: 18px;
    }


    /* ======================================================
       CARDS
       ====================================================== */

    .info-card {
        padding: 20px 22px;
        border-radius: 14px;
        border: 1px solid #e4e7ec;
        background: #ffffff;
        margin-bottom: 15px;
        box-shadow: 0 3px 12px rgba(16, 24, 40, 0.04);
    }

    .card-label {
        font-size: 12px;
        font-weight: 700;
        color: #667085;
        text-transform: uppercase;
        letter-spacing: 0.4px;
        margin-bottom: 4px;
    }

    .card-value {
        font-size: 16px;
        font-weight: 600;
        color: #182230;
    }


    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e4e7ec;
        background: #ffffff;
        text-align: center;
        box-shadow: 0 3px 12px rgba(16, 24, 40, 0.04);
        min-height: 110px;
    }

    .metric-label {
        font-size: 12px;
        font-weight: 700;
        color: #667085;
        letter-spacing: 0.5px;
    }

    .metric-value {
        font-size: 26px;
        font-weight: 800;
        color: #182230;
        margin-top: 8px;
    }


    /* ======================================================
       TOTAL
       ====================================================== */

    .total-box {
        padding: 28px;
        border-radius: 16px;
        border: 2px solid #12b76a;
        background: linear-gradient(
            135deg,
            #ecfdf3,
            #f7fff9
        );
        text-align: center;
        margin: 22px 0;
        box-shadow: 0 6px 18px rgba(18, 183, 106, 0.10);
    }

    .total-label {
        font-size: 13px;
        font-weight: 800;
        color: #027a48;
        letter-spacing: 0.8px;
    }

    .total-value {
        font-size: 36px;
        font-weight: 900;
        color: #05603a;
        margin-top: 7px;
    }


    /* ======================================================
       ASSINATURA
       ====================================================== */

    .assinatura {
        margin-top: 60px;
        padding-top: 15px;
        text-align: center;
        color: #344054;
    }

    .linha-assinatura {
        border-top: 1px solid #344054;
        width: 55%;
        margin: 0 auto 10px auto;
    }

    .assinatura-nome {
        font-size: 15px;
        font-weight: 700;
    }

    .assinatura-cargo {
        margin-top: 5px;
        font-size: 12px;
        color: #667085;
    }


    /* ======================================================
       OBSERVAÇÕES
       ====================================================== */

    .observacao-card {
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid #e4e7ec;
        background: #f9fafb;
        color: #344054;
        line-height: 1.6;
        margin-top: 10px;
        margin-bottom: 15px;
    }


    /* ======================================================
       TABELA
       ====================================================== */

    .table-title {
        font-size: 16px;
        font-weight: 800;
        color: #182230;
        margin-bottom: 10px;
    }


    /* ======================================================
       DIVISOR
       ====================================================== */

    .section-divider {
        margin: 30px 0;
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

    nome = (
        str(nome)
        .strip()
        .replace(" ", "_")
    )

    if not nome:
        nome = "Orcamento_Steel_Framing"

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


    # ========================================================
    # WORKBOOK
    # ========================================================

    wb = Workbook()

    ws = wb.active
    ws.title = "ORÇAMENTO"

    ws_materiais = wb.create_sheet(
        "MATERIAIS"
    )

    ws_mao = wb.create_sheet(
        "MÃO DE OBRA"
    )

    ws_dados = wb.create_sheet(
        "DADOS"
    )


    # ========================================================
    # ESTILOS
    # ========================================================

    azul = "1F4E78"
    azul_claro = "D9EAF7"
    verde = "E2F0D9"
    verde_forte = "548235"
    cinza = "F2F2F2"
    branco = "FFFFFF"
    preto = "000000"

    thin = Side(
        style="thin",
        color="D9D9D9",
    )

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin,
    )


    moeda_format = (
        'R$ #,##0.00'
    )


    # ========================================================
    # ABA ORÇAMENTO
    # ========================================================

    ws.merge_cells(
        "A1:E1"
    )

    ws["A1"] = (
        "ORÇAMENTO — STEEL FRAMING"
    )

    ws["A1"].font = Font(
        bold=True,
        size=18,
        color=branco,
    )

    ws["A1"].fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    ws["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center",
    )

    ws.row_dimensions[1].height = 30


    ws.merge_cells(
        "A2:E2"
    )

    ws["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws["A2"].font = Font(
        italic=True,
        color="666666",
    )

    ws["A2"].alignment = Alignment(
        horizontal="center",
    )


    # --------------------------------------------------------
    # IDENTIFICAÇÃO
    # --------------------------------------------------------

    ws["A4"] = "IDENTIFICAÇÃO DO PROJETO"

    ws["A4"].font = Font(
        bold=True,
        size=13,
    )

    dados = [
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

    for rotulo, valor in dados:

        ws[f"A{linha}"] = rotulo
        ws[f"B{linha}"] = valor

        ws[f"A{linha}"].font = Font(
            bold=True,
        )

        ws[f"A{linha}"].fill = PatternFill(
            "solid",
            fgColor=cinza,
        )

        ws[f"A{linha}"].border = border
        ws[f"B{linha}"].border = border

        linha += 1


    # --------------------------------------------------------
    # DIMENSÕES
    # --------------------------------------------------------

    linha += 1

    ws[f"A{linha}"] = (
        "DIMENSÕES DO PROJETO"
    )

    ws[f"A{linha}"].font = Font(
        bold=True,
        size=13,
    )

    linha += 1

    dimensoes = [
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
    ]

    for rotulo, valor in dimensoes:

        ws[f"A{linha}"] = rotulo
        ws[f"B{linha}"] = float(valor)

        ws[f"A{linha}"].border = border
        ws[f"B{linha}"].border = border

        linha += 1


    # --------------------------------------------------------
    # RESUMO FINANCEIRO
    # --------------------------------------------------------

    linha += 1

    ws[f"A{linha}"] = (
        "RESUMO FINANCEIRO"
    )

    ws[f"A{linha}"].font = Font(
        bold=True,
        size=13,
    )

    linha += 1

    resumo_inicio = linha

    resumo = [
        (
            "Materiais",
            subtotal_materiais,
        ),
        (
            "Massas e telas",
            massas_telas,
        ),
        (
            "Mão de obra",
            custo_mao_de_obra,
        ),
    ]

    for rotulo, valor in resumo:

        ws[f"A{linha}"] = rotulo
        ws[f"B{linha}"] = float(valor)

        ws[f"A{linha}"].border = border
        ws[f"B{linha}"].border = border

        ws[f"B{linha}"].number_format = moeda_format

        linha += 1


    total_linha = linha + 1

    ws[f"A{total_linha}"] = (
        "VALOR TOTAL DO ORÇAMENTO"
    )

    ws[f"B{total_linha}"] = (
        f"=B{resumo_inicio}"
        f"+B{resumo_inicio + 1}"
        f"+B{resumo_inicio + 2}"
    )

    ws[f"A{total_linha}"].font = Font(
        bold=True,
        size=13,
        color=branco,
    )

    ws[f"B{total_linha}"].font = Font(
        bold=True,
        size=14,
        color=branco,
    )

    ws[f"A{total_linha}"].fill = PatternFill(
        "solid",
        fgColor=verde_forte,
    )

    ws[f"B{total_linha}"].fill = PatternFill(
        "solid",
        fgColor=verde_forte,
    )

    ws[f"A{total_linha}"].border = border
    ws[f"B{total_linha}"].border = border

    ws[f"B{total_linha}"].number_format = moeda_format


    # --------------------------------------------------------
    # CONDIÇÕES COMERCIAIS
    # --------------------------------------------------------

    linha = total_linha + 3

    ws[f"A{linha}"] = (
        "CONDIÇÕES COMERCIAIS"
    )

    ws[f"A{linha}"].font = Font(
        bold=True,
        size=13,
    )

    linha += 1

    condicoes = [
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
    ]

    for rotulo, valor in condicoes:

        ws[f"A{linha}"] = rotulo
        ws[f"B{linha}"] = valor

        ws[f"A{linha}"].font = Font(
            bold=True,
        )

        ws[f"A{linha}"].fill = PatternFill(
            "solid",
            fgColor=cinza,
        )

        ws[f"A{linha}"].border = border
        ws[f"B{linha}"].border = border

        linha += 1


    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

    linha += 1

    ws[f"A{linha}"] = (
        "OBSERVAÇÕES COMERCIAIS"
    )

    ws[f"A{linha}"].font = Font(
        bold=True,
        size=13,
    )

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=5,
    )

    ws.cell(
        linha,
        1,
    ).value = (
        observacoes_comerciais
        or "Não informado"
    )

    ws.cell(
        linha,
        1,
    ).alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )


    linha += 2

    ws[f"A{linha}"] = (
        "OBSERVAÇÕES TÉCNICAS"
    )

    ws[f"A{linha}"].font = Font(
        bold=True,
        size=13,
    )

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=5,
    )

    ws.cell(
        linha,
        1,
    ).value = (
        observacoes_tecnicas
        or "Não informado"
    )

    ws.cell(
        linha,
        1,
    ).alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )


    # ========================================================
    # ABA MATERIAIS
    # ========================================================

    ws_materiais.append(
        [
            "Material",
            "Unidade",
            "Quantidade",
            "Preço unitário",
            "Total",
        ]
    )

    for cell in ws_materiais[1]:

        cell.font = Font(
            bold=True,
            color=branco,
        )

        cell.fill = PatternFill(
            "solid",
            fgColor=azul,
        )

        cell.border = border

        cell.alignment = Alignment(
            horizontal="center",
        )


    primeira_linha_material = 2

    for nome, material in materiais.items():

        linha_material = (
            ws_materiais.max_row + 1
        )

        ws_materiais.append(
            [
                nome,
                material.get(
                    "unidade",
                    "",
                ),
                float(
                    material.get(
                        "quantidade",
                        0,
                    )
                ),
                float(
                    material.get(
                        "preco_unitario",
                        0,
                    )
                ),
                (
                    f"=C{linha_material}"
                    f"*D{linha_material}"
                ),
            ]
        )


    ultima_linha_material = (
        ws_materiais.max_row
    )

    linha_total_material = (
        ultima_linha_material + 1
    )

    ws_materiais[
        f"A{linha_total_material}"
    ] = "TOTAL MATERIAIS"

    ws_materiais[
        f"E{linha_total_material}"
    ] = (
        f"=SUM(E{primeira_linha_material}:"
        f"E{ultima_linha_material})"
    )

    ws_materiais[
        f"A{linha_total_material}"
    ].font = Font(
        bold=True,
    )

    ws_materiais[
        f"E{linha_total_material}"
    ].font = Font(
        bold=True,
    )


    # ========================================================
    # ABA MÃO DE OBRA
    # ========================================================

    ws_mao.append(
        [
            "Descrição",
            "Quantidade",
            "Valor unitário",
            "Total",
        ]
    )

    for cell in ws_mao[1]:

        cell.font = Font(
            bold=True,
            color=branco,
        )

        cell.fill = PatternFill(
            "solid",
            fgColor=azul,
        )

        cell.border = border


    ws_mao.append(
        [
            "Mão de obra",
            float(dias),
            float(diaria),
            "=B2*C2",
        ]
    )


    ws_mao["A4"] = (
        "Custo total da mão de obra"
    )

    ws_mao["D4"] = (
        "=D2"
    )

    ws_mao["A4"].font = Font(
        bold=True,
    )

    ws_mao["D4"].font = Font(
        bold=True,
    )


    # ========================================================
    # ABA DADOS
    # ========================================================

    ws_dados.append(
        ["CAMPO", "VALOR"]
    )

    for cell in ws_dados[1]:

        cell.font = Font(
            bold=True,
            color=branco,
        )

        cell.fill = PatternFill(
            "solid",
            fgColor=azul,
        )

    dados_completos = [
        ("Projeto", nome_projeto),
        ("Cliente", cliente),
        ("Local da obra", local_obra),
        ("Responsável", responsavel),
        (
            "Data do orçamento",
            data_orcamento.strftime(
                "%d/%m/%Y"
            ),
        ),
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
        (
            "Observações comerciais",
            observacoes_comerciais or "Não informado",
        ),
        (
            "Observações técnicas",
            observacoes_tecnicas or "Não informado",
        ),
    ]

    for item in dados_completos:

        ws_dados.append(
            list(item)
        )


    # ========================================================
    # FORMATAÇÃO GERAL DAS ABAS
    # ========================================================

    for planilha in wb.worksheets:

        planilha.freeze_panes = "A2"

        for row in planilha.iter_rows():

            for cell in row:

                cell.border = border

                cell.alignment = Alignment(
                    vertical="center",
                    wrap_text=True,
                )


        for column_cells in planilha.columns:

            tamanho = 0

            for cell in column_cells:

                if cell.value is not None:

                    tamanho = max(
                        tamanho,
                        len(str(cell.value)),
                    )

            tamanho = min(
                max(tamanho + 2, 12),
                45,
            )

            letra = get_column_letter(
                column_cells[0].column
            )

            planilha.column_dimensions[
                letra
            ].width = tamanho


    # ========================================================
    # FORMATAÇÃO MONETÁRIA
    # ========================================================

    for row in ws_materiais.iter_rows(
        min_row=2,
        max_row=ws_materiais.max_row,
    ):

        row[3].number_format = moeda_format
        row[4].number_format = moeda_format


    for row in ws_mao.iter_rows(
        min_row=2,
        max_row=ws_mao.max_row,
    ):

        row[2].number_format = moeda_format
        row[3].number_format = moeda_format


    # ========================================================
    # EXPORTAÇÃO
    # ========================================================

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

    comprimento = st.session_state.get(
        "comprimento",
        area,
    )

    altura = st.session_state.get(
        "altura",
        "",
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
        "Titulo",
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
        fontSize=9,
        leading=12,
    )

    estilo_pequeno = ParagraphStyle(
        "Pequeno",
        parent=styles["Normal"],
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
                f"<b>Projeto:</b><br/>"
                f"{escape(nome_projeto) if nome_projeto else 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Cliente:</b><br/>"
                f"{escape(cliente) if cliente else 'Não informado'}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra:</b><br/>"
                f"{escape(local_obra) if local_obra else 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Responsável:</b><br/>"
                f"{escape(responsavel) if responsavel else 'Não informado'}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Data:</b><br/>"
                f"{data_orcamento.strftime('%d/%m/%Y')}",
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
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(tabela_dados)
    elementos.append(Spacer(1, 8))


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
            Paragraph(f"{float(area):.2f} m²", estilo_direita),
        ],
        [
            Paragraph("<b>Comprimento</b>", estilo_normal),
            Paragraph(f"{float(comprimento):.2f} m", estilo_direita),
        ],
        [
            Paragraph("<b>Altura</b>", estilo_normal),
            Paragraph(
                f"{float(altura):.2f} m"
                if altura != ""
                else "Não informado",
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
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f5f5f5")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 10))


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
                Paragraph(str(nome), estilo_pequeno),
                Paragraph(
                    str(material.get("unidade", "")),
                    estilo_centralizado,
                ),
                Paragraph(
                    f'{float(material.get("quantidade", 0)):.2f}',
                    estilo_direita,
                ),
                Paragraph(
                    formatar_moeda(
                        material.get("preco_unitario", 0)
                    ),
                    estilo_direita,
                ),
                Paragraph(
                    formatar_moeda(
                        material.get("custo", 0)
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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#bbbbbb")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabela_material_pdf)
    elementos.append(Spacer(1, 10))


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
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(tabela_financeiro)
    elementos.append(Spacer(1, 10))


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
                ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#1f7a1f")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f3fff3")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    elementos.append(total_tabela)


    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            "5. MÃO DE OBRA",
            estilo_secao,
        )
    )

    mao_obra_tabela = Table(
        [
            [
                Paragraph("<b>Dias estimados</b>", estilo_normal),
                Paragraph(f"{float(dias):.1f}", estilo_direita),
            ],
            [
                Paragraph("<b>Valor da diária</b>", estilo_normal),
                Paragraph(formatar_moeda(diaria), estilo_direita),
            ],
            [
                Paragraph("<b>Custo da mão de obra</b>", estilo_normal),
                Paragraph(
                    formatar_moeda(custo_mao_de_obra),
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
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(mao_obra_tabela)


    # ========================================================
    # CONDIÇÕES
    # ========================================================

    elementos.append(Spacer(1, 10))

    elementos.append(
        Paragraph(
            "6. CONDIÇÕES COMERCIAIS",
            estilo_secao,
        )
    )

    condicoes = [
        [
            Paragraph("<b>Validade</b>", estilo_normal),
            Paragraph(f"{validade} dias", estilo_normal),
        ],
        [
            Paragraph("<b>Prazo de execução</b>", estilo_normal),
            Paragraph(
                escape(prazo_execucao)
                if prazo_execucao
                else "Não informado",
                estilo_normal,
            ),
        ],
        [
            Paragraph("<b>Condição de pagamento</b>", estilo_normal),
            Paragraph(
                escape(condicao_pagamento)
                if condicao_pagamento
                else "Não informado",
                estilo_normal,
            ),
        ],
        [
            Paragraph("<b>Forma de pagamento</b>", estilo_normal),
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
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f5f5f5")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabela_condicoes)


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
                ).replace("\n", "<br/>"),
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
                ).replace("\n", "<br/>"),
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

    elementos.append(assinatura)


    nome_assinatura = (
        escape(
            responsavel.strip()
        )
        if responsavel
        and responsavel.strip()
        else "Responsável pelo orçamento"
    )

    elementos.append(
        Paragraph(
            f"<b>{nome_assinatura}</b>",
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
# IDENTIFICAÇÃO DO PROJETO
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


st.divider()


# ============================================================
# CONDIÇÕES COMERCIAIS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        💼 Condições comerciais
    </div>

    <div class="section-subtitle">
        Defina as condições comerciais do orçamento.
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


st.divider()


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


st.session_state["comprimento"] = comprimento
st.session_state["altura"] = altura


st.divider()


# ============================================================
# PREÇOS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        💰 Preços dos materiais
    </div>

    <div class="section-subtitle">
        Altere os preços conforme fornecedor, região ou condição de compra.
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

    with colunas_precos[indice % 3]:

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

    if nome not in st.session_state["quantidades"]:

        st.session_state["quantidades"][nome] = (
            quantidade_automatica
        )

    with colunas_quantidades[
        indice % 3
    ]:

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

        quantidades_atualizadas[nome] = (
            quantidade_atual
        )


st.session_state["quantidades"] = (
    quantidades_atualizadas
)


st.divider()


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


st.divider()


# ============================================================
# CALCULAR
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
        quantidades=st.session_state["quantidades"],
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

    st.session_state["validade_orcamento"] = (
        validade_orcamento
    )

    st.session_state["prazo_execucao"] = (
        prazo_execucao
    )

    st.session_state["condicao_pagamento"] = (
        condicao_pagamento
    )

    st.session_state["forma_pagamento"] = (
        forma_pagamento
    )

    st.session_state["observacoes_comerciais"] = (
        observacoes_comerciais
    )

    st.session_state["observacoes_tecnicas"] = (
        observacoes_tecnicas
    )

    st.success(
        "Orçamento atualizado com sucesso."
    )


# ============================================================
# DOCUMENTO DO ORÇAMENTO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]

    st.divider()


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
    # DADOS
    # ========================================================

    st.markdown(
        """
        <div class="section-title">
            📋 Dados do orçamento
        </div>
        """,
        unsafe_allow_html=True,
    )


    projeto_nome = escape(
        st.session_state.get(
            "nome_projeto",
            "",
        )
        or "Não informado"
    )

    cliente_nome = escape(
        st.session_state.get(
            "cliente",
            "",
        )
        or "Não informado"
    )

    local_nome = escape(
        st.session_state.get(
            "local_obra",
            "",
        )
        or "Não informado"
    )

    responsavel_nome = escape(
        st.session_state.get(
            "responsavel",
            "",
        )
        or "Não informado"
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
                    {projeto_nome}
                </div>

                <br>

                <div class="card-label">
                    Cliente
                </div>

                <div class="card-value">
                    {cliente_nome}
                </div>

                <br>

                <div class="card-label">
                    Local da obra
                </div>

                <div class="card-value">
                    {local_nome}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with col2:

        data_salva = st.session_state.get(
            "data_orcamento",
            date.today(),
        )

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Responsável
                </div>

                <div class="card-value">
                    {responsavel_nome}
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
                    {st.session_state.get(
                        "validade_orcamento",
                        10,
                    )} dias
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    st.divider()


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


    st.divider()


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

    for nome, material in projeto[
        "materiais"
    ].items():

        tabela_materiais.append(
            {
                "Material": nome,
                "Unidade": material["unidade"],
                "Quantidade": material["quantidade"],
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
        column_config={
            "Quantidade": st.column_config.NumberColumn(
                "Quantidade",
                format="%.2f",
            ),
        },
    )


    st.divider()


    # ========================================================
    # RESUMO FINANCEIRO
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

        st.metric(
            "Materiais",
            formatar_moeda(
                subtotal_materiais
            ),
        )


    with col2:

        st.metric(
            "Massas e telas",
            formatar_moeda(
                massas_telas
            ),
        )


    with col3:

        st.metric(
            "Mão de obra",
            formatar_moeda(
                custo_mao_de_obra
            ),
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


    st.divider()


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

        st.metric(
            "Dias estimados",
            f"{dias:.1f}",
        )


    with col2:

        st.metric(
            "Valor da diária",
            formatar_moeda(
                diaria
            ),
        )


    with col3:

        st.metric(
            "Custo da mão de obra",
            formatar_moeda(
                custo_mao_de_obra
            ),
        )


    st.divider()


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


    prazo_salvo = escape(
        st.session_state.get(
            "prazo_execucao",
            "",
        )
        or "Não informado"
    )

    pagamento_salvo = escape(
        st.session_state.get(
            "condicao_pagamento",
            "",
        )
        or "Não informado"
    )

    forma_pagamento_salva = escape(
        st.session_state.get(
            "forma_pagamento",
            "",
        )
        or "Não informado"
    )

    validade_salva = st.session_state.get(
        "validade_orcamento",
        10,
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

            <div>
                {prazo_salvo}
            </div>

            <br>

            <div class="card-label">
                Condição de pagamento
            </div>

            <div>
                {pagamento_salvo}
            </div>

            <br>

            <div class="card-label">
                Forma de pagamento
            </div>

            <div>
                {forma_pagamento_salva}
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
            <div class="section-title">
                📝 Observações comerciais
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="observacao-card">
                {escape(
                    observacoes_comerciais_salvas
                ).replace(chr(10), "<br>")}
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
            <div class="section-title">
                📝 Observações técnicas
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="observacao-card">
                {escape(
                    observacoes_tecnicas_salvas
                ).replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.divider()


    # ========================================================
    # ASSINATURA — CORRIGIDA
    # ========================================================

    nome_responsavel = escape(
        st.session_state.get(
            "responsavel",
            "",
        ).strip()
    )

    if not nome_responsavel:

        nome_responsavel = (
            "Responsável pelo orçamento"
        )


    st.markdown(
        f"""
        <div class="assinatura">

            <div class="linha-assinatura"></div>

            <div class="assinatura-nome">
                {nome_responsavel}
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

    st.divider()


    st.markdown(
        """
        <div class="section-title">
            📤 Exportação do orçamento
        </div>

        <div class="section-subtitle">
            Gere o documento final em PDF ou Excel.
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
        "O Excel mantém os valores validados pelo orçamento "
        "e permite edição dos quantitativos e preços."
    )
