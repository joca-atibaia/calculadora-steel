# ============================================================
# CALCULADORA STEEL FRAMING
# utils/pdf.py
#
# FASE 6D — GERADOR PROFISSIONAL DE PDF
# ============================================================

from io import BytesIO
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
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
    KeepTogether,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_moeda(valor):
    """
    Formata um número no padrão brasileiro:

    1234.56 -> R$ 1.234,56
    """

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
    """
    Converte valores para float com segurança.
    """

    try:
        if valor is None:
            return float(padrao)

        return float(valor)

    except (TypeError, ValueError):
        return float(padrao)


def texto(valor, padrao="Não informado"):
    """
    Converte valores para texto de forma segura.
    """

    if valor is None:
        return padrao

    valor = str(valor).strip()

    if not valor:
        return padrao

    return valor


def obter_valor(dicionario, chave, padrao=0):
    """
    Obtém um valor de dicionário sem provocar erro.
    """

    if not isinstance(dicionario, dict):
        return padrao

    valor = dicionario.get(chave, padrao)

    if valor is None:
        return padrao

    return valor


def paragraph_seguro(valor, estilo):
    """
    Cria Paragraph escapando HTML.
    """

    valor = texto(valor)

    valor = escape(valor).replace(
        "\n",
        "<br/>",
    )

    return Paragraph(
        valor,
        estilo,
    )


# ============================================================
# CORES
# ============================================================

AZUL = colors.HexColor("#263746")
AZUL_ESCURO = colors.HexColor("#17202A")

VERDE = colors.HexColor("#1F7A1F")
VERDE_CLARO = colors.HexColor("#EAF7EE")

CINZA_TITULO = colors.HexColor("#374151")
CINZA = colors.HexColor("#6B7280")
CINZA_CLARO = colors.HexColor("#F5F7FA")

BORDA = colors.HexColor("#D5DADE")
BORDA_ESCURA = colors.HexColor("#B8C0C7")

BRANCO = colors.white


# ============================================================
# ESTILOS
# ============================================================

def criar_estilos():

    styles = getSampleStyleSheet()

    titulo = ParagraphStyle(
        "TituloSteelFraming",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=19,
        leading=22,
        alignment=TA_CENTER,
        textColor=BRANCO,
        spaceAfter=5,
    )

    subtitulo = ParagraphStyle(
        "SubtituloSteelFraming",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#DCE3E8"),
        spaceAfter=0,
    )

    secao = ParagraphStyle(
        "SecaoSteelFraming",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=AZUL_ESCURO,
        spaceBefore=9,
        spaceAfter=7,
    )

    normal = ParagraphStyle(
        "NormalSteelFraming",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=11.5,
        textColor=CINZA_TITULO,
    )

    normal_pequeno = ParagraphStyle(
        "NormalPequenoSteelFraming",
        parent=normal,
        fontSize=7.7,
        leading=9.5,
    )

    rotulo = ParagraphStyle(
        "RotuloSteelFraming",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10,
        textColor=CINZA,
    )

    valor = ParagraphStyle(
        "ValorSteelFraming",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=CINZA_TITULO,
    )

    direita = ParagraphStyle(
        "DireitaSteelFraming",
        parent=normal,
        alignment=TA_RIGHT,
    )

    centro = ParagraphStyle(
        "CentroSteelFraming",
        parent=normal,
        alignment=TA_CENTER,
    )

    cabecalho_tabela = ParagraphStyle(
        "CabecalhoTabelaSteelFraming",
        parent=normal_pequeno,
        fontName="Helvetica-Bold",
        textColor=AZUL_ESCURO,
        alignment=TA_CENTER,
    )

    total_label = ParagraphStyle(
        "TotalLabelSteelFraming",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=VERDE,
    )

    total_valor = ParagraphStyle(
        "TotalValorSteelFraming",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=20,
        alignment=TA_RIGHT,
        textColor=VERDE,
    )

    assinatura = ParagraphStyle(
        "AssinaturaSteelFraming",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=AZUL_ESCURO,
    )

    assinatura_cargo = ParagraphStyle(
        "AssinaturaCargoSteelFraming",
        parent=normal,
        fontSize=7.8,
        leading=10,
        alignment=TA_CENTER,
        textColor=CINZA,
    )

    return {
        "titulo": titulo,
        "subtitulo": subtitulo,
        "secao": secao,
        "normal": normal,
        "pequeno": normal_pequeno,
        "rotulo": rotulo,
        "valor": valor,
        "direita": direita,
        "centro": centro,
        "cabecalho": cabecalho_tabela,
        "total_label": total_label,
        "total_valor": total_valor,
        "assinatura": assinatura,
        "assinatura_cargo": assinatura_cargo,
    }


# ============================================================
# CABEÇALHO
# ============================================================

def criar_cabecalho(styles):

    titulo = Table(
        [
            [
                Paragraph(
                    "📐 CALCULADORA STEEL FRAMING",
                    styles["titulo"],
                )
            ],
            [
                Paragraph(
                    "ORÇAMENTO PROFISSIONAL",
                    styles["subtitulo"],
                )
            ],
            [
                Paragraph(
                    "Quantitativo de materiais, custos e mão de obra",
                    styles["subtitulo"],
                )
            ],
        ],
        colWidths=[180 * mm],
    )

    titulo.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    AZUL,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, 0),
                    13,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    2,
                ),
                (
                    "TOPPADDING",
                    (0, 1),
                    (-1, -1),
                    2,
                ),
                (
                    "BOTTOMPADDING",
                    (0, -1),
                    (-1, -1),
                    13,
                ),
            ]
        )
    )

    return titulo


# ============================================================
# TABELA DE IDENTIFICAÇÃO
# ============================================================

def criar_tabela_identificacao(
    styles,
    nome_projeto,
    cliente,
    local_obra,
    responsavel,
    data_orcamento,
    validade,
):

    dados = [
        [
            [
                Paragraph(
                    "PROJETO",
                    styles["rotulo"],
                ),
                Paragraph(
                    escape(
                        texto(nome_projeto)
                    ),
                    styles["valor"],
                ),
            ],
            [
                Paragraph(
                    "CLIENTE",
                    styles["rotulo"],
                ),
                Paragraph(
                    escape(
                        texto(cliente)
                    ),
                    styles["valor"],
                ),
            ],
        ],
        [
            [
                Paragraph(
                    "LOCAL DA OBRA",
                    styles["rotulo"],
                ),
                Paragraph(
                    escape(
                        texto(local_obra)
                    ),
                    styles["valor"],
                ),
            ],
            [
                Paragraph(
                    "RESPONSÁVEL",
                    styles["rotulo"],
                ),
                Paragraph(
                    escape(
                        texto(responsavel)
                    ),
                    styles["valor"],
                ),
            ],
        ],
        [
            [
                Paragraph(
                    "DATA DO ORÇAMENTO",
                    styles["rotulo"],
                ),
                Paragraph(
                    escape(
                        data_orcamento
                    ),
                    styles["valor"],
                ),
            ],
            [
                Paragraph(
                    "VALIDADE",
                    styles["rotulo"],
                ),
                Paragraph(
                    f"{numero(validade, 10):.0f} dias",
                    styles["valor"],
                ),
            ],
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[
            90 * mm,
            90 * mm,
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDA_ESCURA,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    BORDA,
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
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
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

    return tabela


# ============================================================
# TABELA DE DIMENSÕES
# ============================================================

def criar_tabela_dimensoes(
    styles,
    comprimento,
    altura,
    area,
):

    dados = [
        [
            Paragraph(
                "Comprimento",
                styles["cabecalho"],
            ),
            Paragraph(
                "Altura",
                styles["cabecalho"],
            ),
            Paragraph(
                "Área",
                styles["cabecalho"],
            ),
        ],
        [
            Paragraph(
                f"{numero(comprimento):.2f} m",
                styles["centro"],
            ),
            Paragraph(
                f"{numero(altura):.2f} m",
                styles["centro"],
            ),
            Paragraph(
                f"{numero(area):.2f} m²",
                styles["centro"],
            ),
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[
            60 * mm,
            60 * mm,
            60 * mm,
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    CINZA_CLARO,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDA_ESCURA,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    BORDA,
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

    return tabela


# ============================================================
# QUANTITATIVO DE MATERIAIS
# ============================================================

def criar_tabela_materiais(
    styles,
    materiais,
):

    dados = [
        [
            Paragraph(
                "Material",
                styles["cabecalho"],
            ),
            Paragraph(
                "Un.",
                styles["cabecalho"],
            ),
            Paragraph(
                "Quantidade",
                styles["cabecalho"],
            ),
            Paragraph(
                "Preço unitário",
                styles["cabecalho"],
            ),
            Paragraph(
                "Total",
                styles["cabecalho"],
            ),
        ]
    ]

    total_materiais = 0.0

    if not isinstance(
        materiais,
        dict,
    ):
        materiais = {}

    for nome, material in materiais.items():

        if not isinstance(
            material,
            dict,
        ):
            material = {}

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

        custo = material.get(
            "custo",
            None,
        )

        if custo is None:
            custo = (
                quantidade * preco
            )

        custo = numero(custo)

        total_materiais += custo

        dados.append(
            [
                Paragraph(
                    escape(
                        str(nome)
                    ),
                    styles["pequeno"],
                ),
                Paragraph(
                    escape(
                        str(
                            material.get(
                                "unidade",
                                "",
                            )
                        )
                    ),
                    styles["centro"],
                ),
                Paragraph(
                    f"{quantidade:.2f}",
                    styles["direita"],
                ),
                Paragraph(
                    formatar_moeda(
                        preco
                    ),
                    styles["direita"],
                ),
                Paragraph(
                    formatar_moeda(
                        custo
                    ),
                    styles["direita"],
                ),
            ]
        )

    dados.append(
        [
            "",
            "",
            "",
            Paragraph(
                "<b>TOTAL MATERIAIS</b>",
                styles["direita"],
            ),
            Paragraph(
                f"<b>{formatar_moeda(total_materiais)}</b>",
                styles["direita"],
            ),
        ]
    )

    tabela = Table(
        dados,
        colWidths=[
            65 * mm,
            16 * mm,
            27 * mm,
            36 * mm,
            36 * mm,
        ],
        repeatRows=1,
    )

    ultima_linha = len(dados) - 1

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    CINZA_CLARO,
                ),
                (
                    "BACKGROUND",
                    (0, ultima_linha),
                    (-1, ultima_linha),
                    VERDE_CLARO,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDA_ESCURA,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    BORDA,
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

    return tabela


# ============================================================
# RESUMO FINANCEIRO
# ============================================================

def criar_tabela_financeiro(
    styles,
    subtotal_materiais,
    massas_telas,
    custo_mao_obra,
):

    dados = [
        [
            Paragraph(
                "Materiais",
                styles["normal"],
            ),
            Paragraph(
                formatar_moeda(
                    subtotal_materiais
                ),
                styles["direita"],
            ),
        ],
        [
            Paragraph(
                "Massas e telas",
                styles["normal"],
            ),
            Paragraph(
                formatar_moeda(
                    massas_telas
                ),
                styles["direita"],
            ),
        ],
        [
            Paragraph(
                "Mão de obra",
                styles["normal"],
            ),
            Paragraph(
                formatar_moeda(
                    custo_mao_obra
                ),
                styles["direita"],
            ),
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[
            115 * mm,
            65 * mm,
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDA_ESCURA,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    BORDA,
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
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
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

    return tabela


# ============================================================
# TOTAL GERAL
# ============================================================

def criar_total(
    styles,
    custo_geral,
):

    tabela = Table(
        [
            [
                Paragraph(
                    "VALOR TOTAL DO ORÇAMENTO",
                    styles["total_label"],
                ),
                Paragraph(
                    formatar_moeda(
                        custo_geral
                    ),
                    styles["total_valor"],
                ),
            ]
        ],
        colWidths=[
            100 * mm,
            80 * mm,
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1.2,
                    VERDE,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    VERDE_CLARO,
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
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
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

    return tabela


# ============================================================
# MÃO DE OBRA
# ============================================================

def criar_tabela_mao_de_obra(
    styles,
    dias,
    diaria,
    custo_mao_obra,
):

    dados = [
        [
            Paragraph(
                "Dias estimados",
                styles["normal"],
            ),
            Paragraph(
                f"{numero(dias):.1f}",
                styles["direita"],
            ),
        ],
        [
            Paragraph(
                "Valor da diária",
                styles["normal"],
            ),
            Paragraph(
                formatar_moeda(
                    diaria
                ),
                styles["direita"],
            ),
        ],
        [
            Paragraph(
                "Custo da mão de obra",
                styles["normal"],
            ),
            Paragraph(
                formatar_moeda(
                    custo_mao_obra
                ),
                styles["direita"],
            ),
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[
            115 * mm,
            65 * mm,
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDA_ESCURA,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    BORDA,
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
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
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

    return tabela


# ============================================================
# CONDIÇÕES COMERCIAIS
# ============================================================

def criar_tabela_condicoes(
    styles,
    validade,
    prazo,
    condicao,
    forma,
):

    dados = [
        [
            Paragraph(
                "Validade",
                styles["rotulo"],
            ),
            Paragraph(
                f"{numero(validade, 10):.0f} dias",
                styles["normal"],
            ),
        ],
        [
            Paragraph(
                "Prazo estimado de execução",
                styles["rotulo"],
            ),
            Paragraph(
                escape(
                    texto(prazo)
                ),
                styles["normal"],
            ),
        ],
        [
            Paragraph(
                "Condição de pagamento",
                styles["rotulo"],
            ),
            Paragraph(
                escape(
                    texto(condicao)
                ),
                styles["normal"],
            ),
        ],
        [
            Paragraph(
                "Forma de pagamento",
                styles["rotulo"],
            ),
            Paragraph(
                escape(
                    texto(forma)
                ),
                styles["normal"],
            ),
        ],
    ]

    tabela = Table(
        dados,
        colWidths=[
            55 * mm,
            125 * mm,
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDA_ESCURA,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    BORDA,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    CINZA_CLARO,
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

    return tabela


# ============================================================
# CAIXA DE OBSERVAÇÃO
# ============================================================

def criar_observacao(
    styles,
    titulo,
    conteudo,
):

    texto_observacao = escape(
        texto(
            conteudo,
            "",
        )
    ).replace(
        "\n",
        "<br/>",
    )

    tabela = Table(
        [
            [
                Paragraph(
                    f"<b>{escape(titulo)}</b><br/>{texto_observacao}",
                    styles["normal"],
                )
            ]
        ],
        colWidths=[
            180 * mm
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BORDA,
                ),
                (
                    "LINEBEFORE",
                    (0, 0),
                    (0, -1),
                    4,
                    AZUL,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.white,
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
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    return tabela


# ============================================================
# ASSINATURA
# ============================================================

def criar_assinatura(
    styles,
    responsavel,
):

    nome = texto(
        responsavel,
        "Responsável pelo orçamento",
    )

    tabela = Table(
        [
            [
                "",
            ]
        ],
        colWidths=[
            100 * mm
        ],
        rowHeights=[
            12 * mm
        ],
    )

    tabela.setStyle(
        TableStyle(
            [
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    AZUL_ESCURO,
                ),
            ]
        )
    )

    return [
        Spacer(
            1,
            18,
        ),
        tabela,
        Paragraph(
            escape(nome),
            styles["assinatura"],
        ),
        Paragraph(
            "Responsável pelo orçamento",
            styles["assinatura_cargo"],
        ),
    ]


# ============================================================
# RODAPÉ
# ============================================================

def desenhar_rodape(
    canvas,
    documento,
):

    canvas.saveState()

    largura, altura = A4

    canvas.setStrokeColor(
        BORDA
    )

    canvas.setLineWidth(
        0.4
    )

    canvas.line(
        15 * mm,
        12 * mm,
        largura - 15 * mm,
        12 * mm,
    )

    canvas.setFont(
        "Helvetica",
        7,
    )

    canvas.setFillColor(
        CINZA
    )

    canvas.drawString(
        15 * mm,
        7 * mm,
        "Calculadora Steel Framing",
    )

    canvas.drawRightString(
        largura - 15 * mm,
        7 * mm,
        f"Página {documento.page}",
    )

    canvas.restoreState()


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def gerar_pdf(
    projeto,
    dados_orcamento=None,
):
    """
    Gera o PDF profissional do orçamento.

    Parâmetros
    ----------
    projeto : dict
        Resultado produzido por calcular_projeto().

    dados_orcamento : dict, opcional
        Dados comerciais e de identificação.

    Retorno
    -------
    bytes
        Conteúdo do PDF.
    """

    if not isinstance(
        projeto,
        dict,
    ):
        projeto = {}

    if not isinstance(
        dados_orcamento,
        dict,
    ):
        dados_orcamento = {}

    styles = criar_estilos()

    # --------------------------------------------------------
    # DADOS DO ORÇAMENTO
    # --------------------------------------------------------

    nome_projeto = texto(
        dados_orcamento.get(
            "nome_projeto",
            "",
        )
    )

    cliente = texto(
        dados_orcamento.get(
            "cliente",
            "",
        )
    )

    local_obra = texto(
        dados_orcamento.get(
            "local_obra",
            "",
        )
    )

    responsavel = texto(
        dados_orcamento.get(
            "responsavel",
            "",
        )
    )

    data_orcamento = texto(
        dados_orcamento.get(
            "data_orcamento",
            "",
        )
    )

    validade = numero(
        dados_orcamento.get(
            "validade_orcamento",
            10,
        ),
        10,
    )

    prazo = texto(
        dados_orcamento.get(
            "prazo_execucao",
            "",
        )
    )

    condicao = texto(
        dados_orcamento.get(
            "condicao_pagamento",
            "",
        )
    )

    forma = texto(
        dados_orcamento.get(
            "forma_pagamento",
            "",
        )
    )

    obs_comerciais = dados_orcamento.get(
        "observacoes_comerciais",
        "",
    )

    obs_tecnicas = dados_orcamento.get(
        "observacoes_tecnicas",
        "",
    )

    # --------------------------------------------------------
    # RESULTADOS DO CÁLCULO
    # --------------------------------------------------------

    area = numero(
        obter_valor(
            projeto,
            "area",
            0,
        )
    )

    comprimento = numero(
        obter_valor(
            projeto,
            "comprimento",
            dados_orcamento.get(
                "comprimento",
                0,
            ),
        )
    )

    altura = numero(
        obter_valor(
            projeto,
            "altura",
            dados_orcamento.get(
                "altura",
                0,
            ),
        )
    )

    materiais = projeto.get(
        "materiais",
        {},
    )

    subtotal_materiais = numero(
        obter_valor(
            projeto,
            "subtotal_materiais",
            0,
        )
    )

    massas_telas = numero(
        obter_valor(
            projeto,
            "massas_telas",
            0,
        )
    )

    custo_geral = numero(
        obter_valor(
            projeto,
            "custo_geral",
            0,
        )
    )

    mao_de_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    if not isinstance(
        mao_de_obra,
        dict,
    ):
        mao_de_obra = {}

    dias = numero(
        mao_de_obra.get(
            "dias",
            0,
        )
    )

    diaria = numero(
        mao_de_obra.get(
            "diaria",
            0,
        )
    )

    custo_mao_obra = numero(
        mao_de_obra.get(
            "custo",
            0,
        )
    )

    # --------------------------------------------------------
    # DOCUMENTO
    # --------------------------------------------------------

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
        title=(
            f"Orçamento Steel Framing - "
            f"{nome_projeto}"
        ),
        author=responsavel,
        subject="Orçamento profissional Steel Framing",
    )

    elementos = []

    # --------------------------------------------------------
    # CABEÇALHO
    # --------------------------------------------------------

    elementos.append(
        criar_cabecalho(
            styles
        )
    )

    elementos.append(
        Spacer(
            1,
            8,
        )
    )

    # --------------------------------------------------------
    # 1 — IDENTIFICAÇÃO
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "1. DADOS DO ORÇAMENTO",
            styles["secao"],
        )
    )

    elementos.append(
        criar_tabela_identificacao(
            styles,
            nome_projeto,
            cliente,
            local_obra,
            responsavel,
            data_orcamento,
            validade,
        )
    )

    # --------------------------------------------------------
    # 2 — DIMENSÕES
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "2. RESUMO DO PROJETO",
            styles["secao"],
        )
    )

    elementos.append(
        criar_tabela_dimensoes(
            styles,
            comprimento,
            altura,
            area,
        )
    )

    # --------------------------------------------------------
    # 3 — MATERIAIS
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "3. QUANTITATIVO DE MATERIAIS",
            styles["secao"],
        )
    )

    elementos.append(
        criar_tabela_materiais(
            styles,
            materiais,
        )
    )

    # --------------------------------------------------------
    # 4 — RESUMO FINANCEIRO
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "4. RESUMO FINANCEIRO",
            styles["secao"],
        )
    )

    elementos.append(
        criar_tabela_financeiro(
            styles,
            subtotal_materiais,
            massas_telas,
            custo_mao_obra,
        )
    )

    elementos.append(
        Spacer(
            1,
            8,
        )
    )

    elementos.append(
        criar_total(
            styles,
            custo_geral,
        )
    )

    # --------------------------------------------------------
    # 5 — MÃO DE OBRA
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "5. MÃO DE OBRA",
            styles["secao"],
        )
    )

    elementos.append(
        criar_tabela_mao_de_obra(
            styles,
            dias,
            diaria,
            custo_mao_obra,
        )
    )

    # --------------------------------------------------------
    # 6 — CONDIÇÕES COMERCIAIS
    # --------------------------------------------------------

    elementos.append(
        Paragraph(
            "6. CONDIÇÕES COMERCIAIS",
            styles["secao"],
        )
    )

    elementos.append(
        criar_tabela_condicoes(
            styles,
            validade,
            prazo,
            condicao,
            forma,
        )
    )

    # --------------------------------------------------------
    # 7 — OBSERVAÇÕES COMERCIAIS
    # --------------------------------------------------------

    if str(
        obs_comerciais or ""
    ).strip():

        elementos.append(
            Paragraph(
                "7. OBSERVAÇÕES COMERCIAIS",
                styles["secao"],
            )
        )

        elementos.append(
            criar_observacao(
                styles,
                "Inclusões / observações comerciais",
                obs_comerciais,
            )
        )

    # --------------------------------------------------------
    # 8 — OBSERVAÇÕES TÉCNICAS
    # --------------------------------------------------------

    if str(
        obs_tecnicas or ""
    ).strip():

        elementos.append(
            Paragraph(
                "8. OBSERVAÇÕES TÉCNICAS",
                styles["secao"],
            )
        )

        elementos.append(
            criar_observacao(
                styles,
                "Observações técnicas",
                obs_tecnicas,
            )
        )

    # --------------------------------------------------------
    # ASSINATURA
    # --------------------------------------------------------

    elementos.extend(
        criar_assinatura(
            styles,
            responsavel,
        )
    )

    # --------------------------------------------------------
    # GERA PDF
    # --------------------------------------------------------

    doc.build(
        elementos,
        onFirstPage=desenhar_rodape,
        onLaterPages=desenhar_rodape,
    )

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# FIM DO ARQUIVO
# ============================================================
