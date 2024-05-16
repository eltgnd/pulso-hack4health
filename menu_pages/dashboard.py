import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
import openai
import random
import time
import base64

# Page config
st.set_page_config(page_title='Dashboard', page_icon='📊', layout="centered", initial_sidebar_state="auto", menu_items=None)


# Title
st.title('📊 PULSO Dashboard')
with st.container(border=True):
    st.caption('❤️ AT A GLANCE')
    st.write("""PULSO Dashboard is your centralized hub for monitoring and managing healthcare data. Stay informed about population well-being, hospital capacity, and disease trends at a glance. From tracking hospital bed utilization to receiving AI-driven recommendations for proactive interventions, this dashboard empowers you to optimize resource allocation and enhance patient care.""")


# On-click function
if 'generate_button' not in st.session_state:
    st.session_state['generate_button'] = False
def update_generate_button():
    st.session_state['generate_button'] = True


with st.container(border=True):
    st.caption('✨ AgapAI')
    st.write('AgapAI is a PULSO feature that utilizes Generative AI to generate recommendations and actionable next steps for your municipality\'s health data.')
    st.button('Generate Analysis', type='primary', on_click=update_generate_button)

if st.session_state.generate_button:
    with st.spinner('Analyzing data...'):
        time.sleep(3)
    st.success('✅ Analysis generated!')
    with st.expander('1️⃣ Recommendation 1: Improve Diabetes Management'):
        st.caption('JUSTIFICATION')
        st.write('he health data shows a high prevalence of diabetes in the past 30 days, particularly among the elderly population. Uncontrolled diabetes can lead to serious complications, including heart disease and kidney damage.')
        st.caption('SMART GOAL')
        st.write("""
        **Specific**: Implement a community-wide diabetes management program that includes regular screening, patient education, and support groups.

        **Measurable**: Aim to reduce the rate of uncontrolled diabetes in the municipality by 20% within two years
        
        **Achievable**: Collaborate with local healthcare providers, pharmacies, and community organizations to provide resources and support for the program.

        **Relevant**: According to the health data, diabetes is a prevalent condition in the municipality, and improving management can significantly enhance health outcomes.

        **Time-bound**: Review the program’s progress every six months and make necessary adjustments to ensure the goal is met within two years.
        """)

    with st.expander('2️⃣ Recommendation 2: Increase Youth\'s Physical Activity'):
        st.caption('JUSTIFICATION')
        st.write('The data indicates that a significant portion of the population, particularly the youth, reports low levels of physical activity.')
        st.caption('SMART GOAL')
        st.write("""
        **Specific**: Develop safe and accessible walking paths in the municipality to encourage physical activity.

        **Measurable**: Aim for a 15% increase in the number of residents who report regular physical activity within a year.

        **Achievable**: Work with the local government and community groups to identify suitable locations and secure funding for the walking paths.

        **Relevant**: Physical activity is a key factor in preventing and managing many health conditions, including heart disease and diabetes.

        **Time-bound**: Complete the development of the walking paths within six months, and measure the impact after one year.
        """)        

    with st.expander('3️⃣ Recommendation 3: Increase Youth\'s Physical Activity'):
        st.caption('JUSTIFICATION')
        st.write("""According to the data, there is a high demand for mental health services, but access is limited due to a shortage of mental health professionals and long waiting times for appointments.""")
        st.caption('SMART GOAL')
        st.write("""
        **Specific**: Increase the availability of mental health services in the municipality by partnering with mental health professionals and organizations.

        **Measurable**: Aim to reduce the waiting time for mental health appointments to less than two weeks.

        **Achievable**: Recruit additional mental health professionals and explore options for teletherapy services.

        **Relevant**: Mental health is a critical component of overall health, and timely access to services can significantly improve outcomes.

        **Time-bound**: Implement the enhancements within a year and evaluate the impact after six months.
        """)       
st.divider()

# Row 1
st.caption('POPULATION WELL-BEING')
col1, col2, col3 = st.columns(3)
row1= [col1, col2, col3]
homepage_impact = {
    0 : ['Annual check-up population rate', '47%', 13],
    1 : ['COVID-19 immunization rate', '53%', 8],
    2 : ['Rate of patients at risk', '11%', 16]
}
for ind, col in enumerate(row1):
    col.metric(label=homepage_impact[ind][0], value=homepage_impact[ind][1], delta=homepage_impact[ind][2])
style_metric_cards(border_left_color='#B23939', border_radius_px=7, box_shadow=False)


# Row 2
st.caption('HEALTH FACILITY STATUS')

with st.container(border=True):
    st.write(f'**Cumulative Bed Capacity of {st.session_state.municipality} over 30 days**')
    chart_data = pd.DataFrame(np.random.random(30), columns=['Cumulative Bed Capacity Rate'])
    st.line_chart(chart_data)

conn = st.connection("beds", type=GSheetsConnection) # Google Sheets connection
sql = 'SELECT * FROM Sheet1;'
beds = conn.query(sql=sql, ttl=0)
beds["trend"] = [[random.randint(0, 600) for _ in range(30)] for _ in range(len(beds))]

with st.expander('View Table'):
    st.dataframe(
        beds,
        column_config = {
            "trend": st.column_config.LineChartColumn(
                "Past 30-day Capacity", y_min=0, y_max=700
            )
        },
        use_container_width=True
    )

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.caption('📉 HIGHEST BED CAPACITY')
        st.write('Lingayen Rural Health Unit II')
with col2:
    with st.container(border=True):
        st.caption('📈 LOWEST BED CAPACITY')
        st.write('Domalandan East Barangay Health Station')



# Row 3
st.write('\n')
st.caption('NON-COMMUNICABLE DISEASE SITUATIONER')

file_ = open("images/Lingayen_MRS.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

# Display the GIF in the center with altered size
st.markdown(
    f'''
    <div style="display: flex; justify-content: center;">
        <img src="data:image/gif;base64,{data_url}" alt="SIRV Simulation" style="width: 130%; height: auto;">
    </div>
    ''',
    unsafe_allow_html=True,
)


# Row 4
st.write('\n')
st.caption('COMMUNICABLE DISEASE SITUATIONER')