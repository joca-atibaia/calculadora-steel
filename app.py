import streamlit as st
import pandas as pd
import math

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Calculadora Steel Framing",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #0f1115;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        color: #ff9f1c !important;
    }

    .card-total {
        background-color: #1e222b;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid #ff9f1c;
        box-shadow: 2px 4px 15px rgba(0,0,0,0.4);
        margin-top: 15px;
        margin-bottom: 25px;
        text-align: center;
    }

    .card-total h4 {
        color: #8a92a6;
        margin: 0;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .card-total p {
        color: #ffffff;
        margin: 8px 0 0 0;
        font-size: 38px;
        font-weight: bold;
    }

    .card-item {
        background-color: #161a22;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2e3440;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# CABEÇALHO
# ============================================================

st.title("📐 Detalhamento do Projeto")

st.markdown(
    "Insira as dimensões do projeto abaixo para gerar automaticamente "
    "os quantitativos e custos dos materiais."
)

st.markdown("---")

# ============================================================
# DIMENSÕES DO PROJETO
# ============================================================

st.header("📐 Dimensões do Projeto")

col_geo1, col_geo2, col_geo3 = st.columns(3)

with col_geo1:
    comp_linear = st.number_input(
        "Comprimento Linear (Metros)",
        min_value=0.0,
        value=30.00,
        step=0.01,
    )

with col_geo2:
    altura_parede = st.number_input(
        "Altura da Parede / Pé-Direito (Metros)",
        min_value=0.0,
        value=3.00,
        step=0.01,
    )

area_calculada = comp_linear * altura_parede

with col_geo3:
    st.metric(
        label="Área Total Calculada (m²)",
        value=f"{area_calculada:.2f} m²",
    )

st.markdown("---")

# ============================================================
# COEFICIENTES
# ============================================================

COEFICIENTES = {
    "Perfil 90x0,80": 113.0 / 30.0,
    "Guia Perimetral": 20.0 / 30.0,
    "Plywood 8mm": 60.0 / 90.0,
    "Placa ST 12.5mm": 36.0 / 90.0,
    "Placa Cimentícia 12mm": 36.0 / 90.0,
    "Lã PET": 6.0 / 90.0,
    "Parafusos": 80.0,
    "Cola PU 40": 36.0 / 90.0,
    "Manta Hidrófuga": 3.0 / 90.0,
}

# ============================================================
# PREÇOS BASE
# ============================================================

PRECOS_BASE = {
    "Perfil 90x0,80": 50.0,
    "Guia Perimetral": 50.0,
    "Plywood 8mm": 80.0,
    "Placa ST 12.5mm": 40.0,
    "Placa Cimentícia 12mm": 140.0,
    "Lã PET": 200.0,
    "Parafusos": 0.07,
    "Cola PU 40": 40.0,
    "Manta Hidrófuga": 500.0,
}

# ============================================================
# QUANTIDADES
# ============================================================

qtd_perfil = math.ceil(
    comp_linear * COEFICIENTES["Perfil 90x0,80"]
)

qtd_guia = math.ceil(
    comp_linear * COEFICIENTES["Guia Perimetral"]
)

qtd_plywood = math.ceil(
    area_calculada * COEFICIENTES["Plywood 8mm"]
)

qtd_placa_st = math.ceil(
    area_calculada * COEFICIENTES["Placa ST 12.5mm"]
)

qtd_placa_cimenticia = math.ceil(
    area_calculada * COEFICIENTES["Placa Cimentícia 12mm"]
)

qtd_la_pet = math.ceil(
    area_calculada * COEFICIENTES["Lã PET"]
)

qtd_parafusos = math.ceil(
    area_calculada * COEFICIENTES["Parafusos"]
)

qtd_cola_pu = math.ceil(
    area_calculada * COEFICIENTES["Cola PU 40"]
)

qtd_manta = math.ceil(
    area_calculada * COEFICIENTES["Manta Hidrófuga"]
)

itens_parciais = [
    {
        "Item": "Perfil 90x0,80",
        "Qtd_Sugerida": qtd_perfil,
        "Preco_Base": PRECOS_BASE["Perfil 90x0,80"],
    },
    {
        "Item": "Guia Perimetral",
        "Qtd_Sugerida": qtd_guia,
        "Preco_Base": PRECOS_BASE["Guia Perimetral"],
    },
    {
        "Item": "Plywood 8mm",
        "Qtd_Sugerida": qtd_plywood,
        "Preco_Base": PRECOS_BASE["Plywood 8mm"],
    },
    {
        "Item": "Placa ST 12.5mm",
        "Qtd_Sugerida": qtd_placa_st,
        "Preco_Base": PRECOS_BASE["Placa ST 12.5mm"],
    },
    {
        "Item": "Placa Cimentícia 12mm",
        "Qtd_Sugerida": qtd_placa_cimenticia,
        "Preco_Base": PRECOS_BASE["Placa Cimentícia 12mm"],
    },
    {
        "Item": "Lã PET",
        "Qtd_Sugerida": qtd_la_pet,
        "Preco_Base": PRECOS_BASE["Lã PET"],
    },
    {
        "Item": "Parafusos",
        "Qtd_Sugerida": qtd_parafusos,
        "Preco_Base": PRECOS_BASE["Parafusos"],
    },
    {
        "Item": "Cola PU 40",
        "Qtd_Sugerida": qtd_cola_pu,
        "Preco_Base": PRECOS_BASE["Cola PU 40"],
    },
    {
        "Item": "Manta Hidrófuga",
        "Qtd_Sugerida": qtd_manta,
        "Preco_Base": PRECOS_BASE["Manta Hidrófuga"],
    },
]

# ============================================================
# INSUMOS
# ============================================================

st.header("📋 Insumos Calculados Automaticamente")

st.markdown(
    "As quantidades e os preços podem ser ajustados manualmente."
)

dados_atualizados = []

id_metragem = f"{comp_linear}_{altura_parede}"

col1, col2 = st.columns(2)

for i, item in enumerate(itens_parciais):

    target_col = col1 if i % 2 == 0 else col2

    with target_col:

        st.markdown(
            f"""
            <div class="card-item">
                <b style="color:#ff9f1c; font-size:18px;">
                    {item["Item"]}
                </b>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sub_c1, sub_c2 = st.columns(2)

        with sub_c1:

            nova_qtd = st.number_input(
                f'{item["Item"]} (Qtd)',
                min_value=0.0,
                value=float(item["Qtd_Sugerida"]),
                step=1.0,
                key=f"qtd_{i}_{id_metragem}",
            )

        with sub_c2:

            novo_preco = st.number_input(
                f'{item["Item"]} (Preço R$)',
                min_value=0.0,
                value=float(item["Preco_Base"]),
                step=1.0 if item["Preco_Base"] >= 1 else 0.01,
                key=f"prc_{i}_{id_metragem}",
            )

        total_item = nova_qtd * novo_preco

        st.write(
            f"**Subtotal do Item:** R$ {total_item:,.2f}"
        )

        dados_atualizados.append(
            {
                "Item": item["Item"],
                "Quantidade": nova_qtd,
                "Preço Unitário (R$)": novo_preco,
                "Total (R$)": total_item,
            }
        )

# ============================================================
# MASSAS E TELAS
# ============================================================

subtotal_acumulado = sum(
    item["Total (R$)"] for item in dados_atualizados
)

preco_sugerido_massas_telas = subtotal_acumulado * 0.05

st.markdown("---")

st.header("🎨 Acabamento e Perdas")

col_m1, col_m2 = st.columns(2)

with col_m1:

    st.markdown(
        """
        <div class="card-item">
            <b style="color:#ff9f1c; font-size:18px;">
                Massas e Telas
            </b>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sub_cm1, sub_cm2 = st.columns(2)

    with sub_cm1:

        qtd_massas = st.number_input(
            "Massas e Telas (Qtd)",
            min_value=0.0,
            value=1.0,
            step=1.0,
            key=f"qtd_massas_{id_metragem}",
        )

    with sub_cm2:

        preco_massas = st.number_input(
            "Massas e Telas (Preço R$)",
            min_value=0.0,
            value=float(preco_sugerido_massas_telas),
            step=10.0,
            key=f"prc_massas_{id_metragem}",
        )

    total_massas = qtd_massas * preco_massas

    st.write(
        f"**Subtotal do Item:** R$ {total_massas:,.2f}"
    )

dados_atualizados.append(
    {
        "Item": "Massas e Telas",
        "Quantidade": qtd_massas,
        "Preço Unitário (R$)": preco_massas,
        "Total (R$)": total_massas,
    }
)

# ============================================================
# TOTAL DOS MATERIAIS
# ============================================================

df = pd.DataFrame(dados_atualizados)

total_materiais = df["Total (R$)"].sum()

# ============================================================
# MÃO DE OBRA
# ============================================================

dias_sugeridos = max(
    1,
    math.ceil((area_calculada / 90.0) * 30)
)

st.markdown("---")

st.header("🛠️ Custos Adicionais (Mão de Obra)")

col_mo1, col_mo2 = st.columns(2)

with col_mo1:

    dias_trabalho = st.number_input(
        "Dias de Execução",
        min_value=0,
        value=int(dias_sugeridos),
        step=1,
        key=f"dias_exec_{id_metragem}",
    )

with col_mo2:

    valor_diaria = st.number_input(
        "Valor da Diária (R$)",
        min_value=0.0,
        value=755.0,
        step=5.0,
        key=f"v_diaria_{id_metragem}",
    )

mao_de_obra = dias_trabalho * valor_diaria

# ============================================================
# TOTAL GERAL
# ============================================================

total_geral = total_materiais + mao_de_obra

# ============================================================
# RESUMO
# ============================================================

st.markdown("---")

st.header("📊 Resumo e Fechamento")

tipo_total_selecionado = st.selectbox(
    "Selecione o tipo de total que deseja visualizar no painel:",
    [
        "Material Total",
        "Mão de Obra Total",
        "Custo Geral da Obra (Global)",
    ],
)

if tipo_total_selecionado == "Material Total":

    rotulo_card = "Material Total"
    valor_card = total_materiais

elif tipo_total_selecionado == "Mão de Obra Total":

    rotulo_card = "Mão de Obra Total"
    valor_card = mao_de_obra

else:

    rotulo_card = "Custo Geral da Obra"
    valor_card = total_geral

# ============================================================
# CARD FINAL
# ============================================================

st.markdown(
    f"""
    <div class="card-total">
        <h4>{rotulo_card}</h4>
        <p>R$ {valor_card:,.2f}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# TABELA RESUMIDA
# ============================================================

st.subheader("📋 Tabela Consolidada")

st.dataframe(
    df,
    width="stretch",
    hide_index=True,
)

# ============================================================
# EXPORTAÇÃO CSV
# ============================================================

csv_data = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 Exportar Orçamento",
    data=csv_data,
    file_name="orcamento_steel_framing.csv",
    mime="text/csv",
    width="stretch",
)

# ============================================================
# PAINEL LATERAL
# ============================================================

st.sidebar.header("💰 Resumo Financeiro")

st.sidebar.metric(
    "Material Total",
    f"R$ {total_materiais:,.2f}",
)

st.sidebar.metric(
    "Mão de Obra",
    f"R$ {mao_de_obra:,.2f}",
)

st.sidebar.metric(
    "Custo Geral",
    f"R$ {total_geral:,.2f}",
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Calculadora Steel Framing"
)