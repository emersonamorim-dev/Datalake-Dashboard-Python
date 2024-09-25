import streamlit as st
import pandas as pd
import os
import json
import geopandas as gpd
import plotly.express as px
from datetime import timedelta

# Configuração inicial da página
st.set_page_config(page_title="Dashboard Datalake - Minsait", layout="wide")

# Sidebar para seleção de exibição
view_option = st.sidebar.selectbox(
    "Escolha a visualização",
    ("Home", "Visualizar por horas", "Visualizar por regiões no mapa")
)

# carrega e processa dados do arquivo JSON
def load_data_from_json(file_path):
    if not os.path.exists(file_path):
        st.warning("Nenhum arquivo de dados foi encontrado.")
        return pd.DataFrame()  

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            all_data = []
            # Iterar pelas regiões (north, south, east, west)
            for zone, zone_data in data.items():
                if 'data' in zone_data and isinstance(zone_data['data'], list):
                    for parameter_data in zone_data['data']:
                        if 'coordinates' in parameter_data and isinstance(parameter_data['coordinates'], list):
                            for coord_data in parameter_data['coordinates']:
                                for date_record in coord_data['dates']:
                                    all_data.append({
                                        'zone': zone.capitalize(),
                                        'timestamp': date_record.get('date'),
                                        'temperature': date_record.get('value'),  # Valor da temperatura
                                        'latitude': coord_data.get('lat'),
                                        'longitude': coord_data.get('lon')
                                    })
                else:
                    st.error(f"Dados da zona {zone} não estão no formato esperado.")
        except json.JSONDecodeError:
            st.error(f"Erro ao ler o arquivo JSON: {file_path}")
            return pd.DataFrame()

    # Retorna um DataFrame com os dados agregados
    return pd.DataFrame(all_data)

# exibe gráficos profissionais com Plotly 
def show_professional_charts(df):
    st.write("Visualização Profissional por Zona:")
    # Converte o campo 'timestamp' para datetime para facilitar o gráfico
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  

    for zone in df['zone'].unique():
        zone_data = df[df['zone'] == zone]
        
        if zone_data.empty:
            st.write(f"Sem dados para a Zona {zone}")
        else:
            st.subheader(f"Zona {zone}")
            # Cria gráfico usando Plotly Express
            fig = px.line(
                zone_data,
                x='timestamp',
                y='temperature',
                title=f"Temperatura ao Longo do Tempo - Zona {zone}",
                labels={'timestamp': 'Data e Hora', 'temperature': 'Temperatura (°C)'}
            )
            fig.update_layout(
                xaxis_title="Data e Hora",
                yaxis_title="Temperatura (°C)",
                title_font_size=24,
                xaxis_tickformat='%d/%m %H:%M',
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12),
                hovermode="x unified"
            )
            st.plotly_chart(fig)

# exibe gráficos por intervalo de horas (visualização por horas)
def show_professional_charts_by_hours(df, hours_interval):
    st.write(f"Visualização Profissional por Zona - Intervalo de {hours_interval} horas:")
    # Converter o campo 'timestamp' para datetime para facilitar o gráfico
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  

    # Filtra os dados com base no intervalo de horas selecionado
    max_timestamp = df['timestamp'].max()
    min_timestamp = max_timestamp - timedelta(hours=hours_interval)
    filtered_df = df[df['timestamp'] >= min_timestamp]

    for zone in filtered_df['zone'].unique():
        zone_data = filtered_df[filtered_df['zone'] == zone]
        
        if zone_data.empty:
            st.write(f"Sem dados para a Zona {zone}")
        else:
            st.subheader(f"Zona {zone}")
            # Cria gráfico usando Plotly Express
            fig = px.line(
                zone_data,
                x='timestamp',
                y='temperature',
                title=f"Temperatura ao Longo do Tempo - Zona {zone}",
                labels={'timestamp': 'Data e Hora', 'temperature': 'Temperatura (°C)'}
            )
            fig.update_layout(
                xaxis_title="Data e Hora",
                yaxis_title="Temperatura (°C)",
                title_font_size=24,
                xaxis_tickformat='%d/%m %H:%M',
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Arial, sans-serif", size=12),
                hovermode="x unified"
            )
            st.plotly_chart(fig)

# exibe o gráfico por regiões em um mapa usando GeoPandas e Plotly
def show_map_by_region(df):
    st.write("Visualização das Regiões de São Paulo no Mapa")
    
    # GeoJSON simulado para as regiões de São Paulo (substitua pelo GeoJSON oficial)
    geojson_regions = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "properties": {"zone": "North"}, "geometry": {"type": "Polygon", "coordinates": [[[-46.63611, -23.5489], [-46.63611, -23.6389], [-46.54611, -23.6389], [-46.54611, -23.5489]]]}},
            {"type": "Feature", "properties": {"zone": "South"}, "geometry": {"type": "Polygon", "coordinates": [[[-46.63611, -23.6889], [-46.63611, -23.7889], [-46.54611, -23.7889], [-46.54611, -23.6889]]]}},
            {"type": "Feature", "properties": {"zone": "East"}, "geometry": {"type": "Polygon", "coordinates": [[[-46.63611, -23.5489], [-46.63611, -23.4489], [-46.54611, -23.4489], [-46.54611, -23.5489]]]}},
            {"type": "Feature", "properties": {"zone": "West"}, "geometry": {"type": "Polygon", "coordinates": [[[-46.63611, -23.5489], [-46.63611, -23.6489], [-46.73611, -23.6489], [-46.73611, -23.5489]]]}}
        ]
    }

    # Carrega o GeoDataFrame das regiões
    gdf = gpd.GeoDataFrame.from_features(geojson_regions["features"])

    # Agrupa os dados de temperatura por zona
    df_grouped = df.groupby("zone")["temperature"].mean().reset_index()

    # Mescla os dados de temperatura com o GeoDataFrame
    gdf = gdf.merge(df_grouped, left_on="zone", right_on="zone")

    # Exibe o mapa
    fig = px.choropleth_mapbox(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color="temperature",
        featureidkey="properties.zone",
        center={"lat": -23.5505, "lon": -46.6333},
        mapbox_style="open-street-map",
        zoom=10,
        title="Mapa de Temperatura por Região de São Paulo",
        labels={"temperature": "Temperatura (°C)"}
    )

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

# Exibe Home, por Horas, ou por Regiões conforme seleção
if view_option == "Home":
    # Título principal da Home
    st.title("Dashboard Datalake - Minsait: Home")
    st.write("Monitoramento geral da temperatura do ar em São Paulo.")
    
    # Caminho do arquivo JSON
    data_file = 'data/raw/processed/data.json'
    
    # Carrega os dados do arquivo JSON
    df = load_data_from_json(data_file)
    
    # Se o DataFrame não estiver vazio, exibir os gráficos
    if not df.empty:
        show_professional_charts(df)
    else:
        st.error("Nenhum dado disponível para visualização.")

elif view_option == "Visualizar por horas":
    # Sidebar para seleção de intervalo de horas
    st.sidebar.title("Configuração de Exibição")
    hours_options = [3, 6, 9, 12, 15, 18, 21, 24]
    selected_hours = st.sidebar.selectbox("Selecione o intervalo de horas:", hours_options)

    # Título principal da visualização por horas
    st.title(f"Dashboard Datalake - Minsait: Visualização por {selected_hours} Horas")
    
    # Caminho do arquivo JSON
    data_file = 'data/raw/processed/data.json'
    
    # Carrega os dados do arquivo JSON
    df = load_data_from_json(data_file)
    
    # Se o DataFrame não estiver vazio, exibir os gráficos
    if not df.empty:
        show_professional_charts_by_hours(df, selected_hours)
    else:
        st.error("Nenhum dado disponível para visualização.")

elif view_option == "Visualizar por regiões no mapa":
    # Título da visualização por regiões
    st.title("Dashboard Datalake - Minsait: Visualização por Regiões no Mapa")

    # Caminho do arquivo JSON
    data_file = 'data/raw/processed/data.json'

    # Carrega os dados do arquivo JSON
    df = load_data_from_json(data_file)

    # Se o DataFrame não estiver vazio, exibir o mapa
    if not df.empty:
        show_map_by_region(df)
    else:
        st.error("Nenhum dado disponível para visualização.")
