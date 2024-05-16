import streamlit as st

# Page config
st.set_page_config(page_title='PULSO SMS', page_icon='📶', layout="centered", initial_sidebar_state="auto", menu_items=None)

# Title
st.title('📶 PULSO SMS')
st.write('Lorem ipsum')

st.divider()


# Demographic demo
with st.container(border=True):
    col1, col2 = st.columns(2)
    col1.selectbox('Select age group', )