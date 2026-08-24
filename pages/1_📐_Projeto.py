import streamlit as st
import pandas as pd
from datetime import date
import math

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Calculadora Steel Framing",
    page_icon="📐",
    layout="wide",
)

# ============================================================
# CSS CUSTOMIZADO - DESIGN PROFISSIONAL
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://googleapis.com');

    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    .stApp {
        background: #f5f7fa;
    }
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    div[data-testid="stVerticalBlock"] > div:has(h1) {
        background: linear-gradient(135deg, #17202a 0%, #263746 55%, #34495e 100%);
        border-radius: 18px;
        padding: 35px 38px 30px 38px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
    }
    div[data-testid="stVerticalBlock"] h1 {
        color: #6fa8c9 !important;
        font-size: 3.5rem !important;
        line-height: 1.2 !important;
        font-weight: 900 !important;
        letter-spacing: -1px !important;
        margin: 0 0 10px 0 !important;
        border: none !important;
    }
    div[data-testid="stVerticalBlock"] h1 + p {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título Principal do Aplicativo
st.title("📐 Detalhamento do Projeto")
st.markdown("Preencha as dimensões da estrutura para gerar automaticamente a lista de materiais necessários.")

# ============================================================
# SEÇÃO 1: INFORMAÇÕES DO CLIENTE E DIMENSÕES
# ============================================================
st.header("📋 Informações Gerais")
col_cli1, col_cli2 = st.columns(2)
with col_cli1:
    cliente = st.text_input("Nome do Cliente", value="João Silva")
with col_cli2:
    data_projeto = st.date_input("Data do Orçamento", date.today())

st.header("🏠 Dimensões da Estrutura")
col_dim1, col_dim2, col_dim3 = st.columns(3)
with col_dim1:
    area_total = st.number_input("Área Total de Paredes (m²)", min_value=1.0, value=90.0, step=5.0)
with col_dim2:
    pe_direito = st.number_input("Pé Direito (m)", min_value=1.0, value=3.0, step=0.1)
with col_dim3:
    area_cobertura = st.number_input("Área de Cobertura/Telhado (m²)", min_value=0.0, value=80.0, step=5.0)

# Preços padrão de mercado
PRECOS_BASE = {
    "perfil": 50.0, "guia": 50.0, "plywood": 80.0, "placa_st": 40.0,
    "placa_cimenticia": 140.0, "la_pet": 200.0, "parafusos": 35.0,
    "massas": 500.0, "telas": 500.0, "adesivo": 150.0, "telha": 400.0, "manta": 1000.0
}

# ============================================================
# SEÇÃO 2: CÁLCULOS DE ENGENHARIA DE MATERIAIS
# ============================================================
qtd_perfil = area_total * 1.25
qtd_guia = area_total * 0.55
qtd_plywood = area_total / 2.2
qtd_placa_st = area_total / 2.4
qtd_cimenticia = area_total / 2.4
qtd_la = area_total / 10.0
qtd_parafuso = area_total * 0.5
qtd_massa = area_total / 30.0
qtd_tela = area_total / 40.0
qtd_adesivo = area_total / 15.0
qtd_telha = area_cobertura * 1.15
qtd_manta = area_cobertura / 50.0

lista_materiais = [
    {"nome": "Perfil 90x0,80", "qtd": qtd_perfil, "preco": PRECOS_BASE["perfil"]},
    {"nome": "Guia Perimetral", "qtd": qtd_guia, "preco": PRECOS_BASE["guia"]},
    {"nome": "Plywood 8mm", "qtd": qtd_plywood, "preco": PRECOS_BASE["plywood"]},
    {"nome": "Placa ST 12.5mm", "qtd": qtd_placa_st, "preco": PRECOS_BASE["placa_st"]},
    {"nome": "Placa Cimentícia 12mm", "qtd": qtd_cimenticia, "preco": PRECOS_BASE["placa_cimenticia"]},
    {"nome": "Lã PET", "qtd": qtd_la, "preco": PRECOS_BASE["la_pet"]},
    {"nome": "Parafusos (Cento)", "qtd": qtd_parafuso, "preco": PRECOS_BASE["parafusos"]},
    {"nome": "Massas (Balde/Saco)", "qtd": qtd_massa, "preco": PRECOS_BASE["massas"]},
    {"nome": "Telas (Rolo)", "qtd": qtd_tela, "preco": PRECOS_BASE["telas"]},
    {"nome": "Adesivo PU (Cx)", "qtd": qtd_adesivo, "preco": PRECOS_BASE["adesivo"]},
    {"nome": "Telha Sanduíche", "qtd": qtd_telha, "preco": PRECOS_BASE["telha"]},
    {"nome": "Manta Hidrófuga", "qtd": qtd_manta, "preco": PRECOS_BASE["manta"]},
]

# ============================================================
# SEÇÃO 3: RENDERS E AJUSTES VISUAIS (CORRIGIDO SEM HTML ESPAN)
# ============================================================
st.header("📋 Insumos Calculados Automaticamente")
st.markdown("Ajuste refinado de quantidades e valores unitários:")

dados_atualizados = []
total_materiais = 0.0

col_grid1, col_grid2 = st.columns(2)

for idx, mat in enumerate(lista_materiais):
    coluna_painel = col_grid1 if idx % 2 == 0 else col_grid2
    with coluna_painel:
        st.subheader(f"🔹 {mat['nome']}")
        c_qtd, c_prc = st.columns(2)
        with c_qtd:
            nova_qtd = st.number_input(f"{mat['nome']} (Qtd)", min_value=0.0, value=float(round(mat['qtd'], 1)), key=f"q_{idx}")
        with c_prc:
            novo_prc = st.number_input(f"{mat['nome']} (Preço R$)", min_value=0.0, value=float(mat['preco']), key=f"p_{idx}")
        
        subtotal_calculado = nova_qtd * novo_prc
        total_materiais += subtotal_calculado
        
        dados_atualizados.append({
            "Item": mat['nome'],
            "Quantidade": nova_qtd,
            "Preço Unitário": novo_prc,
            "Total Item": subtotal_calculado
        })
        
        # AQUI FOI CORRIGIDO: Exibição limpa oficial do Streamlit
        st.write(f"**Subtotal do Item:** R$ {subtotal_calculado:,.2f}")
        st.write("---")

# ============================================================
# SEÇÃO 4: RESUMO E EXPORTAÇÃO
# ============================================================
st.header("📊 Resumo Consolidado do Orçamento")
df_resumo = pd.DataFrame(dados_atualizados)
st.dataframe(df_resumo.style.format({"Preço Unitário": "R$ {:.2f}", "Total Item": "R$ {:.2f}"}), use_container_width=True)

# Configurações na barra lateral
st.sidebar.header("💰 Custos de Instalação")
mao_de_obra = st.sidebar.number_input("Mão de Obra Geral (R$)", min_value=0.0, value=11635.0, step=100.0)
total_geral = total_materiais + mao_de_obra

st.sidebar.markdown("---")
st.sidebar.metric(label="Total Materiais", value=f"R$ {total_materiais:,.2f}")
st.sidebar.metric(label="Total Mão de Obra", value=f"R$ {mao_de_obra:,.2f}")
st.sidebar.subheader(f"Total Geral: R$ {total_geral:,.2f}")

# Download da planilha
csv_data = df_resumo.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Exportar Orçamento Completo (CSV)",
    data=csv_data,
    file_name=f'orcamento_steel_{cliente}_{data_projeto}.csv',
    mime='text/csv',
)
