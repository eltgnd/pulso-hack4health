import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_gsheets import GSheetsConnection
from st_pages import Page, Section,show_pages, add_page_title
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_image_select import image_select
import datetime
from PIL import Image

# Page config
st.set_page_config(page_title='Project PULSO', page_icon='💙', layout="centered", initial_sidebar_state="auto", menu_items=None)


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
            <span style=" font-size:80px ; color:#023E8A ; font-weight:bold; ">Lorem </span>
            <span style=" font-size:80px ; color:#31333F ; font-weight:bold; ">ipsum</span>
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
            st.session_state['name'] = df[df.user_id == st.session_state.user_id].reset_index().at[0,'name']
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
        <span style=" font-size:60px ; color:#023E8A ; font-weight:bold; ">{st.session_state.name}</span>
        <span style=" font-size:60px ; color:#31333F ; font-weight:bold; ">👋</span>
    </div>""",
    unsafe_allow_html=True
)

# Welcome
show_pages(
    [
        Page('Home.py', 'Homepage', '👤'),

        Section(name='Policy and Operations'),

        Page('menu_pages/dashboard.py', 'Dashboard', '📊', in_section=True),
        Page('menu_pages/geo.py', 'Geomapping', '🗺️'),

        Section(name='Smart Predict'),

        Page('menu_pages/ml.py', 'Diabetes', '💉'),
        Page('menu_pages/simulate.py', 'Simulation', '🖥️'),

        Section(name='Smart Prevent'),

        Page('menu_pages/sms.py', 'SMS', '📶'),
        Page('menu_pages/post.py', 'Announcements', '📲'),
        Page('menu_pages/about.py', 'About', '💡'),
    ]
)