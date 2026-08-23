import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

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
        padding: 22px 25px;
        border-radius: 12px;
        border: 1px solid #d9d9d9;
        background: linear-gradient(
            135deg,
            #f8f9fa 0%,
            #ffffff 100%
        );
        margin-bottom: 20px;
    }

    .orcamento-header h1 {
        margin-bottom: 4px;
    }

    .orcamento-header p {
        margin-top: 0;
        color: #666;
    }

    .total-box {
        padding: 24px;
        border-radius: 12px;
        border: 2px solid #1f7a1f;
        background-color: #f3fff3;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .total-label {
        font-size: 15px;
        font-weight: 600;
        color: #555;
    }

    .total-value {
        font-size: 32px;
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
        margin-top: 55px;
        padding-top: 20px;
        text-align: center;
    }

    .linha-assinatura {
        border-top: 1px solid #333;
        width: 80%;
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


def nome_arquivo_orcamento():
    nome = (
        st.session_state.get(
            "nome_projeto",
            "",
        )
        .strip()
        .replace(" ", "_")
    )

    if not nome:
        nome = "Orcamento_Steel_Framing"

    return nome


# ============================================================
# GERAÇÃO DO EXCEL — FASE 6B
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
    # DADOS DO PROJETO
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


    # ========================================================
    # VALORES VALIDADOS PELO CORE
    # ========================================================

    area = float(
        obter_valor(
            projeto,
            "area",
        )
    )

    subtotal_materiais_validado = float(
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

    custo_geral_validado = float(
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

    custo_mao_de_obra_validado = float(
        obter_valor(
            mao_de_obra,
            "custo",
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
    # ESTILOS
    # ========================================================

    fill_titulo = PatternFill(
        "solid",
        fgColor="1F4E78",
    )

    fill_secao = PatternFill(
        "solid",
        fgColor="D9EAF7",
    )

    fill_cabecalho = PatternFill(
        "solid",
        fgColor="5B9BD5",
    )

    fill_total = PatternFill(
        "solid",
        fgColor="E2F0D9",
    )

    fill_info = PatternFill(
        "solid",
        fgColor="F2F2F2",
    )

    fonte_titulo = Font(
        bold=True,
        size=16,
        color="FFFFFF",
    )

    fonte_secao = Font(
        bold=True,
        size=12,
    )

    fonte_cabecalho = Font(
        bold=True,
        color="FFFFFF",
    )

    fonte_total = Font(
        bold=True,
        size=14,
    )

    fonte_negrito = Font(
        bold=True,
    )

    borda_fina = Border(
        left=Side(
            style="thin",
            color="D9D9D9",
        ),
        right=Side(
            style="thin",
            color="D9D9D9",
        ),
        top=Side(
            style="thin",
            color="D9D9D9",
        ),
        bottom=Side(
            style="thin",
            color="D9D9D9",
        ),
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

    formato_moeda = (
        '"R$" #,##0.00'
    )

    formato_numero = (
        '#,##0.00'
    )


    # ========================================================
    # FUNÇÃO PARA LARGURA DAS COLUNAS
    # ========================================================

    def ajustar_larguras(ws, limites=None):

        if limites:

            for coluna, largura in limites.items():

                ws.column_dimensions[
                    coluna
                ].width = largura

            return

        for coluna in ws.columns:

            maior = 0

            letra = get_column_letter(
                coluna[0].column
            )

            for celula in coluna:

                valor = celula.value

                if valor is None:
                    continue

                tamanho = len(
                    str(valor)
                )

                if tamanho > maior:
                    maior = tamanho

            ws.column_dimensions[
                letra
            ].width = min(
                max(maior + 2, 10),
                45,
            )


    # ========================================================
    # ABA DADOS
    # ========================================================

    ws_dados.merge_cells(
        "A1:B1"
    )

    ws_dados["A1"] = (
        "DADOS DO PROJETO E CONDIÇÕES COMERCIAIS"
    )

    ws_dados["A1"].fill = fill_titulo
    ws_dados["A1"].font = fonte_titulo
    ws_dados["A1"].alignment = alinhamento_centro

    dados = [
        (
            "Nome do projeto",
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
            "Responsável pelo orçamento",
            responsavel,
        ),
        (
            "Data do orçamento",
            data_orcamento,
        ),
        (
            "Validade do orçamento",
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
        (
            "Comprimento",
            comprimento,
        ),
        (
            "Altura",
            altura,
        ),
        (
            "Área",
            area,
        ),
    ]

    linha = 3

    for campo, valor in dados:

        ws_dados.cell(
            linha,
            1,
            campo,
        )

        ws_dados.cell(
            linha,
            2,
            valor,
        )

        ws_dados.cell(
            linha,
            1,
        ).font = fonte_negrito

        ws_dados.cell(
            linha,
            1,
        ).fill = fill_info

        ws_dados.cell(
            linha,
            1,
        ).border = borda_fina

        ws_dados.cell(
            linha,
            2,
        ).border = borda_fina

        ws_dados.cell(
            linha,
            2,
        ).alignment = Alignment(
            vertical="top",
            wrap_text=True,
        )

        linha += 1


    # Formatação de data
    if isinstance(
        ws_dados["B7"].value,
        date,
    ):

        ws_dados["B7"].number_format = (
            "dd/mm/yyyy"
        )


    # Formatação dimensões
    ws_dados["B14"].number_format = (
        formato_numero
    )

    ws_dados["B15"].number_format = (
        formato_numero
    )

    ws_dados["B16"].number_format = (
        formato_numero
    )


    ajustar_larguras(
        ws_dados,
        {
            "A": 35,
            "B": 70,
        },
    )

    ws_dados.freeze_panes = "A3"


    # ========================================================
    # ABA MATERIAIS
    # ========================================================

    ws_materiais.merge_cells(
        "A1:E1"
    )

    ws_materiais["A1"] = (
        "QUANTITATIVO DE MATERIAIS"
    )

    ws_materiais["A1"].fill = fill_titulo
    ws_materiais["A1"].font = fonte_titulo
    ws_materiais["A1"].alignment = alinhamento_centro

    cabecalho_materiais = [
        "Material",
        "Unidade",
        "Quantidade",
        "Preço unitário",
        "Total",
    ]

    for coluna, titulo in enumerate(
        cabecalho_materiais,
        start=1,
    ):

        celula = ws_materiais.cell(
            3,
            coluna,
            titulo,
        )

        celula.fill = fill_cabecalho
        celula.font = fonte_cabecalho
        celula.alignment = alinhamento_centro
        celula.border = borda_fina


    primeira_linha_material = 4

    linha_material = (
        primeira_linha_material
    )

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

        custo_validado = float(
            material.get(
                "custo",
                quantidade * preco_unitario,
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
            preco_unitario,
        )

        # ----------------------------------------------------
        # Fórmula somente se reproduzir o valor validado
        # ----------------------------------------------------

        valor_calculado = (
            quantidade *
            preco_unitario
        )

        if abs(
            valor_calculado -
            custo_validado
        ) < 0.005:

            ws_materiais.cell(
                linha_material,
                5,
                f"=C{linha_material}*D{linha_material}",
            )

        else:

            ws_materiais.cell(
                linha_material,
                5,
                custo_validado,
            )

        for coluna in range(1, 6):

            celula = ws_materiais.cell(
                linha_material,
                coluna,
            )

            celula.border = borda_fina
            celula.alignment = (
                alinhamento_direita
                if coluna >= 3
                else alinhamento_esquerda
            )

        ws_materiais.cell(
            linha_material,
            3,
        ).number_format = formato_numero

        ws_materiais.cell(
            linha_material,
            4,
        ).number_format = formato_moeda

        ws_materiais.cell(
            linha_material,
            5,
        ).number_format = formato_moeda

        linha_material += 1


    ultima_linha_material = (
        linha_material - 1
    )


    # --------------------------------------------------------
    # SUBTOTAL
    # --------------------------------------------------------

    linha_subtotal = (
        ultima_linha_material + 2
    )

    ws_materiais.cell(
        linha_subtotal,
        4,
        "SUBTOTAL MATERIAIS",
    )

    ws_materiais.cell(
        linha_subtotal,
        4,
    ).font = fonte_negrito

    ws_materiais.cell(
        linha_subtotal,
        4,
    ).fill = fill_secao

    ws_materiais.cell(
        linha_subtotal,
        4,
    ).border = borda_fina

    # Verifica se a fórmula reproduz
    # exatamente o subtotal validado.

    soma_materiais_calculada = sum(
        float(
            material.get(
                "custo",
                0,
            )
        )
        for material in materiais.values()
    )

    if abs(
        soma_materiais_calculada -
        subtotal_materiais_validado
    ) < 0.005:

        ws_materiais.cell(
            linha_subtotal,
            5,
            f"=SUM(E{primeira_linha_material}:E{ultima_linha_material})",
        )

    else:

        ws_materiais.cell(
            linha_subtotal,
            5,
            subtotal_materiais_validado,
        )

    ws_materiais.cell(
        linha_subtotal,
        5,
    ).font = fonte_negrito

    ws_materiais.cell(
        linha_subtotal,
        5,
    ).fill = fill_secao

    ws_materiais.cell(
        linha_subtotal,
        5,
    ).border = borda_fina

    ws_materiais.cell(
        linha_subtotal,
        5,
    ).number_format = formato_moeda


    ajustar_larguras(
        ws_materiais,
        {
            "A": 45,
            "B": 14,
            "C": 16,
            "D": 20,
            "E": 20,
        },
    )

    ws_materiais.freeze_panes = "A4"
    ws_materiais.auto_filter.ref = (
        f"A3:E{ultima_linha_material}"
    )


    # ========================================================
    # ABA MÃO DE OBRA
    # ========================================================

    ws_mao_obra.merge_cells(
        "A1:D1"
    )

    ws_mao_obra["A1"] = (
        "MÃO DE OBRA"
    )

    ws_mao_obra["A1"].fill = fill_titulo
    ws_mao_obra["A1"].font = fonte_titulo
    ws_mao_obra["A1"].alignment = alinhamento_centro


    cabecalho_mao_obra = [
        "Descrição",
        "Dias",
        "Diária",
        "Custo",
    ]

    for coluna, titulo in enumerate(
        cabecalho_mao_obra,
        start=1,
    ):

        celula = ws_mao_obra.cell(
            3,
            coluna,
            titulo,
        )

        celula.fill = fill_cabecalho
        celula.font = fonte_cabecalho
        celula.alignment = alinhamento_centro
        celula.border = borda_fina


    ws_mao_obra["A4"] = (
        "Mão de obra"
    )

    ws_mao_obra["B4"] = dias
    ws_mao_obra["C4"] = diaria


    # --------------------------------------------------------
    # Fórmula da mão de obra
    # somente se reproduzir o valor validado.
    # --------------------------------------------------------

    custo_calculado_mao_obra = (
        dias * diaria
    )

    if abs(
        custo_calculado_mao_obra -
        custo_mao_de_obra_validado
    ) < 0.005:

        ws_mao_obra["D4"] = (
            "=B4*C4"
        )

    else:

        ws_mao_obra["D4"] = (
            custo_mao_de_obra_validado
        )


    for linha in range(4, 5):

        for coluna in range(1, 5):

            celula = ws_mao_obra.cell(
                linha,
                coluna,
            )

            celula.border = borda_fina

            if coluna >= 2:

                celula.alignment = (
                    alinhamento_direita
                )


    ws_mao_obra["B4"].number_format = (
        formato_numero
    )

    ws_mao_obra["C4"].number_format = (
        formato_moeda
    )

    ws_mao_obra["D4"].number_format = (
        formato_moeda
    )


    # --------------------------------------------------------
    # TOTAL MÃO DE OBRA
    # --------------------------------------------------------

    linha_total_mao_obra = 6

    ws_mao_obra.cell(
        linha_total_mao_obra,
        3,
        "TOTAL",
    )

    ws_mao_obra.cell(
        linha_total_mao_obra,
        3,
    ).font = fonte_negrito

    ws_mao_obra.cell(
        linha_total_mao_obra,
        3,
    ).fill = fill_secao

    ws_mao_obra.cell(
        linha_total_mao_obra,
        3,
    ).border = borda_fina

    ws_mao_obra.cell(
        linha_total_mao_obra,
        4,
        "=D4",
    )

    ws_mao_obra.cell(
        linha_total_mao_obra,
        4,
    ).font = fonte_negrito

    ws_mao_obra.cell(
        linha_total_mao_obra,
        4,
    ).fill = fill_secao

    ws_mao_obra.cell(
        linha_total_mao_obra,
        4,
    ).border = borda_fina

    ws_mao_obra.cell(
        linha_total_mao_obra,
        4,
    ).number_format = formato_moeda


    ajustar_larguras(
        ws_mao_obra,
        {
            "A": 35,
            "B": 16,
            "C": 20,
            "D": 20,
        },
    )


    # ========================================================
    # ABA ORÇAMENTO
    # ========================================================

    ws_orcamento.merge_cells(
        "A1:D1"
    )

    ws_orcamento["A1"] = (
        "ORÇAMENTO — STEEL FRAMING"
    )

    ws_orcamento["A1"].fill = fill_titulo
    ws_orcamento["A1"].font = fonte_titulo
    ws_orcamento["A1"].alignment = alinhamento_centro


    ws_orcamento.merge_cells(
        "A2:D2"
    )

    ws_orcamento["A2"] = (
        "Quantitativo de materiais e mão de obra"
    )

    ws_orcamento["A2"].alignment = (
        alinhamento_centro
    )


    # --------------------------------------------------------
    # IDENTIFICAÇÃO
    # --------------------------------------------------------

    ws_orcamento.merge_cells(
        "A4:D4"
    )

    ws_orcamento["A4"] = (
        "IDENTIFICAÇÃO DO PROJETO"
    )

    ws_orcamento["A4"].fill = fill_secao
    ws_orcamento["A4"].font = fonte_secao


    identificacao = [
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
            "Data",
            data_orcamento,
        ),
    ]

    linha = 5

    for campo, valor in identificacao:

        ws_orcamento.cell(
            linha,
            1,
            campo,
        )

        ws_orcamento.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=4,
        )

        ws_orcamento.cell(
            linha,
            2,
            valor,
        )

        ws_orcamento.cell(
            linha,
            1,
        ).font = fonte_negrito

        ws_orcamento.cell(
            linha,
            1,
        ).fill = fill_info

        for coluna in range(1, 5):

            ws_orcamento.cell(
                linha,
                coluna,
            ).border = borda_fina

        linha += 1


    # --------------------------------------------------------
    # DIMENSÕES
    # --------------------------------------------------------

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
    )

    ws_orcamento.cell(
        linha,
        1,
        "DIMENSÕES DO PROJETO",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).fill = fill_secao

    ws_orcamento.cell(
        linha,
        1,
    ).font = fonte_secao

    linha += 1


    dimensoes = [
        (
            "Comprimento (m)",
            comprimento,
        ),
        (
            "Altura (m)",
            altura,
        ),
        (
            "Área (m²)",
            area,
        ),
    ]

    for campo, valor in dimensoes:

        ws_orcamento.cell(
            linha,
            1,
            campo,
        )

        ws_orcamento.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=4,
        )

        ws_orcamento.cell(
            linha,
            2,
            valor,
        )

        ws_orcamento.cell(
            linha,
            1,
        ).font = fonte_negrito

        ws_orcamento.cell(
            linha,
            1,
        ).fill = fill_info

        for coluna in range(1, 5):

            ws_orcamento.cell(
                linha,
                coluna,
            ).border = borda_fina

        linha += 1


    # --------------------------------------------------------
    # RESUMO FINANCEIRO
    # --------------------------------------------------------

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
    )

    ws_orcamento.cell(
        linha,
        1,
        "RESUMO FINANCEIRO",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).fill = fill_secao

    ws_orcamento.cell(
        linha,
        1,
    ).font = fonte_secao

    linha += 1


    linha_materiais_orcamento = linha
    linha_materiais_planilha = (
        primeira_linha_material
    )

    ws_orcamento.cell(
        linha,
        1,
        "Materiais",
    )

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=3,
    )

    ws_orcamento.cell(
        linha,
        4,
        f"=MATERIAIS!E{linha_subtotal}",
    )

    linha += 1


    ws_orcamento.cell(
        linha,
        1,
        "Massas e telas",
    )

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=3,
    )

    ws_orcamento.cell(
        linha,
        4,
        massas_telas,
    )

    linha += 1


    ws_orcamento.cell(
        linha,
        1,
        "Mão de obra",
    )

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=3,
    )

    ws_orcamento.cell(
        linha,
        4,
        "=MÃO DE OBRA!D6",
    )

    linha_mao_obra_orcamento = linha

    linha += 1


    # --------------------------------------------------------
    # FORMATAÇÃO RESUMO
    # --------------------------------------------------------

    for linha_resumo in range(
        linha_materiais_orcamento,
        linha + 1,
    ):

        for coluna in range(1, 5):

            ws_orcamento.cell(
                linha_resumo,
                coluna,
            ).border = borda_fina

        ws_orcamento.cell(
            linha_resumo,
            4,
        ).number_format = formato_moeda

        ws_orcamento.cell(
            linha_resumo,
            4,
        ).alignment = alinhamento_direita


    # --------------------------------------------------------
    # TOTAL GERAL
    # --------------------------------------------------------

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
    ).font = fonte_total

    ws_orcamento.cell(
        linha,
        1,
    ).fill = fill_total

    ws_orcamento.cell(
        linha,
        4,
    ).fill = fill_total

    # --------------------------------------------------------
    # Teste de segurança da fórmula do total
    # --------------------------------------------------------

    total_calculado = (
        subtotal_materiais_validado
        + massas_telas
        + custo_mao_de_obra_validado
    )

    if abs(
        total_calculado -
        custo_geral_validado
    ) < 0.005:

        ws_orcamento.cell(
            linha,
            4,
            f"=D{linha_materiais_orcamento}+D{linha_materiais_orcamento + 1}+D{linha_mao_obra_orcamento}",
        )

    else:

        ws_orcamento.cell(
            linha,
            4,
            custo_geral_validado,
        )

    ws_orcamento.cell(
        linha,
        4,
    ).font = fonte_total

    ws_orcamento.cell(
        linha,
        4,
    ).number_format = formato_moeda

    ws_orcamento.cell(
        linha,
        4,
    ).alignment = alinhamento_direita


    for coluna in range(1, 5):

        ws_orcamento.cell(
            linha,
            coluna,
        ).border = Border(
            left=Side(
                style="medium",
                color="70AD47",
            ),
            right=Side(
                style="medium",
                color="70AD47",
            ),
            top=Side(
                style="medium",
                color="70AD47",
            ),
            bottom=Side(
                style="medium",
                color="70AD47",
            ),
        )


    # --------------------------------------------------------
    # CONDIÇÕES COMERCIAIS
    # --------------------------------------------------------

    linha += 3

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
    )

    ws_orcamento.cell(
        linha,
        1,
        "CONDIÇÕES COMERCIAIS",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).fill = fill_secao

    ws_orcamento.cell(
        linha,
        1,
    ).font = fonte_secao

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


    for campo, valor in condicoes:

        ws_orcamento.cell(
            linha,
            1,
            campo,
        )

        ws_orcamento.merge_cells(
            start_row=linha,
            start_column=2,
            end_row=linha,
            end_column=4,
        )

        ws_orcamento.cell(
            linha,
            2,
            valor,
        )

        ws_orcamento.cell(
            linha,
            1,
        ).font = fonte_negrito

        ws_orcamento.cell(
            linha,
            1,
        ).fill = fill_info

        for coluna in range(1, 5):

            ws_orcamento.cell(
                linha,
                coluna,
            ).border = borda_fina

        linha += 1


    # --------------------------------------------------------
    # OBSERVAÇÕES
    # --------------------------------------------------------

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
    )

    ws_orcamento.cell(
        linha,
        1,
        "OBSERVAÇÕES COMERCIAIS",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).fill = fill_secao

    ws_orcamento.cell(
        linha,
        1,
    ).font = fonte_secao

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
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


    for coluna in range(1, 5):

        ws_orcamento.cell(
            linha,
            coluna,
        ).border = borda_fina


    linha += 2

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
    )

    ws_orcamento.cell(
        linha,
        1,
        "OBSERVAÇÕES TÉCNICAS",
    )

    ws_orcamento.cell(
        linha,
        1,
    ).fill = fill_secao

    ws_orcamento.cell(
        linha,
        1,
    ).font = fonte_secao

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=1,
        end_row=linha,
        end_column=4,
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

    for coluna in range(1, 5):

        ws_orcamento.cell(
            linha,
            coluna,
        ).border = borda_fina


    # --------------------------------------------------------
    # ASSINATURA
    # --------------------------------------------------------

    linha += 3

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=2,
        end_row=linha,
        end_column=3,
    )

    ws_orcamento.cell(
        linha,
        2,
        "__________________________________",
    )

    ws_orcamento.cell(
        linha,
        2,
    ).alignment = alinhamento_centro

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=2,
        end_row=linha,
        end_column=3,
    )

    ws_orcamento.cell(
        linha,
        2,
        responsavel or "Responsável pelo orçamento",
    )

    ws_orcamento.cell(
        linha,
        2,
    ).font = fonte_negrito

    ws_orcamento.cell(
        linha,
        2,
    ).alignment = alinhamento_centro

    linha += 1

    ws_orcamento.merge_cells(
        start_row=linha,
        start_column=2,
        end_row=linha,
        end_column=3,
    )

    ws_orcamento.cell(
        linha,
        2,
        "Responsável pelo orçamento",
    )

    ws_orcamento.cell(
        linha,
        2,
    ).alignment = alinhamento_centro


    # --------------------------------------------------------
    # CONFIGURAÇÃO DA ABA
    # --------------------------------------------------------

    ajustar_larguras(
        ws_orcamento,
        {
            "A": 28,
            "B": 20,
            "C": 20,
            "D": 24,
        },
    )

    ws_orcamento.freeze_panes = "A5"

    ws_orcamento.sheet_view.showGridLines = False
    ws_materiais.sheet_view.showGridLines = False
    ws_mao_obra.sheet_view.showGridLines = False
    ws_dados.sheet_view.showGridLines = False


    # ========================================================
    # CONFIGURAÇÃO DE IMPRESSÃO
    # ========================================================

    for ws in [
        ws_orcamento,
        ws_materiais,
        ws_mao_obra,
        ws_dados,
    ]:

        ws.page_setup.orientation = (
            "landscape"
        )

        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0

        ws.sheet_properties.pageSetUpPr.fitToPage = True

        ws.page_margins.left = 0.25
        ws.page_margins.right = 0.25
        ws.page_margins.top = 0.50
        ws.page_margins.bottom = 0.50


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


    # ========================================================
    # ESTILOS
    # ========================================================

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
                f"<b>Projeto:</b><br/>{nome_projeto or 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Cliente:</b><br/>{cliente or 'Não informado'}",
                estilo_normal,
            ),
        ],
        [
            Paragraph(
                f"<b>Local da obra:</b><br/>{local_obra or 'Não informado'}",
                estilo_normal,
            ),
            Paragraph(
                f"<b>Responsável:</b><br/>{responsavel or 'Não informado'}",
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
        repeatRows=0,
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


    comprimento = st.session_state.get(
        "comprimento",
        "",
    )

    altura = st.session_state.get(
        "altura",
        "",
    )


    if comprimento == "":
        comprimento = area


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
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
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
    # 7. OBSERVAÇÕES COMERCIAIS
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
                observacoes_comerciais.replace(
                    "\n",
                    "<br/>",
                ),
                estilo_normal,
            )
        )


    # ========================================================
    # 8. OBSERVAÇÕES TÉCNICAS
    # ========================================================

    if observacoes_tecnicas:

        elementos.append(
            Paragraph(
                "8. OBSERVAÇÕES TÉCNICAS",
                estilo_secao,
            )
        )

        elementos.append(
            Paragraph(
                observacoes_tecnicas.replace(
                    "\n",
                    "<br/>",
                ),
                estilo_normal,
            )
        )


    # ========================================================
    # ASSINATURA — FASE 6A.1
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


    if responsavel and responsavel.strip():

        elementos.append(
            Paragraph(
                f"<b>{responsavel.strip()}</b>",
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
                ParagraphStyle(
                    "ResponsavelSemNome",
                    parent=estilo_normal,
                    alignment=TA_CENTER,
                    fontName="Helvetica-Bold",
                    fontSize=9,
                    leading=12,
                    spaceBefore=5,
                ),
            )
        )


    # ========================================================
    # RODAPÉ
    # ========================================================

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
                {observacoes_comerciais_salvas}
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
                {st.session_state.get(
                    "responsavel",
                    "Responsável pelo orçamento"
                ) or "Responsável pelo orçamento"}
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
    # EXCEL — FASE 6B
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
