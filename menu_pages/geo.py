import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import leafmap.foliumap as leafmap
from streamlit_gsheets import GSheetsConnection
import requests


# Page config
st.set_page_config(page_title='Geo', page_icon='🗺️', layout="wide", initial_sidebar_state="auto", menu_items=None)

# Title
st.title('🗺️ Geomapping')

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    'Health Facilities',
    'Heat Index',
    'Disease A Chloropleth',
    'Disease B Chloropleth',
    'Disease C Chloropleth',
    'Hospital Beds'
])

# Load geospatial data
@st.cache_data
def load_geospatial(shp_location):
    latitude, longitude = float(st.session_state['latitude']), float(st.session_state['longitude']) 
    gdf = gpd.read_file(shp_location)
    gdf.rename(columns={'ADM3_EN': 'MUNICITY', 'ADM2_EN': 'PROVINCE', 'ADM1_EN':'REGION'}, inplace=True)

    gdf_barangay = gpd.read_file('datasets/phmap/phl_admbnda_adm4_psa_namria_20231106.shp')
    gdf_barangay_filtered = gdf_barangay[gdf_barangay['ADM3_EN'] == 'Lingayen (Capital)']

    np.random.seed(42)
    gdf_barangay_filtered['disease_a'] = np.random.rand(len(gdf_barangay_filtered))
    np.random.seed(13)
    gdf_barangay_filtered['disease_b'] = np.random.rand(len(gdf_barangay_filtered))
    np.random.seed(77)
    gdf_barangay_filtered['disease_c'] = np.random.rand(len(gdf_barangay_filtered))

    return gdf, gdf_barangay_filtered

shp_location = 'datasets/phl_adminboundaries_candidate_adm3/phl_admbnda_adm3_psa_namria_20200529.shp'
gdf, gdf_barangay_filtered = load_geospatial(shp_location)

# Specific municipality
st.session_state['municipality'] = 'Lingayen'
municipality_gdf = gdf[gdf['MUNICITY'] == st.session_state.municipality]
centroid = municipality_gdf.geometry.centroid.iloc[0]

# Map 1 - add facilities
with tab1:
    m_1 = leafmap.Map(center=[centroid.y, centroid.x], zoom=12)
    m_1.add_gdf(gdf_barangay_filtered, layer_name='Municipality Border')

    facilities = pd.read_csv('datasets/pangasinan.csv')
    filtered_facilities = facilities[facilities['City/Municipality Name'] == 'LINGAYEN (CAPITAL)']
    filtered_facilities = filtered_facilities.dropna(subset=['Latitude', 'Longitude'])

    m_1.add_points_from_xy(
        filtered_facilities,
        x="Longitude",
        y="Latitude",
        icon_names=["gear", "map", "leaf", "globe"],
        spin=True,
        add_legend=True,
        layer_name='Health Facilities'
    )
    m_1.to_streamlit(height=700)

# Map 2 - heat index
with tab2:
    m_2 = leafmap.Map(center=[centroid.y, centroid.x], zoom=12)
    m_2.add_gdf(gdf_barangay_filtered, layer_name='Municipality Border')

    @st.cache_data
    def generate_heat_index_df():
        latitude_lst = []
        longitude_lst = []
        heat_index_lst = []

        api_key = st.secrets['openweathermap_api']
        facilities_list = filtered_facilities['Facility Code'].tolist()

        for f in facilities_list:
            f_long = filtered_facilities.loc[filtered_facilities['Facility Code'] == f, 'Longitude'].values[0]
            f_lat = filtered_facilities.loc[filtered_facilities['Facility Code'] == f, 'Latitude'].values[0]
            url = f'http://api.openweathermap.org/data/2.5/weather?lat={f_lat}&lon={f_long}&appid={api_key}&units=metric'

            # Fetch the current weather data
            response = requests.get(url)
            data = response.json()
            # Extract necessary information
            heat_latitude = data['coord']['lat']
            heat_longitude = data['coord']['lon']
            heat_index = data['main']['feels_like']  # Using 'feels_like' as the heat index
            # Add to lst
            latitude_lst.append(heat_latitude)
            longitude_lst.append(heat_longitude)
            heat_index_lst.append(heat_index)
        
        heat_index_df = pd.DataFrame({
        'Latitude': latitude_lst,
        'Longitude': longitude_lst,
        'Heat_Index': heat_index_lst
        })

        return heat_index_df

    m_2.add_heatmap(
        generate_heat_index_df(),
        latitude='Latitude',
        longitude='Longitude',
        value='Heat_Index',
        name='Heat Index',
        radius=40
    )
    m_2.to_streamlit(height=700)


# Maps 3-5 - chloropleth diseases
colors = ['Greens','Oranges','Reds']
map_title = ['Disease A','Disease B','Disease C']
columns = ['disease_a', 'disease_b', 'disease_c']
with tab3:
    m_3 = leafmap.Map(center=[centroid.y, centroid.x], zoom=12)
    m_3.add_gdf(gdf_barangay_filtered, layer_name='Municipality Border')
    m_3.add_data(
        gdf_barangay_filtered,
        column=columns[0], 
        legend_title=f'{map_title[0]} Chloropleth',
        cmap=colors[0],
        scheme='Quantiles', 
        k=5,
        legend_position='bottomright',
        layer_name=map_title[0]
    )
    m_3.to_streamlit(height=700)
with tab4:
    m_4 = leafmap.Map(center=[centroid.y, centroid.x], zoom=12)
    m_4.add_gdf(gdf_barangay_filtered, layer_name='Municipality Border')
    m_4.add_data(
        gdf_barangay_filtered,
        column=columns[1], 
        legend_title=f'{map_title[1]} Chloropleth',
        cmap=colors[1],
        scheme='Quantiles', 
        k=5,
        legend_position='bottomright',
        layer_name=map_title[1]
    )
    m_4.to_streamlit(height=700)
with tab5:
    m_5 = leafmap.Map(center=[centroid.y, centroid.x], zoom=12)
    m_5.add_gdf(gdf_barangay_filtered, layer_name='Municipality Border')
    m_5.add_data(
        gdf_barangay_filtered,
        column=columns[2], 
        legend_title=f'{map_title[2]} Chloropleth',
        cmap=colors[2],
        scheme='Quantiles', 
        k=5,
        legend_position='bottomright',
        layer_name=map_title[2]
    )
    m_5.to_streamlit(height=700)

# Map 6 - hospital beds
with tab6:
    pangasinan = pd.read_csv('datasets\pangasinan.csv')
    conn = st.connection("beds", type=GSheetsConnection) # Google Sheets connection
    sql = 'SELECT * FROM Sheet1;'
    beds = conn.query(sql=sql, ttl=0)
    beds_with_location = beds.merge(pangasinan, on='Facility Name')
    beds_with_location = beds_with_location.dropna(subset=['Latitude', 'Longitude'])

    m_6 = leafmap.Map(center=[centroid.y, centroid.x], zoom=12)
    m_6.add_gdf(gdf_barangay_filtered, layer_name='Municipality Border')

    m_6.add_heatmap(
        beds_with_location,
        latitude='Latitude',
        longitude='Longitude',
        value='Capacity Rate',
        name='Hospital Beds',
        radius=20
    )
    m_6.to_streamlit(height=700)