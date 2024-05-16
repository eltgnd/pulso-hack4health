import os
import pickle
import streamlit as st
import pandas as pd

working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(working_dir, '..', 'saved_models', 'diabetes_model.sav')
diabetes_model = pickle.load(open(model_path, 'rb'))


# page title
st.title('Diabetes Prediction System 🧬')

# getting the input data from the user
col1, col2, col3 = st.columns(3)

with col1:
    Pregnancies = st.text_input('Parameter A') # Number of Pregnancies

with col2:
    Glucose = st.text_input('Parameter B') #Glucose Level

with col3:
    BloodPressure = st.text_input('Parameter C') # Blood Pressure value

with col1:
    SkinThickness = st.text_input('Parameter D') # Skin Thickness value

with col2:
    Insulin = st.text_input('Parameter E') # Insulin Level

with col3:
    BMI = st.text_input('Parameter F') # BMI value

with col1:
    DiabetesPedigreeFunction = st.text_input('Parameter G') # Diabetes Pedigree Function value'

with col2:
    Age = st.text_input('Parameter H') # Age of the Person

# code for Prediction
diab_diagnosis = ''

# creating a button for Prediction
if st.button('Diabetes Test Result'):
    try:
        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
            st.error(diab_diagnosis)
        else:
            diab_diagnosis = 'The person is not diabetic'
            st.success(diab_diagnosis)
    except ValueError:
        st.error("Not completed input: Please enter all fields with valid numbers.")