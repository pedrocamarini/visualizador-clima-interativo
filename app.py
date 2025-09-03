# app.py
import streamlit as st
import pandas as pd
from api_client import get_climate_data, process_climate_data

# --- Configuração da Página ---
st.set_page_config(
    page_title="Visualizador Climático",
    page_icon="🌦️",
    layout="wide"
)

# --- Título e Descrição ---
st.title("🌦️ Visualizador Climático Interativo")
st.markdown("Uma ferramenta para buscar e visualizar dados climáticos históricos.")

# --- Barra Lateral (Sidebar) com os Controles ---
st.sidebar.header("Parâmetros de Busca")

# Inputs para latitude e longitude
lat = st.sidebar.number_input("Latitude", value=-23.55, format="%.2f")
lon = st.sidebar.number_input("Longitude", value=-46.63, format="%.2f")

# Inputs para as datas
start_date = st.sidebar.date_input("Data de Início", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("Data de Fim", value=pd.to_datetime("2023-12-31"))

# --- Lógica Principal e Exibição ---
if st.sidebar.button("Buscar Dados Climáticos"):
    st.subheader(f"Analisando dados de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")

    with st.spinner("Buscando dados na API... Isso pode levar um momento."):
        # 1. Busca os dados brutos (convertendo as datas para o formato string 'YYYY-MM-DD')
        raw_data = get_climate_data(lat, lon, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

    if raw_data:
        # 2. Processa os dados com Pandas
        df = process_climate_data(raw_data)
        st.success("Dados recebidos e processados com sucesso!")

        # 3. Mostra a tabela de dados
        st.subheader("Dados em Tabela")
        st.dataframe(df)

        # 4. Mostra gráficos
        st.subheader("Gráficos do Período")
        
        col1, col2 = st.columns(2) # Cria duas colunas para os gráficos

        with col1:
            st.metric(label="Temp. Média", value=f"{df['temp_max_c'].mean():.1f} °C")
            st.line_chart(df.set_index('data')['temp_max_c'])

        with col2:
            st.metric(label="Precip. Total", value=f"{df['precipitacao_mm'].sum():.1f} mm")
            st.bar_chart(df.set_index('data')['precipitacao_mm'])

    else:
        st.error("Não foi possível buscar os dados. Verifique os parâmetros ou sua conexão com a internet.")