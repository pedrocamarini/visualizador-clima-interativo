# api_client.py
import requests
import pandas as pd

def get_climate_data(latitude, longitude, start_date, end_date):
    """
    Busca dados climáticos históricos de uma API para um local e período específicos.
    Usa a API 'archive' da Open-Meteo, que é a correta para dados passados.
    """
    
    # URL base para a API de dados históricos
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    
    # Parâmetros da nossa requisição
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": "America/Sao_Paulo"
    }
    
    try:
        # A biblioteca requests montará a URL final de forma segura
        response = requests.get(base_url, params=params)
        
        # Isso vai gerar um erro para respostas ruins (4xx ou 5xx)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Imprime o erro no terminal para depuração
        print(f"Erro ao fazer a requisição para a API: {e}")
        return None

def process_climate_data(api_data):
    """
    Converte os dados brutos da API em um DataFrame do Pandas,
    que é muito mais fácil de usar para visualizações.
    """
    if not api_data or 'daily' not in api_data:
        return None
    
    daily_data = api_data['daily']
    
    # Cria o DataFrame a partir do dicionário de dados diários
    df = pd.DataFrame(daily_data)
    
    # Converte a coluna 'time' para o formato de data, o que é essencial para gráficos
    df['time'] = pd.to_datetime(df['time'])
    
    # Renomeia as colunas para nomes mais amigáveis em português
    df.rename(columns={
        'time': 'data',
        'temperature_2m_max': 'temp_max_c',
        'precipitation_sum': 'precipitacao_mm'
    }, inplace=True)
    
    return df