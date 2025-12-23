# Instalar bibliotecas.
# 1 - digitar no terminal pip install pandas, streamlit, openpyxl
# 2 - digitar no terminal python -m streamlit run app.py


import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ranking", layout="wide")
st.title("📊 Ranking - Comparação")

uploaded_file = st.file_uploader(
    "Faça upload do arquivo RATING.xlsx",
    type=["xlsx"]
)

if uploaded_file:
    # Ler planilhas
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
    df2 = pd.read_excel(uploaded_file, sheet_name='Sheet2')
    
    # Remover coluna 'Id' se existir
    if 'Id' in df.columns:
        df = df.drop(columns=['Id'])
    if 'Id' in df2.columns:
        df2 = df2.drop(columns=['Id'])

    # Ordenar para manter alinhamento
    df = df.sort_values(by='nome').reset_index(drop=True)
    df2 = df2.sort_values(by='nome').reset_index(drop=True)

    # Manter estrutura
    df3 = df.copy()

    # Variacao vem do RANK da Sheet2
    df3['Variacao'] = df2['RANK'].fillna(0)

    # Ranking Atual = RANK + Variacao
    df3['Ranking_Atual'] = df3['RANK'] + df3['Variacao']

    # Conversão segura
    df3['Variacao'] = df3['Variacao'].astype(int)
    df3['Ranking_Atual'] = df3['Ranking_Atual'].astype(int)

    # Criar ID (maior RANK = 1)
    df3['ID'] = (
        df3['RANK']
        .rank(method='dense', ascending=False)
        .astype(int)
    )

    # Criar coluna visual da variação
    def format_variacao(valor):
        if valor > 0:
            return f"{valor} ↑"
        elif valor < 0:
            return f"{valor} ↓"
        else:
            return f"{valor}"

    df3['Variacao'] = df3['Variacao'].apply(format_variacao)

    # Ordenar pelo ID (1 primeiro)
    df3 = df3.sort_values(by='ID', ascending=True).reset_index(drop=True)

    # Reordenar colunas (ID primeiro)
    cols = ['ID'] + [c for c in df3.columns if c != 'ID']
    df3 = df3[cols]

    # Colorir variação
    def color_variacao(val):
        if '↑' in val:
            return 'color: green; font-weight: bold'
        elif '↓' in val:
            return 'color: red; font-weight: bold'
        else:
            return 'color: gray'

    styled_df = df3.style.applymap(
        color_variacao,
        subset=['Variacao']
    )

    st.subheader("📋 Tabela de Ranking")
    st.dataframe(styled_df, use_container_width=True)

else:
    st.info("⬆️ Envie o arquivo Excel para visualizar os dados.")