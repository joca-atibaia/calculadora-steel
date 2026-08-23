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
# CSS — VISUAL PROFISSIONAL
# ============================================================

st.markdown(
    """
    <style>

    .orcamento-header {
        padding: 20px 24px;
        border-radius: 12px;
        border: 1px solid #d9d9d9;
        background: linear-gradient(
            135deg,
            #f8f9fa 0%,
            #ffffff 100%
        );
        margin-bottom: 18px;
    }

    .orcamento-header h1 {
        margin: 0 0 4px 0;
    }

    .orcamento-header p {
        margin: 0;
        color: #666;
    }

    .total-box {
        padding: 22px;
        border-radius: 12px;
        border: 2px solid #1f7a1f;
        background-color: #f3fff3;
        text-align: center;
        margin-top: 18px;
        margin-bottom: 18px;
    }

    .total-label {
        font-size: 15px;
        font-weight: 600;
        color: #555;
    }

    .total-value {
        font-size: 30px;
        font-weight: 800;
        margin-top: 5px;
    }

    .info-box {
        padding: 15px 18px;
        border-radius: 8px;
        border: 1px solid #dddddd;
        background-color: #fafafa;
        margin-bottom: 10px;
    }

    .assinatura {
        margin-top: 45px;
        padding-top: 10px;
        text-align: center;
    }

    .linha-assinatura {
        border-top: 1px solid #333;
        width: 70%;
        margin: 0 auto 8px auto;
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


def texto_seguro(valor, padrao="Não informado"):
    if valor is None:
        return padrao

    valor = str(valor).strip()

    return valor if valor else padrao


# ============================================================
# GERAÇÃO DO PDF
# FASE 6A.1 — ACABAMENTO
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
            PageBreak,
            KeepTogether,
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

    # ========================================================
    # VALORES DO PROJETO
    # ========================================================

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

    # ========================================================
    # DOCUMENTO
    # ========================================================

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=13 * mm,
        leftMargin=13 * mm,
        topMargin=13 * mm,
        bottomMargin=17 * mm,
        title="Orçamento Steel Framing",
        author=responsavel or "Calculadora Steel Framing",
    )

    styles = getSampleStyleSheet()

    # ========================================================
    # ESTILOS
    # ========================================================

    estilo_titulo = ParagraphStyle(
        "TituloOrcamento",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=21,
        alignment=TA_CENTER,
        spaceAfter=3,
    )

    estilo_subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=8,
    )

    estilo_secao = ParagraphStyle(
        "Secao",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        spaceBefore=5,
        spaceAfter=5,
    )

    estilo_normal = ParagraphStyle(
        "NormalOrcamento",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=10.5,
    )

    estilo_pequeno = ParagraphStyle(
        "Pequeno",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
    )

    estilo_direita = ParagraphStyle(
        "Direita",
        parent=estilo_normal,
        alignment=TA_RIGHT,
    )

    estilo_total = ParagraphStyle(
        "Total",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=19,
        alignment=TA_RIGHT,
    )

    estilo_assinatura = ParagraphStyle(
        "Assinatura",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
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
    # 1. DADOS DO ORÇAMENTO
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
                f"<b>Projeto:</b><br/>{escape(texto_seguro(nome_projeto))}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Cliente:</b><br/>{escape(texto_seguro(cliente))}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra:</b><br/>{escape(texto_seguro(local_obra))}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Responsável:</b><br/>{escape(texto_seguro(responsavel))}",
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
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
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

    elementos.append(tabela_dados)
    elementos.append(Spacer(1, 5))

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
                f"{float(comprimento):.2f} m"
                if comprimento != ""
                else "Não informado",
                estilo_direita,
            ),
        ],
        [
            Paragraph(
                "<b>Altura</b>",
                estilo_normal,
            ),
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
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
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

    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 5))

    # ========================================================
    # 3. QUANTITATIVO DE MATERIAIS
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
                    escape(
                        str(
                            material.get(
                                "unidade",
                                "",
                            )
                        )
                    ),
                    estilo_pequeno,
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
            64 * mm,
            14 * mm,
            27 * mm,
            35 * mm,
            36 * mm,
        ],
        repeatRows=1,
    )

    tabela_material_pdf.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#e9e9e9"),
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
                    4,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
            ]
        )
    )

    elementos.append(
        tabela_material_pdf
    )

    elementos.append(Spacer(1, 5))

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
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
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

    elementos.append(
        tabela_financeiro
    )

    elementos.append(Spacer(1, 5))

    # ========================================================
    # VALOR TOTAL
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
                    9,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ]
        )
    )

    elementos.append(total_tabela)

    # ========================================================
    # QUEBRA INTENCIONAL DE PÁGINA
    #
    # FASE 6A.1:
    # Página 1 termina após o resumo financeiro.
    # Página 2 começa com mão de obra.
    # ========================================================

    elementos.append(
        PageBreak()
    )

    # ========================================================
    # CABEÇALHO DA PÁGINA 2
    # ========================================================

    elementos.append(
        Paragraph(
            "ORÇAMENTO — STEEL FRAMING",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Continuação do orçamento",
            estilo_subtitulo,
        )
    )

    # ========================================================
    # 5. MÃO DE OBRA
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
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
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

    elementos.append(Spacer(1, 8))

    # ========================================================
    # 6. CONDIÇÕES COMERCIAIS
    # ========================================================

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
                    texto_seguro(
                        prazo_execucao
                    )
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
                    texto_seguro(
                        condicao_pagamento
                    )
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
                    texto_seguro(
                        forma_pagamento
                    )
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
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
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
    # 7. OBSERVAÇÕES COMERCIAIS
    # ========================================================

    if observacoes_comerciais:

        elementos.append(
            Spacer(1, 8)
        )

        elementos.append(
            Paragraph(
                "7. OBSERVAÇÕES COMERCIAIS",
                estilo_secao,
            )
        )

        texto_comercial = escape(
            observacoes_comerciais
        ).replace(
            "\n",
            "<br/>",
        )

        elementos.append(
            Paragraph(
                texto_comercial,
                estilo_normal,
            )
        )

    # ========================================================
    # 8. OBSERVAÇÕES TÉCNICAS
    # ========================================================

    if observacoes_tecnicas:

        elementos.append(
            Spacer(1, 8)
        )

        elementos.append(
            Paragraph(
                "8. OBSERVAÇÕES TÉCNICAS",
                estilo_secao,
            )
        )

        texto_tecnico = escape(
            observacoes_tecnicas
        ).replace(
            "\n",
            "<br/>",
        )

        elementos.append(
            Paragraph(
                texto_tecnico,
                estilo_normal,
            )
        )

    # ========================================================
    # ASSINATURA — CORRIGIDA
    #
    # Apenas UMA linha.
    # Apenas UMA identificação do responsável.
    # ========================================================

    elementos.append(
        Spacer(1, 35)
    )

    assinatura_nome = (
        responsavel.strip()
        if responsavel
        else "Responsável pelo orçamento"
    )

    assinatura = Table(
        [
            [
                Paragraph(
                    "________________________________________",
                    estilo_assinatura,
                )
            ],
            [
                Paragraph(
                    escape(assinatura_nome),
                    estilo_assinatura,
                )
            ],
            [
                Paragraph(
                    "Responsável pelo orçamento",
                    estilo_pequeno,
                )
            ],
        ],
        colWidths=[
            100 * mm,
        ],
    )

    assinatura.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
            ]
        )
    )

    elementos.append(
        assinatura
    )

    # ========================================================
    # RODAPÉ
    # ========================================================

    def adicionar_rodape(canvas, documento):

        canvas.saveState()

        largura, altura = A4

        canvas.setStrokeColor(
            colors.HexColor("#dddddd")
        )

        canvas.setLineWidth(
            0.4
        )

        canvas.line(
            13 * mm,
            12 * mm,
            largura - 13 * mm,
            12 * mm,
        )

        canvas.setFont(
            "Helvetica",
            7,
        )

        canvas.setFillColor(
            colors.grey
        )

        canvas.drawCentredString(
            largura / 2,
            7 * mm,
            f"Orçamento Steel Framing • Página {documento.page}",
        )

        canvas.restoreState()

    # ========================================================
    # GERAR PDF
    # ========================================================

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
    <div class="orcamento-header">
        <h1>📐 CALCULADORA STEEL FRAMING</h1>
        <p>
            Sistema profissional para orçamento de materiais
            e mão de obra
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# IDENTIFICAÇÃO DO PROJETO
# ============================================================

st.subheader("📋 Identificação do projeto")

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

st.subheader("💼 Condições comerciais")

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

st.subheader("📐 Dimensões do projeto")

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

    st.metric(
        "Área do projeto",
        f"{area_preview:.2f} m²",
    )

st.session_state["comprimento"] = comprimento
st.session_state["altura"] = altura

st.divider()


# ============================================================
# PREÇOS
# ============================================================

if "precos" not in st.session_state:

    st.session_state["precos"] = (
        PRECOS_BASE.copy()
    )

st.subheader("💰 Preços dos materiais")

st.caption(
    "Altere os preços conforme fornecedor, "
    "região ou condição de compra."
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

    precos_atualizados[nome] = preco_atual

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

st.subheader("📦 Quantidades dos materiais")

st.caption(
    "As quantidades são calculadas automaticamente. "
    "Você pode ajustar qualquer quantidade."
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

st.divider()


# ============================================================
# CALCULAR ORÇAMENTO
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
# DOCUMENTO DO ORÇAMENTO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state["projeto"]

    st.divider()

    st.header("📄 ORÇAMENTO PROFISSIONAL")

    # ========================================================
    # CABEÇALHO
    # ========================================================

    st.markdown(
        """
        <div class="orcamento-header">
            <h1>ORÇAMENTO — STEEL FRAMING</h1>
            <p>
                Quantitativo de materiais e mão de obra
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # DADOS
    # ========================================================

    st.subheader("📋 Dados do orçamento")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            **Projeto:**  
            {st.session_state.get("nome_projeto", "")}

            **Cliente:**  
            {st.session_state.get("cliente", "")}

            **Local da obra:**  
            {st.session_state.get("local_obra", "")}
            """
        )

    with col2:

        data_salva = st.session_state.get(
            "data_orcamento",
            date.today(),
        )

        st.markdown(
            f"""
            **Responsável:**  
            {st.session_state.get("responsavel", "")}

            **Data:**  
            {data_salva.strftime("%d/%m/%Y")}

            **Validade:**  
            {st.session_state.get("validade_orcamento", 10)} dias
            """
        )

    st.divider()

    # ========================================================
    # RESUMO
    # ========================================================

    st.subheader("📐 Resumo do projeto")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Área",
            f'{projeto["area"]:.2f} m²',
        )

    with col2:

        st.metric(
            "Comprimento",
            f"{comprimento:.2f} m",
        )

    with col3:

        st.metric(
            "Altura",
            f"{altura:.2f} m",
        )

    st.divider()

    # ========================================================
    # TABELA DE MATERIAIS
    # ========================================================

    st.subheader(
        "📦 Quantitativo de materiais"
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

    st.divider()

    # ========================================================
    # FINANCEIRO
    # ========================================================

    st.subheader(
        "💰 Resumo financeiro"
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

    st.subheader("👷 Mão de obra")

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

    st.subheader(
        "💼 Condições comerciais"
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

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            **Validade do orçamento:**  
            {validade_salva} dias

            **Prazo estimado de execução:**  
            {prazo_salvo if prazo_salvo else "Não informado"}
            """
        )

    with col2:

        st.markdown(
            f"""
            **Condição de pagamento:**  
            {pagamento_salvo if pagamento_salvo else "Não informado"}

            **Forma de pagamento:**  
            {forma_pagamento_salva if forma_pagamento_salva else "Não informado"}
            """
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
            <div class="info-box">
                <strong>
                    Inclusões / Observações comerciais
                </strong>
                <br><br>
                {escape(observacoes_comerciais_salvas)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

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

        st.subheader(
            "📝 Observações técnicas"
        )

        st.info(
            observacoes_tecnicas_salvas
        )

        st.divider()

    # ========================================================
    # VALOR FINAL
    # ========================================================

    st.subheader(
        "💵 Valor final"
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
    # ASSINATURA — ÚNICA
    # ========================================================

    responsavel_tela = (
        st.session_state.get(
            "responsavel",
            "",
        ).strip()
    )

    if not responsavel_tela:
        responsavel_tela = (
            "Responsável pelo orçamento"
        )

    st.markdown(
        f"""
        <div class="assinatura">

            <div class="linha-assinatura"></div>

            <strong>
                {escape(responsavel_tela)}
            </strong>

            <div style="margin-top: 5px;">
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

    st.subheader(
        "📤 Exportação do orçamento"
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
                    st.session_state.get(
                        "nome_projeto",
                        "",
                    )
                    .strip()
                    .replace(" ", "_")
                )

                if not nome_arquivo:

                    nome_arquivo = (
                        "Orcamento_Steel_Framing"
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
    # EXCEL — PRÓXIMA FASE
    # ========================================================

    with col2:

        st.button(
            "📊 EXPORTAR EXCEL",
            use_container_width=True,
            disabled=True,
            help=(
                "Será implementado na Fase 6B."
            ),
        )

    st.caption(
        "PDF disponível nesta fase. "
        "Exportação Excel será implementada na próxima etapa."
    )
