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
# CSS — INTERFACE PROFISSIONAL
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       CABEÇALHO
    ------------------------------------------------------- */

    .orcamento-header {
        padding: 26px 30px;
        border-radius: 14px;
        border: 1px solid #d9dee3;
        background: linear-gradient(
            135deg,
            #f5f7f9 0%,
            #ffffff 100%
        );
        margin-bottom: 22px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .orcamento-header h1 {
        margin: 0 0 6px 0;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.4px;
    }

    .orcamento-header p {
        margin: 0;
        color: #687078;
        font-size: 14px;
    }


    /* -------------------------------------------------------
       TOTAL
    ------------------------------------------------------- */

    .total-box {
        padding: 25px 28px;
        border-radius: 14px;
        border: 2px solid #198754;
        background: linear-gradient(
            135deg,
            #f2fff6 0%,
            #ffffff 100%
        );
        text-align: center;
        margin-top: 20px;
        margin-bottom: 22px;
        box-shadow: 0 3px 10px rgba(25,135,84,0.08);
    }

    .total-label {
        font-size: 14px;
        font-weight: 700;
        color: #555;
        letter-spacing: 0.5px;
    }

    .total-value {
        font-size: 34px;
        font-weight: 900;
        margin-top: 6px;
        color: #146c43;
    }


    /* -------------------------------------------------------
       CAIXAS DE INFORMAÇÃO
    ------------------------------------------------------- */

    .info-box {
        padding: 16px 19px;
        border-radius: 10px;
        border: 1px solid #dcdfe3;
        background-color: #fafafa;
        margin-bottom: 12px;
        line-height: 1.6;
    }


    /* -------------------------------------------------------
       ASSINATURA
    ------------------------------------------------------- */

    .assinatura {
        margin-top: 50px;
        padding-top: 20px;
        text-align: center;
    }

    .linha-assinatura {
        border-top: 1px solid #333;
        width: 70%;
        margin: 0 auto 9px auto;
    }


    /* -------------------------------------------------------
       MÉTRICAS
    ------------------------------------------------------- */

    div[data-testid="stMetric"] {
        border: 1px solid #e0e3e7;
        border-radius: 10px;
        padding: 12px;
        background: #ffffff;
    }


    /* -------------------------------------------------------
       BOTÕES
    ------------------------------------------------------- */

    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
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

    nome = str(nome).strip()

    if not nome:
        return "Orcamento_Steel_Framing"

    caracteres_invalidos = [
        "\\",
        "/",
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
            "_",
        )

    nome = nome.replace(
        " ",
        "_",
    )

    return nome


# ============================================================
# GERAÇÃO DO EXCEL — FASE 6B / 6C
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


    # ========================================================
    # PROJETO
    # ========================================================

    area = float(
        obter_valor(
            projeto,
            "area",
        )
    )

    subtotal_materiais = float(
        obter_valor(
            projeto,
            "subtotal_materiais",
        )
    )

    massas_telas = float(
        obter_valor(
            projeto,
            "massas_telas",
        )
    )

    custo_geral = float(
        obter_valor(
            projeto,
            "custo_geral",
        )
    )

    materiais = projeto.get(
        "materiais",
        {},
    )

    mao_de_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    dias = float(
        obter_valor(
            mao_de_obra,
            "dias",
        )
    )

    diaria = float(
        obter_valor(
            mao_de_obra,
            "diaria",
        )
    )

    custo_mao_de_obra = float(
        obter_valor(
            mao_de_obra,
            "custo",
        )
    )

    comprimento = float(
        st.session_state.get(
            "comprimento",
            0,
        )
    )

    altura = float(
        st.session_state.get(
            "altura",
            0,
        )
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
    # CORES / ESTILOS
    # ========================================================

    cinza_escuro = "343A40"
    cinza = "6C757D"
    cinza_claro = "F1F3F5"
    cinza_borda = "D9DEE3"
    branco = "FFFFFF"
    verde = "198754"
    verde_claro = "EAF7EF"

    fill_titulo = PatternFill(
        "solid",
        fgColor=cinza_escuro,
    )

    fill_secao = PatternFill(
        "solid",
        fgColor=cinza_claro,
    )

    fill_total = PatternFill(
        "solid",
        fgColor=verde_claro,
    )

    borda_fina = Border(
        left=Side(
            style="thin",
            color=cinza_borda,
        ),
        right=Side(
            style="thin",
            color=cinza_borda,
        ),
        top=Side(
            style="thin",
            color=cinza_borda,
        ),
        bottom=Side(
            style="thin",
            color=cinza_borda,
        ),
    )

    moeda_format = (
        'R$ #,##0.00'
    )

    quantidade_format = (
        '#,##0.00'
    )


    # ========================================================
    # FUNÇÕES DE ESTILO DO EXCEL
    # ========================================================

    def aplicar_titulo(ws, texto, ultima_coluna=5):

        ws.merge_cells(
            start_row=1,
            start_column=1,
            end_row=1,
            end_column=ultima_coluna,
        )

        cell = ws.cell(
            row=1,
            column=1,
            value=texto,
        )

        cell.fill = fill_titulo
        cell.font = Font(
            bold=True,
            color=branco,
            size=16,
        )
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

        ws.row_dimensions[1].height = 28


    def aplicar_secao(
        ws,
        linha,
        texto,
        ultima_coluna=5,
    ):

        ws.merge_cells(
            start_row=linha,
            start_column=1,
            end_row=linha,
            end_column=ultima_coluna,
        )

        cell = ws.cell(
            row=linha,
            column=1,
            value=texto,
        )

        cell.fill = fill_secao
        cell.font = Font(
            bold=True,
            size=11,
            color=cinza_escuro,
        )

        cell.alignment = Alignment(
            horizontal="left",
            vertical="center",
        )

        ws.row_dimensions[linha].height = 22


    def formatar_larguras(
        ws,
        larguras,
    ):

        for coluna, largura in larguras.items():

            ws.column_dimensions[
                coluna
            ].width = largura


    # ========================================================
    # ABA ORÇAMENTO
    # ========================================================

    aplicar_titulo(
        ws_orcamento,
        "ORÇAMENTO — STEEL FRAMING",
        5,
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
        size=10,
    )

    ws_orcamento["A2"].alignment = (
        Alignment(horizontal="center")
    )


    aplicar_secao(
        ws_orcamento,
        4,
        "IDENTIFICAÇÃO DO PROJETO",
        5,
    )


    dados_identificacao = [
        ("Projeto", nome_projeto or "Não informado"),
        ("Cliente", cliente or "Não informado"),
        ("Local da obra", local_obra or "Não informado"),
        ("Responsável", responsavel or "Não informado"),
        ("Data", data_orcamento),
        ("Validade", f"{validade} dias"),
    ]


    linha = 5

    for rotulo, valor in dados_identificacao:

        ws_orcamento.cell(
            linha,
            1,
            rotulo,
        )

        ws_orcamento.cell(
            linha,
            1,
        ).font = Font(
            bold=True
        )

        ws_orcamento.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=5,
        )

        ws_orcamento.cell(
            linha,
            2,
            valor,
        )

        for coluna in range(1, 6):

            ws_orcamento.cell(
                linha,
                coluna,
            ).border = borda_fina

            ws_orcamento.cell(
                linha,
                coluna,
            ).alignment = Alignment(
                vertical="center"
            )

        if rotulo == "Data":
            ws_orcamento.cell(
                linha,
                2,
            ).number_format = "dd/mm/yyyy"

        linha += 1


    # ========================================================
    # DIMENSÕES
    # ========================================================

    linha += 1

    aplicar_secao(
        ws_orcamento,
        linha,
        "DIMENSÕES DO PROJETO",
        5,
    )

    linha += 1

    dimensoes = [
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
    ]

    for rotulo, valor in dimensoes:

        ws_orcamento.cell(
            linha,
            1,
            rotulo,
        )

        ws_orcamento.cell(
            linha,
            1,
        ).font = Font(
            bold=True
        )

        ws_orcamento.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=5,
        )

        ws_orcamento.cell(
            linha,
            2,
            valor,
        )

        ws_orcamento.cell(
            linha,
            2,
        ).number_format = quantidade_format

        for coluna in range(1, 6):

            ws_orcamento.cell(
                linha,
                coluna,
            ).border = borda_fina

        linha += 1


    # ========================================================
    # RESUMO FINANCEIRO
    # ========================================================

    linha += 1

    aplicar_secao(
        ws_orcamento,
        linha,
        "RESUMO FINANCEIRO",
        5,
    )

    linha += 1

    linha_materiais = linha
    ws_orcamento.cell(
        linha,
        1,
        "Materiais",
    )

    ws_orcamento.cell(
        linha,
        2,
        subtotal_materiais,
    )

    ws_orcamento.cell(
        linha,
        2,
    ).number_format = moeda_format

    linha += 1

    linha_massas = linha

    ws_orcamento.cell(
        linha,
        1,
        "Massas e telas",
    )

    ws_orcamento.cell(
        linha,
        2,
        massas_telas,
    )

    ws_orcamento.cell(
        linha,
        2,
    ).number_format = moeda_format

    linha += 1

    linha_mao_obra = linha

    ws_orcamento.cell(
        linha,
        1,
        "Mão de obra",
    )

    ws_orcamento.cell(
        linha,
        2,
        f"='MÃO DE OBRA'!C5",
    )

    ws_orcamento.cell(
        linha,
        2,
    ).number_format = moeda_format

    for r in range(
        linha_materiais,
        linha + 1,
    ):

        for coluna in range(1, 6):

            ws_orcamento.cell(
                r,
                coluna,
            ).border = borda_fina


    # ========================================================
    # TOTAL
    # ========================================================

    linha += 2

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=3,
    )

    ws_orcamento.cell(
        linha,
        1,
        "VALOR TOTAL DO ORÇAMENTO",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).font = Font(
        bold=True,
        size=13,
        color=verde,
    )

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=4,
        end_row=linha,
        end_column=5,
    )

    ws_orcamento.cell(
        linha,
        4,
        f"=SUM(B{linha_materiais}:B{linha_mao_obra})",
    )

    ws_orcamento.cell(
        linha,
        4,
    ).number_format = moeda_format

    ws_orcamento.cell(
        linha,
        4,
    ).font = Font(
        bold=True,
        size=16,
        color=verde,
    )

    for coluna in range(1, 6):

        ws_orcamento.cell(
            linha,
            coluna,
        ).fill = fill_total

        ws_orcamento.cell(
            linha,
            coluna,
        ).border = Border(
            left=Side(
                style="medium",
                color=verde,
            ),
            right=Side(
                style="medium",
                color=verde,
            ),
            top=Side(
                style="medium",
                color=verde,
            ),
            bottom=Side(
                style="medium",
                color=verde,
            ),
        )

    linha += 2


    # ========================================================
    # CONDIÇÕES COMERCIAIS
    # ========================================================

    aplicar_secao(
        ws_orcamento,
        linha,
        "CONDIÇÕES COMERCIAIS",
        5,
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

        ws_orcamento.cell(
            linha,
            1,
            rotulo,
        )

        ws_orcamento.cell(
            linha,
            1,
        ).font = Font(
            bold=True
        )

        ws_orcamento.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=5,
        )

        ws_orcamento.cell(
            linha,
            2,
            valor,
        )

        for coluna in range(1, 6):

            ws_orcamento.cell(
                linha,
                coluna,
            ).border = borda_fina

        linha += 1


    # ========================================================
    # OBSERVAÇÕES
    # ========================================================

    linha += 1

    aplicar_secao(
        ws_orcamento,
        linha,
        "OBSERVAÇÕES COMERCIAIS",
        5,
    )

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha + 1,
        end_column=5,
    )

    ws_orcamento.cell(
        linha,
        1,
        observacoes_comerciais or "Não informado",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )

    linha += 3

    aplicar_secao(
        ws_orcamento,
        linha,
        "OBSERVAÇÕES TÉCNICAS",
        5,
    )

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha + 1,
        end_column=5,
    )

    ws_orcamento.cell(
        linha,
        1,
        observacoes_tecnicas or "Não informado",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).alignment = Alignment(
        wrap_text=True,
        vertical="top",
    )


    # ========================================================
    # CONFIGURAÇÃO ORÇAMENTO
    # ========================================================

    formatar_larguras(
        ws_orcamento,
        {
            "A": 28,
            "B": 22,
            "C": 18,
            "D": 18,
            "E": 18,
        },
    )

    ws_orcamento.freeze_panes = "A4"

    ws_orcamento.sheet_view.showGridLines = False


    # ========================================================
    # ABA MATERIAIS
    # ========================================================

    aplicar_titulo(
        ws_materiais,
        "QUANTITATIVO DE MATERIAIS",
        5,
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
            valor,
        )

        cell.fill = fill_secao
        cell.font = Font(
            bold=True
        )
        cell.border = borda_fina
        cell.alignment = Alignment(
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

        preco = float(
            material.get(
                "preco_unitario",
                0,
            )
        )

        ws_materiais.cell(
            linha_material,
            1,
            str(nome),
        )

        ws_materiais.cell(
            linha_material,
            2,
            str(
                material.get(
                    "unidade",
                    "",
                )
            ),
        )

        ws_materiais.cell(
            linha_material,
            3,
            quantidade,
        )

        ws_materiais.cell(
            linha_material,
            4,
            preco,
        )

        ws_materiais.cell(
            linha_material,
            5,
            f"=C{linha_material}*D{linha_material}",
        )

        ws_materiais.cell(
            linha_material,
            3,
        ).number_format = quantidade_format

        ws_materiais.cell(
            linha_material,
            4,
        ).number_format = moeda_format

        ws_materiais.cell(
            linha_material,
            5,
        ).number_format = moeda_format

        for coluna in range(1, 6):

            ws_materiais.cell(
                linha_material,
                coluna,
            ).border = borda_fina

        linha_material += 1


    total_materiais_linha = linha_material

    ws_materiais.cell(
        total_materiais_linha,
        1,
        "TOTAL DOS MATERIAIS",
    )

    ws_materiais.cell(
        total_materiais_linha,
        1,
    ).font = Font(
        bold=True
    )

    ws_materiais.merge_cells(
        start_row=total_materiais_linha,
        start_column=1,
        end_row=total_materiais_linha,
        end_column=4,
    )

    ws_materiais.cell(
        total_materiais_linha,
        5,
        f"=SUM(E4:E{total_materiais_linha - 1})",
    )

    ws_materiais.cell(
        total_materiais_linha,
        5,
    ).number_format = moeda_format

    ws_materiais.cell(
        total_materiais_linha,
        5,
    ).font = Font(
        bold=True,
        color=verde,
    )

    for coluna in range(1, 6):

        ws_materiais.cell(
            total_materiais_linha,
            coluna,
        ).fill = fill_total

        ws_materiais.cell(
            total_materiais_linha,
            coluna,
        ).border = borda_fina


    formatar_larguras(
        ws_materiais,
        {
            "A": 34,
            "B": 14,
            "C": 16,
            "D": 18,
            "E": 18,
        },
    )

    ws_materiais.freeze_panes = "A4"
    ws_materiais.sheet_view.showGridLines = False


    # ========================================================
    # ABA MÃO DE OBRA
    # ========================================================

    aplicar_titulo(
        ws_mao_obra,
        "MÃO DE OBRA",
        3,
    )

    headers_mao_obra = [
        "Descrição",
        "Valor",
        "Cálculo",
    ]

    for coluna, valor in enumerate(
        headers_mao_obra,
        start=1,
    ):

        cell = ws_mao_obra.cell(
            3,
            coluna,
            valor,
        )

        cell.fill = fill_secao
        cell.font = Font(
            bold=True
        )
        cell.border = borda_fina
        cell.alignment = Alignment(
            horizontal="center"
        )


    ws_mao_obra["A4"] = "Dias estimados"
    ws_mao_obra["B4"] = dias
    ws_mao_obra["C4"] = "Quantidade de dias"

    ws_mao_obra["A5"] = "Valor da diária"
    ws_mao_obra["B5"] = diaria
    ws_mao_obra["C5"] = "=B4*B5"


    # Para manter o custo validado e simultaneamente
    # permitir edição da diária/dias, o custo é calculado
    # pela própria planilha.

    ws_mao_obra["A6"] = "Custo da mão de obra"
    ws_mao_obra["B6"] = "=B4*B5"
    ws_mao_obra["C6"] = "Dias × diária"


    for celula in [
        "B5",
        "B6",
    ]:

        ws_mao_obra[celula].number_format = moeda_format


    ws_mao_obra["B4"].number_format = quantidade_format


    for linha_mao in range(4, 7):

        for coluna in range(1, 4):

            ws_mao_obra.cell(
                linha_mao,
                coluna,
            ).border = borda_fina


    for coluna in range(1, 4):

        ws_mao_obra.cell(
            6,
            coluna,
        ).fill = fill_total

        ws_mao_obra.cell(
            6,
            coluna,
        ).font = Font(
            bold=True
        )


    formatar_larguras(
        ws_mao_obra,
        {
            "A": 28,
            "B": 20,
            "C": 28,
        },
    )

    ws_mao_obra.sheet_view.showGridLines = False


    # ========================================================
    # ABA DADOS
    # ========================================================

    aplicar_titulo(
        ws_dados,
        "DADOS DO ORÇAMENTO",
        2,
    )

    dados = [
        ("Projeto", nome_projeto or "Não informado"),
        ("Cliente", cliente or "Não informado"),
        ("Local da obra", local_obra or "Não informado"),
        ("Responsável", responsavel or "Não informado"),
        ("Data", data_orcamento),
        ("Validade", f"{validade} dias"),
        ("Prazo de execução", prazo_execucao or "Não informado"),
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
        ("Comprimento (m)", comprimento),
        ("Altura (m)", altura),
        ("Área (m²)", area),
    ]

    linha_dados = 3

    for rotulo, valor in dados:

        ws_dados.cell(
            linha_dados,
            1,
            rotulo,
        )

        ws_dados.cell(
            linha_dados,
            1,
        ).font = Font(
            bold=True
        )

        ws_dados.cell(
            linha_dados,
            2,
            valor,
        )

        ws_dados.cell(
            linha_dados,
            1,
        ).border = borda_fina

        ws_dados.cell(
            linha_dados,
            2,
        ).border = borda_fina

        ws_dados.cell(
            linha_dados,
            2,
        ).alignment = Alignment(
            wrap_text=True,
            vertical="top",
        )

        if rotulo == "Data":

            ws_dados.cell(
                linha_dados,
                2,
            ).number_format = "dd/mm/yyyy"

        linha_dados += 1


    formatar_larguras(
        ws_dados,
        {
            "A": 28,
            "B": 70,
        },
    )

    ws_dados.sheet_view.showGridLines = False


    # ========================================================
    # CONFIGURAÇÕES GERAIS DO WORKBOOK
    # ========================================================

    try:

        wb.calculation.fullCalcOnLoad = True
        wb.calculation.forceFullCalc = True
        wb.calculation.calcMode = "auto"

    except Exception:
        pass


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
# GERAÇÃO DO PDF — FASE 6C
# ============================================================

def gerar_pdf(projeto):

    try:

        from reportlab.lib import colors
        from reportlab.lib.enums import (
            TA_CENTER,
            TA_RIGHT,
            TA_LEFT,
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
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=16 * mm,
        bottomMargin=22 * mm,
        title="Orçamento Steel Framing",
        author=responsavel or "Calculadora Steel Framing",
    )


    styles = getSampleStyleSheet()


    # ========================================================
    # ESTILOS
    # ========================================================

    estilo_titulo = ParagraphStyle(
        "TituloOrcamento6C",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#212529"),
        spaceAfter=4,
    )


    estilo_subtitulo = ParagraphStyle(
        "Subtitulo6C",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6c757d"),
        spaceAfter=13,
    )


    estilo_secao = ParagraphStyle(
        "Secao6C",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#343a40"),
        spaceBefore=7,
        spaceAfter=7,
    )


    estilo_normal = ParagraphStyle(
        "Normal6C",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.7,
        leading=11.5,
        textColor=colors.HexColor("#212529"),
    )


    estilo_pequeno = ParagraphStyle(
        "Pequeno6C",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#212529"),
    )


    estilo_direita = ParagraphStyle(
        "Direita6C",
        parent=estilo_normal,
        alignment=TA_RIGHT,
    )


    estilo_centralizado = ParagraphStyle(
        "Centralizado6C",
        parent=estilo_normal,
        alignment=TA_CENTER,
    )


    estilo_total = ParagraphStyle(
        "Total6C",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=21,
        alignment=TA_RIGHT,
        textColor=colors.HexColor("#146c43"),
    )


    estilo_assinatura_nome = ParagraphStyle(
        "AssinaturaNome6C",
        parent=estilo_normal,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        spaceBefore=5,
        spaceAfter=2,
    )


    estilo_assinatura_cargo = ParagraphStyle(
        "AssinaturaCargo6C",
        parent=estilo_pequeno,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6c757d"),
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
    # 1 — IDENTIFICAÇÃO
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
                f"<b>Projeto</b><br/>{escape(str(nome_projeto or 'Não informado'))}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Cliente</b><br/>{escape(str(cliente or 'Não informado'))}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra</b><br/>{escape(str(local_obra or 'Não informado'))}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Responsável</b><br/>{escape(str(responsavel or 'Não informado'))}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Data</b><br/>{data_formatada}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Validade</b><br/>{validade} dias",
                estilo_normal,
            ),
        ],
    ]


    tabela_dados = Table(
        dados_orcamento,
        colWidths=[
            89 * mm,
            89 * mm,
        ],
    )


    tabela_dados.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.HexColor("#ced4da"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor("#dee2e6"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#ffffff"),
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


    elementos.append(
        tabela_dados
    )

    elementos.append(
        Spacer(1, 8)
    )


    # ========================================================
    # 2 — DIMENSÕES
    # ========================================================

    elementos.append(
        Paragraph(
            "2. RESUMO DO PROJETO",
            estilo_secao,
        )
    )


    comprimento_exibicao = comprimento

    if comprimento_exibicao == "":
        comprimento_exibicao = area


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
            Paragraph(
                "<b>Comprimento</b>",
                estilo_normal,
            ),
            Paragraph(
                f"{float(comprimento_exibicao):.2f} m",
                estilo_direita,
            ),
            Paragraph(
                "<b>Altura</b>",
                estilo_normal,
            ),
            Paragraph(
                f"{float(altura):.2f} m",
                estilo_direita,
            ),
        ]
    ]


    tabela_resumo = Table(
        resumo,
        colWidths=[
            24 * mm,
            29 * mm,
            31 * mm,
            29 * mm,
            20 * mm,
            29 * mm,
        ],
    )


    tabela_resumo.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.HexColor("#ced4da"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor("#dee2e6"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    colors.HexColor("#f1f3f5"),
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, 0),
                    colors.HexColor("#f1f3f5"),
                ),
                (
                    "BACKGROUND",
                    (4, 0),
                    (4, 0),
                    colors.HexColor("#f1f3f5"),
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
        tabela_resumo
    )

    elementos.append(
        Spacer(1, 10)
    )


    # ========================================================
    # 3 — MATERIAIS
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


    for indice, (nome, material) in enumerate(
        materiais.items()
    ):

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
            63 * mm,
            15 * mm,
            28 * mm,
            35 * mm,
            37 * mm,
        ],
        repeatRows=1,
        splitByRow=1,
        hAlign="CENTER",
    )


    estilo_tabela_materiais = [
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#343a40"),
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white,
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.6,
            colors.HexColor("#adb5bd"),
        ),
        (
            "INNERGRID",
            (0, 0),
            (-1, -1),
            0.3,
            colors.HexColor("#dee2e6"),
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
            5,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            5,
        ),
    ]


    # Linhas alternadas
    for linha_tabela in range(
        1,
        len(tabela_materiais),
    ):

        if linha_tabela % 2 == 0:

            estilo_tabela_materiais.append(
                (
                    "BACKGROUND",
                    (0, linha_tabela),
                    (-1, linha_tabela),
                    colors.HexColor("#f8f9fa"),
                )
            )


    tabela_material_pdf.setStyle(
        TableStyle(
            estilo_tabela_materiais
        )
    )


    elementos.append(
        tabela_material_pdf
    )

    elementos.append(
        Spacer(1, 10)
    )


    # ========================================================
    # 4 — RESUMO FINANCEIRO
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
            120 * mm,
            58 * mm,
    ],
    )


    tabela_financeiro.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#ced4da"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dee2e6"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f8f9fa"),
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


    elementos.append(
        tabela_financeiro
    )

    elementos.append(
        Spacer(1, 8)
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
            100 * mm,
            78 * mm,
        ],
    )


    total_tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1.3,
                    colors.HexColor("#198754"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#eaf7ef"),
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


    elementos.append(
        KeepTogether(
            total_tabela
        )
    )


    # ========================================================
    # 5 — MÃO DE OBRA
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
            120 * mm,
            58 * mm,
        ],
    )


    mao_obra_tabela.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#ced4da"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dee2e6"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f8f9fa"),
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


    elementos.append(
        mao_obra_tabela
    )


    # ========================================================
    # 6 — CONDIÇÕES COMERCIAIS
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
                    str(
                        prazo_execucao
                        or "Não informado"
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
                    str(
                        condicao_pagamento
                        or "Não informado"
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
                    str(
                        forma_pagamento
                        or "Não informado"
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
            123 * mm,
        ],
    )


    tabela_condicoes.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#ced4da"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#dee2e6"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#f8f9fa"),
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


    elementos.append(
        tabela_condicoes
    )


    # ========================================================
    # 7 — OBSERVAÇÕES COMERCIAIS
    # ========================================================

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(
        Paragraph(
            "7. OBSERVAÇÕES COMERCIAIS",
            estilo_secao,
        )
    )


    texto_comercial = (
        observacoes_comerciais
        or "Não informado"
    )


    texto_comercial = escape(
        str(texto_comercial)
    ).replace(
        "\n",
        "<br/>",
    )


    tabela_obs_comercial = Table(
        [
            [
                Paragraph(
                    texto_comercial,
                    estilo_normal,
                )
            ]
        ],
        colWidths=[
            178 * mm,
        ],
    )


    tabela_obs_comercial.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#ced4da"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#fafafa"),
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


    elementos.append(
        tabela_obs_comercial
    )


    # ========================================================
    # 8 — OBSERVAÇÕES TÉCNICAS
    # ========================================================

    elementos.append(
        Spacer(1, 10)
    )

    elementos.append(
        Paragraph(
            "8. OBSERVAÇÕES TÉCNICAS",
            estilo_secao,
        )
    )


    texto_tecnico = (
        observacoes_tecnicas
        or "Não informado"
    )


    texto_tecnico = escape(
        str(texto_tecnico)
    ).replace(
        "\n",
        "<br/>",
    )


    tabela_obs_tecnica = Table(
        [
            [
                Paragraph(
                    texto_tecnico,
                    estilo_normal,
                )
            ]
        ],
        colWidths=[
            178 * mm,
        ],
    )


    tabela_obs_tecnica.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#ced4da"),
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#fafafa"),
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


    elementos.append(
        tabela_obs_tecnica
    )


    # ========================================================
    # ASSINATURA
    # ========================================================

    elementos.append(
        Spacer(1, 24)
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
            105 * mm,
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


    if responsavel and responsavel.strip():

        elementos.append(
            Paragraph(
                f"<b>{escape(responsavel.strip())}</b>",
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

        # Linha superior do rodapé
        canvas.setStrokeColor(
            colors.HexColor("#dee2e6")
        )

        canvas.setLineWidth(
            0.4
        )

        canvas.line(
            14 * mm,
            14 * mm,
            largura - 14 * mm,
            14 * mm,
        )

        canvas.setFont(
            "Helvetica",
            7,
        )

        canvas.setFillColor(
            colors.HexColor("#6c757d")
        )

        canvas.drawString(
            14 * mm,
            8 * mm,
            "Orçamento Steel Framing",
        )

        canvas.drawRightString(
            largura - 14 * mm,
            8 * mm,
            f"Página {documento.page}",
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
# CABEÇALHO DA APLICAÇÃO
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

st.subheader(
    "📋 Identificação do projeto"
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

st.subheader(
    "💼 Condições comerciais"
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

st.subheader(
    "📐 Dimensões do projeto"
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

    st.metric(
        "Área do projeto",
        f"{area_preview:.2f} m²",
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


st.subheader(
    "💰 Preços dos materiais"
)


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
# QUANTIDADES DOS MATERIAIS
# ============================================================

st.subheader(
    "📦 Quantidades dos materiais"
)


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

    st.header(
        "📄 ORÇAMENTO PROFISSIONAL"
    )


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
    # DADOS DO ORÇAMENTO
    # ========================================================

    st.subheader(
        "📋 Dados do orçamento"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            f"""
            **Projeto:**  
            {st.session_state.get("nome_projeto", "") or "Não informado"}

            **Cliente:**  
            {st.session_state.get("cliente", "") or "Não informado"}

            **Local da obra:**  
            {st.session_state.get("local_obra", "") or "Não informado"}
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
            {st.session_state.get("responsavel", "") or "Não informado"}

            **Data:**  
            {data_salva.strftime("%d/%m/%Y")}

            **Validade:**  
            {st.session_state.get("validade_orcamento", 10)} dias
            """
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


    tabela_materiais_interface = []


    for nome, material in (
        projeto["materiais"].items()
    ):

        tabela_materiais_interface.append(
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
        tabela_materiais_interface
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
    # ASSINATURA NA INTERFACE
    # ========================================================

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
