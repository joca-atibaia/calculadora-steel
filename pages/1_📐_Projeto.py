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
# CSS — APARÊNCIA 6C
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       BASE
       ====================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        padding: 30px 32px;
        border-radius: 18px;
        margin-bottom: 28px;
        border: 1px solid rgba(0, 0, 0, 0.08);
        background: linear-gradient(
            135deg,
            #f8fafc 0%,
            #ffffff 55%,
            #eef6ff 100%
        );
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
    }

    .hero-title {
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 6px;
        color: #111827;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #64748b;
        margin-bottom: 16px;
        line-height: 1.5;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: #e2e8f0;
        color: #334155;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }


    /* ======================================================
       SEÇÕES
       ====================================================== */

    .section-card {
        padding: 20px 22px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 19px;
        font-weight: 750;
        color: #111827;
        margin-bottom: 4px;
    }

    .section-subtitle {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 16px;
    }


    /* ======================================================
       CARDS DE INFORMAÇÃO
       ====================================================== */

    .info-card {
        padding: 18px 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background: #fafafa;
        min-height: 110px;
    }

    .card-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6b7280;
        margin-bottom: 4px;
    }

    .card-value {
        font-size: 16px;
        font-weight: 650;
        color: #111827;
    }


    /* ======================================================
       MÉTRICAS
       ====================================================== */

    .metric-card {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
    }

    .metric-label {
        font-size: 11px;
        font-weight: 750;
        color: #6b7280;
        letter-spacing: 0.7px;
        margin-bottom: 7px;
    }

    .metric-value {
        font-size: 25px;
        font-weight: 800;
        color: #111827;
    }


    /* ======================================================
       TOTAL
       ====================================================== */

    .total-box {
        padding: 25px;
        border-radius: 16px;
        border: 2px solid #15803d;
        background: linear-gradient(
            135deg,
            #f0fdf4,
            #ffffff
        );
        text-align: center;
        margin-top: 18px;
        margin-bottom: 20px;
        box-shadow: 0 5px 18px rgba(21, 128, 61, 0.08);
    }

    .total-label {
        font-size: 13px;
        font-weight: 750;
        color: #166534;
        letter-spacing: 0.8px;
    }

    .total-value {
        font-size: 34px;
        font-weight: 850;
        color: #14532d;
        margin-top: 5px;
    }


    /* ======================================================
       ASSINATURA
       ====================================================== */

    .assinatura {
        margin-top: 50px;
        padding: 20px;
        text-align: center;
    }

    .linha-assinatura {
        border-top: 1px solid #333333;
        width: 65%;
        margin: 0 auto 10px auto;
    }


    /* ======================================================
       AVISOS
       ====================================================== */

    .info-box {
        padding: 16px 18px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        background: #f8fafc;
        margin-top: 12px;
    }


    /* ======================================================
       TABELAS
       ====================================================== */

    .table-title {
        font-size: 16px;
        font-weight: 750;
        color: #111827;
        margin-bottom: 10px;
    }


    /* ======================================================
       RODAPÉ
       ====================================================== */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 11px;
        margin-top: 35px;
        padding-top: 18px;
        border-top: 1px solid #e5e7eb;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def formatar_moeda(valor):
    """
    Formata número para moeda brasileira.
    """
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
    """
    Obtém valor de um dicionário com segurança.
    """
    if not isinstance(dicionario, dict):
        return padrao

    valor = dicionario.get(chave, padrao)

    if valor is None:
        return padrao

    return valor


def nome_arquivo_orcamento():
    """
    Gera nome seguro para os arquivos exportados.
    """
    nome = st.session_state.get(
        "nome_projeto",
        "",
    )

    nome = str(nome).strip()

    if not nome:
        return "Orcamento_Steel_Framing"

    caracteres_invalidos = (
        "\\",
        "/",
        ":",
        "*",
        "?",
        '"',
        "<",
        ">",
        "|",
    )

    for caractere in caracteres_invalidos:
        nome = nome.replace(
            caractere,
            "_",
        )

    nome = nome.replace(
        " ",
        "_",
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

    preenchimento_titulo = PatternFill(
        fill_type="solid",
        fgColor="1F2937",
    )

    preenchimento_secao = PatternFill(
        fill_type="solid",
        fgColor="E5E7EB",
    )

    preenchimento_total = PatternFill(
        fill_type="solid",
        fgColor="DCFCE7",
    )

    fonte_titulo = Font(
        bold=True,
        size=18,
        color="FFFFFF",
    )

    fonte_secao = Font(
        bold=True,
        size=12,
        color="111827",
    )

    fonte_cabecalho = Font(
        bold=True,
        color="FFFFFF",
    )

    fonte_total = Font(
        bold=True,
        size=14,
        color="14532D",
    )

    borda_fina = Border(
        left=Side(style="thin", color="D1D5DB"),
        right=Side(style="thin", color="D1D5DB"),
        top=Side(style="thin", color="D1D5DB"),
        bottom=Side(style="thin", color="D1D5DB"),
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

    formato_moeda = 'R$ #,##0.00'

    # ========================================================
    # ABA ORÇAMENTO
    # ========================================================

    ws = ws_orcamento

    ws.merge_cells(
        "A1:E1"
    )

    ws["A1"] = (
        "ORÇAMENTO — STEEL FRAMING"
    )

    ws["A1"].fill = preenchimento_titulo
    ws["A1"].font = fonte_titulo
    ws["A1"].alignment = alinhamento_centro

    ws.merge_cells(
        "A2:E2"
    )

    ws["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws["A2"].alignment = alinhamento_centro

    # --------------------------------------------------------
    # IDENTIFICAÇÃO
    # --------------------------------------------------------

    ws.merge_cells(
        "A4:E4"
    )

    ws["A4"] = (
        "IDENTIFICAÇÃO DO PROJETO"
    )

    ws["A4"].fill = preenchimento_secao
    ws["A4"].font = fonte_secao

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

        ws.cell(
            linha,
            1,
            rotulo,
        )

        ws.cell(
            linha,
            1,
        ).font = Font(bold=True)

        ws.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=5,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        linha += 1

    # --------------------------------------------------------
    # DIMENSÕES
    # --------------------------------------------------------

    ws.merge_cells(
        f"A{linha + 1}:E{linha + 1}"
    )

    ws.cell(
        linha + 1,
        1,
        "DIMENSÕES DO PROJETO",
    )

    ws.cell(
        linha + 1,
        1,
    ).fill = preenchimento_secao

    ws.cell(
        linha + 1,
        1,
    ).font = fonte_secao

    linha += 2

    dimensoes = [
        (
            "Comprimento (m)",
            float(comprimento)
            if comprimento != ""
            else 0,
        ),
        (
            "Altura (m)",
            float(altura)
            if altura != ""
            else 0,
        ),
        (
            "Área (m²)",
            float(area),
        ),
    ]

    for rotulo, valor in dimensoes:

        ws.cell(
            linha,
            1,
            rotulo,
        ).font = Font(bold=True)

        ws.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=5,
        )

        ws.cell(
            linha,
            2,
            valor,
        )

        ws.cell(
            linha,
            2,
        ).number_format = "0.00"

        linha += 1

    # --------------------------------------------------------
    # RESUMO FINANCEIRO
    # --------------------------------------------------------

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
    ).fill = preenchimento_secao

    ws.cell(
        linha,
        1,
    ).font = fonte_secao

    linha += 1

    resumo_inicio = linha

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

    ws.cell(
        linha,
        2,
    ).number_format = formato_moeda

    linha += 1

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

    ws.cell(
        linha,
        2,
    ).number_format = formato_moeda

    linha += 1

    ws.cell(
        linha,
        1,
        "Mão de obra",
    )

    # Mantém o valor validado vindo do cálculo.
    ws.cell(
        linha,
        2,
        custo_mao_de_obra,
    )

    ws.cell(
        linha,
        2,
    ).number_format = formato_moeda

    linha += 2

    ws.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
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

    ws.cell(
        linha,
        5,
        custo_geral,
    )

    ws.cell(
        linha,
        5,
    ).number_format = formato_moeda

    ws.cell(
        linha,
        5,
    ).font = fonte_total

    ws.cell(
        linha,
        5,
    ).fill = preenchimento_total

    # --------------------------------------------------------
    # LARGURAS
    # --------------------------------------------------------

    larguras = {
        "A": 34,
        "B": 20,
        "C": 20,
        "D": 20,
        "E": 22,
    }

    for coluna, largura in larguras.items():

        ws.column_dimensions[
            coluna
        ].width = largura

    # --------------------------------------------------------
    # BORDAS
    # --------------------------------------------------------

    for row in ws.iter_rows():

        for cell in row:

            if cell.value is not None:

                cell.border = borda_fina

                if cell.column == 1:

                    cell.alignment = alinhamento_esquerda

    # ========================================================
    # ABA MATERIAIS
    # ========================================================

    ws = ws_materiais

    ws.merge_cells(
        "A1:E1"
    )

    ws["A1"] = (
        "QUANTITATIVO DE MATERIAIS"
    )

    ws["A1"].fill = preenchimento_titulo
    ws["A1"].font = fonte_titulo
    ws["A1"].alignment = alinhamento_centro

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

        cell = ws.cell(
            3,
            coluna,
            valor,
        )

        cell.fill = preenchimento_titulo
        cell.font = fonte_cabecalho
        cell.alignment = alinhamento_centro
        cell.border = borda_fina

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

        ws.cell(
            linha_material,
            1,
            str(nome),
        )

        ws.cell(
            linha_material,
            2,
            str(
                material.get(
                    "unidade",
                    "",
                )
            ),
        )

        ws.cell(
            linha_material,
            3,
            quantidade,
        )

        ws.cell(
            linha_material,
            4,
            preco_unitario,
        )

        ws.cell(
            linha_material,
            5,
            custo,
        )

        ws.cell(
            linha_material,
            3,
        ).number_format = "0.00"

        ws.cell(
            linha_material,
            4,
        ).number_format = formato_moeda

        ws.cell(
            linha_material,
            5,
        ).number_format = formato_moeda

        for coluna in range(1, 6):

            ws.cell(
                linha_material,
                coluna,
            ).border = borda_fina

        linha_material += 1

    # Total dos materiais
    ws.cell(
        linha_material + 1,
        4,
        "TOTAL MATERIAIS",
    )

    ws.cell(
        linha_material + 1,
        4,
    ).font = Font(bold=True)

    ws.cell(
        linha_material + 1,
        5,
        subtotal_materiais,
    )

    ws.cell(
        linha_material + 1,
        5,
    ).number_format = formato_moeda

    ws.cell(
        linha_material + 1,
        5,
    ).font = Font(bold=True)

    # Massas e telas
    ws.cell(
        linha_material + 2,
        4,
        "MASSAS E TELAS",
    )

    ws.cell(
        linha_material + 2,
        4,
    ).font = Font(bold=True)

    ws.cell(
        linha_material + 2,
        5,
        massas_telas,
    )

    ws.cell(
        linha_material + 2,
        5,
    ).number_format = formato_moeda

    # Larguras
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 18
    ws.column_dimensions["E"].width = 20

    # ========================================================
    # ABA MÃO DE OBRA
    # ========================================================

    ws = ws_mao_obra

    ws.merge_cells(
        "A1:C1"
    )

    ws["A1"] = (
        "MÃO DE OBRA"
    )

    ws["A1"].fill = preenchimento_titulo
    ws["A1"].font = fonte_titulo
    ws["A1"].alignment = alinhamento_centro

    dados_mao_obra = [
        (
            "Dias estimados",
            dias,
            "dias",
        ),
        (
            "Valor da diária",
            diaria,
            "R$",
        ),
        (
            "Custo da mão de obra",
            custo_mao_de_obra,
            "R$",
        ),
    ]

    ws["A3"] = "Descrição"
    ws["B3"] = "Valor"
    ws["C3"] = "Unidade"

    for coluna in range(1, 4):

        ws.cell(
            3,
            coluna,
        ).fill = preenchimento_titulo

        ws.cell(
            3,
            coluna,
        ).font = fonte_cabecalho

        ws.cell(
            3,
            coluna,
        ).alignment = alinhamento_centro

        ws.cell(
            3,
            coluna,
        ).border = borda_fina

    linha_mao = 4

    for descricao, valor, unidade in dados_mao_obra:

        ws.cell(
            linha_mao,
            1,
            descricao,
        )

        ws.cell(
            linha_mao,
            2,
            float(valor),
        )

        ws.cell(
            linha_mao,
            3,
            unidade,
        )

        if unidade == "R$":

            ws.cell(
                linha_mao,
                2,
            ).number_format = formato_moeda

        else:

            ws.cell(
                linha_mao,
                2,
            ).number_format = "0.00"

        for coluna in range(1, 4):

            ws.cell(
                linha_mao,
                coluna,
            ).border = borda_fina

        linha_mao += 1

    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 14

    # ========================================================
    # ABA DADOS
    # ========================================================

    ws = ws_dados

    ws.merge_cells(
        "A1:B1"
    )

    ws["A1"] = (
        "DADOS DO ORÇAMENTO"
    )

    ws["A1"].fill = preenchimento_titulo
    ws["A1"].font = fonte_titulo
    ws["A1"].alignment = alinhamento_centro

    dados = [
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
            observacoes_comerciais
            or "Não informado",
        ),
        (
            "Observações técnicas",
            observacoes_tecnicas
            or "Não informado",
        ),
    ]

    linha_dados = 3

    for rotulo, valor in dados:

        ws.cell(
            linha_dados,
            1,
            rotulo,
        )

        ws.cell(
            linha_dados,
            1,
        ).font = Font(bold=True)

        ws.cell(
            linha_dados,
            2,
            valor,
        )

        ws.cell(
            linha_dados,
            1,
        ).border = borda_fina

        ws.cell(
            linha_dados,
            2,
        ).border = borda_fina

        ws.cell(
            linha_dados,
            2,
        ).alignment = Alignment(
            vertical="top",
            wrap_text=True,
        )

        linha_dados += 1

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 85

    # ========================================================
    # CONGELAR CABEÇALHOS
    # ========================================================

    ws_materiais.freeze_panes = "A4"
    ws_mao_obra.freeze_panes = "A4"

    # ========================================================
    # SALVAR EM MEMÓRIA
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
            ]
        )
    )

    elementos.append(
        tabela_financeiro
    )

    elementos.append(
        Spacer(1, 10)
    )

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
                    formatar_moeda(
                        diaria
                    ),
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
            ]
        )
    )

    elementos.append(
        tabela_condicoes
    )

    # ========================================================
    # 7. OBSERVAÇÕES COMERCIAIS
    # ========================================================

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
            ).replace(
                "\n",
                "<br/>",
            ),
            estilo_normal,
        )
    )

    # ========================================================
    # 8. OBSERVAÇÕES TÉCNICAS
    # ========================================================

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
            ).replace(
                "\n",
                "<br/>",
            ),
            estilo_normal,
        )
    )

    # ========================================================
    # ASSINATURA — CORREÇÃO 6C
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
    # NOME DO RESPONSÁVEL — SEM DUPLICAÇÃO
    # --------------------------------------------------------

    nome_responsavel_pdf = (
        responsavel.strip()
        if responsavel
        else ""
    )

    if nome_responsavel_pdf:

        elementos.append(
            Paragraph(
                f"<b>{escape(nome_responsavel_pdf)}</b>",
                estilo_assinatura_nome,
            )
        )

    else:

        elementos.append(
            Paragraph(
                "<b>Responsável pelo orçamento</b>",
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
# IDENTIFICAÇÃO DO PROJETO
# ============================================================

st.markdown(
    """
    <div class="section-card">

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

st.divider()


# ============================================================
# CONDIÇÕES COMERCIAIS
# ============================================================

st.markdown(
    """
    <div class="section-card">

        <div class="section-title">
            💼 Condições comerciais
        </div>

        <div class="section-subtitle">
            Defina as condições comerciais deste orçamento.
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

st.divider()


# ============================================================
# DIMENSÕES
# ============================================================

st.markdown(
    """
    <div class="section-card">

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
# PREÇOS DOS MATERIAIS
# ============================================================

if "precos" not in st.session_state:

    st.session_state["precos"] = (
        PRECOS_BASE.copy()
    )

st.markdown(
    """
    <div class="section-card">

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
# QUANTIDADES DOS MATERIAIS
# ============================================================

st.markdown(
    """
    <div class="section-card">

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

for nome, material in (
    previa["materiais"].items()
):

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
# CALCULAR / ATUALIZAR ORÇAMENTO
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

    st.subheader(
        "📋 Dados do orçamento"
    )

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

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="info-card">

                <div class="card-label">
                    Projeto
                </div>

                <div class="card-value">
                    {escape(str(nome_exibicao))}
                </div>

                <br>

                <div class="card-label">
                    Cliente
                </div>

                <div class="card-value">
                    {escape(str(cliente_exibicao))}
                </div>

                <br>

                <div class="card-label">
                    Local da obra
                </div>

                <div class="card-value">
                    {escape(str(local_exibicao))}
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
                    {escape(str(responsavel_exibicao))}
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

    st.divider()

    # ========================================================
    # RESUMO DO PROJETO
    # ========================================================

    st.subheader(
        "📐 Resumo do projeto"
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
                    {float(projeto["area"]):.2f} m²
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
                    {float(comprimento):.2f} m
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
                    {float(altura):.2f} m
                </div>

            </div>
            """,
            unsafe_allow_html=True,
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
    # RESUMO FINANCEIRO
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

    st.subheader(
        "👷 Mão de obra"
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
            f"{float(dias):.1f}",
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
                {escape(str(prazo_salvo or "Não informado"))}
            </div>

            <br>

            <div class="card-label">
                Condição de pagamento
            </div>

            <div>
                {escape(str(pagamento_salvo or "Não informado"))}
            </div>

            <br>

            <div class="card-label">
                Forma de pagamento
            </div>

            <div>
                {escape(str(forma_pagamento_salva or "Não informado"))}
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
            <div class="info-box">

                <strong>
                    Inclusões / Observações comerciais
                </strong>

                <br><br>

                {escape(
                    observacoes_comerciais_salvas
                ).replace(chr(10), "<br>")}

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
    # ASSINATURA — CORRIGIDA
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

            <strong>
                {escape(str(nome_assinatura))}
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


# ============================================================
# RODAPÉ DA APLICAÇÃO
# ============================================================

st.markdown(
    """
    <div class="footer">
        Calculadora Steel Framing • Orçamento Profissional • Fase 6C
    </div>
    """,
    unsafe_allow_html=True,
)
