import streamlit as st
import openai
import time

# Page config
st.set_page_config(page_title='PULSO SMS', page_icon='📶', layout="centered", initial_sidebar_state="auto", menu_items=None)

# Generate SMS
openai.api_key = st.secrets['openai_api']

def generate_sms_message(age_group, message_type):
    prompt = f"Generate a short and effective SMS message in the Filipino language for a {age_group}. The message will be sent by the individual's government municipal health office about {message_type}."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

# Title
st.title('📶 PULSO SMS')
st.write('Lorem ipsum')
st.divider()

# Demographic demo
with st.container(border=True):
    st.caption('✨ PULSO Analyze')
    st.write('Utilize Generative AI to generate a personalized SMS for your municipality\'s citizens.')

    col1, col2 = st.columns(2)
    age_group = col1.selectbox('Select age group', 
        [
            'Teenagers (13-19 years)',
            'Young Adults (20-29 years)',
            'Adults (30-49 years)',
            'Older Adults (50-64 years)',
            'Seniors (65+ years)'
        ]
    )

    message_type = col2.selectbox('Select message type',
        [
            'Check-up reminder',
            'At-risk for non-communicable disease',
            'High heat index health tip'
            'Warning for high cases of Disease A'
        ]
    )

    generate_sms = st.button('Generate SMS', type='primary')

if generate_sms:
    with st.spinner('Generating SMS...'):
        message = generate_sms_message(age_group, message_type)
    st.success('Message generated!', icon='✅')
    with st.container(border=True):
        st.caption('GENERATED SMS')
        st.write(message)        

st.write('\n')

# Mass text
with st.container(border=True):
    st.caption('MASS TEXT')
    st.write('Send mass texts to all phone numbers in your municipality.')
    to_send = st.text_input('Enter message here')

    send_mass = st.button('Send to all')

    if send_mass:
        with st.spinner('Sending SMS...'):
            time.sleep(3)
        st.success('SMS sent!', icon='✅')