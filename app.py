import streamlit as st
import pandas as pd
import math

# 1. Configuração da Página e Cores do Tema Dinâmico (Seu Padrão)
st.set_page_config(
    page_title="Calculadora Inteligente - Steel Framing", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS para estilização (Mantendo o tema Dark e os cartões)
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

# Título Principal (Idêntico ao seu print)
st.markdown("<h1 style='color: #ffffff; font-family: sans-serif;'>🏗️ Calculadora de Engenharia <span style='color: #ff9f1c;'>Steel Framing</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8a92a6;'>Insira as dimensões do projeto abaixo para o cálculo automático dos insumos e m².</p>", unsafe_allow_html=True)
st.markdown("---")

# 📐 SEÇÃO DE DIMENSÕES (Exatamente como o layout da sua imagem)
st.markdown("<h3 style='color: #ffffff;'>📐 Dimensões do Projeto (SketchUp)</h3>", unsafe_allow_html=True)

# Mantendo os inputs simples e diretos empilhados conforme o seu modelo mobile/tablet
comp_linear = st.number_input("Comprimento Linear (Metros)", min_value=0.0, value=25.63, step=0.1)
altura_parede = st.number_input("Altura da Parede / Pé-Direito (Metros)", min_value=0.0, value=2.93, step=0.1)

# CÁLCULO DINÂMICO DA ÁREA
area_calculada = comp_linear * altura_parede

# Exibição do resultado da área
st.metric(label="Área Total Calculada (m²)", value=f"{area_calculada:.2f} m²")

st.markdown("---")

# 📋 MOTOR DE PROPORÇÃO MATEMÁTICA (Vinculado diretamente aos inputs acima)
# Cada insumo usa o fator proporcional derivado da sua planilha base de 90m² e 30m lineares
itens_projeto = [
    {"Item": "Perfil 90x0,80", "Qtd_Sugerida": math.ceil(comp_linear * (113.0 / 30.0)), "Preco_Base": 50.0},
    {"Item": "Guia Perimetral", "Qtd_Sugerida": math.ceil(comp_linear * (20.0 / 30.0)), "Preco_Base": 50.0},
    {"Item": "Plywood 8mm", "Qtd_Sugerida": math.ceil(area_calculada / 1.5), "Preco_Base": 80.0},
    {"Item": "Placa ST 12.5mm", "Qtd_Sugerida": math.ceil(area_calculada / 2.5), "Preco_Base": 40.0},
    {"Item": "Placa Cimentícia 12mm", "Qtd_Sugerida": math.ceil(area_calculada / 2.5), "Preco_Base": 140.0},
    {"Item": "Lã PET", "Qtd_Sugerida": math.ceil(area_calculada / 15.0), "Preco_Base": 200.0},
    {"Item": "Parafusos", "Qtd_Sugerida": math.ceil(area_calculada * (8000.0 / 90.0)), "Preco_Base": 0.07},
    {"Item": "Cola PU 40", "Qtd_Sugerida": math.ceil(area_calculada * (36.0 / 90.0)), "Preco_Base": 40.0},
    {"Item": "Manta Hidrófuga", "Qtd_Sugerida": math.ceil(area_calculada / 30.0), "Preco_Base": 500.0}
]

st.markdown("<h3 style='color: #ffffff;'>📋 Insumos Calculados Automaticamente</h3>", unsafe_allow_html=True)
dados_atualizados = []

# Exibição em duas colunas para os cartões inferiores
col1, col2 = st.columns(2)

for i, item in enumerate(itens_projeto):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        st.markdown(f"<div class='card-item'><b style='color: #ff9f1c;'>{item['Item']}</b>", unsafe_allow_html=True)
        
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            # Agora a quantidade reage dinamicamente aos inputs do topo através da variável 'Qtd_Sugerida'
            nova_qtd = st.number_input(
                f"{item['Item']} (Qtd)", 
                min_value=0.0, 
                value=float(item['Qtd_Sugerida']), 
                step=1.0 if item['Qtd_Sugerida'] >= 1 else 0.1,
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
        
        st.markdown("</div>", unsafe_allow_html=True)
        total_item = nova_qtd * novo_preco
        dados_atualizados.append({
            "Item": item['Item'],
            "Quantidade": nova_qtd,
            "Preço Unitário (R$)": novo_preco,
            "Total (R$)": total_item
        })

# Processamento do DataFrame e Totais Finais
df = pd.DataFrame(dados_atualizados)
subtotal_materiais = df["Total (R$)"].sum()

# Taxa de 5% de Massas e Telas conforme a planilha original
taxa_massas_telas = subtotal_materiais * 0.05

# Configuração da Barra Lateral (Painel Financeiro)
st.sidebar.markdown("<h2 style='color: #ffffff; text-align: center;'>📊 Painel Financeiro</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.markdown("<b style='color: #ffffff;'>🛠️ Custos Adicionais:</b>", unsafe_allow_html=True)

# Mão de obra parametrizada (Padrão: 30 dias a R$ 755,00)
dias_trabalho = st.sidebar.number_input("Dias de Execução", min_value=0, value=30, step=1)
valor_diaria = st.sidebar.number_input("Valor da Diária (R$)", min_value=0.0, value=755.0, step=5.0)
mao_de_obra = dias_trabalho * valor_diaria

st.sidebar.markdown("---")

# Cálculo do Custo Total
total_geral = subtotal_materiais + taxa_massas_telas + mao_de_obra

# Painel de Resultados Lateral
st.sidebar.markdown(f"""
    <div class='card-total'>
        <h4>Subtotal Materiais</h4>
        <p>R$ {subtotal_materiais:,.2f}</p>
    </div>
    <div class='card-total' style='border-left-color: #a2d2ff;'>
        <h4>Massas, Telas (5%)</h4>
        <p style='color: #a2d2ff;'>R$ {taxa_massas_telas:,.2f}</p>
    </div>
    <div class='card-total'>
        <h4>Mão de Obra ({dias_trabalho} dias)</h4>
        <p>R$ {mao_de_obra:,.2f}</p>
    </div>
    <div class='card-total' style='border-left-color: #30d158;'>
        <h4>Total Geral da Obra</h4>
        <p style='color: #30d158;'>R$ {total_geral:,.2f}</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Exportar Dados
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="📥 Exportar Orçamento",
    data=csv,
    file_name='orcamento_calculadora.csv',
    mime='text/csv',
    use_container_width=True
)
