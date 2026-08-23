import streamlit as st
import pandas as pd

from core.calculos import (
    calcular_indicadores_projeto,
)


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Análise do Projeto",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# TÍTULO
# ============================================================

st.title("📊 Análise do Projeto")
st.caption(
    "Análise financeira e indicadores do orçamento "
    "de Steel Framing."
)


# ============================================================
# RECUPERAÇÃO DO PROJETO
# ============================================================

projeto = st.session_state.get(
    "projeto_calculado",
    None,
)


# ============================================================
# COMPATIBILIDADE COM SESSION STATE
# ============================================================

if projeto is None:

    # Algumas versões da aplicação podem armazenar
    # o resultado com outros nomes.

    for chave in (
        "projeto",
        "resultado_projeto",
        "calculo_projeto",
        "resultado",
    ):

        candidato = st.session_state.get(
            chave,
            None,
        )

        if isinstance(candidato, dict):

            if (
                "area" in candidato
                and "custo_geral" in candidato
            ):
                projeto = candidato
                break


# ============================================================
# VERIFICAÇÃO
# ============================================================

if not isinstance(projeto, dict):

    st.warning(
        "⚠️ Ainda não existe um projeto calculado "
        "para análise."
    )

    st.info(
        "Vá até a página 📐 Projeto, preencha os dados "
        "e execute o cálculo antes de acessar esta página."
    )

    st.stop()


# ============================================================
# INDICADORES
# ============================================================

indicadores = calcular_indicadores_projeto(
    projeto
)


area = float(
    projeto.get(
        "area",
        0.0,
    )
)

subtotal_materiais = float(
    projeto.get(
        "subtotal_materiais",
        0.0,
    )
)

massas_telas = float(
    projeto.get(
        "massas_telas",
        0.0,
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

custo_mao_de_obra = float(
    mao_de_obra.get(
        "custo",
        0.0,
    )
)

dias_mao_de_obra = float(
    mao_de_obra.get(
        "dias",
        0.0,
    )
)

diaria = float(
    mao_de_obra.get(
        "diaria",
        0.0,
    )
)

custo_geral = float(
    projeto.get(
        "custo_geral",
        0.0,
    )
)

custo_por_m2 = float(
    indicadores.get(
        "custo_por_m2",
        0.0,
    )
)

percentual_materiais = float(
    indicadores.get(
        "percentual_materiais",
        0.0,
    )
)

percentual_massas = float(
    indicadores.get(
        "percentual_massas_telas",
        0.0,
    )
)

percentual_mao_de_obra = float(
    indicadores.get(
        "percentual_mao_de_obra",
        0.0,
    )
)


# ============================================================
# FUNÇÃO DE MOEDA
# ============================================================

def moeda(valor):
    """
    Formata valores em reais.
    """

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ============================================================
# INFORMAÇÕES DO PROJETO
# ============================================================

st.subheader("📐 Informações do projeto")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Área",
        f"{area:.2f} m²",
    )

with col2:
    st.metric(
        "Custo geral",
        moeda(custo_geral),
    )

with col3:
    st.metric(
        "Custo por m²",
        moeda(custo_por_m2),
    )


# ============================================================
# RESUMO FINANCEIRO
# ============================================================

st.divider()

st.subheader("💰 Resumo financeiro")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🧱 Materiais",
        moeda(subtotal_materiais),
        f"{percentual_materiais:.1f}%",
    )

with col2:

    st.metric(
        "🪣 Massas e Telas",
        moeda(massas_telas),
        f"{percentual_massas:.1f}%",
    )

with col3:

    st.metric(
        "👷 Mão de Obra",
        moeda(custo_mao_de_obra),
        f"{percentual_mao_de_obra:.1f}%",
    )

with col4:

    st.metric(
        "💰 Custo Geral",
        moeda(custo_geral),
    )


# ============================================================
# COMPOSIÇÃO DO CUSTO
# ============================================================

st.divider()

st.subheader("📊 Composição do custo")

dados_composicao = pd.DataFrame(
    {
        "Categoria": [
            "Materiais",
            "Massas e Telas",
            "Mão de Obra",
        ],
        "Valor": [
            subtotal_materiais,
            massas_telas,
            custo_mao_de_obra,
        ],
    }
)

st.bar_chart(
    dados_composicao.set_index(
        "Categoria"
    ),
    width="stretch",
)


# ============================================================
# PARTICIPAÇÃO PERCENTUAL
# ============================================================

st.subheader("📈 Participação no custo geral")

dados_percentuais = pd.DataFrame(
    {
        "Categoria": [
            "Materiais",
            "Massas e Telas",
            "Mão de Obra",
        ],
        "Participação (%)": [
            percentual_materiais,
            percentual_massas,
            percentual_mao_de_obra,
        ],
    }
)

st.dataframe(
    dados_percentuais,
    hide_index=True,
    width="stretch",
    column_config={
        "Participação (%)": st.column_config.NumberColumn(
            format="%.1f%%",
        ),
    },
)


# ============================================================
# MÃO DE OBRA
# ============================================================

st.divider()

st.subheader("👷 Análise da mão de obra")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Dias estimados",
        f"{dias_mao_de_obra:.1f} dias",
    )

with col2:

    st.metric(
        "Diária",
        moeda(diaria),
    )

with col3:

    st.metric(
        "Custo da mão de obra",
        moeda(custo_mao_de_obra),
    )


# ============================================================
# ANÁLISE DOS MATERIAIS
# ============================================================

st.divider()

st.subheader("🧱 Análise dos materiais")

materiais = projeto.get(
    "materiais",
    {},
)

if isinstance(
    materiais,
    dict,
) and materiais:

    linhas = []

    for nome, item in materiais.items():

        if not isinstance(
            item,
            dict,
        ):
            continue

        quantidade = float(
            item.get(
                "quantidade",
                0.0,
            )
        )

        preco = float(
            item.get(
                "preco_unitario",
                0.0,
            )
        )

        custo = float(
            item.get(
                "custo",
                0.0,
            )
        )

        quantidade_automatica = float(
            item.get(
                "quantidade_automatica",
                0.0,
            )
        )

        origem = item.get(
            "origem_quantidade",
            "automática",
        )

        unidade = item.get(
            "unidade",
            "un",
        )

        categoria = item.get(
            "categoria",
            "Outros",
        )

        percentual = (
            custo / custo_geral * 100
            if custo_geral > 0
            else 0
        )

        linhas.append(
            {
                "Material": nome,
                "Categoria": categoria,
                "Quantidade": quantidade,
                "Unidade": unidade,
                "Preço unitário": preco,
                "Custo": custo,
                "Participação": percentual,
                "Origem": origem,
            }
        )

    if linhas:

        df_materiais = pd.DataFrame(
            linhas
        )

        st.dataframe(
            df_materiais,
            hide_index=True,
            width="stretch",
            column_config={
                "Quantidade": st.column_config.NumberColumn(
                    format="%.2f",
                ),
                "Preço unitário": st.column_config.NumberColumn(
                    format="R$ %.2f",
                ),
                "Custo": st.column_config.NumberColumn(
                    format="R$ %.2f",
                ),
                "Participação": st.column_config.NumberColumn(
                    format="%.1f%%",
                ),
            },
        )

    else:

        st.info(
            "Não há materiais disponíveis para análise."
        )

else:

    st.info(
        "Nenhum material foi encontrado no projeto."
    )


# ============================================================
# MATERIAIS — GRÁFICO
# ============================================================

if isinstance(
    materiais,
    dict,
) and materiais:

    dados_grafico = []

    for nome, item in materiais.items():

        if not isinstance(
            item,
            dict,
        ):
            continue

        custo = float(
            item.get(
                "custo",
                0.0,
            )
        )

        if custo > 0:

            dados_grafico.append(
                {
                    "Material": nome,
                    "Custo": custo,
                }
            )

    if dados_grafico:

        st.subheader(
            "📊 Custo por material"
        )

        df_grafico = (
            pd.DataFrame(
                dados_grafico
            )
            .sort_values(
                "Custo",
                ascending=False,
            )
            .set_index(
                "Material"
            )
        )

        st.bar_chart(
            df_grafico,
            width="stretch",
        )


# ============================================================
# INDICADORES GERENCIAIS
# ============================================================

st.divider()

st.subheader("🎯 Indicadores gerenciais")

custo_materiais_m2 = (
    subtotal_materiais / area
    if area > 0
    else 0
)

custo_massas_m2 = (
    massas_telas / area
    if area > 0
    else 0
)

custo_mao_obra_m2 = (
    custo_mao_de_obra / area
    if area > 0
    else 0
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Materiais / m²",
        moeda(custo_materiais_m2),
    )

with col2:

    st.metric(
        "Massas / m²",
        moeda(custo_massas_m2),
    )

with col3:

    st.metric(
        "Mão de obra / m²",
        moeda(custo_mao_obra_m2),
    )

with col4:

    st.metric(
        "Total / m²",
        moeda(custo_por_m2),
    )


# ============================================================
# CONFERÊNCIA
# ============================================================

st.divider()

st.subheader("✅ Conferência do orçamento")

soma_percentuais = (
    percentual_materiais
    + percentual_massas
    + percentual_mao_de_obra
)

diferenca = abs(
    soma_percentuais - 100.0
)

if diferenca < 0.1:

    st.success(
        "Composição financeira conferida: "
        "os componentes representam 100% "
        "do custo geral."
    )

else:

    st.warning(
        f"A composição apresenta "
        f"{soma_percentuais:.2f}% do custo geral."
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "Calculadora Profissional de Steel Framing • "
    "Análise 6D • Dados calculados pelo motor 6C"
)
