import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora de Orçamento - Construção", layout="wide")

st.title("🏗️ Calculadora de Materiais e Orçamento")
st.markdown("Ajuste as quantidades para recalcular o orçamento total do projeto em tempo real.")

# Dados base extraídos da tabela
dados_iniciais = [
    {"Item": "Perfil 90x0,80", "Quantidade": 63.0, "Preço Unitário (R$)": 50.0},
    {"Item": "Guia Perimetral", "Quantidade": 50.0, "Preço Unitário (R$)": 50.0},
    {"Item": "Plywood 8mm", "Quantidade": 55.0, "Preço Unitário (R$)": 80.0},
    {"Item": "Placa ST 12.5mm", "Quantidade": 40.0, "Preço Unitário (R$)": 40.0},
    {"Item": "Placa Cimentícia 12mm", "Quantidade": 30.0, "Preço Unitário (R$)": 140.0},
    {"Item": "Lã PET", "Quantidade": 5.0, "Preço Unitário (R$)": 200.0},
    {"Item": "Parafusos (Cento)", "Quantidade": 12.0, "Preço Unitário (R$)": 35.0},
    {"Item": "Massas (Balde/Saco)", "Quantidade": 1.0, "Preço Unitário (R$)": 500.0},
    {"Item": "Telas (Rolo)", "Quantidade": 1.0, "Preço Unitário (R$)": 500.0},
    {"Item": "Adesivo PU (Cx)", "Quantidade": 1.0, "Preço Unitário (R$)": 150.0},
    {"Item": "Telha Sanduíche", "Quantidade": 10.0, "Preço Unitário (R$)": 400.0},
    {"Item": "Manta Hidrófuga", "Quantidade": 2.0, "Preço Unitário (R$)": 1000.0},
]

st.header("📋 Quantitativo de Materiais")
dados_atualizados = []

# Criando colunas de inputs interativos
col1, col2 = st.columns(2)

for i, item in enumerate(dados_iniciais):
    target_col = col1 if i % 2 == 0 else col2
    with target_col:
        nova_qtd = st.number_input(
            f"{item['Item']} (Qtd)", 
            min_value=0.0, 
            value=float(item['Quantidade']), 
            step=1.0,
            key=f"qtd_{i}"
        )
        novo_preco = st.number_input(
            f"{item['Item']} (Preço R$)", 
            min_value=0.0, 
            value=float(item['Preço Unitário (R$)']), 
            step=5.0,
            key=f"prc_{i}"
        )
        total_item = nova_qtd * novo_preco
        dados_atualizados.append({
            "Item": item['Item'],
            "Quantidade": nova_qtd,
            "Preço Unitário (R$)": novo_preco,
            "Total (R$)": total_item
        })

# Criar DataFrame e calcular totais
df = pd.DataFrame(dados_atualizados)

st.subheader("📊 Resumo do Orçamento")
st.dataframe(df.style.format({"Preço Unitário (R$)": "R$ {:.2f}", "Total (R$)": "R$ {:.2f}"}), use_container_width=True)

total_materiais = df["Total (R$)"].sum()

st.sidebar.header("💰 Custos Adicionais")
mao_de_obra = st.sidebar.number_input("Mão de Obra (20 dias)", min_value=0.0, value=11635.0, step=100.0)

total_geral = total_materials = total_materiais + mao_de_obra

# Exibição dos resultados finais
st.sidebar.markdown("---")
st.sidebar.metric(label="Total Materiais", value=f"R$ {total_materiais:,.2f}")
st.sidebar.metric(label="Total Mão de Obra", value=f"R$ {mao_de_obra:,.2f}")
st.sidebar.subheader(f"Total Geral: R$ {total_geral:,.2f}")

# Opção de download dos dados atualizados
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Exportar Orçamento em CSV",
    data=csv,
    file_name='orcamento_atualizado.csv',
    mime='text/csv',
)
