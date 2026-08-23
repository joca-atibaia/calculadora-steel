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
    page_title="Orçamento | Calculadora Steel",
    page_icon="📐",
    layout="wide",
)


# ============================================================
# CSS — APARÊNCIA 6C
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GERAL
    -------------------------------------------------------- */

    .stApp {
        background: #f5f7fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.3px;
    }

    /* --------------------------------------------------------
       CABEÇALHO PRINCIPAL
       -------------------------------------------------------- */

    .hero {
        padding: 30px 32px;
        border-radius: 18px;
        background: linear-gradient(
            135deg,
            #17212b 0%,
            #263746 100%
        );
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 8px 24px rgba(0,0,0,.10);
    }

    .hero-title {
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        font-size: 15px;
        opacity: .82;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 15px;
        padding: 6px 12px;
        border-radius: 20px;
        background: rgba(255,255,255,.12);
        font-size: 12px;
        font-weight: 600;
    }

    /* --------------------------------------------------------
       SEÇÕES
       -------------------------------------------------------- */

    .section-title {
        font-size: 20px;
        font-weight: 750;
        margin-top: 10px;
        margin-bottom: 14px;
        color: #17212b;
    }

    .section-subtitle {
        color: #6b7280;
        font-size: 13px;
        margin-bottom: 16px;
    }

    /* --------------------------------------------------------
       CARDS
       -------------------------------------------------------- */

    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 14px;
        box-shadow: 0 3px 12px rgba(0,0,0,.045);
    }

    .card-label {
        color: #6b7280;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: .5px;
        margin-bottom: 5px;
    }

    .card-value {
        color: #17212b;
        font-size: 18px;
        font-weight: 750;
    }

    /* --------------------------------------------------------
       TOTAL
       -------------------------------------------------------- */

    .total-box {
        padding: 28px;
        border-radius: 18px;
        border: 2px solid #1f7a1f;
        background: linear-gradient(
            135deg,
            #f3fff3 0%,
            #ffffff 100%
        );
        text-align: center;
        margin: 22px 0;
        box-shadow: 0 5px 18px rgba(31,122,31,.08);
    }

    .total-label {
        font-size: 13px;
        font-weight: 700;
        color: #4b5563;
        letter-spacing: .8px;
    }

    .total-value {
        font-size: 38px;
        font-weight: 850;
        color: #14532d;
        margin-top: 5px;
    }

    /* --------------------------------------------------------
       MÉTRICAS
       -------------------------------------------------------- */

    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,.04);
    }

    .metric-label {
        color: #6b7280;
        font-size: 12px;
        font-weight: 650;
    }

    .metric-value {
        color: #17212b;
        font-size: 23px;
        font-weight: 800;
        margin-top: 5px;
    }

    /* --------------------------------------------------------
       ASSINATURA
       -------------------------------------------------------- */

    .assinatura {
        margin-top: 55px;
        padding-top: 20px;
        padding-bottom: 20px;
        text-align: center;
        background: white;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
    }

    .linha-assinatura {
        border-top: 1px solid #333;
        width: 60%;
        margin: 0 auto 10px auto;
    }

    /* --------------------------------------------------------
       INFO
       -------------------------------------------------------- */

    .info-box {
        padding: 17px 20px;
        border-radius: 12px;
        border: 1px solid #dbe2e8;
        background: white;
        margin: 12px 0;
    }

    /* --------------------------------------------------------
       BOTÕES
       -------------------------------------------------------- */

    div.stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 46px;
    }

    /* --------------------------------------------------------
       DIVISORES
       -------------------------------------------------------- */

    hr {
        margin-top: 28px;
        margin-bottom: 28px;
        border-color: #e5e7eb;
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
    ).strip()

    nome = (
        nome
        .replace(" ", "_")
        .replace("/", "-")
        .replace("\\", "-")
    )

    if not nome:
        nome = "Orcamento_Steel_Framing"

    return nome


# ============================================================
# EXCEL
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
        "nome_projeto", ""
    )

    cliente = st.session_state.get(
        "cliente", ""
    )

    local_obra = st.session_state.get(
        "local_obra", ""
    )

    responsavel = st.session_state.get(
        "responsavel", ""
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
        "",
    )

    altura = st.session_state.get(
        "altura",
        "",
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

    custo_geral = obter_valor(
        projeto,
        "custo_geral",
    )

    mao_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    dias = obter_valor(
        mao_obra,
        "dias",
    )

    diaria = obter_valor(
        mao_obra,
        "diaria",
    )

    custo_mao_obra = obter_valor(
        mao_obra,
        "custo",
    )

    # --------------------------------------------------------
    # WORKBOOK
    # --------------------------------------------------------

    wb = Workbook()

    ws = wb.active
    ws.title = "ORÇAMENTO"

    ws_mat = wb.create_sheet("MATERIAIS")
    ws_mo = wb.create_sheet("MÃO DE OBRA")
    ws_dados = wb.create_sheet("DADOS")

    # --------------------------------------------------------
    # ESTILOS
    # --------------------------------------------------------

    titulo_fill = PatternFill(
        "solid",
        fgColor="17212B",
    )

    secao_fill = PatternFill(
        "solid",
        fgColor="E9EEF2",
    )

    total_fill = PatternFill(
        "solid",
        fgColor="EAF7EA",
    )

    branco = "FFFFFF"

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

    # --------------------------------------------------------
    # ABA ORÇAMENTO
    # --------------------------------------------------------

    ws.merge_cells("A1:E1")

    ws["A1"] = "ORÇAMENTO — STEEL FRAMING"

    ws["A1"].font = Font(
        bold=True,
        size=20,
        color=branco,
    )

    ws["A1"].fill = titulo_fill
    ws["A1"].alignment = Alignment(
        horizontal="center"
    )

    ws.merge_cells("A2:E2")

    ws["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws["A2"].alignment = Alignment(
        horizontal="center"
    )

    # Identificação

    ws.merge_cells("A4:E4")
    ws["A4"] = "IDENTIFICAÇÃO DO PROJETO"
    ws["A4"].fill = secao_fill
    ws["A4"].font = Font(bold=True)

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

    for chave, valor in dados:

        ws.cell(
            linha,
            1,
            chave,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        ws.cell(
            linha,
            1,
        ).font = Font(bold=True)

        linha += 1

    # Dimensões

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
        "DIMENSÕES DO PROJETO",
    )

    ws.cell(
        linha,
        1,
    ).fill = secao_fill

    ws.cell(
        linha,
        1,
    ).font = Font(bold=True)

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
        )

        ws.cell(
            linha,
            2,
            float(valor),
        )

        linha += 1

    # Resumo financeiro

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
        "RESUMO FINANCEIRO",
    )

    ws.cell(
        linha,
        1,
    ).fill = secao_fill

    ws.cell(
        linha,
        1,
    ).font = Font(bold=True)

    linha += 1

    ws.cell(linha, 1, "Materiais")
    ws.cell(linha, 2, subtotal_materiais)
    linha += 1

    ws.cell(linha, 1, "Massas e telas")
    ws.cell(linha, 2, massas_telas)
    linha += 1

    ws.cell(linha, 1, "Mão de obra")
    ws.cell(linha, 2, custo_mao_obra)
    linha += 1

    linha += 1

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=1,
    )

    ws.cell(
        linha,
        1,
        "VALOR TOTAL DO ORÇAMENTO",
    )

    ws.cell(
        linha,
        2,
        custo_geral,
    )

    ws.cell(
        linha,
        1,
    ).fill = total_fill

    ws.cell(
        linha,
        2,
    ).fill = total_fill

    ws.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        size=13,
    )

    ws.cell(
        linha,
        2,
    ).font = Font(
        bold=True,
        size=15,
    )

    # Formatação moeda

    for row in ws.iter_rows():

        for cell in row:

            if isinstance(
                cell.value,
                (int, float),
            ):

                cell.number_format = (
                    '"R$" #,##0.00'
                )

            cell.border = border

    # --------------------------------------------------------
    # ABA MATERIAIS
    # --------------------------------------------------------

    ws_mat.merge_cells("A1:E1")

    ws_mat["A1"] = "QUANTITATIVO DE MATERIAIS"

    ws_mat["A1"].fill = titulo_fill
    ws_mat["A1"].font = Font(
        bold=True,
        color=branco,
        size=16,
    )

    cabecalho = [
        "Material",
        "Unidade",
        "Quantidade",
        "Preço unitário",
        "Total",
    ]

    for col, valor in enumerate(
        cabecalho,
        1,
    ):

        cell = ws_mat.cell(
            3,
            col,
            valor,
        )

        cell.fill = secao_fill
        cell.font = Font(bold=True)
        cell.border = border

    linha = 4

    for nome, material in materiais.items():

        ws_mat.cell(
            linha,
            1,
            nome,
        )

        ws_mat.cell(
            linha,
            2,
            material.get(
                "unidade",
                "",
            ),
        )

        ws_mat.cell(
            linha,
            3,
            float(
                material.get(
                    "quantidade",
                    0,
                )
            ),
        )

        ws_mat.cell(
            linha,
            4,
            float(
                material.get(
                    "preco_unitario",
                    0,
                )
            ),
        )

        # Fórmula editável
        ws_mat.cell(
            linha,
            5,
            f"=C{linha}*D{linha}",
        )

        for col in range(1, 6):

            ws_mat.cell(
                linha,
                col,
            ).border = border

        ws_mat.cell(
            linha,
            3,
        ).number_format = "0.00"

        ws_mat.cell(
            linha,
            4,
        ).number_format = '"R$" #,##0.00'

        ws_mat.cell(
            linha,
            5,
        ).number_format = '"R$" #,##0.00'

        linha += 1

    linha_total_materiais = linha

    ws_mat.cell(
        linha,
        4,
        "TOTAL",
    )

    ws_mat.cell(
        linha,
        5,
        f"=SUM(E4:E{linha - 1})",
    )

    ws_mat.cell(
        linha,
        4,
    ).font = Font(bold=True)

    ws_mat.cell(
        linha,
        5,
    ).font = Font(bold=True)

    ws_mat.cell(
        linha,
        5,
    ).number_format = '"R$" #,##0.00'

    # --------------------------------------------------------
    # ABA MÃO DE OBRA
    # --------------------------------------------------------

    ws_mo.merge_cells("A1:D1")

    ws_mo["A1"] = "MÃO DE OBRA"

    ws_mo["A1"].fill = titulo_fill
    ws_mo["A1"].font = Font(
        bold=True,
        color=branco,
        size=16,
    )

    headers_mo = [
        "Descrição",
        "Dias",
        "Diária",
        "Custo",
    ]

    for col, valor in enumerate(
        headers_mo,
        1,
    ):

        cell = ws_mo.cell(
            3,
            col,
            valor,
        )

        cell.fill = secao_fill
        cell.font = Font(bold=True)
        cell.border = border

    ws_mo["A4"] = "Mão de obra"
    ws_mo["B4"] = float(dias)
    ws_mo["C4"] = float(diaria)

    # Fórmula editável
    ws_mo["D4"] = "=B4*C4"

    for row in range(4, 5):

        for col in range(1, 5):

            ws_mo.cell(
                row,
                col,
            ).border = border

    ws_mo["B4"].number_format = "0.0"
    ws_mo["C4"].number_format = '"R$" #,##0.00'
    ws_mo["D4"].number_format = '"R$" #,##0.00'

    # --------------------------------------------------------
    # ABA DADOS
    # --------------------------------------------------------

    ws_dados.merge_cells("A1:B1")

    ws_dados["A1"] = "DADOS DO ORÇAMENTO"

    ws_dados["A1"].fill = titulo_fill
    ws_dados["A1"].font = Font(
        bold=True,
        color=branco,
        size=16,
    )

    dados_completos = [
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
        (
            "Observações comerciais",
            observacoes_comerciais or "Não informado",
        ),
        (
            "Observações técnicas",
            observacoes_tecnicas or "Não informado",
        ),
    ]

    for linha, (chave, valor) in enumerate(
        dados_completos,
        3,
    ):

        ws_dados.cell(
            linha,
            1,
            chave,
        )

        ws_dados.cell(
            linha,
            2,
            valor,
        )

        ws_dados.cell(
            linha,
            1,
        ).font = Font(bold=True)

        ws_dados.cell(
            linha,
            1,
        ).border = border

        ws_dados.cell(
            linha,
            2,
        ).border = border

        ws_dados.cell(
            linha,
            2,
        ).alignment = Alignment(
            wrap_text=True,
            vertical="top",
        )

    # --------------------------------------------------------
    # LARGURAS
    # --------------------------------------------------------

    for sheet in wb.worksheets:

        for column_cells in sheet.columns:

            length = 0

            column_letter = get_column_letter(
                column_cells[0].column
            )

            for cell in column_cells:

                try:
                    length = max(
                        length,
                        len(str(cell.value)),
                    )
                except Exception:
                    pass

            sheet.column_dimensions[
                column_letter
            ].width = min(
                max(length + 3, 12),
                45,
            )

        sheet.freeze_panes = "A4"

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
            "Adicione 'reportlab' ao requirements.txt."
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
        "",
    )

    altura = st.session_state.get(
        "altura",
        "",
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
        alignment=TA_CENTER,
        spaceAfter=5,
    )

    estilo_subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Normal"],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=15,
    )

    estilo_secao = ParagraphStyle(
        "Secao",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
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
        parent=estilo_normal,
        fontName="Helvetica-Bold",
        fontSize=18,
        alignment=TA_RIGHT,
    )

    elementos = []

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

    # --------------------------------------------------------
    # DADOS
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "1. DADOS DO ORÇAMENTO",
            estilo_secao,
        )
    )

    dados_orcamento = [
        [
            Paragraph(
                f"<b>Projeto:</b><br/>{escape(nome_projeto or 'Não informado')}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Cliente:</b><br/>{escape(cliente or 'Não informado')}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra:</b><br/>{escape(local_obra or 'Não informado')}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Responsável:</b><br/>{escape(responsavel or 'Não informado')}",
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

    tabela = Table(
        dados_orcamento,
        colWidths=[88 * mm, 88 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), .5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#dddddd")),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 7),
                ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ]
        )
    )

    elementos.append(tabela)

    # --------------------------------------------------------
    # DIMENSÕES
    # --------------------------------------------------------

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

    tabela = Table(
        resumo,
        colWidths=[88 * mm, 88 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), .5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#dddddd")),
                ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f5f5f5")),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]
        )
    )

    elementos.append(tabela)

    # --------------------------------------------------------
    # MATERIAIS
    # --------------------------------------------------------

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
                    str(material.get("unidade", "")),
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

    tabela = Table(
        tabela_materiais,
        colWidths=[
            61 * mm,
            16 * mm,
            28 * mm,
            35 * mm,
            36 * mm,
        ],
        repeatRows=1,
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#eeeeee")),
                ("BOX", (0,0), (-1,-1), .5, colors.HexColor("#bbbbbb")),
                ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#dddddd")),
                ("ALIGN", (1,1), (1,-1), "CENTER"),
                ("ALIGN", (2,1), (-1,-1), "RIGHT"),
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("LEFTPADDING", (0,0), (-1,-1), 5),
                ("RIGHTPADDING", (0,0), (-1,-1), 5),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]
        )
    )

    elementos.append(tabela)

    # --------------------------------------------------------
    # FINANCEIRO
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "4. RESUMO FINANCEIRO",
            estilo_secao,
        )
    )

    financeiro = [
        ["Materiais", formatar_moeda(subtotal_materiais)],
        ["Massas e telas", formatar_moeda(massas_telas)],
        ["Mão de obra", formatar_moeda(custo_mao_de_obra)],
    ]

    tabela = Table(
        [
            [
                Paragraph(escape(x), estilo_normal),
                Paragraph(y, estilo_direita),
            ]
            for x, y in financeiro
        ],
        colWidths=[110 * mm, 66 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), .5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#dddddd")),
                ("ALIGN", (1,0), (1,-1), "RIGHT"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 7),
                ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ]
        )
    )

    elementos.append(tabela)

    elementos.append(Spacer(1, 8))

    total = Table(
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
        colWidths=[90 * mm, 86 * mm],
    )

    total.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), 1.2, colors.HexColor("#1f7a1f")),
                ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f3fff3")),
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("LEFTPADDING", (0,0), (-1,-1), 9),
                ("RIGHTPADDING", (0,0), (-1,-1), 9),
                ("TOPPADDING", (0,0), (-1,-1), 12),
                ("BOTTOMPADDING", (0,0), (-1,-1), 12),
            ]
        )
    )

    elementos.append(total)

    # --------------------------------------------------------
    # MÃO DE OBRA
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "5. MÃO DE OBRA",
            estilo_secao,
        )
    )

    mo = [
        ["Dias estimados", f"{float(dias):.1f}"],
        ["Valor da diária", formatar_moeda(diaria)],
        ["Custo da mão de obra", formatar_moeda(custo_mao_de_obra)],
    ]

    tabela = Table(
        [
            [
                Paragraph(f"<b>{escape(x)}</b>", estilo_normal),
                Paragraph(y, estilo_direita),
            ]
            for x, y in mo
        ],
        colWidths=[110 * mm, 66 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), .5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#dddddd")),
                ("ALIGN", (1,0), (1,-1), "RIGHT"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]
        )
    )

    elementos.append(tabela)

    # --------------------------------------------------------
    # CONDIÇÕES
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "6. CONDIÇÕES COMERCIAIS",
            estilo_secao,
        )
    )

    condicoes = [
        ["Validade", f"{validade} dias"],
        ["Prazo de execução", prazo_execucao or "Não informado"],
        ["Condição de pagamento", condicao_pagamento or "Não informado"],
        ["Forma de pagamento", forma_pagamento or "Não informado"],
    ]

    tabela = Table(
        [
            [
                Paragraph(f"<b>{escape(x)}</b>", estilo_normal),
                Paragraph(escape(str(y)), estilo_normal),
            ]
            for x, y in condicoes
        ],
        colWidths=[55 * mm, 121 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), .5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), .3, colors.HexColor("#dddddd")),
                ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f5f5f5")),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]
        )
    )

    elementos.append(tabela)

    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

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
                or "Não informado"
            ).replace("\n", "<br/>"),
            estilo_normal,
        )
    )

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
                or "Não informado"
            ).replace("\n", "<br/>"),
            estilo_normal,
        )
    )

    # --------------------------------------------------------
    # ASSINATURA
    # --------------------------------------------------------

    elementos.append(
        Spacer(1, 28)
    )

    assinatura = Table(
        [[" "]],
        colWidths=[100 * mm],
        rowHeights=[12 * mm],
    )

    assinatura.setStyle(
        TableStyle(
            [
                (
                    "LINEBELOW",
                    (0,0),
                    (-1,-1),
                    .8,
                    colors.HexColor("#333333"),
                ),
                (
                    "ALIGN",
                    (0,0),
                    (-1,-1),
                    "CENTER",
                ),
            ]
        )
    )

    elementos.append(assinatura)

    elementos.append(
        Paragraph(
            f"<b>{escape(responsavel or 'Responsável pelo orçamento')}</b>",
            ParagraphStyle(
                "Assinatura",
                parent=estilo_normal,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
            ),
        )
    )

    elementos.append(
        Paragraph(
            "Responsável pelo orçamento",
            ParagraphStyle(
                "Cargo",
                parent=estilo_normal,
                alignment=TA_CENTER,
                textColor=colors.grey,
                fontSize=8,
            ),
        )
    )

    def adicionar_rodape(canvas, documento):

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
            f"Orçamento Steel Framing • Página {documento.page}",
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
# CABEÇALHO
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
    '<div class="section-title">📋 Identificação do projeto</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Informe os dados principais do orçamento.</div>',
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
    '<div class="section-title">💼 Condições comerciais</div>',
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
        placeholder="Ex.: 50% entrada + 50% entrega",
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
    placeholder="Descreva inclusões, exclusões, transporte, prazo etc.",
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
    '<div class="section-title">📐 Dimensões do projeto</div>',
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

    area_preview = comprimento * altura

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
    '<div class="section-title">💰 Preços dos materiais</div>',
    unsafe_allow_html=True,
)

st.caption(
    "Altere os preços conforme fornecedor, região ou condição de compra."
)

if "precos" not in st.session_state:

    st.session_state["precos"] = PRECOS_BASE.copy()

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
# QUANTIDADES
# ============================================================

st.markdown(
    '<div class="section-title">📦 Quantidades dos materiais</div>',
    unsafe_allow_html=True,
)

st.caption(
    "As quantidades são calculadas automaticamente, mas podem ser ajustadas."
)

if "quantidades" not in st.session_state:

    st.session_state["quantidades"] = {}

quantidades_atualizadas = {}

for nome, material in previa["materiais"].items():

    quantidade_automatica = material[
        "quantidade"
    ]

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
# OBSERVAÇÕES TÉCNICAS
# ============================================================

observacoes_tecnicas = st.text_area(
    "📝 Observações técnicas",
    placeholder="Ex.: medidas finais deverão ser conferidas antes da fabricação.",
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

    st.session_state["projeto"] = resultado

    st.session_state["nome_projeto"] = nome_projeto
    st.session_state["cliente"] = cliente
    st.session_state["local_obra"] = local_obra
    st.session_state["responsavel"] = responsavel
    st.session_state["data_orcamento"] = data_orcamento

    st.session_state["validade_orcamento"] = validade_orcamento
    st.session_state["prazo_execucao"] = prazo_execucao
    st.session_state["condicao_pagamento"] = condicao_pagamento
    st.session_state["forma_pagamento"] = forma_pagamento
    st.session_state["observacoes_comerciais"] = observacoes_comerciais
    st.session_state["observacoes_tecnicas"] = observacoes_tecnicas

    st.success(
        "Orçamento atualizado com sucesso."
    )


# ============================================================
# ORÇAMENTO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]

    st.divider()

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


    # --------------------------------------------------------
    # IDENTIFICAÇÃO
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Dados do orçamento</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="card">

                <div class="card-label">Projeto</div>
                <div class="card-value">
                    {escape(st.session_state.get("nome_projeto") or "Não informado")}
                </div>

                <br>

                <div class="card-label">Cliente</div>
                <div class="card-value">
                    {escape(st.session_state.get("cliente") or "Não informado")}
                </div>

                <br>

                <div class="card-label">Local da obra</div>
                <div class="card-value">
                    {escape(st.session_state.get("local_obra") or "Não informado")}
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
            <div class="card">

                <div class="card-label">Responsável</div>
                <div class="card-value">
                    {escape(st.session_state.get("responsavel") or "Não informado")}
                </div>

                <br>

                <div class="card-label">Data</div>
                <div class="card-value">
                    {data_salva.strftime("%d/%m/%Y")}
                </div>

                <br>

                <div class="card-label">Validade</div>
                <div class="card-value">
                    {st.session_state.get("validade_orcamento", 10)} dias
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # DIMENSÕES
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📐 Resumo do projeto</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">ÁREA</div>
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
                <div class="metric-label">COMPRIMENTO</div>
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
                <div class="metric-label">ALTURA</div>
                <div class="metric-value">
                    {altura:.2f} m
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # MATERIAIS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📦 Quantitativo de materiais</div>',
        unsafe_allow_html=True,
    )

    tabela_materiais = []

    for nome, material in (
        projeto["materiais"].items()
    ):

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


    # --------------------------------------------------------
    # FINANCEIRO
    # --------------------------------------------------------

    subtotal_materiais = obter_valor(
        projeto,
        "subtotal_materiais",
    )

    massas_telas = obter_valor(
        projeto,
        "massas_telas",
    )

    mao_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    custo_mao_de_obra = obter_valor(
        mao_obra,
        "custo",
    )

    custo_geral = obter_valor(
        projeto,
        "custo_geral",
    )

    st.markdown(
        '<div class="section-title">💰 Resumo financeiro</div>',
        unsafe_allow_html=True,
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


    # --------------------------------------------------------
    # MÃO DE OBRA
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">👷 Mão de obra</div>',
        unsafe_allow_html=True,
    )

    dias = obter_valor(
        mao_obra,
        "dias",
    )

    diaria = obter_valor(
        mao_obra,
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


    # --------------------------------------------------------
    # CONDIÇÕES
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">💼 Condições comerciais</div>',
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

    validade_salva = st.session_state.get(
        "validade_orcamento",
        10,
    )

    st.markdown(
        f"""
        <div class="card">

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
                {escape(prazo_salvo or "Não informado")}
            </div>

            <br>

            <div class="card-label">
                Condição de pagamento
            </div>

            <div>
                {escape(pagamento_salvo or "Não informado")}
            </div>

            <br>

            <div class="card-label">
                Forma de pagamento
            </div>

            <div>
                {escape(forma_pagamento_salva or "Não informado")}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

    observacoes_comerciais_salvas = (
        st.session_state.get(
            "observacoes_comerciais",
            "",
        )
    )

    if observacoes_comerciais_salvas:

        st.markdown(
            '<div class="section-title">📝 Observações comerciais</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-box">
                {escape(observacoes_comerciais_salvas)}
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
            '<div class="section-title">🔧 Observações técnicas</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="info-box">
                {escape(observacoes_tecnicas_salvas)}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # ASSINATURA
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="assinatura">

            <div class="linha-assinatura"></div>

            <strong>
                {escape(
                    st.session_state.get(
                        "responsavel",
                        "Responsável pelo orçamento"
                    )
                    or "Responsável pelo orçamento"
                )}
            </strong>

            <div style="margin-top: 5px;">
                Responsável pelo orçamento
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # EXPORTAÇÃO
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📤 Exportação do orçamento</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)


    # PDF

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


    # EXCEL

    with col2:

        if st.button(
            "📊 EXPORTAR EXCEL",
            type="secondary",
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
