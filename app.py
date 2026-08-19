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
    </style>
""", unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 style='color: #ffffff; font-family: sans-serif;'>🏗️ Calculadora de Engenharia <span style='color: #ff9f1c;'>Steel Framing</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8a92a6;'>Ajuste os valores abaixo para calcular o orçamento em tempo real conforme sua planilha.</p>", unsafe_allow_html=True)
st.markdown("---")

# 📐 SEÇÃO DE DIMENSÕES (Mantida idêntica ao seu padrão visual para referência)
st.markdown("<h3 style='color: #ffffff;'>📐 Dimensões do Projeto (SketchUp)</h3>", unsafe_allow_html=True)
col_geo1, col_geo2, col_geo3 = st.columns(3)

with col_geo1:
    comp_linear = st.number_input("Comprimento Linear (Metros)", min_value=0.0, value=25.63, step=0.01)

with col_geo2:
    altura_parede = st.number_input("Altura da Parede / Pé-Direito (Metros)", min_value=0.0, value=2.93, step=0.01)

area_calculada = comp_linear * altura_parede

with col_geo3:
    st.metric(label="Área Total Calculada (m²)", value=f"{area_calculada:.2f} m²")

st.markdown("---")

# 📋 LISTA DE INSUMOS COM AS QUANTIDADES REAIS EXATAS DA SUA PLANILHA
# Puxando os valores consolidados que estão calculados nas células do seu Excel
itens_projeto = [
    {"Item": "Plywood 8mm", "Qtd_Sugerida": 40.0, "Preco_Base": 80.0},
    {"Item": "Placa ST 12.5mm", "Qtd_Sugerida": 24.0, "Preco_Base": 40.0},
    {"Item": "Placa Cimentícia 12mm", "Qtd_Sugerida": 24.0, "Preco_Base": 140.0},
    {"Item": "Lã PET 15m²", "Qtd_Sugerida": 4.0, "Preco_Base": 200.0},
    {"Item": "Manta Hidrófuga", "Qtd_Sugerida": 2.0, "Preco_Base": 500.0},
    {"Item": "PU (Adesivo)", "Qtd_Sugerida": 24.0, "Preco_Base": 40.0},
    {"Item": "Cola PU 40", "Qtd_Sugerida": 24.0, "Preco_Base": 40.0}
]

st.markdown("<h3 style='color: #ffffff;'>📋 Insumos do Orçamento</h3>", unsafe_allow_html=True)
dados_atualizados = []

col1, col2 = st.columns(2)

for i, item in enumerate(itens_projeto):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"<div class='card-item'><b style='color: #ff9f1c;'>{item['Item']}</b>", unsafe_allow_html=True)
        
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            # Aplica a função de arredondamento TETO para garantir números inteiros como no Excel
            nova_qtd = st.number_input(
                f"{item['Item']} (Qtd)", 
                min_value=0.0, 
                value=float(math.ceil(item['Qtd_Sugerida'])), 
                step=1.0,
                key=f"qtd_{i}"
            )
        with sub_c2:
            novo_preco = st.number_input(
                f"{item['Item']} (Preço R$)", 
                min_value=0.0, 
                value=float(item['Preco_Base']), 
                step=5.0,
                key=f"prc_{i}"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        total_item = nova_qtd * novo_preco
        dados_atualizados.append({
            "Item": item['Item'],
            "Quantidade": nova_qtd,
            "Preço Unitário (R$)": novo_preco,
            "Total (R$)": total_item
        })

# Processamento dos totais matemáticos
df = pd.DataFrame(dados_atualizados)
total_materiais = df["Total (R$)"].sum()

# Configuração da Barra Lateral (Painel Financeiro)
st.sidebar.markdown("<h2 style='color: #ffffff; text-align: center;'>📊 Painel Financeiro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("<b style='color: #ffffff;'>🛠️ Custos Adicionais:</b>", unsafe_allow_html=True)
# Mão de obra parametrizada zerada conforme seu print (Pronta para você preencher se quiser)
mao_de_obra = st.sidebar.number_input("Mão de Obra (20 dias)", min_value=0.0, value=0.0, step=100.0)
st.sidebar.markdown("---")

total_geral = total_materiais + mao_de_obra

# Exibição dos Cartões Laterais de Custo
st.sidebar.markdown(f"""
    <div class='card-total'>
        <h4>Material Total</h4>
        <p>R$ {total_materiais:,.2f}</p>
    </div>
    <div class='card-total'>
        <h4>Mão de Obra</h4>
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
Use o código com cuidado.
