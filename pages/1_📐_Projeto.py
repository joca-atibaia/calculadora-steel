import streamlit as st
import pandas as pd
from datetime import date

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
        value=10,
        step=1,
    )

    prazo_execucao = st.text_input(
        "Prazo estimado de execução",
        placeholder="Ex.: 30 dias úteis",
    )


with col2:

    condicao_pagamento = st.text_input(
        "Condição de pagamento",
        placeholder="Ex.: 50% entrada + 50% na entrega",
    )

    forma_pagamento = st.text_input(
        "Forma de pagamento",
        placeholder="Ex.: Pix, transferência ou boleto",
    )


observacoes_comerciais = st.text_area(
    "Inclusões / observações comerciais",
    placeholder=(
        "Descreva inclusões, exclusões, condições "
        "de fornecimento, transporte, prazo etc."
    ),
)


st.divider()


# ============================================================
# DIMENSÕES DO PROJETO
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


st.divider()


# ============================================================
# PREÇOS DOS MATERIAIS
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


st.session_state["precos"] = precos_atualizados


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
        "antes da fabricação; orçamento baseado nas "
        "informações fornecidas pelo cliente."
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
    # CABEÇALHO DO DOCUMENTO
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
    # RESUMO DO PROJETO
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
    # QUANTITATIVO DE MATERIAIS
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


    # ========================================================
    # VALOR TOTAL
    # ========================================================

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
    # MÃO DE OBRA DETALHADA
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
                <strong>Inclusões / Observações comerciais</strong><br><br>
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
    # ASSINATURA
    # ========================================================

    st.markdown(
        """
        <div class="assinatura">

            <div class="linha-assinatura"></div>

            <strong>
                Responsável pelo orçamento
            </strong>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # BOTÕES — PREPARAÇÃO PARA PDF / EXCEL
    # ========================================================

    st.divider()

    st.subheader(
        "📤 Exportação do orçamento"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.button(
            "📄 GERAR PDF",
            use_container_width=True,
            disabled=True,
            help=(
                "Será ativado na próxima etapa."
            ),
        )


    with col2:

        st.button(
            "📊 EXPORTAR EXCEL",
            use_container_width=True,
            disabled=True,
            help=(
                "Será ativado na próxima etapa."
            ),
        )


    st.caption(
        "PDF e Excel serão implementados na próxima etapa, "
        "sem alteração do motor de cálculo."
    )
