import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np
import openai
import random
import base64

# Page config
st.set_page_config(page_title='Dashboard', page_icon='📊', layout="centered", initial_sidebar_state="auto", menu_items=None)


# Title
st.title('📊 PULSO Dashboard')
st.write('The PULSO dashboard is a four-pronged... lorem ipsum smart dashboard that generates easy-to-understand visualizations...')


# On-click function
if 'generate_button' not in st.session_state:
    st.session_state['generate_button'] = False
def update_generate_button():
    st.session_state['generate_button'] = True


# Generate action steps
openai.api_key = st.secrets['openai_api']
@st.cache_data
def generate_recommendations():
    # Collect data
    # data_str = data.to_csv(index=False)
    
    # Define the prompt
    prompt = (
        "The following health data from a municipality are provided in CSV format: (1)  "
        "Act as a data analyst and provide actionable next steps and recommendations for policymakers and health offices to improve public health. The data is as follows:\n\n"
        f"{data_str}\n\n"
        "Please provide actionable next steps."
    )
    
    # Make a request to the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    
    # Extract and return the text from the response
    recommendations = response.choices[0].text.strip()
    return recommendations

with st.container(border=True):
    st.caption('✨ AgapAI')
    st.write('Utilize Generative AI to generate actionable next steps for your municipality\'s health data.')
    st.button('Generate Analysis', type='primary', on_click=update_generate_button)

if st.session_state.generate_button:
    with st.spinner('Analyzing data...'):
        recommendations = generate_recommendations()
    with st.expander('View recommendations'):
        st.write(recommendations)
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