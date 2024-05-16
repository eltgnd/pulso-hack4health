import os
import pickle
import streamlit as st
import pandas as pd

working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(working_dir, '..', 'saved_models', 'heart_disease_model.sav')
heart_disease_model = pickle.load(open(model_path, 'rb'))

st.title('Heart Disease Prediction using ML')

col1, col2, col3 = st.columns(3)

with col1:
    age = st.text_input('Parameter A') # Age

with col2:
    sex = st.text_input('Parameter B') # Sex

with col3:
    cp = st.text_input('Parameter C') #Chest Pain types

with col1:
    trestbps = st.text_input('Parameter D') # Resting Blood Pressure

with col2:
    chol = st.text_input('Parameter E') # Serum Cholestoral in mg/dl

with col3:
    fbs = st.text_input('Parameter F') # Fasting Blood Sugar > 120 mg/dl

with col1:
    restecg = st.text_input('Parameter G') # Resting Electrocardiographic results

with col2:
    thalach = st.text_input('Parameter H') # Maximum Heart Rate achieved'

with col3:
    exang = st.text_input('Parameter I') # Exercise Induced Angina

with col1:
    oldpeak = st.text_input('Parameter J') # ST depression induced by exercise

with col2:
    slope = st.text_input('Parameter K') # Slope of the peak exercise ST segment

with col3:
    ca = st.text_input('Parameter L') # Major vessels colored by flourosopy

with col1:
    thal = st.text_input('Paramater M') # thal: 0 = normal; 1 = fixed defect; 2 = reversable defect

# code for Prediction
heart_diagnosis = ''

# creating a button for Prediction

if st.button('Heart Disease Test Result'):
    try:
        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
            st.error(heart_diagnosis)
        else:
            heart_diagnosis = 'The person does not have any heart disease'
            st.success(heart_diagnosis)
    except ValueError:
        st.error("Not completed input: Please enter all fields with valid numbers.")

