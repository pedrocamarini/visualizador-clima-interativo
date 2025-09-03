# api_client.py
import requests

def get_climate_data(latitude, longitude):
    """Busca dados climáticos para uma latitude e longitude específicas."""
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&"
        f"daily=temperature_2m_max,precipitation_sum&"
        f"timezone=America/Sao_Paulo"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição para a API: {e}")
        return None

if __name__ == "__main__":
    # Coordenadas de exemplo: São Paulo, Brasil
    lat_sp = -23.55
    lon_sp = -46.63
    
    print("Buscando dados para São Paulo...")
    climate_data = get_climate_data(lat_sp, lon_sp)
    
    if climate_data:
        print("Dados recebidos com sucesso!")
        for i in range(5):
            date = climate_data['daily']['time'][i]
            temp_max = climate_data['daily']['temperature_2m_max'][i]
            precip = climate_data['daily']['precipitation_sum'][i]
            print(f"Data: {date}, Temp. Máx: {temp_max}°C, Precipitação: {precip}mm")