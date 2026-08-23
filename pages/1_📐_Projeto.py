import streamlit as st
import pandas as pd

from datetime import date
from io import BytesIO
from html import escape

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
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Calculadora Steel Framing",
    page_icon="📐",
    layout="wide",
)


# ============================================================
# CSS — VERSÃO 6B
# ============================================================

st.markdown(
    """
    <style>

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

    /* --------------------------------------------------------
       HERO
       -------------------------------------------------------- */

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
            0 10px 30px rgba(0,0,0,0.12);

        color: white;
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
            rgba(255,255,255,0.12);

        border:
            1px solid rgba(255,255,255,0.22);

        border-radius: 999px;

        padding:
            7px 14px;

        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: #ffffff;
    }

    /* --------------------------------------------------------
       SEÇÕES
       -------------------------------------------------------- */

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

    /* --------------------------------------------------------
       CARDS
       -------------------------------------------------------- */

    .info-card {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 14px;

        padding:
            18px 20px;

        margin-bottom: 14px;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
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

    /* --------------------------------------------------------
       MÉTRICAS
       -------------------------------------------------------- */

    .metric-card {
        background: #ffffff;

        border:
            1px solid #e1e6eb;

        border-radius: 14px;

        padding: 20px;

        text-align: center;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.04);
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

    /* --------------------------------------------------------
       TOTAL
       -------------------------------------------------------- */

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
            0 5px 18px rgba(40,167,69,0.10);
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

    /* --------------------------------------------------------
       AVISO
       -------------------------------------------------------- */

    .notice-card {
        background: #ffffff;

        border-left:
            4px solid #34495e;

        border-radius: 10px;

        padding:
            15px 18px;

        margin:
            12px 0;

        color: #374151;

        line-height: 1.6;
    }

    /* --------------------------------------------------------
       INPUTS
       -------------------------------------------------------- */

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

    /* --------------------------------------------------------
       BOTÕES
       -------------------------------------------------------- */

    .stButton > button {
        border-radius: 9px;

        font-weight: 700;

        min-height: 42px;
    }

    /* --------------------------------------------------------
       DATAFRAME
       -------------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
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
    Converte qualquer valor numérico com segurança.
    """

    try:
        if valor is None:
            return float(padrao)

        return float(valor)

    except (TypeError, ValueError):
        return float(padrao)


def formatar_moeda(valor):
    """
    Formata número no padrão brasileiro.
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
    Obtém valor de dicionário com segurança.
    """

    if not isinstance(dicionario, dict):
        return padrao

    valor = dicionario.get(chave, padrao)

    if valor is None:
        return padrao

    return valor


def inicializar_estado():
    """
    Inicializa os estados da aplicação.
    """

    defaults = {

        "nome_projeto": "",

        "cliente": "",

        "local_obra": "",

        "responsavel": "",

        "data_orcamento": date.today(),

        "validade_orcamento": 10,

        "prazo_execucao": "",

        "condicao_pagamento": "",

        "forma_pagamento": "",

        "observacoes_comerciais": "",

        "observacoes_tecnicas": "",

        "comprimento": 30.00,

        "altura": 3.00,

        "diaria_mao_obra":
            CONFIGURACAO_PROJETO.get(
                "diaria_mao_de_obra",
                755.00,
            ),

        "precos": PRECOS_BASE.copy(),

        "quantidades": {},

        "projeto": None,

        "massas_telas_manual": None,
    }

    for chave, valor in defaults.items():

        if chave not in st.session_state:
            st.session_state[chave] = valor


inicializar_estado()


# ============================================================
# PDF
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
            "A biblioteca reportlab não está instalada."
        )

        return None

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,

        pagesize=A4,

        rightMargin=15 * mm,
        leftMargin=15 * mm,

        topMargin=15 * mm,
        bottomMargin=18 * mm,

        title="Orçamento Steel Framing",

        author=
            st.session_state.get(
                "responsavel",
                "",
            )
            or
            "Calculadora Steel Framing",
    )

    styles = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloSteel",
        parent=styles["Title"],

        fontName="Helvetica-Bold",

        fontSize=19,

        alignment=TA_CENTER,

        textColor=
            colors.HexColor(
                "#263746"
            ),

        spaceAfter=5,
    )

    subtitulo = ParagraphStyle(
        "SubtituloSteel",
        parent=styles["Normal"],

        fontSize=9,

        alignment=TA_CENTER,

        textColor=colors.grey,

        spaceAfter=15,
    )

    secao = ParagraphStyle(
        "SecaoSteel",
        parent=styles["Heading2"],

        fontName="Helvetica-Bold",

        fontSize=12,

        textColor=
            colors.HexColor(
                "#263746"
            ),

        spaceBefore=10,

        spaceAfter=8,
    )

    normal = ParagraphStyle(
        "NormalSteel",
        parent=styles["Normal"],

        fontSize=9,

        leading=12,
    )

    direita = ParagraphStyle(
        "DireitaSteel",
        parent=normal,

        alignment=TA_RIGHT,
    )

    pequeno = ParagraphStyle(
        "PequenoSteel",
        parent=normal,

        fontSize=8,

        leading=10,
    )

    elementos = []

    # --------------------------------------------------------
    # CABEÇALHO
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "ORÇAMENTO — STEEL FRAMING",
            titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Quantitativo de materiais, custos e mão de obra",
            subtitulo,
        )
    )

    # --------------------------------------------------------
    # DADOS
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "1. DADOS DO ORÇAMENTO",
            secao,
        )
    )

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

    dados = [
        [
            Paragraph(
                f"<b>Projeto:</b><br/>"
                f"{escape(nome_projeto or 'Não informado')}",
                normal,
            ),

            Paragraph(
                f"<b>Cliente:</b><br/>"
                f"{escape(cliente or 'Não informado')}",
                normal,
            ),
        ],

        [
            Paragraph(
                f"<b>Local da obra:</b><br/>"
                f"{escape(local_obra or 'Não informado')}",
                normal,
            ),

            Paragraph(
                f"<b>Responsável:</b><br/>"
                f"{escape(responsavel or 'Não informado')}",
                normal,
            ),
        ],

        [
            Paragraph(
                f"<b>Data:</b><br/>"
                f"{data_orcamento.strftime('%d/%m/%Y')}",
                normal,
            ),

            Paragraph(
                f"<b>Validade:</b><br/>"
                f"{validade} dias",
                normal,
            ),
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[
            88 * mm,
            88 * mm,
        ],
    )

    tabela.setStyle(
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

    elementos.append(tabela)

    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "2. RESUMO DO PROJETO",
            secao,
        )
    )

    resumo = [
        [
            Paragraph("Área", normal),
            Paragraph(
                f"{numero(projeto.get('area')):.2f} m²",
                direita,
            ),
        ],

        [
            Paragraph("Comprimento", normal),
            Paragraph(
                f"{numero(projeto.get('comprimento')):.2f} m",
                direita,
            ),
        ],

        [
            Paragraph("Altura", normal),
            Paragraph(
                f"{numero(projeto.get('altura')):.2f} m",
                direita,
            ),
        ],
    ]

    tabela = Table(
        resumo,
        colWidths=[
            88 * mm,
            88 * mm,
        ],
    )

    tabela.setStyle(
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
            secao,
        )
    )

    dados_mat = [
        [
            "Material",
            "Un.",
            "Quantidade",
            "Preço unitário",
            "Total",
        ]
    ]

    for nome, material in projeto.get(
        "materiais",
        {},
    ).items():

        quantidade = numero(
            material.get(
                "quantidade",
                0,
            )
        )

        preco = numero(
            material.get(
                "preco_unitario",
                0,
            )
        )

        custo = numero(
            material.get(
                "custo",
                quantidade * preco,
            )
        )

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

                f"{quantidade:.2f}",

                formatar_moeda(preco),

                formatar_moeda(custo),
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
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#263746"),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
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
            secao,
        )
    )

    subtotal = numero(
        projeto.get(
            "subtotal_materiais",
            0,
        )
    )

    massas = numero(
        projeto.get(
            "massas_telas",
            0,
        )
    )

    mao_obra = numero(
        projeto.get(
            "mao_de_obra",
            {},
        ).get(
            "custo",
            0,
        )
        if isinstance(
            projeto.get(
                "mao_de_obra",
                {},
            ),
            dict,
        )
        else 0
    )

    total = numero(
        projeto.get(
            "custo_geral",
            0,
        )
    )

    financeiro = [
        [
            "Materiais",
            formatar_moeda(subtotal),
        ],

        [
            "Massas e telas",
            formatar_moeda(massas),
        ],

        [
            "Mão de obra",
            formatar_moeda(mao_obra),
        ],

        [
            "TOTAL",
            formatar_moeda(total),
        ],
    ]

    tabela = Table(
        financeiro,
        colWidths=[
            110 * mm,
            66 * mm,
        ],
    )

    tabela.setStyle(
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
                    "FONTNAME",
                    (0, -1),
                    (-1, -1),
                    "Helvetica-Bold",
                ),
            ]
        )
    )

    elementos.append(tabela)

    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "5. OBSERVAÇÕES",
            secao,
        )
    )

    observacoes = (
        st.session_state.get(
            "observacoes_tecnicas",
            "",
        )
        or
        "Nenhuma observação técnica informada."
    )

    elementos.append(
        Paragraph(
            escape(observacoes),
            normal,
        )
    )

    # --------------------------------------------------------
    # ASSINATURA
    # --------------------------------------------------------

    elementos.append(
        Spacer(
            1,
            45,
        )
    )

    elementos.append(
        Paragraph(
            "________________________________________",
            titulo,
        )
    )

    elementos.append(
        Paragraph(
            escape(
                responsavel
                or
                "Responsável pelo orçamento"
            ),
            ParagraphStyle(
                "Assinatura",
                parent=normal,
                alignment=TA_CENTER,
            ),
        )
    )

    doc.build(elementos)

    buffer.seek(0)

    return buffer.getvalue()


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

    except ImportError:

        st.error(
            "A biblioteca openpyxl não está instalada."
        )

        return None

    wb = Workbook()

    ws = wb.active

    ws.title = "Resumo"

    ws_mat = wb.create_sheet(
        "Materiais"
    )

    ws_mo = wb.create_sheet(
        "Mão de obra"
    )

    ws_dados = wb.create_sheet(
        "Dados"
    )

    # --------------------------------------------------------
    # ESTILOS
    # --------------------------------------------------------

    azul = "263746"

    verde = "176B35"

    verde_claro = "ECFDF3"

    branco = "FFFFFF"

    cinza = "E1E6EB"

    border = Border(
        left=Side(
            style="thin",
            color=cinza,
        ),

        right=Side(
            style="thin",
            color=cinza,
        ),

        top=Side(
            style="thin",
            color=cinza,
        ),

        bottom=Side(
            style="thin",
            color=cinza,
        ),
    )

    moeda = (
        'R$ #,##0.00'
    )

    # --------------------------------------------------------
    # RESUMO
    # --------------------------------------------------------

    ws["A1"] = (
        "ORÇAMENTO STEEL FRAMING"
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

    ws.merge_cells(
        "A1:B1"
    )

    resumo = [

        (
            "Projeto",
            st.session_state.get(
                "nome_projeto",
                "",
            ),
        ),

        (
            "Cliente",
            st.session_state.get(
                "cliente",
                "",
            ),
        ),

        (
            "Local da obra",
            st.session_state.get(
                "local_obra",
                "",
            ),
        ),

        (
            "Responsável",
            st.session_state.get(
                "responsavel",
                "",
            ),
        ),

        (
            "Data",
            st.session_state.get(
                "data_orcamento",
                date.today(),
            ).strftime(
                "%d/%m/%Y"
            ),
        ),

        (
            "Área",
            numero(
                projeto.get(
                    "area",
                    0,
                )
            ),
        ),

        (
            "Materiais",
            numero(
                projeto.get(
                    "subtotal_materiais",
                    0,
                )
            ),
        ),

        (
            "Massas e Telas",
            numero(
                projeto.get(
                    "massas_telas",
                    0,
                )
            ),
        ),

        (
            "Mão de obra",
            numero(
                projeto.get(
                    "mao_de_obra",
                    {},
                ).get(
                    "custo",
                    0,
                )
                if isinstance(
                    projeto.get(
                        "mao_de_obra",
                        {},
                    ),
                    dict,
                )
                else 0
            ),
        ),

        (
            "Custo Geral",
            numero(
                projeto.get(
                    "custo_geral",
                    0,
                )
            ),
        ),
    ]

    linha = 3

    for nome, valor in resumo:

        ws.cell(
            linha,
            1,
            nome,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        ws.cell(
            linha,
            1,
        ).border = border

        ws.cell(
            linha,
            2,
        ).border = border

        if isinstance(
            valor,
            (int, float),
        ):

            ws.cell(
                linha,
                2,
            ).number_format = moeda

        linha += 1

    # --------------------------------------------------------
    # MATERIAIS
    # --------------------------------------------------------

    ws_mat.append(
        [
            "Material",
            "Unidade",
            "Quantidade",
            "Preço unitário",
            "Total",
        ]
    )

    for cell in ws_mat[1]:

        cell.font = Font(
            bold=True,
            color=branco,
        )

        cell.fill = PatternFill(
            "solid",
            fgColor=azul,
        )

        cell.border = border

    linha_mat = 2

    for nome, material in projeto.get(
        "materiais",
        {},
    ).items():

        quantidade = numero(
            material.get(
                "quantidade",
                0,
            )
        )

        preco = numero(
            material.get(
                "preco_unitario",
                0,
            )
        )

        ws_mat.cell(
            linha_mat,
            1,
            nome,
        )

        ws_mat.cell(
            linha_mat,
            2,
            material.get(
                "unidade",
                "",
            ),
        )

        ws_mat.cell(
            linha_mat,
            3,
            quantidade,
        )

        ws_mat.cell(
            linha_mat,
            4,
            preco,
        )

        ws_mat.cell(
            linha_mat,
            5,
            f"=C{linha_mat}*D{linha_mat}",
        )

        for coluna in range(
            1,
            6,
        ):

            ws_mat.cell(
                linha_mat,
                coluna,
            ).border = border

        ws_mat.cell(
            linha_mat,
            4,
        ).number_format = moeda

        ws_mat.cell(
            linha_mat,
            5,
        ).number_format = moeda

        linha_mat += 1

    ws_mat.cell(
        linha_mat,
        4,
        "TOTAL",
    )

    ws_mat.cell(
        linha_mat,
        5,
        f"=SUM(E2:E{linha_mat-1})",
    )

    ws_mat.cell(
        linha_mat,
        4,
    ).font = Font(
        bold=True
    )

    ws_mat.cell(
        linha_mat,
        5,
    ).font = Font(
        bold=True
    )

    ws_mat.cell(
        linha_mat,
        5,
    ).number_format = moeda

    # --------------------------------------------------------
    # MÃO DE OBRA
    # --------------------------------------------------------

    ws_mo.append(
        [
            "Descrição",
            "Quantidade",
            "Valor unitário",
            "Total",
        ]
    )

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

    mao_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    dias = numero(
        mao_obra.get(
            "dias",
            0,
        )
        if isinstance(
            mao_obra,
            dict,
        )
        else 0
    )

    diaria = numero(
        mao_obra.get(
            "diaria",
            0,
        )
        if isinstance(
            mao_obra,
            dict,
        )
        else 0
    )

    ws_mo.append(
        [
            "Mão de obra",
            dias,
            diaria,
            "=B2*C2",
        ]
    )

    for cell in ws_mo[2]:

        cell.border = border

    ws_mo["C2"].number_format = moeda

    ws_mo["D2"].number_format = moeda

    # --------------------------------------------------------
    # DADOS
    # --------------------------------------------------------

    ws_dados.append(
        [
            "Campo",
            "Informação",
        ]
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

    dados = [

        (
            "Projeto",
            st.session_state.get(
                "nome_projeto",
                "",
            ),
        ),

        (
            "Cliente",
            st.session_state.get(
                "cliente",
                "",
            ),
        ),

        (
            "Local da obra",
            st.session_state.get(
                "local_obra",
                "",
            ),
        ),

        (
            "Responsável",
            st.session_state.get(
                "responsavel",
                "",
            ),
        ),

        (
            "Data",
            st.session_state.get(
                "data_orcamento",
                date.today(),
            ).strftime(
                "%d/%m/%Y"
            ),
        ),

        (
            "Validade",
            f"{st.session_state.get('validade_orcamento', 10)} dias",
        ),

        (
            "Prazo",
            st.session_state.get(
                "prazo_execucao",
                "",
            ),
        ),

        (
            "Condição de pagamento",
            st.session_state.get(
                "condicao_pagamento",
                "",
            ),
        ),

        (
            "Forma de pagamento",
            st.session_state.get(
                "forma_pagamento",
                "",
            ),
        ),

        (
            "Observações comerciais",
            st.session_state.get(
                "observacoes_comerciais",
                "",
            ),
        ),

        (
            "Observações técnicas",
            st.session_state.get(
                "observacoes_tecnicas",
                "",
            ),
        ),
    ]

    for item in dados:

        ws_dados.append(
            list(item)
        )

    # --------------------------------------------------------
    # FORMATAÇÃO
    # --------------------------------------------------------

    for planilha in [
        ws,
        ws_mat,
        ws_mo,
        ws_dados,
    ]:

        for row in planilha.iter_rows():

            for cell in row:

                cell.border = border

                cell.alignment = Alignment(
                    vertical="center",
                    wrap_text=True,
                )

    # --------------------------------------------------------
    # LARGURAS
    # --------------------------------------------------------

    ws.column_dimensions[
        "A"
    ].width = 32

    ws.column_dimensions[
        "B"
    ].width = 28

    ws_mat.column_dimensions[
        "A"
    ].width = 34

    ws_mat.column_dimensions[
        "B"
    ].width = 14

    ws_mat.column_dimensions[
        "C"
    ].width = 16

    ws_mat.column_dimensions[
        "D"
    ].width = 18

    ws_mat.column_dimensions[
        "E"
    ].width = 20

    ws_mo.column_dimensions[
        "A"
    ].width = 30

    ws_mo.column_dimensions[
        "B"
    ].width = 18

    ws_mo.column_dimensions[
        "C"
    ].width = 20

    ws_mo.column_dimensions[
        "D"
    ].width = 20

    ws_dados.column_dimensions[
        "A"
    ].width = 30

    ws_dados.column_dimensions[
        "B"
    ].width = 70

    # --------------------------------------------------------
    # FREEZE
    # --------------------------------------------------------

    ws_mat.freeze_panes = "A2"

    ws_mo.freeze_panes = "A2"

    ws_dados.freeze_panes = "A2"

    # --------------------------------------------------------
    # SALVAR
    # --------------------------------------------------------

    buffer = BytesIO()

    wb.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            📐 CALCULADORA STEEL FRAMING
        </div>

        <div class="hero-subtitle">
            Sistema profissional para orçamento de
            materiais, quantitativos e mão de obra.
        </div>

        <div class="hero-badge">
            ORÇAMENTO PROFISSIONAL • VERSÃO 6B
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

        placeholder=
            "Ex.: Residência Atibaia",

        key="nome_projeto_input",
    )

    cliente = st.text_input(
        "Cliente",

        placeholder=
            "Nome do cliente",

        key="cliente_input",
    )

with col2:

    local_obra = st.text_input(
        "Local da obra",

        placeholder=
            "Ex.: Atibaia - SP",

        key="local_obra_input",
    )

    responsavel = st.text_input(
        "Responsável pelo orçamento",

        placeholder=
            "Nome do profissional",

        key="responsavel_input",
    )


data_orcamento = st.date_input(
    "Data do orçamento",

    value=
        st.session_state.get(
            "data_orcamento",
            date.today(),
        ),

    key="data_orcamento_input",
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

        value=int(
            st.session_state.get(
                "validade_orcamento",
                10,
            )
        ),

        step=1,

        key="validade_input",
    )

    prazo_execucao = st.text_input(
        "Prazo estimado de execução",

        placeholder=
            "Ex.: 30 dias úteis",

        key="prazo_input",
    )

with col2:

    condicao_pagamento = st.text_input(
        "Condição de pagamento",

        placeholder=
            "Ex.: 50% entrada + 50% entrega",

        key="condicao_input",
    )

    forma_pagamento = st.selectbox(
        "Forma de pagamento",

        [
            "Pix",
            "Transferência bancária",
            "Boleto",
            "Cartão",
            "Dinheiro",
            "A combinar",
        ],

        key="forma_pagamento_input",
    )


observacoes_comerciais = st.text_area(
    "Inclusões / observações comerciais",

    placeholder=
        "Informe inclusões, exclusões e demais condições comerciais.",

    key="observacoes_comerciais_input",
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

        format="%.2f",

        key="comprimento_input",
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

        format="%.2f",

        key="altura_input",
    )

with col3:

    area_preview = (
        comprimento *
        altura
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
            Os preços padrão podem ser alterados conforme
            fornecedor, região ou condição de compra.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

precos_atualizados = {}

colunas_precos = st.columns(3)

for indice, (
    nome,
    preco_padrao,
) in enumerate(
    PRECOS_BASE.items()
):

    with colunas_precos[
        indice % 3
    ]:

        preco = st.number_input(
            nome,

            min_value=0.00,

            value=float(
                st.session_state[
                    "precos"
                ].get(
                    nome,
                    preco_padrao,
                )
            ),

            step=0.01,

            format="%.2f",

            key=f"preco_{nome}",
        )

        precos_atualizados[
            nome
        ] = preco


st.session_state[
    "precos"
] = precos_atualizados


# ============================================================
# PRÉ-CÁLCULO
# ============================================================

try:

    previa = calcular_projeto(

        comprimento=comprimento,

        altura=altura,

        precos=
            st.session_state[
                "precos"
            ],

    )

except Exception as erro:

    st.error(
        f"Erro no cálculo inicial: {erro}"
    )

    st.stop()


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
            A quantidade automática é calculada pelo sistema.
            Você pode alterar manualmente qualquer quantidade.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="notice-card">
        <b>Como funciona:</b><br>
        A quantidade automática é calculada conforme a área
        e os coeficientes cadastrados. Se você alterar uma
        quantidade abaixo, o valor manual passa a ser utilizado
        no orçamento.
    </div>
    """,
    unsafe_allow_html=True,
)


quantidades_atualizadas = {}

colunas_quantidades = st.columns(3)

for indice, (
    nome,
    material,
) in enumerate(
    previa.get(
        "materiais",
        {},
    ).items()
):

    quantidade_automatica = numero(
        material.get(
            "quantidade",
            0,
        )
    )

    if nome not in st.session_state[
        "quantidades"
    ]:

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
                ].get(
                    nome,
                    quantidade_automatica,
                )
            ),

            step=1.0,

            format="%.2f",

            key=f"quantidade_{nome}",
        )

        quantidades_atualizadas[
            nome
        ] = quantidade_atual

        st.caption(
            f"Automática: "
            f"{quantidade_automatica:.2f} "
            f"{material.get('unidade', '')}"
        )


st.session_state[
    "quantidades"
] = quantidades_atualizadas


# ============================================================
# MASSAS E TELAS
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            🧱 Massas e telas
        </div>

        <div class="section-subtitle">
            Este custo é calculado separadamente dos demais materiais.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


subtotal_previo = numero(
    previa.get(
        "subtotal_materiais",
        0,
    )
)

percentual_massas = numero(
    CONFIGURACAO_PROJETO.get(
        "percentual_massas_telas",
        0.05,
    )
)


massas_automaticas = (
    subtotal_previo *
    percentual_massas
)


col1, col2 = st.columns(2)

with col1:

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                VALOR AUTOMÁTICO
            </div>

            <div class="metric-value">
                {formatar_moeda(massas_automaticas)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:

    usar_manual = st.checkbox(
        "Informar valor manual",
        value=False,
        key="usar_massas_manual",
    )

    if usar_manual:

        valor_massas_telas = st.number_input(
            "Valor de Massas e Telas",

            min_value=0.00,

            value=float(
                massas_automaticas
            ),

            step=10.00,

            format="%.2f",

            key="massas_manual_input",
        )

    else:

        valor_massas_telas = None


# ============================================================
# MÃO DE OBRA
# ============================================================

st.markdown(
    """
    <div class="section-header">

        <div class="section-title">
            👷 Mão de obra
        </div>

        <div class="section-subtitle">
            Configure a diária utilizada no cálculo.
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)

with col1:

    diaria_mao_obra = st.number_input(
        "Diária de mão de obra",

        min_value=0.00,

        value=float(
            st.session_state.get(
                "diaria_mao_obra",
                CONFIGURACAO_PROJETO.get(
                    "diaria_mao_de_obra",
                    755.00,
                ),
            )
        ),

        step=10.00,

        format="%.2f",

        key="diaria_input",
    )

with col2:

    dias_preview = (
        (
            area_preview /
            numero(
                CONFIGURACAO_PROJETO.get(
                    "area_referencia",
                    30.00,
                )
            )
        )
        *
        numero(
            CONFIGURACAO_PROJETO.get(
                "dias_mao_de_obra_referencia",
                10.00,
            )
        )
    )

    custo_mao_preview = (
        dias_preview *
        diaria_mao_obra
    )

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                MÃO DE OBRA ESTIMADA
            </div>

            <div class="metric-value">
                {formatar_moeda(custo_mao_preview)}
            </div>

            <div style="
                margin-top:8px;
                color:#6b7280;
                font-size:0.8rem;
            ">
                {dias_preview:.2f} dias
            </div>

        </div>
        """,
        unsafe_allow_html=True,
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

    key="observacoes_tecnicas_input",
)


# ============================================================
# BOTÃO CALCULAR
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)


if st.button(
    "🧮 CALCULAR / ATUALIZAR ORÇAMENTO",

    type="primary",

    width="stretch",
):

    try:

        resultado = calcular_projeto(

            comprimento=comprimento,

            altura=altura,

            diaria=diaria_mao_obra,

            precos=
                st.session_state[
                    "precos"
                ],

            quantidades=
                st.session_state[
                    "quantidades"
                ],

            valor_massas_telas=
                valor_massas_telas,
        )

    except Exception as erro:

        st.error(
            f"Não foi possível calcular o orçamento: {erro}"
        )

        st.stop()

    # --------------------------------------------------------
    # SALVAR DADOS
    # --------------------------------------------------------

    st.session_state[
        "projeto"
    ] = resultado

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

    st.session_state[
        "comprimento"
    ] = comprimento

    st.session_state[
        "altura"
    ] = altura

    st.session_state[
        "diaria_mao_obra"
    ] = diaria_mao_obra

    st.session_state[
        "massas_telas_manual"
    ] = valor_massas_telas

    st.success(
        "Orçamento atualizado com sucesso."
    )


# ============================================================
# RESULTADO
# ============================================================

if not st.session_state.get(
    "projeto"
):

    st.info(
        "Preencha os dados e clique em "
        "🧮 CALCULAR / ATUALIZAR ORÇAMENTO."
    )

else:

    projeto = st.session_state[
        "projeto"
    ]

    # ========================================================
    # CABEÇALHO DO RESULTADO
    # ========================================================

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                📄 ORÇAMENTO PROFISSIONAL
            </div>

            <div class="hero-subtitle">
                Quantitativo de materiais, custos e mão de obra
            </div>

            <div class="hero-badge">
                VERSÃO 6B
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # INDICADORES
    # ========================================================

    indicadores = (
        calcular_indicadores_projeto(
            projeto
        )
    )

    area = numero(
        projeto.get(
            "area",
            0,
        )
    )

    materiais_total = numero(
        projeto.get(
            "subtotal_materiais",
            0,
        )
    )

    massas_total = numero(
        projeto.get(
            "massas_telas",
            0,
        )
    )

    mao_obra_dados = projeto.get(
        "mao_de_obra",
        {},
    )

    mao_obra_total = numero(
        mao_obra_dados.get(
            "custo",
            0,
        )
        if isinstance(
            mao_obra_dados,
            dict,
        )
        else 0
    )

    custo_geral = numero(
        projeto.get(
            "custo_geral",
            0,
        )
    )


    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                📊 Indicadores do orçamento
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

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

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    MATERIAIS
                </div>

                <div class="metric-value">
                    {formatar_moeda(materiais_total)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    MASSAS E TELAS
                </div>

                <div class="metric-value">
                    {formatar_moeda(massas_total)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    MÃO DE OBRA
                </div>

                <div class="metric-value">
                    {formatar_moeda(mao_obra_total)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c5:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-label">
                    CUSTO / m²
                </div>

                <div class="metric-value">
                    {formatar_moeda(
                        indicadores.get(
                            "custo_por_m2",
                            0,
                        )
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # TOTAL
    # ========================================================

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


    # ========================================================
    # DADOS DO CLIENTE
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


    projeto_nome = (
        st.session_state.get(
            "nome_projeto",
            "",
        )
        or
        "Não informado"
    )

    cliente_salvo = (
        st.session_state.get(
            "cliente",
            "",
        )
        or
        "Não informado"
    )

    local_salvo = (
        st.session_state.get(
            "local_obra",
            "",
        )
        or
        "Não informado"
    )

    responsavel_salvo = (
        st.session_state.get(
            "responsavel",
            "",
        )
        or
        "Não informado"
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
                    {st.session_state.get(
                        "data_orcamento",
                        date.today()
                    ).strftime("%d/%m/%Y")}
                </div>

                <br>

                <div class="card-label">
                    Validade
                </div>

                <div class="card-value">
                    {st.session_state.get(
                        "validade_orcamento",
                        10
                    )} dias
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # QUANTITATIVO
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                📦 Quantitativo de materiais
            </div>

            <div class="section-subtitle">
                Quantidades finais utilizadas no orçamento.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    linhas = []

    for nome, material in projeto.get(
        "materiais",
        {},
    ).items():

        quantidade = numero(
            material.get(
                "quantidade",
                0,
            )
        )

        quantidade_auto = numero(
            material.get(
                "quantidade_automatica",
                0,
            )
        )

        preco = numero(
            material.get(
                "preco_unitario",
                0,
            )
        )

        custo = numero(
            material.get(
                "custo",
                0,
            )
        )

        origem = (
            "Manual"
            if material.get(
                "origem_quantidade"
            )
            == "manual"
            else
            "Automática"
        )

        linhas.append(
            {
                "Material": nome,

                "Unidade":
                    material.get(
                        "unidade",
                        "",
                    ),

                "Quantidade":
                    quantidade,

                "Qtd. automática":
                    quantidade_auto,

                "Origem":
                    origem,

                "Preço unitário":
                    preco,

                "Total":
                    custo,
            }
        )


    df_materiais = pd.DataFrame(
        linhas
    )


    if not df_materiais.empty:

        st.dataframe(
            df_materiais,

            width="stretch",

            hide_index=True,

            column_config={

                "Quantidade":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),

                "Qtd. automática":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),

                "Preço unitário":
                    st.column_config.NumberColumn(
                        format="R$ %.2f"
                    ),

                "Total":
                    st.column_config.NumberColumn(
                        format="R$ %.2f"
                    ),
            },
        )


    # ========================================================
    # RESUMO FINANCEIRO
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


    financeiro = pd.DataFrame(
        [
            {
                "Categoria": "Materiais",
                "Valor": materiais_total,
                "%": indicadores.get(
                    "percentual_materiais",
                    0,
                ),
            },

            {
                "Categoria": "Massas e Telas",
                "Valor": massas_total,
                "%": indicadores.get(
                    "percentual_massas_telas",
                    0,
                ),
            },

            {
                "Categoria": "Mão de obra",
                "Valor": mao_obra_total,
                "%": indicadores.get(
                    "percentual_mao_de_obra",
                    0,
                ),
            },

            {
                "Categoria": "CUSTO GERAL",
                "Valor": custo_geral,
                "%": 100.00,
            },
        ]
    )


    st.dataframe(
        financeiro,

        width="stretch",

        hide_index=True,

        column_config={

            "Valor":
                st.column_config.NumberColumn(
                    format="R$ %.2f"
                ),

            "%":
                st.column_config.NumberColumn(
                    format="%.2f%%"
                ),
        },
    )


    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    st.markdown(
        """
        <div class="section-header">

            <div class="section-title">
                👷 Composição da mão de obra
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    dias = numero(
        mao_obra_dados.get(
            "dias",
            0,
        )
        if isinstance(
            mao_obra_dados,
            dict,
        )
        else 0
    )

    diaria = numero(
        mao_obra_dados.get(
            "diaria",
            0,
        )
        if isinstance(
            mao_obra_dados,
            dict,
        )
        else 0
    )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Dias estimados",
            f"{dias:.2f}",
        )

    with col2:

        st.metric(
            "Diária",
            formatar_moeda(
                diaria
            ),
        )

    with col3:

        st.metric(
            "Total",
            formatar_moeda(
                mao_obra_total
            ),
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


    condicoes_df = pd.DataFrame(
        [
            {
                "Campo":
                    "Prazo de execução",

                "Informação":
                    st.session_state.get(
                        "prazo_execucao",
                        "",
                    )
                    or
                    "Não informado",
            },

            {
                "Campo":
                    "Condição de pagamento",

                "Informação":
                    st.session_state.get(
                        "condicao_pagamento",
                        "",
                    )
                    or
                    "Não informado",
            },

            {
                "Campo":
                    "Forma de pagamento",

                "Informação":
                    st.session_state.get(
                        "forma_pagamento",
                        "",
                    )
                    or
                    "Não informado",
            },

            {
                "Campo":
                    "Observações comerciais",

                "Informação":
                    st.session_state.get(
                        "observacoes_comerciais",
                        "",
                    )
                    or
                    "Não informado",
            },
        ]
    )


    st.dataframe(
        condicoes_df,

        width="stretch",

        hide_index=True,
    )


    # ========================================================
    # OBSERVAÇÕES TÉCNICAS
    # ========================================================

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


    observacao_final = (
        st.session_state.get(
            "observacoes_tecnicas",
            "",
        )
        or
        "Nenhuma observação técnica informada."
    )


    st.markdown(
        f"""
        <div class="notice-card">
            {escape(observacao_final)}
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
                📤 Exportar orçamento
            </div>

            <div class="section-subtitle">
                Gere os arquivos do orçamento para enviar
                ao cliente ou arquivar.
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

        try:

            pdf_bytes = gerar_pdf(
                projeto
            )

            if pdf_bytes:

                nome_pdf = (
                    projeto_nome
                    .strip()
                    .replace(
                        " ",
                        "_",
                    )
                    .replace(
                        "/",
                        "_",
                    )
                    or
                    "Orcamento_Steel_Framing"
                )

                st.download_button(

                    "📄 BAIXAR PDF",

                    data=pdf_bytes,

                    file_name=
                        f"{nome_pdf}.pdf",

                    mime=
                        "application/pdf",

                    width="stretch",
                )

        except Exception as erro:

            st.error(
                f"Erro ao gerar PDF: {erro}"
            )


    # --------------------------------------------------------
    # EXCEL
    # --------------------------------------------------------

    with col2:

        try:

            excel_bytes = gerar_excel(
                projeto
            )

            if excel_bytes:

                nome_excel = (
                    projeto_nome
                    .strip()
                    .replace(
                        " ",
                        "_",
                    )
                    .replace(
                        "/",
                        "_",
                    )
                    or
                    "Orcamento_Steel_Framing"
                )

                st.download_button(

                    "📊 BAIXAR EXCEL",

                    data=excel_bytes,

                    file_name=
                        f"{nome_excel}.xlsx",

                    mime=
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                    width="stretch",
                )

        except Exception as erro:

            st.error(
                f"Erro ao gerar Excel: {erro}"
            )


    # ========================================================
    # ASSINATURA
    # ========================================================

    st.markdown(
        f"""
        <div style="
            margin:55px auto 25px auto;
            max-width:520px;
            text-align:center;
        ">

            <div style="
                border-top:1px solid #333;
                width:85%;
                margin:0 auto 10px auto;
            "></div>

            <div style="
                font-weight:700;
                color:#17202a;
                font-size:0.95rem;
            ">
                {escape(responsavel_salvo)}
            </div>

            <div style="
                color:#777;
                font-size:0.8rem;
                margin-top:5px;
            ">
                Responsável pelo orçamento
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )
