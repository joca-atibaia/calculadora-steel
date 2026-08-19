import streamlit as st
import pandas as pd
import math

# 1. Configuração da Página e Cores do Tema Dinâmico
st.set_page_config(
    page_title="Calculadora Inteligente - Steel Framing", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS para estilização avançada
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

# Título Principal com Ícone estilizado
st.markdown("<h1 style='color: #ffffff; font-family: sans-serif;'>🏗️ Calculadora de Engenharia <span style='color: #ff9f1c;'>Steel Framing</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8a92a6;'>Insira as dimensões do projeto extraídas do SketchUp para calcular o quantitativo real.</p>", unsafe_allow_html=True)
st.markdown("---")

# CAMPOS DE ENTRADA GEOMÉTRICA (Substituindo a digitação manual de quantidade)
st.markdown("<h3 style='color: #ffffff;'>📐 Dimensões do Projeto (SketchUp)</h3>", unsafe_allow_html=True)
col_geo1, col_geo2 = st.columns(2)

with col_geo1:
    comp_linear = st.number_input("Comprimento Linear da Estrutura (Metros)", min_value=0.0, value=25.63, step=1.0)
with col_geo2:
    area_total = st.number_input("Área Total de Paredes / Fechamento (m²)", min_value=0.0, value=75.0, step=1.0)

st.markdown("---")

# Definição dos itens e suas fórmulas matemáticas com base no Excel
itens_calculados = [
    {"Item": "Perfil 90x0,80", "Quantidade": math.ceil(comp_linear * 2.4581), "Preço Unitário (R$)": 50.0},
    {"Item": "Guia Perimetral", "Quantidade": math.ceil(comp_linear * 1.9508), "Preço Unitário (R$)": 50.0},
    {"Item": "Plywood 8mm", "Quantidade": math.ceil(area_total / 1.375), "Preço Unitário (R$)": 80.0},
    {"Item": "Placa ST 12.5mm", "Quantidade": math.ceil(area_total / 1.875), "Preço Unitário (R$)": 40.0},
    {"Item": "Placa Cimentícia 12mm", "Quantidade": math.ceil(area_total / 2.5), "Preço Unitário (R$)": 140.0},
    {"Item": "Lã PET", "Quantidade": math.ceil(area_total / 15.0), "Preço Unitário (R$)": 200.0},
    {"Item": "Parafusos (Cento)", "Quantidade": math.ceil((area_total * 80) / 100), "Preço Unitário (R$)": 35.0},
    {"Item": "Massas (Balde/Saco)", "Quantidade": 1.0, "Preço Unitário (R$)": 500.0},
    {"Item": "Telas (Rolo)", "Quantidade": 1.0, "Preço Unitário (R$)": 500.0},
    {"Item": "Adesivo PU (Cx)", "Quantidade": 1.0, "Preço Unitário (R$)": 150.0},
    {"Item": "Telha Sanduíche", "Quantidade": 10.0, "Preço Unitário (R$)": 400.0},
    {"Item": "Manta Hidrófuga", "Quantidade": math.ceil(area_total / 37.5), "Preço Unitário (R$)": 500.0},
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
                step=5.0,
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

# Configuração da Barra Lateral
st.sidebar.markdown("<h2 style='color: #ffffff; text-align: center;'>📊 Painel Financeiro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("<b style='color: #ffffff;'>Ajuste Operacional:</b>", unsafe_allow_html=True)
mao_de_obra = st.sidebar.number_input("Mão de Obra", min_value=0.0, value=11635.0, step=100.0)
st.sidebar.markdown("---")

total_geral = total_materiais + mao_de_obra

# Exibição dos novos Cartões de Custo Avançados na Barra Lateral
st.sidebar.markdown(f"""
    <div class='card-total'>
        <h4>Material Total</h4>
        <p>R$ {total_materiais:,.2f}</p>
    </div>
    <div class='card-total'>
        <h4>Mão de Obra</h4>
        <p>R$ {mao_de_obra:,.2f}</p>
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
    file_name='orcamento_automatizado.csv',
    mime='text/csv',
    use_container_width=True
)

# Tabela detalhada analítica
with st.expander("🔍 Visualizar Tabela Analítica Completa"):
    st.dataframe(
        df.style.format({"Preço Unitário (R$)": "R$ {:.2f}", "Total (R$)": "R$ {:.2f}"}), 
        use_container_width=True
    )
