import streamlit as st
import pandas as pd
import math

# 1. Configuração da Página e Cores do Tema Dinâmico
st.set_page_config(
    page_title="Calculadora Inteligente - Steel Framing", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS para estilização avançada (Mantendo seu excelente padrão visual)
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
st.markdown("<p style='color: #8a92a6;'>Insira as dimensões do projeto abaixo para o cálculo automático dos insumos e m².</p>", unsafe_allow_html=True)
st.markdown("---")

# Dimensões do Projeto lado a lado
st.markdown("<h3 style='color: #ffffff;'>📐 Dimensões do Projeto (SketchUp)</h3>", unsafe_allow_html=True)
col_geo1, col_geo2, col_geo3 = st.columns(3)

with col_geo1:
    comp_linear = st.number_input("Comprimento Linear (Metros)", min_value=0.0, value=30.0, step=0.1) # Ajustado padrão para coincidir com os 30m lineares da planilha

with col_geo2:
    altura_parede = st.number_input("Altura da Parede / Pé-Direito (Metros)", min_value=0.0, value=3.0, step=0.1) # Ajustado padrão para os 3m de altura da planilha

# CÁLCULO AUTOMÁTICO DA ÁREA
area_calculada = comp_linear * altura_parede

with col_geo3:
    st.metric(label="Área Total Calculada (m²)", value=f"{area_calculada:.2f} m²")

st.markdown("---")

# RECONCILIAÇÃO MATEMÁTICA BASEADA NA SUA PLANILHA ORIGINAL (Área Base = 90m²)
# As fórmulas foram ajustadas dividindo a quantidade original por 90 (para área) ou por 30 (para comp_linear)
itens_calculados = [
    {"Item": "Perfil 90x0,80", "Quantidade": math.ceil(comp_linear * 3.766), "Preço Unitário (R$)": 50.0}, # 113 m / 30m linear
    {"Item": "Guia Perimetral", "Quantidade": math.ceil(comp_linear * 0.666), "Preço Unitário (R$)": 50.0}, # 20 m / 30m linear
    {"Item": "Plywood 8mm", "Quantidade": math.ceil(area_calculada / 1.5), "Preço Unitário (R$)": 80.0}, # Rendimento exato: 1.5m² por placa
    {"Item": "Placa ST 12.5mm", "Quantidade": math.ceil(area_calculada / 2.5), "Preço Unitário (R$)": 40.0}, # Rendimento exato: 2.5m² por placa
    {"Item": "Placa Cimentícia 12mm", "Quantidade": math.ceil(area_calculada / 2.5), "Preço Unitário (R$)": 140.0}, # Rendimento exato: 2.5m² por placa
    {"Item": "Lã PET 15m²", "Quantidade": math.ceil(area_calculada / 15.0), "Preço Unitário (R$)": 200.0}, # Rendimento exato: 15m² por rolo
    {"Item": "Parafusos (Unidade)", "Quantidade": math.ceil((area_calculada * 88.88)), "Preço Unitário (R$)": 0.07}, # 8000 parafusos / 90m²
    {"Item": "Cola PU 40", "Quantidade": math.ceil(area_calculada * 0.4), "Preço Unitário (R$)": 40.0}, # 36 tubos / 90m²
    {"Item": "Manta Hidrófuga", "Quantidade": math.ceil(area_calculada / 30.0), "Preço Unitário (R$)": 500.0}, # 3 rolos / 90m² -> 30m² por rolo
]

st.markdown("<h3 style='color: #ffffff;'>📋 Insumos Calculados Automaticamente</h3>", unsafe_allow_html=True)
dados_atualizados = []

col1, col2 = st.columns(2)

for i, item in enumerate(itens_calculados):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"<div class='card-item'><b style='color: #ff9f1c;'>{item['Item']}</b>", unsafe_allow_html=True)
        
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            st.metric(label="Qtd Sugerida", value=int(item['Quantidade']))
        with sub_c2:
            novo_preco = st.number_input(
                f"Preço Unitário (R$)", 
                min_value=0.0, 
                value=float(item['Preço Unitário (R$)']), 
                step=1.0 if item['Preço Unitário (R$)'] < 1 else 5.0,
                key=f"prc_{i}"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        total_item = item['Quantidade'] * novo_preco
        dados_atualizados.append({
            "Item": item['Item'],
            "Quantidade": item['Quantidade'],
            "Preço Unitário (R$)": novo_preco,
            "Total (R$)": total_item
        })

# Criar DataFrame para processamento
df = pd.DataFrame(dados_atualizados)
total_materiais = df["Total (R$)"].sum()

# Cálculo dinâmico da taxa de Massas, Telas e Perdas (5% do subtotal)
taxa_massas_telas = total_materiais * 0.05

# Configuração da Barra Lateral
st.sidebar.markdown("<h2 style='color: #ffffff; text-align: center;'>📊 Painel Financeiro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("<b style='color: #ffffff;'>Configuração de Mão de Obra:</b>", unsafe_allow_html=True)
# Escalona os dias dinamicamente com base na área (Base: 30 dias para 90m²)
dias_estimados = math.ceil((area_calculada / 90) * 30)
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", min_value=0.0, value=755.0, step=10.0)
mao_de_obra_total = dias_estimados * valor_diaria

st.sidebar.markdown(f"<p style='color: #8a92a6; font-size:13px;'>Tempo estimado para execução: <b>{dias_estimados} dias</b></p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Cálculo do Total Geral
total_geral = total_materiais + taxa_massas_telas + mao_de_obra_total

# Exibição dos novos Cartões de Custo Avançados na Barra Lateral
st.sidebar.markdown(f"""
    <div class='card-total'>
        <h4>Insumos Base</h4>
        <p>R$ {total_materiais:,.2f}</p>
    </div>
    <div class='card-total' style='border-left-color: #a2d2ff;'>
        <h4>Massas, Telas e Perdas (5%)</h4>
        <p style='color: #a2d2ff;'>R$ {taxa_massas_telas:,.2f}</p>
    </div>
    <div class='card-total'>
        <h4>Mão de Obra ({dias_estimados} dias)</h4>
        <p>R$ {mao_de_obra_total:,.2f}</p>
    </div>
    <div class='card-total' style='border-left-color: #00b4d8;'>
        <h4>Total do Projeto</h4>
        <p style='color: #00b4d8;'>R$ {total_geral:,.2f}</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Opção de download
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Exportar Planilha (Excel/CSV)",
    data=csv,
    file_name='orcamento_steel_frame.csv',
    mime='text/csv',
    use_container_width=True
)

# Tabela detalhada analítica
with st.expander("🔍 Visualizar Tabela Analítica Completa"):
    st.dataframe(
        df.style.format({"Preço Unitário (R$)": "R$ {:.2f}", "Total (R$)": "R$ {:.2f}"}), 
        use_container_width=True
    )
