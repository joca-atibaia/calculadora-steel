import streamlit as st
import pandas as pd
import math

# 1. Configuração da Página e Cores do Tema Dinâmico
st.set_page_config(
    page_title="Calculadora Inteligente - Steel Framing", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS para estilização (Mantendo seu excelente padrão visual)
st.markdown("""
    <style>
    .main { background-color: #0f1115; }
    div[data-testid="stMetricValue"] { font-size: 28px !important; color: #ff9f1c !important; }
    .card-total {
        background-color: #1e222b;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ff9f1c;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    .card-total h4 { color: #8a92a6; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    .card-total p { color: #ffffff; margin: 5px 0 0 0; font-size: 32px; font-weight: bold; }
    .card-item {
        background-color: #161a22;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2e3440;
        margin-bottom: 15px;
    }
    .total-item-text {
        font-size: 1rem;
        color: #ff9f1c;
        font-weight: bold;
        margin-top: 8px;
        border-top: 1px dashed #2e3440;
        padding-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 style='color: #ffffff; font-family: sans-serif;'>🏗️ Calculadora de Engenharia <span style='color: #ff9f1c;'>Steel Framing</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8a92a6;'>Insira as dimensões do projeto abaixo para o cálculo automático com base nos coeficientes reais da planilha.</p>", unsafe_allow_html=True)
st.markdown("---")

# 📐 SEÇÃO DE DIMENSÕES
st.markdown("<h3 style='color: #ffffff;'>📐 Dimensões do Projeto (SketchUp)</h3>", unsafe_allow_html=True)
col_geo1, col_geo2, col_geo3 = st.columns(3)

with col_geo1:
    comp_linear = st.number_input("Comprimento Linear (Metros)", min_value=0.0, value=30.00, step=0.01)

with col_geo2:
    altura_parede = st.number_input("Altura da Parede / Pé-Direito (Metros)", min_value=0.0, value=3.00, step=0.01)

# CÁLCULO DINÂMICO DA ÁREA BASEADO NO SKETCHUP
area_calculada = comp_linear * altura_parede

with col_geo3:
    st.metric(label="Área Total Calculada (m²)", value=f"{area_calculada:.2f} m²")

st.markdown("---")

# 📋 PROPORÇÕES REAIS EXTRAÍDAS DA PLANILHA (BASE DA OBRA = 90m² / 30m linear)
qtd_perfil = math.ceil(comp_linear * (113.0 / 30.0))
qtd_guia = math.ceil(comp_linear * (20.0 / 30.0))
qtd_plywood = math.ceil(area_calculada * (60.0 / 90.0))
qtd_placa_st = math.ceil(area_calculada * (36.0 / 90.0))
qtd_placa_cimenticia = math.ceil(area_calculada * (36.0 / 90.0))
qtd_la_pet = math.ceil(area_calculada * (6.0 / 90.0))
qtd_parafusos = math.ceil(area_calculada * (8000.0 / 90.0))
qtd_cola_pu = math.ceil(area_calculada * (36.0 / 90.0))
qtd_manta = math.ceil(area_calculada * (3.0 / 90.0))
qtd_massas_telas = math.ceil(area_calculada * (1.0 / 90.0))

itens_projeto = [
    {"Item": "Perfil 90x0,80", "Qtd_Sugerida": qtd_perfil, "Preco_Base": 50.0},
    {"Item": "Guia Perimetral", "Qtd_Sugerida": qtd_guia, "Preco_Base": 50.0},
    {"Item": "Plywood 8mm", "Qtd_Sugerida": qtd_plywood, "Preco_Base": 80.0},
    {"Item": "Placa ST 12.5mm", "Qtd_Sugerida": qtd_placa_st, "Preco_Base": 40.0},
    {"Item": "Placa Cimentícia 12mm", "Qtd_Sugerida": qtd_placa_cimenticia, "Preco_Base": 140.0},
    {"Item": "Lã PET", "Qtd_Sugerida": qtd_la_pet, "Preco_Base": 200.0},
    {"Item": "Parafusos", "Qtd_Sugerida": qtd_parafusos, "Preco_Base": 0.07},
    {"Item": "Cola PU 40", "Qtd_Sugerida": qtd_cola_pu, "Preco_Base": 40.0},
    {"Item": "Manta Hidrófuga", "Qtd_Sugerida": qtd_manta, "Preco_Base": 500.0},
    {"Item": "Massas e Telas", "Qtd_Sugerida": qtd_massas_telas, "Preco_Base": 1200.0}
]

st.markdown("<h3 style='color: #ffffff;'>📋 Insumos Calculados Automaticamente</h3>", unsafe_allow_html=True)
dados_atualizados = []

col1, col2 = st.columns(2)

for i, item in enumerate(itens_projeto):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"<div class='card-item'><b style='color: #ff9f1c;'>{item['Item']}</b>", unsafe_allow_html=True)
        
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            nova_qtd = st.number_input(
                f"{item['Item']} (Qtd)", 
                min_value=0.0, 
                value=float(item['Qtd_Sugerida']), 
                step=1.0,
                key=f"qtd_{i}"
            )
        with sub_c2:
            novo_preco = st.number_input(
                f"{item['Item']} (Preço R$)", 
                min_value=0.0, 
                value=float(item['Preco_Base']), 
                step=1.0 if item['Preco_Base'] > 1 else 0.01,
                key=f"prc_{i}"
            )
        
        # CÁLCULO E EXIBIÇÃO DO TOTAL INDIVIDUAL DO ITEM DENTRO DO CARTÃO
        total_item = nova_qtd * novo_preco
        st.markdown(f"<p class='total-item-text'>Total do Item: R$ {total_item:,.2f}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        dados_atualizados.append({
            "Item": item['Item'],
            "Quantidade": nova_qtd,
            "Preço Unitário (R$)": novo_preco,
            "Total (R$)": total_item
        })

# Processamento do DataFrame e Custo Total de Insumos
df = pd.DataFrame(dados_atualizados)
total_materiais = df["Total (R$)"].sum()

# Configuração da Barra Lateral (Painel Financeiro)
st.sidebar.markdown("<h2 style='color: #ffffff; text-align: center;'>📊 Painel Financeiro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("<b style='color: #ffffff;'>🛠️ Custos Adicionais:</b>", unsafe_allow_html=True)

# Mão de obra parametrizada (Padrão: 30 dias a R$ 755,00)
dias_trabalho = st.sidebar.number_input("Dias de Execução", min_value=0, value=30, step=1)
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", min_value=0.0, value=755.0, step=5.0)
mao_de_obra = dias_trabalho * valor_diaria

st.sidebar.markdown("---")

# Total Geral da Obra unindo os insumos e a mão de obra
total_geral = total_materiais + mao_de_obra

# Exibição dos Cartões Laterais de Custo
st.sidebar.markdown(f"""
    <div class='card-total'>
        <h4>Material Total</h4>
        <p>R$ {total_materiais:,.2f}</p>
    </div>
    <div class='card-total'>
        <h4>Mão de Obra ({dias_trabalho} dias)</h4>
        <p>R$ {mao_de_obra:,.2f}</p>
    </div>
    <div class='card-total' style='border-left-color: #30d158;'>
        <h4>Total Geral do Projeto</h4>
        <p style='color: #30d158;'>R$ {total_geral:,.2f}</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Exportar Orçamento",
    data=csv,
    file_name='orcamento_steel_frame.csv',
    mime='text/csv',
    use_container_width=True
)
