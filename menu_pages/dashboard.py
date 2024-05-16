import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
import openai
import random as rand
import time
import base64


# Page config
st.set_page_config(page_title='Dashboard', page_icon='📊', layout="centered", initial_sidebar_state="auto", menu_items=None)

# Title
col1, col2, col3 = st.columns([0.1,0.2,7])
with col1:
    st.image('images/logo.png', width=30) 
with col3:
    st.caption('🧑‍⚕️ PULSO | Predictive Understanding for Localized Health Surveillance and Optimization')

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
beds["trend"] = [[rand.randint(0, 600) for _ in range(30)] for _ in range(len(beds))]

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

with st.container(border=True):
    st.caption('Measles-Rubella Situation Updates')
    # Display the GIF in the center with altered size
    st.markdown(
        f'''
        <div style="display: flex; justify-content: center;">
            <img src="data:image/gif;base64,{data_url}" alt="SIRV Simulation" style="width: 100%; height: auto;">
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.text('')

# Check if the seed is already stored in the session state
if 'random_seed' not in st.session_state:
    # Generate and store a random seed
    st.session_state.random_seed = rand.randint(0, 99)

# Set the random seed using the stored value
np.random.seed(st.session_state.random_seed)

# Define the list of barangays
barangays = [
    "Aliwekwek", "Baay", "Balangobong", "Balococ", "Bantayan", "Basing", "Capandanan", "Domalandan Center", 
    "Domalandan East", "Domalandan West", "Dorongan", "Dulag", "Estanza", "Lasip", "Libsong East", "Libsong West", 
    "Malawa", "Malimpuec", "Maniboc", "Matalava", "Naguelguel", "Namolan", "Pangapisan North", "Pangapisan Sur", 
    "Poblacion", "Quibaol", "Rosario", "Sabangan", "Talogtog", "Tonton", "Tumbar", "Wawa"
]

# Generate random data
population = np.random.randint(1000, 5000, size=len(barangays))
total_cases = np.random.randint(1, 100, size=len(barangays))
prev_5_6_weeks = np.random.randint(1, 50, size=len(barangays))
prev_3_4_weeks = np.random.randint(1, 50, size=len(barangays))
recent_1_2_weeks = np.random.randint(1, 50, size=len(barangays))

# Create the dataframe
df = pd.DataFrame({
    'Population': population,
    'Total Cases (2024)': total_cases,
    'Previous 5-6 weeks (Mar 24 to Apr 06)': prev_5_6_weeks,
    'Previous 3-4 weeks (Apr 7 to Apr 20)': prev_3_4_weeks,
    'Recent 1-2 weeks (Apr 21 to May 04)': recent_1_2_weeks,
}, index=barangays)

# Calculate the two-week growth rates
df['Two-week Growth Rate (Previous 3-4 weeks vs 5-6 weeks)'] = round(
    ((df['Previous 3-4 weeks (Apr 7 to Apr 20)'] - df['Previous 5-6 weeks (Mar 24 to Apr 06)']) / df['Previous 5-6 weeks (Mar 24 to Apr 06)']) * 100, 2)
df['Two-week Growth Rate (Recent 1-2 weeks vs 3-4 weeks)'] = round(
    ((df['Recent 1-2 weeks (Apr 21 to May 04)'] - df['Previous 3-4 weeks (Apr 7 to Apr 20)']) / df['Previous 3-4 weeks (Apr 7 to Apr 20)']) * 100, 2)

# Limit the growth rate to maximum 100%
df['Two-week Growth Rate (Previous 3-4 weeks vs 5-6 weeks)'] = df['Two-week Growth Rate (Previous 3-4 weeks vs 5-6 weeks)'].apply(lambda x: min(max(x, -100), 100))
df['Two-week Growth Rate (Recent 1-2 weeks vs 3-4 weeks)'] = df['Two-week Growth Rate (Recent 1-2 weeks vs 3-4 weeks)'].apply(lambda x: min(max(x, -100), 100))

# Drop unnecessary columns
df = df.drop(['Population', 'Total Cases (2024)', 'Previous 5-6 weeks (Mar 24 to Apr 06)', 'Previous 3-4 weeks (Apr 7 to Apr 20)', 'Recent 1-2 weeks (Apr 21 to May 04)'], axis=1)

# Rename columns with HTML tags for line breaks
df.columns = [
    'Two-week Growth Rate<br>(Previous 3-4 weeks vs 5-6 weeks)',
    'Two-week Growth Rate<br>(Recent 1-2 weeks vs 3-4 weeks)'
]

# Function to apply conditional formatting
def highlight_cells(val):
    if isinstance(val, (int, float)):
        if val < 0:
            return 'background-color: #E2EDDC'  # light green
        else:
            return 'background-color: #F3CCCC'  # light red
    return ''

# Applying the function to style the DataFrame
styled_df = df.style.applymap(highlight_cells)

# Set the CSS style for scrollable div
scrollable_div_style = """
<style>
.scrollable-div {
    max-height: 300px;
    overflow-y: auto;
}
</style>
"""

# Display the DataFrame in Streamlit using markdown and HTML


with st.container(border=True):
    st.caption('Growth Rate per Barangay')
    st.markdown(scrollable_div_style, unsafe_allow_html=True)
    st.markdown(f'<div class="scrollable-div">{styled_df.to_html(escape=False)}</div>', unsafe_allow_html=True)

# Row 4
st.write('\n')
st.caption('COMMUNICABLE DISEASE SITUATIONER')
col1, col2, col3 = st.columns(3)
row1= [col1, col2, col3]
homepage_impact = {
    0 : ['Disease A', '11%', 11],
    1 : ['Disease B', '23%', 10],
    2 : ['Disease C', '42%', 9]
}
for ind, col in enumerate(row1):
    col.metric(label=homepage_impact[ind][0], value=homepage_impact[ind][1], delta=homepage_impact[ind][2], delta_color="inverse")
style_metric_cards(border_left_color='#B23939', border_radius_px=7, box_shadow=False)