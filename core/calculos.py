"""
📊 ANÁLISE PROFISSIONAL DO PROJETO

Calculadora Profissional de Steel Framing
Versão 6D

Esta página utiliza o motor de cálculo existente em:

    core/calculos.py

Objetivos:
    • Analisar custos do projeto
    • Mostrar custo por m²
    • Comparar materiais, massas/telas e mão de obra
    • Identificar materiais de maior impacto
    • Mostrar participação percentual dos custos
    • Apresentar indicadores gerenciais
    • Permitir exportação da análise
"""

import streamlit as st
import pandas as pd

from core.calculos import (
    calcular_projeto,
    calcular_indicadores_projeto,
)


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Análise | Calculadora Steel Framing",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# ESTILO
# ============================================================

st.markdown(
    """
    <style>

    .titulo-principal {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitulo {
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .card-analise {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        background-color: rgba(128,128,128,0.05);
        margin-bottom: 10px;
    }

    .card-titulo {
        font-size: 0.9rem;
        color: #777;
        margin-bottom: 4px;
    }

    .card-valor {
        font-size: 1.65rem;
        font-weight: 700;
    }

    .destaque {
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #555;
        background-color: rgba(128,128,128,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES DA INTERFACE
# ============================================================

def moeda(valor):
    """Formata número como moeda brasileira."""
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        valor = 0.0

    return (
        "R$ "
        + f"{valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def numero(valor, casas=2):
    """Formata número."""
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        valor = 0.0

    return f"{valor:,.{casas}f}".replace(
        ",", "X"
    ).replace(
        ".", ","
    ).replace(
        "X", "."
    )


def percentual(valor):
    """Formata percentual."""
    try:
        valor = float(valor)
    except (TypeError, ValueError):
        valor = 0.0

    return f"{valor:.1f}%".replace(".", ",")


def obter_estado(chaves, padrao=None):
    """
    Procura um valor no session_state utilizando
    várias possibilidades de nome.

    Isso deixa a página compatível com diferentes
    versões da interface principal.
    """

    for chave in chaves:

        if chave in st.session_state:

            valor = st.session_state.get(chave)

            if valor is not None:
                return valor

    return padrao


def converter_float(valor, padrao=0.0):
    """Conversão segura para float."""

    if valor is None:
        return padrao

    try:
        return float(valor)
    except (TypeError, ValueError):
        return padrao


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    '<div class="titulo-principal">'
    '📊 Análise Profissional'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitulo">'
    'Análise financeira e quantitativa do projeto '
    'de Steel Framing'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# RECUPERAÇÃO DO PROJETO
# ============================================================

projeto_existente = obter_estado(
    [
        "projeto",
        "resultado_projeto",
        "calculo_projeto",
        "projeto_calculado",
        "resultado",
    ],
    None,
)


# ============================================================
# OBTENÇÃO DAS DIMENSÕES
# ============================================================

comprimento_estado = obter_estado(
    [
        "comprimento",
        "comprimento_projeto",
        "dim_comprimento",
    ],
    None,
)

altura_estado = obter_estado(
    [
        "altura",
        "altura_projeto",
        "dim_altura",
    ],
    None,
)


# ============================================================
# SE JÁ EXISTIR PROJETO CALCULADO
# ============================================================

if isinstance(projeto_existente, dict):

    if "area" in projeto_existente:

        projeto = projeto_existente

    else:

        projeto = None

else:

    projeto = None


# ============================================================
# SE NÃO EXISTIR PROJETO
# ============================================================

if projeto is None:

    st.info(
        "Nenhum cálculo completo foi encontrado "
        "automaticamente. Informe as dimensões abaixo "
        "para gerar a análise."
    )

    col1, col2 = st.columns(2)

    with col1:

        comprimento = st.number_input(
            "Comprimento do projeto (m)",
            min_value=0.01,
            value=30.0
            if comprimento_estado is None
            else converter_float(
                comprimento_estado,
                30.0,
            ),
            step=0.10,
            format="%.2f",
        )

    with col2:

        altura = st.number_input(
            "Altura do projeto (m)",
            min_value=0.01,
            value=1.0
            if altura_estado is None
            else converter_float(
                altura_estado,
                1.0,
            ),
            step=0.10,
            format="%.2f",
        )

    st.markdown("---")

    if st.button(
        "📊 Gerar análise",
        type="primary",
        width="stretch",
    ):

        try:

            projeto = calcular_projeto(
                comprimento=comprimento,
                altura=altura,
            )

            st.session_state[
                "resultado_projeto"
            ] = projeto

            st.rerun()

        except Exception as erro:

            st.error(
                "Não foi possível calcular o projeto."
            )

            st.exception(erro)

            st.stop()

    st.stop()


# ============================================================
# VALIDAÇÃO DO PROJETO
# ============================================================

try:

    area = converter_float(
        projeto.get("area", 0.0)
    )

    subtotal_materiais = converter_float(
        projeto.get(
            "subtotal_materiais",
            0.0,
        )
    )

    massas_telas = converter_float(
        projeto.get(
            "massas_telas",
            0.0,
        )
    )

    custo_geral = converter_float(
        projeto.get(
            "custo_geral",
            0.0,
        )
    )

    mao_de_obra = projeto.get(
        "mao_de_obra",
        {},
    )

    if not isinstance(mao_de_obra, dict):
        mao_de_obra = {}

    custo_mao_obra = converter_float(
        mao_de_obra.get(
            "custo",
            0.0,
        )
    )

    dias_mao_obra = converter_float(
        mao_de_obra.get(
            "dias",
            0.0,
        )
    )

    diaria = converter_float(
        mao_de_obra.get(
            "diaria",
            0.0,
        )
    )

except Exception as erro:

    st.error(
        "O resultado do projeto possui "
        "uma estrutura incompatível com a análise."
    )

    st.exception(erro)

    st.stop()


# ============================================================
# INDICADORES
# ============================================================

indicadores = calcular_indicadores_projeto(
    projeto
)

custo_por_m2 = converter_float(
    indicadores.get(
        "custo_por_m2",
        0.0,
    )
)

pct_materiais = converter_float(
    indicadores.get(
        "percentual_materiais",
        0.0,
    )
)

pct_massas = converter_float(
    indicadores.get(
        "percentual_massas_telas",
        0.0,
    )
)

pct_mao_obra = converter_float(
    indicadores.get(
        "percentual_mao_de_obra",
        0.0,
    )
)


# ============================================================
# CARDS PRINCIPAIS
# ============================================================

st.subheader("📌 Indicadores principais")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Área do projeto",
        f"{numero(area)} m²",
    )

with c2:

    st.metric(
        "Custo geral",
        moeda(custo_geral),
    )

with c3:

    st.metric(
        "Custo por m²",
        moeda(custo_por_m2),
    )

with c4:

    st.metric(
        "Mão de obra",
        moeda(custo_mao_obra),
    )


# ============================================================
# COMPOSIÇÃO DO CUSTO
# ============================================================

st.markdown("---")

st.subheader("💰 Composição do custo")

df_composicao = pd.DataFrame(
    {
        "Categoria": [
            "Materiais",
            "Massas e Telas",
            "Mão de Obra",
        ],
        "Valor": [
            subtotal_materiais,
            massas_telas,
            custo_mao_obra,
        ],
        "Participação": [
            pct_materiais,
            pct_massas,
            pct_mao_obra,
        ],
    }
)


col_grafico, col_tabela = st.columns(
    [1.4, 1]
)


with col_grafico:

    st.bar_chart(
        df_composicao.set_index(
            "Categoria"
        )["Valor"],
        width="stretch",
    )


with col_tabela:

    tabela_composicao = df_composicao.copy()

    tabela_composicao["Valor"] = (
        tabela_composicao["Valor"]
        .apply(moeda)
    )

    tabela_composicao["Participação"] = (
        tabela_composicao["Participação"]
        .apply(percentual)
    )

    st.dataframe(
        tabela_composicao,
        width="stretch",
        hide_index=True,
    )


# ============================================================
# MATERIAIS
# ============================================================

st.markdown("---")

st.subheader("🧱 Análise dos materiais")

materiais = projeto.get(
    "materiais",
    {}
)

if not isinstance(materiais, dict):
    materiais = {}


linhas_materiais = []


for nome, item in materiais.items():

    if not isinstance(item, dict):
        continue

    quantidade = converter_float(
        item.get(
            "quantidade",
            0.0,
        )
    )

    quantidade_automatica = converter_float(
        item.get(
            "quantidade_automatica",
            0.0,
        )
    )

    preco_unitario = converter_float(
        item.get(
            "preco_unitario",
            0.0,
        )
    )

    custo = converter_float(
        item.get(
            "custo",
            0.0,
        )
    )

    categoria = item.get(
        "categoria",
        "Outros",
    )

    unidade = item.get(
        "unidade",
        "un",
    )

    origem = item.get(
        "origem_quantidade",
        "automática",
    )

    pct = (
        (custo / subtotal_materiais) * 100
        if subtotal_materiais > 0
        else 0.0
    )

    linhas_materiais.append(
        {
            "Material": nome,
            "Categoria": categoria,
            "Quantidade": quantidade,
            "Unidade": unidade,
            "Preço unitário": preco_unitario,
            "Custo": custo,
            "Participação": pct,
            "Origem": origem,
        }
    )


df_materiais = pd.DataFrame(
    linhas_materiais
)


# ============================================================
# ORDENAÇÃO
# ============================================================

if not df_materiais.empty:

    df_materiais = df_materiais.sort_values(
        "Custo",
        ascending=False,
    ).reset_index(drop=True)


# ============================================================
# TABELA DE MATERIAIS
# ============================================================

if df_materiais.empty:

    st.warning(
        "Nenhum material ativo foi encontrado."
    )

else:

    tabela_materiais = df_materiais.copy()

    tabela_materiais["Quantidade"] = (
        tabela_materiais["Quantidade"]
        .apply(
            lambda x: numero(x, 2)
        )
    )

    tabela_materiais["Preço unitário"] = (
        tabela_materiais["Preço unitário"]
        .apply(moeda)
    )

    tabela_materiais["Custo"] = (
        tabela_materiais["Custo"]
        .apply(moeda)
    )

    tabela_materiais["Participação"] = (
        tabela_materiais["Participação"]
        .apply(percentual)
    )

    st.dataframe(
        tabela_materiais,
        width="stretch",
        hide_index=True,
    )


# ============================================================
# TOP MATERIAIS
# ============================================================

if not df_materiais.empty:

    st.markdown("---")

    st.subheader(
        "🏆 Materiais de maior impacto"
    )

    top = df_materiais.head(5).copy()

    top["Custo"] = top["Custo"].apply(
        moeda
    )

    top["Participação"] = (
        top["Participação"]
        .apply(percentual)
    )

    st.dataframe(
        top[
            [
                "Material",
                "Categoria",
                "Custo",
                "Participação",
            ]
        ],
        width="stretch",
        hide_index=True,
    )


# ============================================================
# GRÁFICO DOS MATERIAIS
# ============================================================

if not df_materiais.empty:

    st.markdown("---")

    st.subheader(
        "📊 Distribuição do custo dos materiais"
    )

    grafico_materiais = (
        df_materiais[
            [
                "Material",
                "Custo",
            ]
        ]
        .set_index("Material")
        .head(10)
    )

    st.bar_chart(
        grafico_materiais,
        width="stretch",
    )


# ============================================================
# ANÁLISE POR CATEGORIA
# ============================================================

if not df_materiais.empty:

    st.markdown("---")

    st.subheader(
        "📦 Custo por categoria"
    )

    df_categoria = (
        df_materiais
        .groupby(
            "Categoria",
            as_index=False,
        )["Custo"]
        .sum()
        .sort_values(
            "Custo",
            ascending=False,
        )
    )

    df_categoria["Participação"] = (
        df_categoria["Custo"]
        .apply(
            lambda x:
            (
                x / subtotal_materiais * 100
                if subtotal_materiais > 0
                else 0.0
            )
        )
    )

    col_cat_grafico, col_cat_tabela = (
        st.columns([1.4, 1])
    )

    with col_cat_grafico:

        st.bar_chart(
            df_categoria.set_index(
                "Categoria"
            )["Custo"],
            width="stretch",
        )

    with col_cat_tabela:

        tabela_categoria = (
            df_categoria.copy()
        )

        tabela_categoria["Custo"] = (
            tabela_categoria["Custo"]
            .apply(moeda)
        )

        tabela_categoria["Participação"] = (
            tabela_categoria["Participação"]
            .apply(percentual)
        )

        st.dataframe(
            tabela_categoria,
            width="stretch",
            hide_index=True,
        )


# ============================================================
# MÃO DE OBRA
# ============================================================

st.markdown("---")

st.subheader("👷 Análise da mão de obra")

m1, m2, m3 = st.columns(3)

with m1:

    st.metric(
        "Dias calculados",
        f"{numero(dias_mao_obra)} dias",
    )

with m2:

    st.metric(
        "Diária",
        moeda(diaria),
    )

with m3:

    st.metric(
        "Custo da mão de obra",
        moeda(custo_mao_obra),
    )


# ============================================================
# CUSTO POR M²
# ============================================================

st.markdown("---")

st.subheader("📐 Indicadores por metro quadrado")

custo_material_m2 = (
    subtotal_materiais / area
    if area > 0
    else 0.0
)

custo_massas_m2 = (
    massas_telas / area
    if area > 0
    else 0.0
)

custo_mao_obra_m2 = (
    custo_mao_obra / area
    if area > 0
    else 0.0
)


p1, p2, p3, p4 = st.columns(4)

with p1:

    st.metric(
        "Materiais / m²",
        moeda(custo_material_m2),
    )

with p2:

    st.metric(
        "Massas e Telas / m²",
        moeda(custo_massas_m2),
    )

with p3:

    st.metric(
        "Mão de obra / m²",
        moeda(custo_mao_obra_m2),
    )

with p4:

    st.metric(
        "Total / m²",
        moeda(custo_por_m2),
    )


# ============================================================
# DIAGNÓSTICO GERENCIAL
# ============================================================

st.markdown("---")

st.subheader("🔎 Diagnóstico do orçamento")


if custo_geral <= 0:

    st.warning(
        "O custo geral do projeto está zerado. "
        "Verifique preços e quantidades."
    )

else:

    if pct_materiais >= 60:

        mensagem = (
            "Os materiais representam a maior parcela "
            "do orçamento. Pequenas alterações nos preços "
            "dos insumos podem produzir impacto "
            "significativo no custo final."
        )

    elif pct_mao_obra >= 50:

        mensagem = (
            "A mão de obra representa a maior parcela "
            "do orçamento. Ganhos de produtividade "
            "podem produzir impacto relevante "
            "no custo final."
        )

    elif pct_massas >= 20:

        mensagem = (
            "Massas e Telas possuem participação "
            "relevante no orçamento. Vale revisar "
            "o percentual utilizado ou o valor manual."
        )

    else:

        mensagem = (
            "A composição do orçamento apresenta "
            "distribuição relativamente equilibrada "
            "entre materiais, massas/telas e mão de obra."
        )

    st.markdown(
        f"""
        <div class="destaque">
            <strong>📌 Leitura gerencial</strong><br><br>
            {mensagem}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RESUMO FINANCEIRO
# ============================================================

st.markdown("---")

st.subheader("💼 Resumo financeiro")

df_resumo = pd.DataFrame(
    {
        "Indicador": [
            "Área do projeto",
            "Materiais",
            "Massas e Telas",
            "Mão de Obra",
            "Custo Geral",
            "Custo por m²",
        ],
        "Valor": [
            f"{numero(area)} m²",
            moeda(subtotal_materiais),
            moeda(massas_telas),
            moeda(custo_mao_obra),
            moeda(custo_geral),
            moeda(custo_por_m2),
        ],
    }
)

st.dataframe(
    df_resumo,
    width="stretch",
    hide_index=True,
)


# ============================================================
# EXPORTAÇÃO
# ============================================================

st.markdown("---")

st.subheader("📥 Exportar análise")


# ------------------------------------------------------------
# CSV DA COMPOSIÇÃO
# ------------------------------------------------------------

csv_composicao = df_composicao.to_csv(
    index=False
).encode("utf-8-sig")


st.download_button(
    label="📄 Baixar composição em CSV",
    data=csv_composicao,
    file_name="analise_composicao_steel_framing.csv",
    mime="text/csv",
    width="stretch",
)


# ------------------------------------------------------------
# CSV DOS MATERIAIS
# ------------------------------------------------------------

if not df_materiais.empty:

    csv_materiais = (
        df_materiais
        .to_csv(index=False)
        .encode("utf-8-sig")
    )

    st.download_button(
        label="🧱 Baixar materiais em CSV",
        data=csv_materiais,
        file_name="analise_materiais_steel_framing.csv",
        mime="text/csv",
        width="stretch",
    )


# ============================================================
# INFORMAÇÕES TÉCNICAS
# ============================================================

with st.expander(
    "ℹ️ Como esta análise é calculada"
):

    st.markdown(
        """
        ### Área

        A área é calculada pelo motor:

        **comprimento × altura**

        ### Materiais

        Cada material utiliza o coeficiente
        cadastrado no banco de dados.

        Quando não existe quantidade manual:

        **quantidade = (área ÷ área de referência)
        × coeficiente**

        ### Custo dos materiais

        **quantidade × preço unitário**

        ### Massas e Telas

        Quando não existe valor manual:

        **subtotal dos materiais × percentual
        configurado**

        ### Mão de obra

        O motor calcula os dias proporcionalmente
        à área:

        **dias = (área ÷ área de referência)
        × dias de referência**

        Depois:

        **custo = dias × diária**

        ### Custo geral

        **materiais + massas e telas + mão de obra**

        ### Custo por m²

        **custo geral ÷ área**

        Os percentuais exibidos na análise são
        calculados sobre o custo geral do projeto.
        """
    )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")

st.caption(
    "Calculadora Profissional de Steel Framing • "
    "Módulo 6D — Análise • Motor 6C"
)
