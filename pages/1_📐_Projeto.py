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
       GERAL
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
        padding: 32px 34px;
        border-radius: 18px;
        border: 1px solid #dfe3e8;
        background:
            linear-gradient(
                135deg,
                #f8fafc 0%,
                #ffffff 55%,
                #f1f5f9 100%
            );
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.05);
        margin-bottom: 28px;
    }

    .hero-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #111827;
        line-height: 1.2;
    }

    .hero-subtitle {
        margin-top: 8px;
        font-size: 15px;
        color: #64748b;
        line-height: 1.5;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 18px;
        padding: 7px 13px;
        border-radius: 999px;
        background: #e8f5e9;
        color: #166534;
        border: 1px solid #bbf7d0;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }


    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-title {
        font-size: 20px;
        font-weight: 800;
        color: #111827;
        margin-top: 10px;
        margin-bottom: 4px;
    }

    .section-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 16px;
    }


    /* ======================================================
       CARDS
       ====================================================== */

    .info-card {
        padding: 18px 20px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.035);
        min-height: 125px;
    }

    .card-label {
        font-size: 11px;
        font-weight: 800;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }

    .card-value {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
    }


    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.035);
    }

    .metric-label {
        font-size: 11px;
        font-weight: 800;
        color: #64748b;
        letter-spacing: 0.6px;
    }

    .metric-value {
        margin-top: 5px;
        font-size: 25px;
        font-weight: 800;
        color: #111827;
    }


    /* ======================================================
       TOTAL
       ====================================================== */

    .total-box {
        padding: 28px;
        border-radius: 16px;
        border: 2px solid #15803d;
        background:
            linear-gradient(
                135deg,
                #f0fdf4,
                #ffffff
            );
        text-align: center;
        margin-top: 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 16px rgba(21, 128, 61, 0.08);
    }

    .total-label {
        font-size: 12px;
        font-weight: 800;
        color: #166534;
        letter-spacing: 0.8px;
    }

    .total-value {
        font-size: 34px;
        font-weight: 900;
        color: #14532d;
        margin-top: 5px;
    }


    /* ======================================================
       ASSINATURA
       ====================================================== */

    .assinatura {
        margin-top: 45px;
        padding-top: 20px;
        text-align: center;
    }

    .linha-assinatura {
        border-top: 1px solid #333333;
        width: 55%;
        margin: 0 auto 10px auto;
    }

    .assinatura-nome {
        font-size: 14px;
        font-weight: 800;
        color: #111827;
    }

    .assinatura-cargo {
        margin-top: 5px;
        font-size: 12px;
        color: #64748b;
    }


    /* ======================================================
       EXPORTAÇÃO
       ====================================================== */

    .export-card {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
        margin-bottom: 10px;
    }


    /* ======================================================
       TABELAS
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }


    /* ======================================================
       DIVISORES
       ====================================================== */

    hr {
        margin-top: 28px;
        margin-bottom: 28px;
        border-color: #e5e7eb;
    }


    /* ======================================================
       RESPONSIVIDADE
       ====================================================== */

    @media (max-width: 768px) {

        .hero {
            padding: 24px 20px;
        }

        .hero-title {
            font-size: 24px;
        }

        .total-value {
            font-size: 28px;
        }

        .linha-assinatura {
            width: 80%;
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
        valor = float(valor)
    except (TypeError, ValueError):
        valor = 0.0

    return (
        f"R$ {valor:,.2f}"
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
            "",
        )

    nome = nome.replace(
        " ",
        "_",
    )

    return nome or "Orcamento_Steel_Framing"


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


    # ========================================================
    # WORKBOOK
    # ========================================================

    wb = Workbook()

    ws_orcamento = wb.active
    ws_orcamento.title = "ORÇAMENTO"

    ws_materiais = wb.create_sheet(
        "MATERIAIS"
    )

    ws_mao_obra = wb.create_sheet(
        "MÃO DE OBRA"
    )

    ws_dados = wb.create_sheet(
        "DADOS"
    )


    # ========================================================
    # ESTILOS
    # ========================================================

    verde = "166534"
    verde_claro = "DCFCE7"
    cinza = "64748B"
    cinza_claro = "F1F5F9"
    branco = "FFFFFF"
    preto = "111827"
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

    moeda_format = (
        '"R$" #,##0.00'
    )


    def estilizar_titulo(ws, celula, texto):

        ws[celula] = texto

        ws[celula].font = Font(
            bold=True,
            size=18,
            color=branco,
        )

        ws[celula].fill = PatternFill(
            "solid",
            fgColor=verde,
        )

        ws[celula].alignment = Alignment(
            horizontal="left",
            vertical="center",
        )


    def estilizar_secao(ws, linha, texto):

        ws.cell(
            row=linha,
            column=1,
            value=texto,
        )

        ws.merge_cells(
            start_row=linha,
            start_column=1,
            end_row=linha,
            end_column=5,
        )

        celula = ws.cell(
            row=linha,
            column=1,
        )

        celula.font = Font(
            bold=True,
            size=12,
            color=branco,
        )

        celula.fill = PatternFill(
            "solid",
            fgColor=verde,
        )

        celula.alignment = Alignment(
            horizontal="left",
            vertical="center",
        )


    def ajustar_larguras(ws):

        for coluna in ws.columns:

            max_length = 0

            coluna_letra = (
                get_column_letter(
                    coluna[0].column
                )
            )

            for celula in coluna:

                try:
                    valor = str(
                        celula.value
                    )

                    if len(valor) > max_length:
                        max_length = len(valor)

                except Exception:
                    pass

            ws.column_dimensions[
                coluna_letra
            ].width = min(
                max(max_length + 3, 12),
                45,
            )


    # ========================================================
    # ABA ORÇAMENTO
    # ========================================================

    ws = ws_orcamento

    ws.merge_cells(
        "A1:E1"
    )

    estilizar_titulo(
        ws,
        "A1",
        "ORÇAMENTO — STEEL FRAMING",
    )

    ws["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws["A2"].font = Font(
        italic=True,
        color=cinza,
    )

    ws.merge_cells(
        "A2:E2"
    )


    linha = 4

    estilizar_secao(
        ws,
        linha,
        "IDENTIFICAÇÃO DO PROJETO",
    )

    linha += 1

    dados_identificacao = [
        (
            "Projeto",
            nome_projeto or "Não informado",
        ),
        (
            "Cliente",
            cliente or "Não informado",
        ),
        (
            "Local da obra",
            local_obra or "Não informado",
        ),
        (
            "Responsável",
            responsavel or "Não informado",
        ),
        (
            "Data",
            data_orcamento.strftime(
                "%d/%m/%Y"
            ),
        ),
    ]

    for rotulo, valor in dados_identificacao:

        ws.cell(
            linha,
            1,
            rotulo,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        ws.cell(
            linha,
            1,
        ).font = Font(
            bold=True
        )

        ws.cell(
            linha,
            1,
        ).fill = PatternFill(
            "solid",
            fgColor=cinza_claro,
        )

        ws.cell(
            linha,
            1,
        ).border = border

        ws.cell(
            linha,
            2,
        ).border = border

        linha += 1


    linha += 1

    estilizar_secao(
        ws,
        linha,
        "DIMENSÕES DO PROJETO",
    )

    linha += 1

    dimensoes = [
        (
            "Comprimento (m)",
            float(comprimento or 0),
        ),
        (
            "Altura (m)",
            float(altura or 0),
        ),
        (
            "Área (m²)",
            float(area or 0),
        ),
    ]

    for rotulo, valor in dimensoes:

        ws.cell(
            linha,
            1,
            rotulo,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        ws.cell(
            linha,
            1,
        ).font = Font(
            bold=True
        )

        ws.cell(
            linha,
            1,
        ).fill = PatternFill(
            "solid",
            fgColor=cinza_claro,
        )

        ws.cell(
            linha,
            2,
        ).number_format = "0.00"

        ws.cell(
            linha,
            1,
        ).border = border

        ws.cell(
            linha,
            2,
        ).border = border

        linha += 1


    linha += 1

    estilizar_secao(
        ws,
        linha,
        "RESUMO FINANCEIRO",
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
        subtotal_materiais,
    )

    linha += 1

    linha_massas = linha

    ws.cell(
        linha,
        1,
        "Massas e telas",
    )

    ws.cell(
        linha,
        2,
        massas_telas,
    )

    linha += 1

    linha_mao_obra = linha

    ws.cell(
        linha,
        1,
        "Mão de obra",
    )

    ws.cell(
        linha,
        2,
        custo_mao_de_obra,
    )

    linha += 1

    linha += 1

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
    ).font = Font(
        bold=True,
        size=13,
        color=verde,
    )

    ws.cell(
        linha,
        2,
    ).font = Font(
        bold=True,
        size=16,
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

    ws.cell(
        linha,
        1,
    ).border = border

    ws.cell(
        linha,
        2,
    ).border = border

    linha += 2

    estilizar_secao(
        ws,
        linha,
        "CONDIÇÕES COMERCIAIS",
    )

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

    for rotulo, valor in condicoes:

        ws.cell(
            linha,
            1,
            rotulo,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        ws.cell(
            linha,
            1,
        ).font = Font(
            bold=True
        )

        ws.cell(
            linha,
            1,
        ).fill = PatternFill(
            "solid",
            fgColor=cinza_claro,
        )

        ws.cell(
            linha,
            1,
        ).border = border

        ws.cell(
            linha,
            2,
        ).border = border

        linha += 1


    linha += 1

    estilizar_secao(
        ws,
        linha,
        "OBSERVAÇÕES COMERCIAIS",
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
        observacoes_comerciais
        or "Não informado",
    )

    ws.cell(
        linha,
        1,
    ).alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )

    linha += 2

    estilizar_secao(
        ws,
        linha,
        "OBSERVAÇÕES TÉCNICAS",
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
        observacoes_tecnicas
        or "Não informado",
    )

    ws.cell(
        linha,
        1,
    ).alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )


    # Formatação financeira

    for r in [
        linha_materiais,
        linha_massas,
        linha_mao_obra,
    ]:

        ws.cell(
            r,
            2,
        ).number_format = moeda_format


    # Total

    ws.cell(
        linha_mao_obra + 2,
        2,
    ).number_format = moeda_format


    ws.freeze_panes = "A4"

    ajustar_larguras(ws)


    # ========================================================
    # ABA MATERIAIS
    # ========================================================

    ws = ws_materiais

    ws.merge_cells(
        "A1:E1"
    )

    estilizar_titulo(
        ws,
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

    for coluna, titulo in enumerate(
        cabecalho,
        start=1,
    ):

        celula = ws.cell(
            3,
            coluna,
            titulo,
        )

        celula.font = Font(
            bold=True,
            color=branco,
        )

        celula.fill = PatternFill(
            "solid",
            fgColor=verde,
        )

        celula.border = border

        celula.alignment = Alignment(
            horizontal="center"
        )


    linha_material = 4

    for nome, material in materiais.items():

        quantidade = float(
            material.get(
                "quantidade",
                0,
            )
        )

        preco_unitario = float(
            material.get(
                "preco_unitario",
                0,
            )
        )

        custo = float(
            material.get(
                "custo",
                quantidade * preco_unitario,
            )
        )

        valores = [
            nome,
            material.get(
                "unidade",
                "",
            ),
            quantidade,
            preco_unitario,
            custo,
        ]

        for coluna, valor in enumerate(
            valores,
            start=1,
        ):

            celula = ws.cell(
                linha_material,
                coluna,
                valor,
            )

            celula.border = border

        ws.cell(
            linha_material,
            3,
        ).number_format = "0.00"

        ws.cell(
            linha_material,
            4,
        ).number_format = moeda_format

        ws.cell(
            linha_material,
            5,
        ).number_format = moeda_format

        linha_material += 1


    linha_total_material = linha_material

    ws.cell(
        linha_total_material,
        1,
        "TOTAL DE MATERIAIS",
    )

    ws.cell(
        linha_total_material,
        5,
        subtotal_materiais,
    )

    ws.cell(
        linha_total_material,
        1,
    ).font = Font(
        bold=True
    )

    ws.cell(
        linha_total_material,
        5,
    ).font = Font(
        bold=True
    )

    ws.cell(
        linha_total_material,
        1,
    ).fill = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

    ws.cell(
        linha_total_material,
        5,
    ).fill = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

    ws.cell(
        linha_total_material,
        5,
    ).number_format = moeda_format

    ws.freeze_panes = "A4"

    ajustar_larguras(ws)


    # ========================================================
    # ABA MÃO DE OBRA
    # ========================================================

    ws = ws_mao_obra

    ws.merge_cells(
        "A1:C1"
    )

    estilizar_titulo(
        ws,
        "A1",
        "MÃO DE OBRA",
    )

    dados_mao_obra = [
        (
            "Dias estimados",
            dias,
            "0.0",
        ),
        (
            "Valor da diária",
            diaria,
            moeda_format,
        ),
        (
            "Custo da mão de obra",
            custo_mao_de_obra,
            moeda_format,
        ),
    ]

    for linha_idx, (
        rotulo,
        valor,
        formato,
    ) in enumerate(
        dados_mao_obra,
        start=3,
    ):

        ws.cell(
            linha_idx,
            1,
            rotulo,
        )

        ws.cell(
            linha_idx,
            2,
            valor,
        )

        ws.cell(
            linha_idx,
            1,
        ).font = Font(
            bold=True
        )

        ws.cell(
            linha_idx,
            1,
        ).fill = PatternFill(
            "solid",
            fgColor=cinza_claro,
        )

        ws.cell(
            linha_idx,
            1,
        ).border = border

        ws.cell(
            linha_idx,
            2,
        ).border = border

        ws.cell(
            linha_idx,
            2,
        ).number_format = formato


    ajustar_larguras(ws)


    # ========================================================
    # ABA DADOS
    # ========================================================

    ws = ws_dados

    ws.merge_cells(
        "A1:B1"
    )

    estilizar_titulo(
        ws,
        "A1",
        "DADOS DO ORÇAMENTO",
    )

    dados = [
        (
            "Projeto",
            nome_projeto,
        ),
        (
            "Cliente",
            cliente,
        ),
        (
            "Local da obra",
            local_obra,
        ),
        (
            "Responsável",
            responsavel,
        ),
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
            "Prazo estimado de execução",
            prazo_execucao,
        ),
        (
            "Condição de pagamento",
            condicao_pagamento,
        ),
        (
            "Forma de pagamento",
            forma_pagamento,
        ),
        (
            "Observações comerciais",
            observacoes_comerciais,
        ),
        (
            "Observações técnicas",
            observacoes_tecnicas,
        ),
    ]

    for linha_idx, (
        rotulo,
        valor,
    ) in enumerate(
        dados,
        start=3,
    ):

        ws.cell(
            linha_idx,
            1,
            rotulo,
        )

        ws.cell(
            linha_idx,
            2,
            valor or "Não informado",
        )

        ws.cell(
            linha_idx,
            1,
        ).font = Font(
            bold=True
        )

        ws.cell(
            linha_idx,
            1,
        ).fill = PatternFill(
            "solid",
            fgColor=cinza_claro,
        )

        ws.cell(
            linha_idx,
            1,
        ).border = border

        ws.cell(
            linha_idx,
            2,
        ).border = border

        ws.cell(
            linha_idx,
            2,
        ).alignment = Alignment(
            wrap_text=True,
            vertical="top",
        )


    ajustar_larguras(ws)


    # ========================================================
    # AJUSTES GERAIS
    # ========================================================

    for worksheet in wb.worksheets:

        worksheet.sheet_view.showGridLines = False

        for row in worksheet.iter_rows():

            for cell in row:

                if cell.value is not None:

                    cell.alignment = Alignment(
                        vertical="center",
                        wrap_text=True,
                        horizontal=(
                            cell.alignment.horizontal
                            or "left"
                        ),
                    )


    # ========================================================
    # SALVAR
    # ========================================================

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


    # ========================================================
    # 2. RESUMO
    # ========================================================

    elementos.append(
        Paragraph(
            "2. RESUMO DO PROJETO",
            estilo_secao,
        )
    )

    comprimento = st.session_state.get(
        "comprimento",
        "",
    )

    altura = st.session_state.get(
        "altura",
        "",
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
        tabela_resumo
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
                    str(nome),
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


    # ========================================================
    # 4. FINANCEIRO
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
        Spacer(1, 8)
    )

    elementos.append(
        total_tabela
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
    # 6. CONDIÇÕES
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
                prazo_execucao or "Não informado",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                "<b>Condição de pagamento</b>",
                estilo_normal,
            ),
            Paragraph(
                condicao_pagamento or "Não informado",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                "<b>Forma de pagamento</b>",
                estilo_normal,
            ),
            Paragraph(
                forma_pagamento or "Não informado",
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


    # ========================================================
    # NOME DO RESPONSÁVEL
    # ========================================================

    nome_responsavel = (
        responsavel.strip()
        if responsavel
        else ""
    )

    if nome_responsavel:

        elementos.append(
            Paragraph(
                f"<b>{escape(nome_responsavel)}</b>",
                estilo_assinatura_nome,
            )
        )

        elementos.append(
            Paragraph(
                "Responsável pelo orçamento",
                estilo_assinatura_cargo,
            )
        )

    else:

        elementos.append(
            Paragraph(
                "<b>Responsável pelo orçamento</b>",
                estilo_assinatura_nome,
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
                "Orçamento Steel Framing "
                f"• Página {documento.page}"
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
    '<div class="section-title">📋 Identificação do projeto</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Informe os dados principais do orçamento.</div>',
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
    '<div class="section-title">📐 Dimensões do projeto</div>',
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


st.divider()


# ============================================================
# PREÇOS
# ============================================================

st.markdown(
    '<div class="section-title">💰 Preços dos materiais</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Altere os preços conforme fornecedor, região ou condição de compra.</div>',
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

st.markdown(
    '<div class="section-description">As quantidades são calculadas automaticamente, mas podem ser ajustadas.</div>',
    unsafe_allow_html=True,
)


if "quantidades" not in st.session_state:

    st.session_state["quantidades"] = {}


quantidades_atualizadas = {}


for nome, material in (
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


st.divider()


# ============================================================
# OBSERVAÇÕES TÉCNICAS
# ============================================================

st.markdown(
    '<div class="section-title">📝 Observações técnicas</div>',
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
    label_visibility="collapsed",
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
# DOCUMENTO
# ============================================================

if "projeto" in st.session_state:

    projeto = st.session_state[
        "projeto"
    ]

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
        '<div class="section-title">📋 Dados do orçamento</div>',
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


    data_salva = st.session_state.get(
        "data_orcamento",
        date.today(),
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
                    {st.session_state.get("validade_orcamento", 10)} dias
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    st.divider()


    # ========================================================
    # RESUMO
    # ========================================================

    st.markdown(
        '<div class="section-title">📐 Resumo do projeto</div>',
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


    st.divider()


    # ========================================================
    # FINANCEIRO
    # ========================================================

    st.markdown(
        '<div class="section-title">💰 Resumo financeiro</div>',
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
            <div class="metric-card">

                <div class="metric-label">
                    MATERIAIS
                </div>

                <div class="metric-value">
                    {formatar_moeda(subtotal_materiais)}
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
                    MASSAS E TELAS
                </div>

                <div class="metric-value">
                    {formatar_moeda(massas_telas)}
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
                    MÃO DE OBRA
                </div>

                <div class="metric-value">
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


    st.divider()


    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    st.markdown(
        '<div class="section-title">👷 Mão de obra</div>',
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


    st.divider()


    # ========================================================
    # CONDIÇÕES
    # ========================================================

    st.markdown(
        '<div class="section-title">💼 Condições comerciais</div>',
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


    st.markdown(
        f"""
        <div class="info-card">

            <div class="card-label">
                Validade
            </div>

            <div class="card-value">
                {st.session_state.get("validade_orcamento", 10)} dias
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


    observacoes_comerciais_salvas = (
        st.session_state.get(
            "observacoes_comerciais",
            "",
        )
    )


    if observacoes_comerciais_salvas:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Inclusões / Observações comerciais
                </div>

                <div class="card-value">
                    {escape(
                        observacoes_comerciais_salvas
                    ).replace(
                        chr(10),
                        "<br>"
                    )}
                </div>

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

        st.markdown(
            '<div class="section-title">📝 Observações técnicas</div>',
            unsafe_allow_html=True,
        )

        st.info(
            observacoes_tecnicas_salvas
        )


        st.divider()


    # ========================================================
    # ASSINATURA — CORRIGIDA
    # ========================================================

    responsavel_assinatura = (
        st.session_state.get(
            "responsavel",
            "",
        )
        or ""
    ).strip()


    if responsavel_assinatura:

        nome_assinatura = escape(
            responsavel_assinatura
        )

        bloco_assinatura = f"""
        <div class="assinatura">

            <div class="linha-assinatura"></div>

            <div class="assinatura-nome">
                {nome_assinatura}
            </div>

            <div class="assinatura-cargo">
                Responsável pelo orçamento
            </div>

        </div>
        """

    else:

        bloco_assinatura = """
        <div class="assinatura">

            <div class="linha-assinatura"></div>

            <div class="assinatura-nome">
                Responsável pelo orçamento
            </div>

        </div>
        """


    st.markdown(
        bloco_assinatura,
        unsafe_allow_html=True,
    )


    # ========================================================
    # EXPORTAÇÃO
    # ========================================================

    st.divider()


    st.markdown(
        '<div class="section-title">📤 Exportação do orçamento</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">Gere o documento profissional em PDF ou edite o orçamento no Excel.</div>',
        unsafe_allow_html=True,
    )


    col1, col2 = st.columns(2)


    # ========================================================
    # PDF
    # ========================================================

    with col1:

        st.markdown(
            """
            <div class="export-card">
                <strong>📄 PDF</strong><br>
                Documento pronto para apresentação,
                impressão ou envio ao cliente.
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


    # ========================================================
    # EXCEL
    # ========================================================

    with col2:

        st.markdown(
            """
            <div class="export-card">
                <strong>📊 Excel</strong><br>
                Planilha editável com materiais,
                mão de obra, dados e resumo financeiro.
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
        "Os valores do orçamento permanecem vinculados "
        "ao resultado validado pelo sistema."
    )
