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
# CSS — 6C / 6D
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
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.22);
        border-radius: 999px;
        padding: 7px 14px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.6px;
        color: #ffffff;
    }

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

    .info-card {
        background: #ffffff;
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
        line-height: 1.45;
    }

    .metric-card {
        background: #ffffff;
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
        line-height: 1.2;
    }

    .total-card {
        background:
            linear-gradient(
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

    .notice-card {
        background: #ffffff;
        border-left: 4px solid #34495e;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 12px 0;
        color: #374151;
        line-height: 1.6;
    }

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

    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
        min-height: 42px;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e1e6eb;
        border-radius: 12px;
        padding: 12px;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 800 !important;
    }

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


def numero(valor, padrao=0.0):
    try:
        if valor is None:
            return float(padrao)
        return float(valor)
    except (TypeError, ValueError):
        return float(padrao)


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

    nome = (
        str(nome)
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    return nome or "Orcamento_Steel_Framing"


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
            "A biblioteca reportlab não está instalada. "
            "Adicione reportlab ao requirements.txt."
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

    area = numero(
        projeto.get("area", 0)
    )

    comprimento = numero(
        projeto.get("comprimento", 0)
    )

    altura = numero(
        projeto.get("altura", 0)
    )

    materiais = projeto.get(
        "materiais",
        {},
    )

    subtotal_materiais = numero(
        projeto.get(
            "subtotal_materiais",
            0,
        )
    )

    massas_telas = numero(
        projeto.get(
            "massas_telas",
            0,
        )
    )

    custo_geral = numero(
        projeto.get(
            "custo_geral",
            0,
        )
    )

    mao_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    dias = numero(
        mao_obra.get("dias", 0)
        if isinstance(mao_obra, dict)
        else 0
    )

    diaria = numero(
        mao_obra.get("diaria", 0)
        if isinstance(mao_obra, dict)
        else 0
    )

    custo_mao_obra = numero(
        mao_obra.get("custo", 0)
        if isinstance(mao_obra, dict)
        else 0
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
        "TituloSteel",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#263746"),
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
        textColor=colors.HexColor("#263746"),
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
    # IDENTIFICAÇÃO
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "1. DADOS DO ORÇAMENTO",
            secao,
        )
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
    # DIMENSÕES
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
                f"{area:.2f} m²",
                direita,
            ),
        ],
        [
            Paragraph("Comprimento", normal),
            Paragraph(
                f"{comprimento:.2f} m",
                direita,
            ),
        ],
        [
            Paragraph("Altura", normal),
            Paragraph(
                f"{altura:.2f} m",
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
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
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

    for nome, material in materiais.items():

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
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
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

    financeiro = [
        [
            "Materiais",
            formatar_moeda(subtotal_materiais),
        ],
        [
            "Massas e telas",
            formatar_moeda(massas_telas),
        ],
        [
            "Mão de obra",
            formatar_moeda(custo_mao_obra),
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
            ]
        )
    )

    elementos.append(tabela)

    elementos.append(
        Spacer(
            1,
            8,
        )
    )

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

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
                        "TotalValor",
                        parent=normal,
                        fontSize=18,
                        alignment=TA_RIGHT,
                        fontName="Helvetica-Bold",
                        textColor=colors.HexColor(
                            "#176b35"
                        ),
                    ),
                ),
            ]
        ],
        colWidths=[
            90 * mm,
            86 * mm,
        ],
    )

    total.setStyle(
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

    elementos.append(total)

    # --------------------------------------------------------
    # MÃO DE OBRA
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "5. MÃO DE OBRA",
            secao,
        )
    )

    tabela = Table(
        [
            [
                "Dias estimados",
                f"{dias:.1f}",
            ],
            [
                "Valor da diária",
                formatar_moeda(diaria),
            ],
            [
                "Custo da mão de obra",
                formatar_moeda(custo_mao_obra),
            ],
        ],
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
            secao,
        )
    )

    tabela = Table(
        [
            [
                "Validade",
                f"{validade} dias",
            ],
            [
                "Prazo de execução",
                prazo or "Não informado",
            ],
            [
                "Condição de pagamento",
                condicao or "Não informado",
            ],
            [
                "Forma de pagamento",
                forma or "Não informado",
            ],
        ],
        colWidths=[
            55 * mm,
            121 * mm,
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
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
            ]
        )
    )

    elementos.append(tabela)

    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

    if obs_comerciais:

        elementos.append(
            Paragraph(
                "7. OBSERVAÇÕES COMERCIAIS",
                secao,
            )
        )

        elementos.append(
            Paragraph(
                escape(
                    obs_comerciais
                ).replace(
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
                escape(
                    obs_tecnicas
                ).replace(
                    "\n",
                    "<br/>",
                ),
                normal,
            )
        )

    # --------------------------------------------------------
    # ASSINATURA
    # --------------------------------------------------------

    elementos.append(
        Spacer(
            1,
            25,
        )
    )

    assinatura = Table(
        [[" "]],
        colWidths=[
            100 * mm
        ],
        rowHeights=[
            12 * mm
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
            ]
        )
    )

    elementos.append(assinatura)

    elementos.append(
        Paragraph(
            escape(
                responsavel.strip()
                if responsavel and responsavel.strip()
                else "Responsável pelo orçamento"
            ),
            ParagraphStyle(
                "AssNomePDF",
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
                "AssCargoPDF",
                parent=normal,
                alignment=TA_CENTER,
                textColor=colors.grey,
                fontSize=8,
            ),
        )
    )

    # --------------------------------------------------------
    # RODAPÉ
    # --------------------------------------------------------

    def rodape(canvas, documento):

        canvas.saveState()

        largura, _ = A4

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
                "Calculadora Steel Framing • "
                f"Página {documento.page}"
            ),
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
            "A biblioteca openpyxl não está instalada. "
            "Adicione openpyxl ao requirements.txt."
        )

        return None

    buffer = BytesIO()

    wb = Workbook()

    ws = wb.active
    ws.title = "ORÇAMENTO"

    ws_mat = wb.create_sheet("MATERIAIS")
    ws_mo = wb.create_sheet("MÃO DE OBRA")
    ws_dados = wb.create_sheet("DADOS")

    azul = "263746"
    verde = "1F7A1F"
    verde_claro = "EAF7EE"
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

    moeda = '"R$" #,##0.00'

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

    area = numero(
        projeto.get("area", 0)
    )

    comprimento = numero(
        projeto.get("comprimento", 0)
    )

    altura = numero(
        projeto.get("altura", 0)
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

    custo_geral = numero(
        projeto.get(
            "custo_geral",
            0,
        )
    )

    mao = projeto.get(
        "mao_de_obra",
        {},
    )

    dias = numero(
        mao.get("dias", 0)
        if isinstance(mao, dict)
        else 0
    )

    diaria = numero(
        mao.get("diaria", 0)
        if isinstance(mao, dict)
        else 0
    )

    custo_mo = numero(
        mao.get("custo", 0)
        if isinstance(mao, dict)
        else 0
    )

    # --------------------------------------------------------
    # ORÇAMENTO
    # --------------------------------------------------------

    ws.merge_cells("A1:E1")
    ws["A1"] = "ORÇAMENTO — STEEL FRAMING"

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
        horizontal="center"
    )

    ws.merge_cells("A2:E2")
    ws["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    linha = 4

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=5,
    )

    ws.cell(
        linha,
        1,
        "IDENTIFICAÇÃO DO PROJETO",
    )

    ws.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        color=branco,
    )

    ws.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    linha += 1

    for rotulo, valor in [
        ("Projeto", nome_projeto or "Não informado"),
        ("Cliente", cliente or "Não informado"),
        ("Local da obra", local_obra or "Não informado"),
        ("Responsável", responsavel or "Não informado"),
        ("Data", data_orcamento.strftime("%d/%m/%Y")),
    ]:

        ws.cell(linha, 1, rotulo)
        ws.cell(linha, 2, valor)
        ws.cell(linha, 1).font = Font(bold=True)

        linha += 1

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
    ).font = Font(
        bold=True,
        color=branco,
    )

    ws.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    linha += 1

    for rotulo, valor in [
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
    ]:

        ws.cell(linha, 1, rotulo)
        ws.cell(linha, 2, valor)

        linha += 1

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
    ).font = Font(
        bold=True,
        color=branco,
    )

    ws.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=azul,
    )

    linha += 1

    linha_materiais = linha

    ws.cell(
        linha,
        1,
        "Materiais",
    )

    ws.cell(
        linha,
        2,
        subtotal,
    )

    linha += 1

    ws.cell(
        linha,
        1,
        "Massas e telas",
    )

    ws.cell(
        linha,
        2,
        massas,
    )

    linha += 1

    ws.cell(
        linha,
        1,
        "Mão de obra",
    )

    ws.cell(
        linha,
        2,
        custo_mo,
    )

    linha += 1

    ws.cell(
        linha,
        1,
        "VALOR TOTAL DO ORÇAMENTO",
    )

    ws.cell(
        linha,
        2,
        f"=SUM(B{linha_materiais}:B{linha-1})",
    )

    ws.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        color=verde,
    )

    ws.cell(
        linha,
        2,
    ).font = Font(
        bold=True,
        size=14,
        color=verde,
    )

    ws.cell(
        linha,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

    ws.cell(
        linha,
        2,
    ).fill = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

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

        for col in range(1, 6):
            ws_mat.cell(
                linha_mat,
                col,
            ).border = border

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
    ).font = Font(bold=True)

    ws_mat.cell(
        linha_mat,
        5,
    ).font = Font(bold=True)

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

    ws_mo.append(
        [
            "",
            "",
            "TOTAL",
            "=SUM(D2:D2)",
        ]
    )

    ws_mo["C3"].font = Font(bold=True)
    ws_mo["D3"].font = Font(bold=True)

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

        cell.border = border

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

    for item in dados:
        ws_dados.append(list(item))

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

    for row in ws_mat.iter_rows(
        min_row=2,
        min_col=4,
        max_col=5,
    ):

        for cell in row:
            cell.number_format = moeda

    for row in ws_mo.iter_rows(
        min_row=2,
        min_col=3,
        max_col=4,
    ):

        for cell in row:
            cell.number_format = moeda

    for row in ws.iter_rows():

        for cell in row:

            if cell.column == 2 and isinstance(
                cell.value,
                (int, float),
            ):
                cell.number_format = moeda

    larguras = {
        ws: {
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

    for planilha, colunas in larguras.items():

        for coluna, largura in colunas.items():

            planilha.column_dimensions[
                coluna
            ].width = largura

    ws_mat.freeze_panes = "A2"
    ws_mo.freeze_panes = "A2"
    ws_dados.freeze_panes = "A2"

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
            Sistema profissional para orçamento de materiais,
            quantitativos e mão de obra.
        </div>

        <div class="hero-badge">
            ORÇAMENTO PROFISSIONAL • 6C / 6D
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
        value=int(
            st.session_state.get(
                "validade_orcamento",
                10,
            )
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

try:

    previa = calcular_projeto(
        comprimento=comprimento,
        altura=altura,
        precos=st.session_state["precos"],
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
    width="stretch",
):

    try:

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

    except Exception as erro:

        st.error(
            f"Não foi possível calcular o orçamento: {erro}"
        )

        st.stop()

    st.session_state["projeto"] = resultado

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

    st.session_state[
        "comprimento"
    ] = comprimento

    st.session_state[
        "altura"
    ] = altura

    st.success(
        "Orçamento atualizado com sucesso."
    )


# ============================================================
# RESULTADO
# ============================================================

if "projeto" not in st.session_state:
    st.info(
        "Preencha os dados e clique em "
        "🧮 CALCULAR / ATUALIZAR ORÇAMENTO."
    )

else:

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
        or "Não informado"
    )

    cliente_salvo = (
        st.session_state.get(
            "cliente",
            "",
        )
        or "Não informado"
    )

    local_salvo = (
        st.session_state.get(
            "local_obra",
            "",
        )
        or "Não informado"
    )

    responsavel_salvo = (
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
        <div class="section-header">
            <div class="section-title">
                📐 Resumo do projeto
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    area = numero(
        projeto.get(
            "area",
            0,
        )
    )

    comprimento_resultado = numero(
        projeto.get(
            "comprimento",
            comprimento,
        )
    )

    altura_resultado = numero(
        projeto.get(
            "altura",
            altura,
        )
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
                    {comprimento_resultado:.2f} m
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
                    {altura_resultado:.2f} m
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
        <div class="section-header">
            <div class="section-title">
                📦 Quantitativo de materiais
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabela_materiais = []

    for nome, material in projeto.get(
        "materiais",
        {},
    ).items():

        tabela_materiais.append(
            {
                "Material": nome,
                "Unidade": material.get(
                    "unidade",
                    "",
                ),
                "Quantidade": numero(
                    material.get(
                        "quantidade",
                        0,
                    )
                ),
                "Preço unitário": formatar_moeda(
                    material.get(
                        "preco_unitario",
                        0,
                    )
                ),
                "Total": formatar_moeda(
                    material.get(
                        "custo",
                        0,
                    )
                ),
            }
        )

    df_materiais = pd.DataFrame(
        tabela_materiais
    )

    st.dataframe(
        df_materiais,
        width="stretch",
        hide_index=True,
        column_config={
            "Quantidade":
                st.column_config.NumberColumn(
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
        <div class="section-header">
            <div class="section-title">
                💰 Resumo financeiro
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    subtotal_materiais = numero(
        projeto.get(
            "subtotal_materiais",
            0,
        )
    )

    massas_telas = numero(
        projeto.get(
            "massas_telas",
            0,
        )
    )

    mao_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    custo_mao_obra = numero(
        mao_obra.get(
            "custo",
            0,
        )
        if isinstance(mao_obra, dict)
        else 0
    )

    custo_geral = numero(
        projeto.get(
            "custo_geral",
            0,
        )
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
                custo_mao_obra
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
        <div class="section-header">
            <div class="section-title">
                👷 Mão de obra
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dias = numero(
        mao_obra.get(
            "dias",
            0,
        )
        if isinstance(mao_obra, dict)
        else 0
    )

    diaria = numero(
        mao_obra.get(
            "diaria",
            0,
        )
        if isinstance(mao_obra, dict)
        else 0
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
                custo_mao_obra
            ),
        )

    # --------------------------------------------------------
    # CONDIÇÕES
    # --------------------------------------------------------

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

    prazo_salvo = (
        st.session_state.get(
            "prazo_execucao",
            "",
        )
        or "Não informado"
    )

    pagamento_salvo = (
        st.session_state.get(
            "condicao_pagamento",
            "",
        )
        or "Não informado"
    )

    forma_salva = (
        st.session_state.get(
            "forma_pagamento",
            "",
        )
        or "Não informado"
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

    obs_comerciais_salvas = (
        st.session_state.get(
            "observacoes_comerciais",
            "",
        )
    )

    if obs_comerciais_salvas:

        texto_obs = escape(
            obs_comerciais_salvas
        ).replace(
            "\n",
            "<br>",
        )

        st.markdown(
            f"""
            <div class="notice-card">

                <strong>
                    Inclusões / Observações comerciais
                </strong>

                <br><br>

                {texto_obs}

            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # OBSERVAÇÕES TÉCNICAS
    # --------------------------------------------------------

    obs_tecnicas_salvas = (
        st.session_state.get(
            "observacoes_tecnicas",
            "",
        )
    )

    if obs_tecnicas_salvas:

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

        st.info(
            obs_tecnicas_salvas
        )

    # --------------------------------------------------------
    # ASSINATURA
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # EXPORTAÇÃO
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="section-header">
            <div class="section-title">
                📤 Exportação do orçamento
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📄 GERAR PDF",
            type="primary",
            width="stretch",
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
                    width="stretch",
                )

                st.success(
                    "PDF gerado com sucesso."
                )

    with col2:

        if st.button(
            "📊 EXPORTAR EXCEL",
            type="primary",
            width="stretch",
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
                    width="stretch",
                )

                st.success(
                    "Excel gerado com sucesso."
                )

    st.caption(
        "Calculadora Steel Framing • "
        "Quantitativos, orçamento, PDF e Excel."
    )
