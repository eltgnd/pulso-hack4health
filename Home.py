import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_gsheets import GSheetsConnection
from st_pages import *
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_image_select import image_select
import datetime
from PIL import Image

# Page config
st.set_page_config(page_title='Project PULSO', page_icon='❤️', layout="centered", initial_sidebar_state="auto", menu_items=None)


# Bypass log-in
# st.session_state["password_correct"] = True 


# Google Sheets Connection
conn = st.connection("user", type=GSheetsConnection)

# Initialize
placeholder = st.empty()

# Title
# st.image('images/logo.png', width=150) 
add_vertical_space(1)
st.caption('🧑‍⚕️ PULSO | Predictive Understanding for Localized Health Surveillance and Optimization')

add_vertical_space(1)
login_placeholder = st.empty()
with login_placeholder:
    st.markdown(f"""
        <div style="line-height:450%;">
            <span style=" font-size:80px ; color:#31333F ; font-weight:bold; ">Tagapag-alaga ng bawat </span>
            <span style=" font-size:80px ; color:#B23939 ; font-weight:bold; ">Pilipino</span>
            <span style=" font-size:80px ; color:#31333F ; font-weight:bold; ">.</span>
        </div>""",
        unsafe_allow_html=True
    )

placeholder = st.empty()
with placeholder:
    with st.container(border=True):
        st.write('🔓 Try this sample ID: admin, password: test')

# User Authentication
def check_password():
    # Log-in
    def log_in():
        with st.form('Credentials'):
            st.text_input("Enter user ID", type='default', key='user_id')
            st.text_input("Enter your password", type="password", key="password")
            st.form_submit_button("Log-in", on_click=password_entered)
 
    def password_entered():
        sql = 'SELECT * FROM Sheet1;'
        df = conn.query(sql=sql, ttl=0) 
        match = (df['user_id'].eq(st.session_state.user_id) & df['password'].eq(st.session_state.password)).any()
        if match:
            st.session_state["password_correct"] = True  
            st.session_state['user_id'] = st.session_state.user_id

            # Save information as session-state
            st.session_state['name'] = df[df.user_id == st.session_state.user_id].reset_index().at[0,'name']
            st.session_state['municipality'] = 'LINGAYEN'
            st.session_state['latitude'] = df[df.user_id == st.session_state.user_id].reset_index().at[0,'latitude']
            st.session_state['longitude'] = df[df.user_id == st.session_state.user_id].reset_index().at[0,'longitude']

        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    log_in()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

if not check_password():
    st.stop()

# Start
login_placeholder.empty()
placeholder.empty()

st.markdown(f"""
    <div style="line-height:450%;">
        <span style=" font-size:60px ; color:#31333F ; font-weight:bold; ">Welcome, </span>
        <span style=" font-size:60px ; color:#31333F ; font-weight:regular; ">{st.session_state.name}</span>
        <span style=" font-size:60px ; color:#31333F ; font-weight:bold; ">👋</span>
    </div>""",
    unsafe_allow_html=True
)

# Welcome
hide_pages(['Home.py'])
show_pages(
    [
        # Page('Home.py222222', 'Homepage', '👤'),

        Section(name='PULSO Track'),

        Page('menu_pages/dashboard.py', 'Dashboard', '📊', in_section=True),
        Page('menu_pages/geo.py', 'Geomapping', '🗺️'),

        Section(name='PULSO Predict'),

        Page('menu_pages/predict_disease.py', 'Disease Predict', '🔎'),
        Page('menu_pages/forecast.py', 'Forecast', '📉'),
        Page('menu_pages/simulate.py', 'Simulation', '🖥️'),

        Section(name='PULSO Prevent'),

        Page('menu_pages/sms.py', 'SMS', '📶'),
        Page('menu_pages/about.py', 'About', '💡'),
    ]
)


# Information about the app
st.write('PULSO is a web application to be used by government health offices that utilizes data science to monitor and predict their constituent’s health data.')
col1, col2 = st.columns(2)
with col1:
    with st.expander(label='HOW DOES PULSO WORK', expanded=False):
        st.write("""Data will be regularly sourced from the government and through the input of healthcare professionals recognized by the Department of Health, who are mandated to update patient data during every consultation. 
Utilizing this comprehensive dataset, the web application will provide various functionalities, primarily driven by (1) dashboarding, (2) geo-mapping, and (3) epidemiology models. 
""")
with col2:
    with st.expander(label='WHY PULSO'):
        section_text = ''
        st.markdown("The web app will be used as a tool to help government decision-making concerned with rapid intervention, policies, and programs on public health. By focusing on community-level health monitoring, the app aims to improve healthcare outcomes and address specific health needs of Filipino populations across both urban and rural areas.")

st.divider()

with st.container(border=True):
    st.write('💡 Begin utilizing PULSO by visiting its tools under PULSO Track, PULSO Predict, and PULSO Prevent.')