import streamlit as st
import pandas as pd
import math

# ============================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Calculadora Inteligente - Steel Framing",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# ============================================================
# PWA - MANIFESTO DA CALCULADORA STEEL FRAMING
# ============================================================

st.markdown(
    """
    <link rel="manifest" href="/app/static/manifest.json">
    """,
    unsafe_allow_html=True
)
# ============================================================
# 2. ESTILO VISUAL - DRYARTE
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #0f1115;
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

.total-item-container {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px dashed #2e3440;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.total-item-label {
    font-size: 0.9rem;
    color: #8a92a6;
}

.total-item-value {
    font-size: 1.1rem;
    color: #ff9f1c;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. CABEÇALHO
# ============================================================

st.image("LOGO IA.png 002.png", width=280)

st.markdown(
    """
    <p style='color: #8a92a6; margin-top: -10px;'>
    Insira as dimensões do projeto abaixo para o cálculo automático
    com base nos coeficientes reais da planilha.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# 4. DIMENSÕES DO PROJETO
# ============================================================

st.markdown(
    "<h3 style='color: #ffffff;'>📐 Dimensões do Projeto (SketchUp)</h3>",
    unsafe_allow_html=True
)

col_geo1, col_geo2, col_geo3 = st.columns(3)

with col_geo1:
    comp_linear = st.number_input(
        "Comprimento Linear (Metros)",
        min_value=0.0,
        value=30.00,
        step=0.01
    )

with col_geo2:
    altura_parede = st.number_input(
        "Altura da Parede / Pé-Direito (Metros)",
        min_value=0.0,
        value=3.00,
        step=0.01
    )

# Área calculada
area_calculada = comp_linear * altura_parede

with col_geo3:
    st.metric(
        label="Área Total Calculada (m²)",
        value=f"{area_calculada:.2f} m²"
    )

st.markdown("---")

# ============================================================
# 5. COEFICIENTES DOS MATERIAIS
# ============================================================

# Estes valores ficam centralizados.
# No futuro podemos transferi-los para Excel/CSV/banco de dados.

COEFICIENTES = {
    "Perfil 90x0,80": 113.0 / 30.0,
    "Guia Perimetral": 20.0 / 30.0,
    "Plywood 8mm": 60.0 / 90.0,
    "Placa ST 12.5mm": 36.0 / 90.0,
    "Placa Cimentícia 12mm": 36.0 / 90.0,
    "Lã PET": 6.0 / 90.0,
    "Parafusos": 80.0,
    "Cola PU 40": 36.0 / 90.0,
    "Manta Hidrófuga": 3.0 / 90.0
}

# Preços-base
PRECOS_BASE = {
    "Perfil 90x0,80": 50.0,
    "Guia Perimetral": 50.0,
    "Plywood 8mm": 80.0,
    "Placa ST 12.5mm": 40.0,
    "Placa Cimentícia 12mm": 140.0,
    "Lã PET": 200.0,
    "Parafusos": 0.07,
    "Cola PU 40": 40.0,
    "Manta Hidrófuga": 500.0
}

# ============================================================
# 6. CÁLCULO AUTOMÁTICO DAS QUANTIDADES
# ============================================================

qtd_perfil = math.ceil(comp_linear * COEFICIENTES["Perfil 90x0,80"])
qtd_guia = math.ceil(comp_linear * COEFICIENTES["Guia Perimetral"])
qtd_plywood = math.ceil(area_calculada * COEFICIENTES["Plywood 8mm"])
qtd_placa_st = math.ceil(area_calculada * COEFICIENTES["Placa ST 12.5mm"])
qtd_placa_cimenticia = math.ceil(
    area_calculada * COEFICIENTES["Placa Cimentícia 12mm"]
)
qtd_la_pet = math.ceil(area_calculada * COEFICIENTES["Lã PET"])
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
        "Preco_Base": PRECOS_BASE["Perfil 90x0,80"]
    },
    {
        "Item": "Guia Perimetral",
        "Qtd_Sugerida": qtd_guia,
        "Preco_Base": PRECOS_BASE["Guia Perimetral"]
    },
    {
        "Item": "Plywood 8mm",
        "Qtd_Sugerida": qtd_plywood,
        "Preco_Base": PRECOS_BASE["Plywood 8mm"]
    },
    {
        "Item": "Placa ST 12.5mm",
        "Qtd_Sugerida": qtd_placa_st,
        "Preco_Base": PRECOS_BASE["Placa ST 12.5mm"]
    },
    {
        "Item": "Placa Cimentícia 12mm",
        "Qtd_Sugerida": qtd_placa_cimenticia,
        "Preco_Base": PRECOS_BASE["Placa Cimentícia 12mm"]
    },
    {
        "Item": "Lã PET",
        "Qtd_Sugerida": qtd_la_pet,
        "Preco_Base": PRECOS_BASE["Lã PET"]
    },
    {
        "Item": "Parafusos",
        "Qtd_Sugerida": qtd_parafusos,
        "Preco_Base": PRECOS_BASE["Parafusos"]
    },
    {
        "Item": "Cola PU 40",
        "Qtd_Sugerida": qtd_cola_pu,
        "Preco_Base": PRECOS_BASE["Cola PU 40"]
    },
    {
        "Item": "Manta Hidrófuga",
        "Qtd_Sugerida": qtd_manta,
        "Preco_Base": PRECOS_BASE["Manta Hidrófuga"]
    }
]

# ============================================================
# 7. INSUMOS
# ============================================================

st.markdown(
    "<h3 style='color: #ffffff;'>📋 Insumos Calculados Automaticamente</h3>",
    unsafe_allow_html=True
)

dados_atualizados = []

# ID baseado nas dimensões
id_metragem = f"{comp_linear}_{altura_parede}"

col1, col2 = st.columns(2)

for i, item in enumerate(itens_parciais):

    target_col = col1 if i % 2 == 0 else col2

    with target_col:

        st.markdown(
            f"""
            <div class='card-item'>
            <b style='color: #ff9f1c;'>{item['Item']}</b>
            """,
            unsafe_allow_html=True
        )

        sub_c1, sub_c2 = st.columns(2)

        with sub_c1:
            nova_qtd = st.number_input(
                f"{item['Item']} (Qtd)",
                min_value=0.0,
                value=float(item["Qtd_Sugerida"]),
                step=1.0,
                key=f"qtd_{i}_{id_metragem}"
            )

        with sub_c2:
            novo_preco = st.number_input(
                f"{item['Item']} (Preço R$)",
                min_value=0.0,
                value=float(item["Preco_Base"]),
                step=1.0 if item["Preco_Base"] > 1 else 0.01,
                key=f"prc_{i}_{id_metragem}"
            )

        total_item = nova_qtd * novo_preco

        st.write(f"**Subtotal do Item:** R$ {total_item:,.2f}")

        st.markdown("</div>", unsafe_allow_html=True)

        dados_atualizados.append(
            {
                "Item": item["Item"],
                "Quantidade": nova_qtd,
                "Preço Unitário (R$)": novo_preco,
                "Total (R$)": total_item
            }
        )

# ============================================================
# 8. MASSAS E TELAS
# ============================================================

subtotal_acumulado = sum(
    d["Total (R$)"] for d in dados_atualizados
)

preco_sugerido_massas_telas = subtotal_acumulado * 0.05

st.markdown("---")

st.markdown(
    "<h3 style='color: #ffffff;'>🎨 Acabamento e Perdas</h3>",
    unsafe_allow_html=True
)

col_m1, col_m2 = st.columns(2)

with col_m1:

    st.markdown(
        """
        <div class='card-item'>
        <b style='color: #ff9f1c;'>Massas e Telas</b>
        """,
        unsafe_allow_html=True
    )

    sub_cm1, sub_cm2 = st.columns(2)

    with sub_cm1:
        qtd_massas = st.number_input(
            "Massas e Telas (Qtd)",
            min_value=0.0,
            value=1.0,
            step=1.0,
            key=f"qtd_massas_{id_metragem}"
        )

    with sub_cm2:
        preco_massas = st.number_input(
            "Massas e Telas (Preço R$)",
            min_value=0.0,
            value=float(preco_sugerido_massas_telas),
            step=10.0,
            key=f"prc_massas_{id_metragem}"
        )
        total_massas = qtd_massas * preco_massas

    st.write(f"**Subtotal do Item:** R$ {total_massas:,.2f}")

dados_atualizados.append(
    {
        "Item": "Massas e Telas",
        "Quantidade": qtd_massas,
        "Preço Unitário (R$)": preco_massas,
        "Total (R$)": total_massas
    }
)
    



dados_atualizados.append(
    {
        "Item": "Massas e Telas",
        "Quantidade": qtd_massas,
        "Preço Unitário (R$)": preco_massas,
        "Total (R$)": total_massas
    }
)

# ============================================================
# 9. TOTAL DOS MATERIAIS
# ============================================================

df = pd.DataFrame(dados_atualizados)

total_materiais = df["Total (R$)"].sum()

# ============================================================
# 10. MÃO DE OBRA
# ============================================================

dias_sugeridos = math.ceil(
    (area_calculada / 90.0) * 30
)

st.markdown("---")

st.markdown(
    "<h3 style='color: #ffffff;'>🛠️ Custos Adicionais (Mão de Obra)</h3>",
    unsafe_allow_html=True
)

col_mo1, col_mo2 = st.columns(2)

with col_mo1:
    dias_trabalho = st.number_input(
        "Dias de Execução",
        min_value=0,
        value=int(dias_sugeridos),
        step=1,
        key=f"dias_exec_{id_metragem}"
    )

with col_mo2:
    valor_diaria = st.number_input(
        "Valor da Diária (R$)",
        min_value=0.0,
        value=755.0,
        step=5.0,
        key=f"v_diaria_{id_metragem}"
    )

mao_de_obra = dias_trabalho * valor_diaria

# ============================================================
# 11. CUSTO GERAL
# ============================================================

total_geral = total_materiais + mao_de_obra

# ============================================================
# 12. RESUMO E FECHAMENTO
# ============================================================

st.markdown("---")

st.markdown(
    "<h3 style='color: #ffffff;'>📊 Resumo e Fechamento</h3>",
    unsafe_allow_html=True
)

tipo_total_selecionado = st.selectbox(
    "Selecione o tipo de total que deseja visualizar no painel:",
    [
        "Material Total",
        "Mão de Obra Total",
        "Custo Geral da Obra (Global)"
    ]
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
# 13. CARD FINAL
# ============================================================

st.markdown(
    f"""
    <div class='card-total'>
        <h4>{rotulo_card}</h4>
        <p>R$ {valor_card:,.2f}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 14. SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <h2 style='color: #ffffff; text-align: center;'>
    DRYARTE
    </h2>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <p style='text-align: center; color: #8a92a6;'>
    Sistema de Engenharia Inteligente
    </p>
    """,
    unsafe_allow_html=True
)
