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

    /* ======================================================
       BASE
       ====================================================== */

    .stApp {
        background: #f5f7fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
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
        font-size: 2.15rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 1rem;
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
        font-size: 1.35rem;
        font-weight: 800;
        color: #17202a;
        margin-bottom: 3px;
    }

    .section-subtitle {
        color: #6b7280;
        font-size: 0.9rem;
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
       TABELA / CAIXAS
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
       STREAMLIT INPUTS
       ====================================================== */

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        border-radius: 9px;
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
        .replace("/", "_")
        .replace("\\", "_")
    )

    if not nome:
        nome = "Orcamento_Steel_Framing"

    return nome


# ============================================================
# EXCEL — FASE 6B
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

    buffer = BytesIO()

    wb = Workbook()

    ws_orc = wb.active
    ws_orc.title = "ORÇAMENTO"

    ws_mat = wb.create_sheet("MATERIAIS")
    ws_mo = wb.create_sheet("MÃO DE OBRA")
    ws_dados = wb.create_sheet("DADOS")

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

    prazo = st.session_state.get(
        "prazo_execucao",
        "",
    )

    condicao = st.session_state.get(
        "condicao_pagamento",
        "",
    )

    forma = st.session_state.get(
        "forma_pagamento",
        "",
    )

    obs_comerciais = st.session_state.get(
        "observacoes_comerciais",
        "",
    )

    obs_tecnicas = st.session_state.get(
        "observacoes_tecnicas",
        "",
    )

    area = obter_valor(projeto, "area")
    comprimento = st.session_state.get(
        "comprimento",
        0,
    )
    altura = st.session_state.get(
        "altura",
        0,
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
    # ESTILOS EXCEL
    # --------------------------------------------------------

    azul = "263746"
    azul_claro = "EAF0F4"
    verde = "1F7A1F"
    verde_claro = "EAF7EE"
    cinza = "F2F4F6"
    branco = "FFFFFF"

    thin = Side(
        style="thin",
        color="D9DEE3",
    )

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin,
    )

    currency_format = (
        '"R$" #,##0.00'
    )

    # --------------------------------------------------------
    # ABA ORÇAMENTO
    # --------------------------------------------------------

    ws_orc.merge_cells(
        "A1:E1"
    )

    ws_orc["A1"] = (
        "ORÇAMENTO — STEEL FRAMING"
    )

    ws_orc["A1"].font = Font(
        bold=True,
        size=18,
        color=branco,
    )

    ws_orc["A1"].fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    ws_orc["A1"].alignment = Alignment(
        horizontal="center"
    )

    ws_orc.row_dimensions[1].height = 30

    ws_orc.merge_cells("A2:E2")

    ws_orc["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws_orc["A2"].alignment = Alignment(
        horizontal="center"
    )

    # Identificação
    linha = 4

    ws_orc.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=5,
    )

    ws_orc.cell(
        linha,
        1,
        "IDENTIFICAÇÃO DO PROJETO",
    )

    ws_orc.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        color=branco,
    )

    ws_orc.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    linha += 1

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

    for rotulo, valor in dados_identificacao:
        ws_orc.cell(linha, 1, rotulo)
        ws_orc.cell(linha, 2, valor)

        ws_orc.cell(linha, 1).font = Font(
            bold=True
        )

        linha += 1

    # Dimensões
    linha += 1

    ws_orc.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=5,
    )

    ws_orc.cell(
        linha,
        1,
        "DIMENSÕES DO PROJETO",
    )

    ws_orc.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        color=branco,
    )

    ws_orc.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    linha += 1

    dimensoes = [
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
    ]

    for rotulo, valor in dimensoes:
        ws_orc.cell(linha, 1, rotulo)
        ws_orc.cell(linha, 2, float(valor))
        linha += 1

    # Resumo financeiro
    linha += 1

    ws_orc.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=5,
    )

    ws_orc.cell(
        linha,
        1,
        "RESUMO FINANCEIRO",
    )

    ws_orc.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        color=branco,
    )

    ws_orc.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    linha += 1

    ws_orc.cell(linha, 1, "Materiais")
    ws_orc.cell(
        linha,
        2,
        subtotal_materiais,
    )
    linha_materiais = linha

    linha += 1

    ws_orc.cell(linha, 1, "Massas e telas")
    ws_orc.cell(
        linha,
        2,
        massas_telas,
    )

    linha += 1

    ws_orc.cell(linha, 1, "Mão de obra")
    ws_orc.cell(
        linha,
        2,
        custo_mao_de_obra,
    )

    linha += 1

    ws_orc.cell(
        linha,
        1,
        "VALOR TOTAL DO ORÇAMENTO",
    )

    ws_orc.cell(
        linha,
        2,
        f"=SUM(B{linha_materiais}:B{linha-1})",
    )

    ws_orc.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        color=verde,
    )

    ws_orc.cell(
        linha,
        2,
    ).font = Font(
        bold=True,
        size=14,
        color=verde,
    )

    ws_orc.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

    ws_orc.cell(
        linha,
        2,
    ).fill = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

    # --------------------------------------------------------
    # ABA MATERIAIS
    # --------------------------------------------------------

    ws_mat.append([
        "Material",
        "Unidade",
        "Quantidade",
        "Preço unitário",
        "Total",
    ])

    for cell in ws_mat[1]:
        cell.font = Font(
            bold=True,
            color=branco,
        )
        cell.fill = PatternFill(
            "solid",
            fgColor=azul,
        )
        cell.alignment = Alignment(
            horizontal="center"
        )
        cell.border = border

    linha_material = 2

    for nome, material in projeto.get(
        "materiais",
        {},
    ).items():

        quantidade = float(
            material.get(
                "quantidade",
                0,
            )
        )

        preco = float(
            material.get(
                "preco_unitario",
                0,
            )
        )

        ws_mat.cell(
            linha_material,
            1,
            nome,
        )

        ws_mat.cell(
            linha_material,
            2,
            material.get(
                "unidade",
                "",
            ),
        )

        ws_mat.cell(
            linha_material,
            3,
            quantidade,
        )

        ws_mat.cell(
            linha_material,
            4,
            preco,
        )

        ws_mat.cell(
            linha_material,
            5,
            f"=C{linha_material}*D{linha_material}",
        )

        for col in range(1, 6):
            ws_mat.cell(
                linha_material,
                col,
            ).border = border

        linha_material += 1

    ws_mat.cell(
        linha_material,
        4,
        "TOTAL",
    )

    ws_mat.cell(
        linha_material,
        4,
    ).font = Font(
        bold=True
    )

    ws_mat.cell(
        linha_material,
        5,
        f"=SUM(E2:E{linha_material-1})",
    )

    ws_mat.cell(
        linha_material,
        5,
    ).font = Font(
        bold=True
    )

    # --------------------------------------------------------
    # ABA MÃO DE OBRA
    # --------------------------------------------------------

    ws_mo.append([
        "Descrição",
        "Quantidade",
        "Valor unitário",
        "Total",
    ])

    for cell in ws_mo[1]:
        cell.font = Font(
            bold=True,
            color=branco,
        )
        cell.fill = PatternFill(
            "solid",
            fgColor=azul,
        )
        cell.border = border

    ws_mo.append([
        "Mão de obra",
        float(dias),
        float(diaria),
        "=B2*C2",
    ])

    for cell in ws_mo[2]:
        cell.border = border

    ws_mo.append([
        "",
        "",
        "TOTAL",
        "=SUM(D2:D2)",
    ])

    ws_mo["C3"].font = Font(
        bold=True
    )

    ws_mo["D3"].font = Font(
        bold=True
    )

    # --------------------------------------------------------
    # ABA DADOS
    # --------------------------------------------------------

    dados = [
        ("Projeto", nome_projeto),
        ("Cliente", cliente),
        ("Local da obra", local_obra),
        ("Responsável", responsavel),
        (
            "Data do orçamento",
            data_orcamento.strftime("%d/%m/%Y"),
        ),
        ("Validade", f"{validade} dias"),
        ("Prazo de execução", prazo or "Não informado"),
        (
            "Condição de pagamento",
            condicao or "Não informado",
        ),
        (
            "Forma de pagamento",
            forma or "Não informado",
        ),
        (
            "Observações comerciais",
            obs_comerciais or "Não informado",
        ),
        (
            "Observações técnicas",
            obs_tecnicas or "Não informado",
        ),
    ]

    ws_dados.append([
        "Campo",
        "Informação",
    ])

    for cell in ws_dados[1]:
        cell.font = Font(
            bold=True,
            color=branco,
        )
        cell.fill = PatternFill(
            "solid",
            fgColor=azul,
        )
        cell.border = border

    for rotulo, valor in dados:
        ws_dados.append([
            rotulo,
            valor,
        ])

    # --------------------------------------------------------
    # FORMATAÇÃO GERAL
    # --------------------------------------------------------

    for ws in [
        ws_orc,
        ws_mat,
        ws_mo,
        ws_dados,
    ]:

        for row in ws.iter_rows():

            for cell in row:

                cell.border = border
                cell.alignment = Alignment(
                    vertical="center",
                    wrap_text=True,
                )

    # Moeda
    for row in ws_mat.iter_rows(
        min_row=2,
        min_col=4,
        max_col=5,
    ):
        for cell in row:
            cell.number_format = currency_format

    for row in ws_mo.iter_rows(
        min_row=2,
        min_col=3,
        max_col=4,
    ):
        for cell in row:
            cell.number_format = currency_format

    for row in ws_orc.iter_rows():

        for cell in row:

            if cell.column == 2:
                if isinstance(
                    cell.value,
                    (int, float),
                ) or (
                    isinstance(
                        cell.value,
                        str,
                    )
                    and str(cell.value).startswith("=")
                ):
                    cell.number_format = currency_format

    # Larguras
    larguras = {
        ws_orc: {
            "A": 32,
            "B": 28,
            "C": 18,
            "D": 18,
            "E": 18,
        },
        ws_mat: {
            "A": 34,
            "B": 14,
            "C": 16,
            "D": 18,
            "E": 20,
        },
        ws_mo: {
            "A": 30,
            "B": 18,
            "C": 20,
            "D": 20,
        },
        ws_dados: {
            "A": 30,
            "B": 70,
        },
    }

    for ws, colunas in larguras.items():

        for coluna, largura in colunas.items():

            ws.column_dimensions[
                coluna
            ].width = largura

    # Congelar cabeçalho
    ws_mat.freeze_panes = "A2"
    ws_mo.freeze_panes = "A2"
    ws_dados.freeze_panes = "A2"

    wb.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# PDF
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

    prazo = st.session_state.get(
        "prazo_execucao",
        "",
    )

    condicao = st.session_state.get(
        "condicao_pagamento",
        "",
    )

    forma = st.session_state.get(
        "forma_pagamento",
        "",
    )

    obs_comerciais = st.session_state.get(
        "observacoes_comerciais",
        "",
    )

    obs_tecnicas = st.session_state.get(
        "observacoes_tecnicas",
        "",
    )

    area = obter_valor(projeto, "area")
    comprimento = st.session_state.get(
        "comprimento",
        "",
    )
    altura = st.session_state.get(
        "altura",
        "",
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

    titulo = ParagraphStyle(
        "Titulo",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        alignment=TA_CENTER,
        spaceAfter=5,
    )

    subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Normal"],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=15,
    )

    secao = ParagraphStyle(
        "Secao",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceBefore=8,
        spaceAfter=8,
    )

    normal = ParagraphStyle(
        "NormalOrcamento",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
    )

    direita = ParagraphStyle(
        "Direita",
        parent=normal,
        alignment=TA_RIGHT,
    )

    pequeno = ParagraphStyle(
        "Pequeno",
        parent=normal,
        fontSize=8,
        leading=10,
    )

    elementos = []

    elementos.append(
        Paragraph(
            "ORÇAMENTO — STEEL FRAMING",
            titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Quantitativo de materiais e mão de obra",
            subtitulo,
        )
    )

    # Dados
    elementos.append(
        Paragraph(
            "1. DADOS DO ORÇAMENTO",
            secao,
        )
    )

    dados = [
        [
            Paragraph(
                f"<b>Projeto:</b><br/>{escape(nome_projeto or 'Não informado')}",
                normal,
            ),
            Paragraph(
                f"<b>Cliente:</b><br/>{escape(cliente or 'Não informado')}",
                normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra:</b><br/>{escape(local_obra or 'Não informado')}",
                normal,
            ),
            Paragraph(
                f"<b>Responsável:</b><br/>{escape(responsavel or 'Não informado')}",
                normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Data:</b><br/>{data_orcamento.strftime('%d/%m/%Y')}",
                normal,
            ),
            Paragraph(
                f"<b>Validade:</b><br/>{validade} dias",
                normal,
            ),
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[88 * mm, 88 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
                ("VALIGN", (0,0), (-1,-1), "TOP"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 7),
                ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ]
        )
    )

    elementos.append(tabela)

    # Dimensões
    elementos.append(
        Paragraph(
            "2. RESUMO DO PROJETO",
            secao,
        )
    )

    resumo = [
        ["Área", f"{float(area):.2f} m²"],
        ["Comprimento", f"{float(comprimento):.2f} m"],
        ["Altura", f"{float(altura):.2f} m"],
    ]

    tabela = Table(
        resumo,
        colWidths=[88 * mm, 88 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
                ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f5f5f5")),
                ("ALIGN", (1,0), (1,-1), "RIGHT"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]
        )
    )

    elementos.append(tabela)

    # Materiais
    elementos.append(
        Paragraph(
            "3. QUANTITATIVO DE MATERIAIS",
            secao,
        )
    )

    dados_mat = [
        ["Material", "Un.", "Quantidade", "Preço unitário", "Total"]
    ]

    for nome, material in materiais.items():

        dados_mat.append(
            [
                Paragraph(
                    escape(str(nome)),
                    pequeno,
                ),
                str(
                    material.get(
                        "unidade",
                        "",
                    )
                ),
                f'{float(material.get("quantidade", 0)):.2f}',
                formatar_moeda(
                    material.get(
                        "preco_unitario",
                        0,
                    )
                ),
                formatar_moeda(
                    material.get(
                        "custo",
                        0,
                    )
                ),
            ]
        )

    tabela = Table(
        dados_mat,
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
                ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#bbbbbb")),
                ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
                ("ALIGN", (1,1), (1,-1), "CENTER"),
                ("ALIGN", (2,1), (-1,-1), "RIGHT"),
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("LEFTPADDING", (0,0), (-1,-1), 5),
                ("RIGHTPADDING", (0,0), (-1,-1), 5),
                ("TOPPADDING", (0,0), (-1,-1), 5),
                ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ]
        )
    )

    elementos.append(tabela)

    # Financeiro
    elementos.append(
        Paragraph(
            "4. RESUMO FINANCEIRO",
            secao,
        )
    )

    financeiro = [
        ["Materiais", formatar_moeda(subtotal_materiais)],
        ["Massas e telas", formatar_moeda(massas_telas)],
        ["Mão de obra", formatar_moeda(custo_mao_obra)],
    ]

    tabela = Table(
        financeiro,
        colWidths=[110 * mm, 66 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
                ("ALIGN", (1,0), (1,-1), "RIGHT"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 7),
                ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ]
        )
    )

    elementos.append(tabela)

    total = Table(
        [
            [
                Paragraph(
                    "<b>VALOR TOTAL DO ORÇAMENTO</b>",
                    normal,
                ),
                Paragraph(
                    f"<b>{formatar_moeda(custo_geral)}</b>",
                    ParagraphStyle(
                        "TotalPDF",
                        parent=normal,
                        fontSize=18,
                        alignment=TA_RIGHT,
                        fontName="Helvetica-Bold",
                    ),
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

    # Mão de obra
    elementos.append(
        Paragraph(
            "5. MÃO DE OBRA",
            secao,
        )
    )

    tabela = Table(
        [
            ["Dias estimados", f"{float(dias):.1f}"],
            ["Valor da diária", formatar_moeda(diaria)],
            ["Custo da mão de obra", formatar_moeda(custo_mao_obra)],
        ],
        colWidths=[110 * mm, 66 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
                ("ALIGN", (1,0), (1,-1), "RIGHT"),
                ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7),
                ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]
        )
    )

    elementos.append(tabela)

    # Condições
    elementos.append(
        Paragraph(
            "6. CONDIÇÕES COMERCIAIS",
            secao,
        )
    )

    tabela = Table(
        [
            ["Validade", f"{validade} dias"],
            ["Prazo de execução", prazo or "Não informado"],
            ["Condição de pagamento", condicao or "Não informado"],
            ["Forma de pagamento", forma or "Não informado"],
        ],
        colWidths=[55 * mm, 121 * mm],
    )

    tabela.setStyle(
        TableStyle(
            [
                ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
                ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
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

    if obs_comerciais:

        elementos.append(
            Paragraph(
                "7. OBSERVAÇÕES COMERCIAIS",
                secao,
            )
        )

        elementos.append(
            Paragraph(
                escape(obs_comerciais).replace(
                    "\n",
                    "<br/>",
                ),
                normal,
            )
        )

    if obs_tecnicas:

        elementos.append(
            Paragraph(
                "8. OBSERVAÇÕES TÉCNICAS",
                secao,
            )
        )

        elementos.append(
            Paragraph(
                escape(obs_tecnicas).replace(
                    "\n",
                    "<br/>",
                ),
                normal,
            )
        )

    # Assinatura — CORRIGIDA
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
                    0.8,
                    colors.HexColor("#333333"),
                ),
            ]
        )
    )

    elementos.append(assinatura)

    elementos.append(
        Paragraph(
            f"<b>{escape(responsavel.strip())}</b>"
            if responsavel and responsavel.strip()
            else "<b>Responsável pelo orçamento</b>",
            ParagraphStyle(
                "AssNome",
                parent=normal,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
                fontSize=9,
            ),
        )
    )

    elementos.append(
        Paragraph(
            "Responsável pelo orçamento",
            ParagraphStyle(
                "AssCargo",
                parent=normal,
                alignment=TA_CENTER,
                textColor=colors.grey,
                fontSize=8,
            ),
        )
    )

    def rodape(canvas, documento):

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
        onFirstPage=rodape,
        onLaterPages=rodape,
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
# CONDIÇÕES
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
    placeholder=(
        "Descreva inclusões, exclusões, transporte, "
        "prazo e condições de fornecimento."
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
            Altere os preços conforme fornecedor,
            região ou condição de compra.
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

    with colunas_precos[indice % 3]:

        preco_atual = st.number_input(
            nome,
            min_value=0.00,
            value=float(preco_padrao),
            step=0.01,
            format="%.2f",
            key=f"preco_{nome}",
        )

        precos_atualizados[nome] = preco_atual

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

    if nome not in st.session_state[
        "quantidades"
    ]:

        st.session_state[
            "quantidades"
        ][nome] = quantidade_automatica

    with colunas_quantidades[indice % 3]:

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

observacoes_tecnicas = st.text_area(
    "📝 Observações técnicas",
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
# DOCUMENTO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]

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
    # DADOS
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            📋 Dados do orçamento
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    projeto_nome = st.session_state.get(
        "nome_projeto",
        "",
    ) or "Não informado"

    cliente_salvo = st.session_state.get(
        "cliente",
        "",
    ) or "Não informado"

    local_salvo = st.session_state.get(
        "local_obra",
        "",
    ) or "Não informado"

    responsavel_salvo = st.session_state.get(
        "responsavel",
        "",
    ) or "Não informado"

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
                    {escape(projeto_nome)}
                </div>

                <br>

                <div class="card-label">
                    Cliente
                </div>

                <div class="card-value">
                    {escape(cliente_salvo)}
                </div>

                <br>

                <div class="card-label">
                    Local da obra
                </div>

                <div class="card-value">
                    {escape(local_salvo)}
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
                    {escape(responsavel_salvo)}
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


    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            📐 Resumo do projeto
        </div>
        """,
        unsafe_allow_html=True,
    )

    area = obter_valor(
        projeto,
        "area",
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
                    {area:.2f} m²
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


    # --------------------------------------------------------
    # MATERIAIS
    # --------------------------------------------------------

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
            )
        },
    )


    # --------------------------------------------------------
    # FINANCEIRO
    # --------------------------------------------------------

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
        <div class="total-card">

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
        """
        <div class="section-title">
            👷 Mão de obra
        </div>
        """,
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
    ) or "Não informado"

    pagamento_salvo = st.session_state.get(
        "condicao_pagamento",
        "",
    ) or "Não informado"

    forma_salva = st.session_state.get(
        "forma_pagamento",
        "",
    ) or "Não informado"

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
                {escape(prazo_salvo)}
            </div>

            <br>

            <div class="card-label">
                Condição de pagamento
            </div>

            <div class="card-value">
                {escape(pagamento_salvo)}
            </div>

            <br>

            <div class="card-label">
                Forma de pagamento
            </div>

            <div class="card-value">
                {escape(forma_salva)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    obs_comerciais_salvas = st.session_state.get(
        "observacoes_comerciais",
        "",
    )

    if obs_comerciais_salvas:

        st.markdown(
            f"""
            <div class="notice-card">

                <strong>
                    Inclusões / Observações comerciais
                </strong>

                <br><br>

                {escape(obs_comerciais_salvas).replace(chr(10), "<br>")}

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # OBSERVAÇÕES TÉCNICAS
    # --------------------------------------------------------

    obs_tecnicas_salvas = st.session_state.get(
        "observacoes_tecnicas",
        "",
    )

    if obs_tecnicas_salvas:

        st.markdown(
            """
            <div class="section-title">
                📝 Observações técnicas
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            obs_tecnicas_salvas
        )


    # --------------------------------------------------------
    # ASSINATURA — CORRIGIDA
    # --------------------------------------------------------

    nome_assinatura = (
        st.session_state.get(
            "responsavel",
            "",
        ).strip()
    )

    if not nome_assinatura:

        nome_assinatura = (
            "Responsável pelo orçamento"
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


    # --------------------------------------------------------
    # EXPORTAÇÃO
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            📤 Exportação do orçamento
        </div>
        """,
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

    # Excel
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
        "O Excel mantém os valores do orçamento e "
        "permite edição dos quantitativos e preços."
    )
