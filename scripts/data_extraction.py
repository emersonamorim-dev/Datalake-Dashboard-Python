import requests
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth

def extract_meteomatics_data():
    # Base URL da API Meteomatics
    api_url_base = 'https://api.meteomatics.com'
    
    # Usuário e senha
    username = 'SeuUsuario'  
    password = 'SuaSenha'  
    
    # Período de tempo de interesse 
    start_date = "2024-09-24"
    end_date = "2024-10-05"
    
    # Coordenadas para as regiões de São Paulo
    coordinates = {
        "north": "-23.4939,-46.6246",   # Zona Norte (Santana)
        "south": "-23.6525,-46.7151",   # Zona Sul (Santo Amaro)
        "east": "-23.5401,-46.4512",    # Zona Leste (Itaquera)
        "west": "-23.5617,-46.6883"     # Zona Oeste (Pinheiros)
    }
    
    # Dicionário para armazenar os dados de chuva
    rain_data = {}
    
    # Itera pelas regiões e coletar os dados
    for region, coords in coordinates.items():
        # Monta a URL da API com as coordenadas e datas
        url = f"{api_url_base}/{start_date}T00:00:00Z--{end_date}T00:00:00Z/t_2m:C/{coords}/json"
        
        try:
            # Faz a requisição à API
            response = requests.get(url, auth=HTTPBasicAuth(username, password))
            
            if response.status_code == 200:
                # Armazena os dados da região no dicionário
                rain_data[region] = response.json()
                print(f"Dados extraídos com sucesso para {region}.")
            else:
                print(f"Erro ao extrair dados para {region}: {response.status_code} - {response.text}")
        
        except Exception as e:
            print(f"Ocorreu um erro ao extrair dados para {region}: {str(e)}")
    
    # Define o caminho fixo do arquivo JSON para salvar os dados
    output_path = "data/raw/processed/data.json"
    
    # Salva os dados no arquivo JSON
    with open(output_path, "w") as f:
        json.dump(rain_data, f)
    
    print(f"Dados salvos com sucesso em {output_path}")
    return rain_data

# Configuração da API e coleta de dados
if __name__ == "__main__":
    extract_meteomatics_data()


