import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Calculadora Steel Framing",
    page_icon="📐",
    layout="wide",
)


# ============================================================
# CSS CUSTOMIZADO
# ============================================================

st.markdown(
    """
    <style>

    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    .stApp {
        background: #f5f7fa;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    div[data-testid="stVerticalBlock"] > div:has(h1) {
        background: linear-gradient(
            135deg,
            #17202a 0%,
            #263746 55%,
            #34495e 100%
        );
        border-radius: 18px;
        padding: 35px 38px 30px 38px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }

    div[data-testid="stVerticalBlock"] h1 {
        color: #6fa8c9 !important;
        font-size: 3.5rem !important;
        line-height: 1.2 !important;
        font-weight: 900 !important;
        letter-spacing: -1px !important;
        margin: 0 0 10px 0 !important;
        border: none !important;
    }

    div[data-testid="stVerticalBlock"] h1 + p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }

    /* BOTÃO PRINCIPAL DE CÁLCULO */

    div.stButton > button[kind="primary"] {
        height: 60px;
        font-size: 1.25rem;
        font-weight: 800;
        border-radius: 12px;
        width: 100%;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TÍTULO PRINCIPAL
# ============================================================

st.title("📐 Detalhamento do Projeto")

st.markdown(
    "Preencha as dimensões da estrutura e clique em "
    "**CALCULAR PROJETO** para gerar os quantitativos."
)


# ============================================================
# SEÇÃO 1 — INFORMAÇÕES DO CLIENTE
# ============================================================

st.header("📋 Informações Gerais")

col_cli1, col_cli2 = st.columns(2)

with col_cli1:

    cliente = st.text_input(
        "Nome do Cliente",
        value="João Silva"
    )

with col_cli2:

    data_projeto = st.date_input(
        "Data do Orçamento",
        date.today()
    )


# ============================================================
# SEÇÃO 2 — DIMENSÕES DA ESTRUTURA
# ============================================================

st.header("🏠 Dimensões da Estrutura")

col_dim1, col_dim2 = st.columns(2)

with col_dim1:

    comprimento_paredes = st.number_input(
        "Comprimento Total das Paredes (m linear)",
        min_value=1.0,
        value=30.0,
        step=1.0
    )

with col_dim2:

    pe_direito = st.number_input(
        "Pé Direito (m)",
        min_value=1.0,
        value=3.0,
        step=0.1
    )


# ============================================================
# ÁREA DAS PAREDES
# ============================================================

area_total = (
    comprimento_paredes *
    pe_direito
)


# ============================================================
# EXIBIÇÃO DA ÁREA CALCULADA
# ============================================================

st.info(
    f"📐 Área total calculada das paredes: "
    f"**{area_total:.2f} m²**"
)


# ============================================================
# PREÇOS PADRÃO
# ============================================================

PRECOS_BASE = {

    "perfil": 50.0,

    "guia": 50.0,

    "plywood": 80.0,

    "placa_st": 40.0,

    "placa_cimenticia": 140.0,

    "la_pet": 200.0,

    "parafusos": 35.0,

    "massas": 500.0,

    "telas": 500.0,

    "adesivo": 150.0,

    "manta": 1000.0
}


# ============================================================
# CÁLCULOS DOS MATERIAIS
# ============================================================

qtd_perfil = area_total * 1.25

qtd_guia = area_total * 0.55

qtd_plywood = area_total / 2.2

qtd_placa_st = area_total / 2.4

qtd_cimenticia = area_total / 2.4

qtd_la = area_total / 10.0

qtd_parafuso = area_total * 0.5

qtd_massa = area_total / 30.0

qtd_tela = area_total / 40.0

qtd_adesivo = area_total / 15.0

# ============================================================
# IMPORTANTE:
# MANTA HIDRÓFUGA É DAS PAREDES.
# NÃO TEM RELAÇÃO COM TELHADO.
# ============================================================

qtd_manta = area_total / 50.0


# ============================================================
# LISTA DE MATERIAIS
# ============================================================

lista_materiais = [

    {
        "nome": "Perfil 90x0,80",
        "qtd": qtd_perfil,
        "preco": PRECOS_BASE["perfil"]
    },

    {
        "nome": "Guia Perimetral",
        "qtd": qtd_guia,
        "preco": PRECOS_BASE["guia"]
    },

    {
        "nome": "Plywood 8mm",
        "qtd": qtd_plywood,
        "preco": PRECOS_BASE["plywood"]
    },

    {
        "nome": "Placa ST 12.5mm",
        "qtd": qtd_placa_st,
        "preco": PRECOS_BASE["placa_st"]
    },

    {
        "nome": "Placa Cimentícia 12mm",
        "qtd": qtd_cimenticia,
        "preco": PRECOS_BASE["placa_cimenticia"]
    },

    {
        "nome": "Lã PET",
        "qtd": qtd_la,
        "preco": PRECOS_BASE["la_pet"]
    },

    {
        "nome": "Parafusos (Cento)",
        "qtd": qtd_parafuso,
        "preco": PRECOS_BASE["parafusos"]
    },

    {
        "nome": "Massas (Balde/Saco)",
        "qtd": qtd_massa,
        "preco": PRECOS_BASE["massas"]
    },

    {
        "nome": "Telas (Rolo)",
        "qtd": qtd_tela,
        "preco": PRECOS_BASE["telas"]
    },

    {
        "nome": "Adesivo PU (Cx)",
        "qtd": qtd_adesivo,
        "preco": PRECOS_BASE["adesivo"]
    },

    {
        "nome": "Manta Hidrófuga",
        "qtd": qtd_manta,
        "preco": PRECOS_BASE["manta"]
    },

]


# ============================================================
# BOTÃO CALCULAR PROJETO
# ============================================================

st.markdown("---")

st.subheader("🧮 Cálculo do Projeto")

st.markdown(
    "Confira as dimensões acima e clique no botão abaixo "
    "para confirmar o cálculo e disponibilizar os dados "
    "para a página **Análise**."
)

calcular_projeto = st.button(
    "🧮 CALCULAR PROJETO",
    type="primary",
    use_container_width=True
)


# ============================================================
# CÁLCULO E GRAVAÇÃO DO PROJETO
# ============================================================

if calcular_projeto:

    # --------------------------------------------------------
    # Monta a lista inicial dos materiais
    # --------------------------------------------------------

    dados_calculados = []

    total_materiais_calculado = 0.0

    for mat in lista_materiais:

        quantidade = float(
            round(mat["qtd"], 1)
        )

        preco = float(
            mat["preco"]
        )

        subtotal = (
            quantidade *
            preco
        )

        total_materiais_calculado += subtotal

        dados_calculados.append(
            {
                "Item": mat["nome"],
                "Quantidade": quantidade,
                "Preço Unitário": preco,
                "Total Item": subtotal
            }
        )


    # --------------------------------------------------------
    # Mão de obra padrão
    # --------------------------------------------------------

    mao_de_obra_calculada = 11635.0

    total_geral_calculado = (
        total_materiais_calculado +
        mao_de_obra_calculada
    )


    # --------------------------------------------------------
    # SALVA O PROJETO NO SESSION STATE
    # --------------------------------------------------------
    #
    # ESTE É O PONTO QUE ESTAVA FALTANDO.
    #
    # A página "Análise" poderá encontrar:
    #
    # st.session_state["projeto_calculado"]
    #
    # --------------------------------------------------------

    st.session_state["projeto_calculado"] = {

        "cliente": cliente,

        "data_projeto": data_projeto,

        "comprimento_paredes": comprimento_paredes,

        "pe_direito": pe_direito,

        "area_total": area_total,

        "dados_atualizados": dados_calculados,

        "lista_materiais": dados_calculados,

        "total_materiais": total_materiais_calculado,

        "mao_de_obra": mao_de_obra_calculada,

        "total_geral": total_geral_calculado,

        # informações adicionais para a análise
        "dimensoes": {

            "comprimento_paredes": comprimento_paredes,

            "pe_direito": pe_direito,

            "area_paredes": area_total

        },

        "calculado": True

    }


    # --------------------------------------------------------
    # Também grava chaves individuais para compatibilidade
    # --------------------------------------------------------

    st.session_state["area_total"] = area_total

    st.session_state["comprimento_paredes"] = (
        comprimento_paredes
    )

    st.session_state["pe_direito"] = pe_direito

    st.session_state["dados_atualizados"] = (
        dados_calculados
    )

    st.session_state["total_materiais"] = (
        total_materiais_calculado
    )

    st.session_state["mao_de_obra"] = (
        mao_de_obra_calculada
    )

    st.session_state["total_geral"] = (
        total_geral_calculado
    )

    st.session_state["cliente"] = cliente

    st.session_state["data_projeto"] = data_projeto


    # --------------------------------------------------------
    # Confirmação visual
    # --------------------------------------------------------

    st.success(
        "✅ PROJETO CALCULADO COM SUCESSO! "
        "Os dados já estão disponíveis para a página "
        "📊 Análise."
    )

    st.balloons()


# ============================================================
# VERIFICAÇÃO DO STATUS DO PROJETO
# ============================================================

if "projeto_calculado" in st.session_state:

    projeto = st.session_state["projeto_calculado"]

    if projeto.get("calculado", False):

        st.success(
            f"📊 Projeto pronto para análise — "
            f"{projeto['area_total']:.2f} m² de paredes."
        )


# ============================================================
# SEÇÃO 3 — INSUMOS E AJUSTES
# ============================================================

st.header("📋 Insumos Calculados Automaticamente")

st.markdown(
    "As quantidades e os valores unitários podem ser ajustados."
)

dados_atualizados = []

total_materiais = 0.0

col_grid1, col_grid2 = st.columns(2)


for idx, mat in enumerate(lista_materiais):

    coluna_painel = (
        col_grid1
        if idx % 2 == 0
        else col_grid2
    )

    with coluna_painel:

        st.subheader(
            f"🔹 {mat['nome']}"
        )

        c_qtd, c_prc = st.columns(2)

        with c_qtd:

            nova_qtd = st.number_input(
                f"{mat['nome']} (Qtd)",
                min_value=0.0,
                value=float(
                    round(mat["qtd"], 1)
                ),
                key=f"q_{idx}"
            )

        with c_prc:

            novo_prc = st.number_input(
                f"{mat['nome']} (Preço R$)",
                min_value=0.0,
                value=float(
                    mat["preco"]
                ),
                key=f"p_{idx}"
            )

        subtotal_calculado = (
            nova_qtd *
            novo_prc
        )

        total_materiais += (
            subtotal_calculado
        )

        dados_atualizados.append(
            {
                "Item": mat["nome"],
                "Quantidade": nova_qtd,
                "Preço Unitário": novo_prc,
                "Total Item": subtotal_calculado
            }
        )

        st.write(
            f"**Subtotal do Item:** "
            f"R$ {subtotal_calculado:,.2f}"
        )

        st.write("---")


# ============================================================
# ATUALIZA O PROJETO QUANDO HOUVER ALTERAÇÃO NOS INSUMOS
# ============================================================

mao_de_obra = st.sidebar.number_input(
    "Mão de Obra Geral (R$)",
    min_value=0.0,
    value=11635.0,
    step=100.0
)


# ============================================================
# TOTAL GERAL
# ============================================================

total_geral = (
    total_materiais +
    mao_de_obra
)


# ============================================================
# BOTÃO PARA ATUALIZAR O CÁLCULO
# ============================================================

st.markdown("---")

if st.button(
    "🔄 ATUALIZAR CÁLCULO",
    use_container_width=True
):

    st.session_state["projeto_calculado"] = {

        "cliente": cliente,

        "data_projeto": data_projeto,

        "comprimento_paredes": (
            comprimento_paredes
        ),

        "pe_direito": pe_direito,

        "area_total": area_total,

        "dados_atualizados": (
            dados_atualizados
        ),

        "lista_materiais": (
            dados_atualizados
        ),

        "total_materiais": (
            total_materiais
        ),

        "mao_de_obra": (
            mao_de_obra
        ),

        "total_geral": (
            total_geral
        ),

        "dimensoes": {

            "comprimento_paredes": (
                comprimento_paredes
            ),

            "pe_direito": (
                pe_direito
            ),

            "area_paredes": (
                area_total
            )

        },

        "calculado": True

    }

    st.session_state["dados_atualizados"] = (
        dados_atualizados
    )

    st.session_state["total_materiais"] = (
        total_materiais
    )

    st.session_state["mao_de_obra"] = (
        mao_de_obra
    )

    st.session_state["total_geral"] = (
        total_geral
    )

    st.success(
        "✅ Cálculo atualizado. "
        "A página Análise já pode utilizar estes dados."
    )


# ============================================================
# RESUMO CONSOLIDADO
# ============================================================

st.header(
    "📊 Resumo Consolidado do Orçamento"
)

df_resumo = pd.DataFrame(
    dados_atualizados
)

st.dataframe(
    df_resumo.style.format(
        {
            "Preço Unitário": "R$ {:.2f}",
            "Total Item": "R$ {:.2f}"
        }
    ),
    use_container_width=True
)


# ============================================================
# SIDEBAR — CUSTOS
# ============================================================

st.sidebar.header(
    "💰 Custos de Instalação"
)


st.sidebar.markdown("---")


st.sidebar.metric(
    label="Total Materiais",
    value=f"R$ {total_materiais:,.2f}"
)


st.sidebar.metric(
    label="Total Mão de Obra",
    value=f"R$ {mao_de_obra:,.2f}"
)


st.sidebar.subheader(
    f"Total Geral: R$ {total_geral:,.2f}"
)


# ============================================================
# FUNÇÃO PARA GERAR EXCEL
# ============================================================

def gerar_excel():

    wb = Workbook()

    # ========================================================
    # ABA ORÇAMENTO
    # ========================================================

    ws = wb.active

    ws.title = "Orçamento"


    larguras = {

        "A": 28,

        "B": 18,

        "C": 20,

        "D": 20,

        "E": 22,

        "F": 22,

    }


    for coluna, largura in larguras.items():

        ws.column_dimensions[
            coluna
        ].width = largura


    # ========================================================
    # ESTILOS
    # ========================================================

    fundo_titulo = PatternFill(
        "solid",
        fgColor="17202A"
    )

    fundo_secao = PatternFill(
        "solid",
        fgColor="34495E"
    )

    fundo_cabecalho = PatternFill(
        "solid",
        fgColor="D9E2F3"
    )

    fundo_total = PatternFill(
        "solid",
        fgColor="E2F0D9"
    )

    branco = "FFFFFF"


    fonte_titulo = Font(
        name="Calibri",
        size=20,
        bold=True,
        color=branco
    )

    fonte_secao = Font(
        name="Calibri",
        size=12,
        bold=True,
        color=branco
    )

    fonte_cabecalho = Font(
        name="Calibri",
        size=11,
        bold=True
    )

    fonte_normal = Font(
        name="Calibri",
        size=11
    )

    fonte_total = Font(
        name="Calibri",
        size=13,
        bold=True
    )


    borda_fina = Border(

        left=Side(
            style="thin",
            color="B7B7B7"
        ),

        right=Side(
            style="thin",
            color="B7B7B7"
        ),

        top=Side(
            style="thin",
            color="B7B7B7"
        ),

        bottom=Side(
            style="thin",
            color="B7B7B7"
        ),

    )


    # ========================================================
    # TÍTULO
    # ========================================================

    ws.merge_cells("A1:F2")

    ws["A1"] = (
        "ORÇAMENTO STEEL FRAMING"
    )

    ws["A1"].font = fonte_titulo

    ws["A1"].fill = fundo_titulo

    ws["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )


    for row in ws["A1:F2"]:

        for cell in row:

            cell.fill = fundo_titulo


    # ========================================================
    # LOGO
    # ========================================================

    ws.merge_cells("A4:B8")

    ws["A4"] = (
        "INSIRA AQUI\n"
        "O LOGO DA SUA EMPRESA"
    )

    ws["A4"].alignment = Alignment(
        horizontal="center",
        vertical="center",
        wrap_text=True
    )

    ws["A4"].font = Font(
        size=12,
        bold=True,
        color="666666"
    )

    ws["A4"].fill = PatternFill(
        "solid",
        fgColor="F2F2F2"
    )


    for row in ws["A4:B8"]:

        for cell in row:

            cell.border = borda_fina


    # ========================================================
    # DADOS DA EMPRESA
    # ========================================================

    ws.merge_cells("C4:F4")

    ws["C4"] = "DADOS DA EMPRESA"

    ws["C4"].fill = fundo_secao

    ws["C4"].font = fonte_secao

    ws["C4"].alignment = Alignment(
        horizontal="center"
    )


    dados_empresa = [

        (
            "Empresa",
            "Digite o nome da sua empresa"
        ),

        (
            "CNPJ",
            "Digite o CNPJ"
        ),

        (
            "Telefone / WhatsApp",
            "Digite o telefone"
        ),

        (
            "E-mail",
            "Digite o e-mail"
        ),

    ]


    linha = 5


    for campo, valor in dados_empresa:

        ws[f"C{linha}"] = campo

        ws[f"C{linha}"].font = (
            fonte_cabecalho
        )


        ws.merge_cells(

            start_row=linha,

            start_column=4,

            end_row=linha,

            end_column=6

        )


        ws[f"D{linha}"] = valor

        ws[f"D{linha}"].font = (
            fonte_normal
        )


        linha += 1


    # ========================================================
    # IDENTIFICAÇÃO DO PROJETO
    # ========================================================

    ws.merge_cells("A10:F10")

    ws["A10"] = (
        "IDENTIFICAÇÃO DO PROJETO"
    )

    ws["A10"].fill = fundo_secao

    ws["A10"].font = fonte_secao

    ws["A10"].alignment = Alignment(
        horizontal="center"
    )


    dados_projeto = [

        (
            "Cliente",
            cliente
        ),

        (
            "Data do Orçamento",
            data_projeto.strftime(
                "%d/%m/%Y"
            )
        ),

        (
            "Comprimento das Paredes",
            f"{comprimento_paredes:.2f} m linear"
        ),

        (
            "Pé Direito",
            f"{pe_direito:.2f} m"
        ),

        (
            "Área das Paredes",
            f"{area_total:.2f} m²"
        ),

    ]


    linha = 11


    for campo, valor in dados_projeto:

        ws[f"A{linha}"] = campo

        ws[f"A{linha}"].font = (
            fonte_cabecalho
        )


        ws.merge_cells(

            start_row=linha,

            start_column=2,

            end_row=linha,

            end_column=6

        )


        ws[f"B{linha}"] = valor

        linha += 1


    # ========================================================
    # MATERIAIS
    # ========================================================

    linha_inicio_materiais = 18


    ws.merge_cells(

        start_row=linha_inicio_materiais,

        start_column=1,

        end_row=linha_inicio_materiais,

        end_column=6

    )


    ws.cell(
        linha_inicio_materiais,
        1
    ).value = (
        "QUANTITATIVO DE MATERIAIS"
    )


    ws.cell(
        linha_inicio_materiais,
        1
    ).fill = fundo_secao


    ws.cell(
        linha_inicio_materiais,
        1
    ).font = fonte_secao


    ws.cell(
        linha_inicio_materiais,
        1
    ).alignment = Alignment(
        horizontal="center"
    )


    cabecalhos = [

        "Material",

        "Quantidade",

        "Unidade",

        "Preço Unitário",

        "Total",

        "Observação",

    ]


    linha_cabecalho = (
        linha_inicio_materiais + 1
    )


    for col, texto in enumerate(
        cabecalhos,
        start=1
    ):

        cell = ws.cell(
            linha_cabecalho,
            col
        )

        cell.value = texto

        cell.fill = fundo_cabecalho

        cell.font = fonte_cabecalho

        cell.border = borda_fina

        cell.alignment = Alignment(
            horizontal="center"
        )


    linha = (
        linha_cabecalho + 1
    )


    for item in dados_atualizados:

        ws.cell(
            linha,
            1
        ).value = item["Item"]


        ws.cell(
            linha,
            2
        ).value = item["Quantidade"]


        ws.cell(
            linha,
            3
        ).value = "un."


        ws.cell(
            linha,
            4
        ).value = item[
            "Preço Unitário"
        ]


        ws.cell(
            linha,
            5
        ).value = (
            f"=B{linha}*D{linha}"
        )


        ws.cell(
            linha,
            6
        ).value = (
            "Quantidade e preço editáveis"
        )


        for col in range(1, 7):

            cell = ws.cell(
                linha,
                col
            )

            cell.border = borda_fina

            cell.font = fonte_normal


        ws.cell(
            linha,
            2
        ).number_format = "0.00"


        ws.cell(
            linha,
            4
        ).number_format = (
            'R$ #,##0.00'
        )


        ws.cell(
            linha,
            5
        ).number_format = (
            'R$ #,##0.00'
        )


        linha += 1


    # ========================================================
    # TOTAIS
    # ========================================================

    linha_total_materiais = (
        linha + 1
    )


    ws.merge_cells(

        start_row=linha_total_materiais,

        start_column=1,

        end_row=linha_total_materiais,

        end_column=4

    )


    ws.cell(
        linha_total_materiais,
        1
    ).value = (
        "TOTAL DE MATERIAIS"
    )


    ws.cell(
        linha_total_materiais,
        1
    ).font = fonte_total


    ws.cell(
        linha_total_materiais,
        1
    ).fill = fundo_total


    primeira_linha = (
        linha_cabecalho + 1
    )

    ultima_linha = (
        linha - 1
    )


    ws.cell(
        linha_total_materiais,
        5
    ).value = (
        f"=SUM(E{primeira_linha}:"
        f"E{ultima_linha})"
    )


    ws.cell(
        linha_total_materiais,
        5
    ).font = fonte_total


    ws.cell(
        linha_total_materiais,
        5
    ).fill = fundo_total


    ws.cell(
        linha_total_materiais,
        5
    ).number_format = (
        'R$ #,##0.00'
    )


    # ========================================================
    # MÃO DE OBRA
    # ========================================================

    linha_mao_obra = (
        linha_total_materiais + 1
    )


    ws.merge_cells(

        start_row=linha_mao_obra,

        start_column=1,

        end_row=linha_mao_obra,

        end_column=4

    )


    ws.cell(
        linha_mao_obra,
        1
    ).value = "MÃO DE OBRA"


    ws.cell(
        linha_mao_obra,
        1
    ).font = fonte_total


    ws.cell(
        linha_mao_obra,
        1
    ).fill = fundo_total


    ws.cell(
        linha_mao_obra,
        5
    ).value = mao_de_obra


    ws.cell(
        linha_mao_obra,
        5
    ).font = fonte_total


    ws.cell(
        linha_mao_obra,
        5
    ).fill = fundo_total


    ws.cell(
        linha_mao_obra,
        5
    ).number_format = (
        'R$ #,##0.00'
    )


    # ========================================================
    # TOTAL GERAL
    # ========================================================

    linha_total_geral = (
        linha_mao_obra + 1
    )


    ws.merge_cells(

        start_row=linha_total_geral,

        start_column=1,

        end_row=linha_total_geral,

        end_column=4

    )


    ws.cell(
        linha_total_geral,
        1
    ).value = "TOTAL GERAL"


    ws.cell(
        linha_total_geral,
        1
    ).font = Font(
        size=15,
        bold=True
    )


    ws.cell(
        linha_total_geral,
        5
    ).value = (
        f"=E{linha_total_materiais}"
        f"+E{linha_mao_obra}"
    )


    ws.cell(
        linha_total_geral,
        5
    ).font = Font(
        size=15,
        bold=True
    )


    ws.cell(
        linha_total_geral,
        5
    ).number_format = (
        'R$ #,##0.00'
    )


    for col in range(1, 6):

        ws.cell(
            linha_total_geral,
            col
        ).fill = PatternFill(
            "solid",
            fgColor="C6E0B4"
        )


    # ========================================================
    # CONDIÇÕES COMERCIAIS
    # ========================================================

    linha_condicoes = (
        linha_total_geral + 3
    )


    ws.merge_cells(

        start_row=linha_condicoes,

        start_column=1,

        end_row=linha_condicoes,

        end_column=6

    )


    ws.cell(
        linha_condicoes,
        1
    ).value = (
        "CONDIÇÕES COMERCIAIS / OBSERVAÇÕES"
    )


    ws.cell(
        linha_condicoes,
        1
    ).fill = fundo_secao


    ws.cell(
        linha_condicoes,
        1
    ).font = fonte_secao


    for i in range(1, 4):

        linha_obs = (
            linha_condicoes + i
        )


        ws.merge_cells(

            start_row=linha_obs,

            start_column=1,

            end_row=linha_obs,

            end_column=6

        )


        ws.cell(
            linha_obs,
            1
        ).value = (
            "Digite aqui suas condições "
            "comerciais e observações."
        )


        ws.cell(
            linha_obs,
            1
        ).alignment = Alignment(
            vertical="top",
            wrap_text=True
        )


    # ========================================================
    # CONFIGURAÇÕES
    # ========================================================

    ws.freeze_panes = "A20"

    ws.sheet_view.showGridLines = False

    ws.page_setup.orientation = (
        "landscape"
    )

    ws.page_setup.fitToWidth = 1

    ws.page_setup.fitToHeight = 0


    # ========================================================
    # ABA MEMÓRIA DE CÁLCULO
    # ========================================================

    memoria = wb.create_sheet(
        "Memória de Cálculo"
    )


    memoria.column_dimensions[
        "A"
    ].width = 35

    memoria.column_dimensions[
        "B"
    ].width = 20

    memoria.column_dimensions[
        "C"
    ].width = 45

    memoria.column_dimensions[
        "D"
    ].width = 20


    memoria.merge_cells("A1:D2")


    memoria["A1"] = (
        "MEMÓRIA DE CÁLCULO"
    )


    memoria["A1"].font = (
        fonte_titulo
    )

    memoria["A1"].fill = (
        fundo_titulo
    )

    memoria["A1"].alignment = Alignment(
        horizontal="center",
        vertical="center"
    )


    for row in memoria["A1:D2"]:

        for cell in row:

            cell.fill = fundo_titulo


    memoria["A4"] = "Parâmetro"

    memoria["B4"] = "Valor"

    memoria["C4"] = "Critério"

    memoria["D4"] = "Unidade"


    for col in range(1, 5):

        cell = memoria.cell(
            4,
            col
        )

        cell.fill = fundo_cabecalho

        cell.font = fonte_cabecalho

        cell.border = borda_fina


    parametros = [

        (
            "Comprimento das Paredes",
            comprimento_paredes,
            "Informado pelo usuário",
            "m linear"
        ),

        (
            "Pé Direito",
            pe_direito,
            "Informado pelo usuário",
            "m"
        ),

        (
            "Área das Paredes",
            area_total,
            "Comprimento × Pé Direito",
            "m²"
        ),

        (
            "Perfil 90x0,80",
            qtd_perfil,
            "Área × 1,25",
            "un."
        ),

        (
            "Guia Perimetral",
            qtd_guia,
            "Área × 0,55",
            "un."
        ),

        (
            "Plywood 8mm",
            qtd_plywood,
            "Área ÷ 2,20",
            "un."
        ),

        (
            "Placa ST 12.5mm",
            qtd_placa_st,
            "Área ÷ 2,40",
            "un."
        ),

        (
            "Placa Cimentícia 12mm",
            qtd_cimenticia,
            "Área ÷ 2,40",
            "un."
        ),

        (
            "Lã PET",
            qtd_la,
            "Área ÷ 10",
            "un."
        ),

        (
            "Parafusos",
            qtd_parafuso,
            "Área × 0,50",
            "centos"
        ),

        (
            "Massas",
            qtd_massa,
            "Área ÷ 30",
            "un."
        ),

        (
            "Telas",
            qtd_tela,
            "Área ÷ 40",
            "rolos"
        ),

        (
            "Adesivo PU",
            qtd_adesivo,
            "Área ÷ 15",
            "caixas"
        ),

        (
            "Manta Hidrófuga",
            qtd_manta,
            "Área das Paredes ÷ 50",
            "un."
        ),

    ]


    linha = 5


    for parametro, valor, criterio, unidade in parametros:

        memoria.cell(
            linha,
            1
        ).value = parametro


        memoria.cell(
            linha,
            2
        ).value = valor


        memoria.cell(
            linha,
            3
        ).value = criterio


        memoria.cell(
            linha,
            4
        ).value = unidade


        for col in range(1, 5):

            memoria.cell(
                linha,
                col
            ).border = borda_fina


        linha += 1


    memoria["A22"] = (
        "TOTAL MATERIAIS"
    )

    memoria["B22"] = (
        total_materiais
    )


    memoria["A23"] = (
        "MÃO DE OBRA"
    )

    memoria["B23"] = (
        mao_de_obra
    )


    memoria["A24"] = (
        "TOTAL GERAL"
    )

    memoria["B24"] = (
        total_geral
    )


    for linha_total in [
        22,
        23,
        24
    ]:

        memoria.cell(
            linha_total,
            1
        ).font = fonte_total


        memoria.cell(
            linha_total,
            2
        ).font = fonte_total


        memoria.cell(
            linha_total,
            2
        ).number_format = (
            'R$ #,##0.00'
        )


    memoria.sheet_view.showGridLines = False


    # ========================================================
    # GERAR ARQUIVO
    # ========================================================

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    return output.getvalue()


# ============================================================
# EXPORTAÇÃO
# ============================================================

st.markdown("---")

st.subheader(
    "📥 Exportação do Orçamento"
)


st.info(
    "O Excel será gerado sem o logo da Dryarte. "
    "O arquivo possui uma área reservada para você "
    "inserir o logo e os dados da sua própria empresa."
)


excel_data = gerar_excel()


nome_cliente = (

    cliente
    .strip()
    .replace(" ", "_")
    .replace("/", "_")
    .replace("\\", "_")

)


nome_arquivo = (

    f"orcamento_steel_framing_"

    f"{nome_cliente}_"

    f"{data_projeto.strftime('%Y-%m-%d')}.xlsx"

)


st.download_button(

    label=(
        "📊 Baixar Orçamento Profissional "
        "em Excel (.xlsx)"
    ),

    data=excel_data,

    file_name=nome_arquivo,

    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    ),

    use_container_width=True,

)


st.caption(
    "O arquivo Excel pode ser editado posteriormente "
    "no Microsoft Excel ou em programas compatíveis "
    "com .xlsx."
)
