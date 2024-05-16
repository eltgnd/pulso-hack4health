import streamlit as st
import geopandas as gpd
import pandas as pd
import leafmap.foliumap as leafmap
import requests

# Page config
st.set_page_config(page_title='Geo', page_icon='🗺️', layout="wide", initial_sidebar_state="auto", menu_items=None)

# Title
st.title('🗺️ Geomapping')

# Load geospatial data
@st.cache_data
def load_geospatial(shp_location):
    latitude, longitude = float(st.session_state['latitude']), float(st.session_state['longitude']) 
    gdf = gpd.read_file(shp_location)
    gdf.rename(columns={'ADM3_EN': 'MUNICITY', 'ADM2_EN': 'PROVINCE', 'ADM1_EN':'REGION'}, inplace=True)
    return gdf

shp_location = 'datasets/phl_adminboundaries_candidate_adm3/phl_admbnda_adm3_psa_namria_20200529.shp'
gdf = load_geospatial(shp_location)

# Specific municipality
st.session_state['municipality'] = 'Lingayen'
municipality_gdf = gdf[gdf['MUNICITY'] == st.session_state.municipality]

# Display boundary
centroid = municipality_gdf.geometry.centroid.iloc[0]
m = leafmap.Map(center=[centroid.y, centroid.x], zoom=12)


###################

# Add the municipality boundaries to the map
m.add_gdf(municipality_gdf, layer_name='Municipality Border')

facilities = pd.read_csv('datasets/pangasinan.csv')
filtered_facilities = facilities[facilities['City/Municipality Name'] == 'LINGAYEN (CAPITAL)']
filtered_facilities = filtered_facilities.dropna(subset=['Latitude', 'Longitude'])

m.add_points_from_xy(
    filtered_facilities,
    x="Longitude",
    y="Latitude",
    icon_names=["gear", "map", "leaf", "globe"],
    spin=True,
    add_legend=True,
    layer_name='Health Facilities'
)

###################

# Add heat index
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

# Add the heatmap layer to the map
m.add_heatmap(
    generate_heat_index_df(),
    latitude='Latitude',
    longitude='Longitude',
    value='Heat_Index',
    name='Heat Index',
    radius=40
)

# Display
m.to_streamlit(height=700)


# col1, col2 = st.columns([4, 1])
# options = list(leafmap.basemaps.keys())
# index = options.index("OpenTopoMap")

# with col2:
#     basemap = st.selectbox("Select a basemap:", options, index)


# with col1:
#     # Longitude and latitude of municipality
#     latitude, longitude = float(st.session_state['latitude']), float(st.session_state['longitude']) 

#     m = leafmap.Map(
#         locate_control=True, latlon_control=True, draw_export=True, minimap_control=True,
#         center=[latitude, longitude], zoom=12
#     )
#     m.add_basemap(basemap)
#     m.to_streamlit(height=700)