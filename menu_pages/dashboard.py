import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import openai

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
    st.caption('✨ PULSO Analyze')
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
    0 : ['Updated EMRs', '2748', 1406],
    1 : ['Lorem Ipsum', '376', 8],
    2 : ['Active Health Facilities', '49', 16]
}
for ind, col in enumerate(row1):
    col.metric(label=homepage_impact[ind][0], value=homepage_impact[ind][1], delta=homepage_impact[ind][2])
style_metric_cards(border_left_color='#B23939', border_radius_px=7, box_shadow=False)


# Row 2
st.caption('HEALTH FACILITY STATUS')
col1, col2 = st.columns([3,1])
with col1:
    pass
# get highest and lowest
col2.metric(label='Highest Capacity', value=16, delta=4)
col2.metric(label='Lowest Capacity', value=16, delta=4)


# Row 3
st.caption('NON-COMMUNICABLE DISEASE SITUATIONER')



# Row 4
st.caption('COMMUNICABLE DISEASE SITUATIONER')
