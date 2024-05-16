import os
import pickle
import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title='Disease Predict', page_icon='🧬', layout="centered", initial_sidebar_state="auto", menu_items=None)


st.title('Disease Prediction System 🧬')
with st.expander('❤️ AT A GLANCE'):
    st.write("""Welcome to the Disease Predict page of PULSO, your comprehensive tool for disease prediction and forecasting. Utilizing machine learning models, this feature empowers healthcare professionals to identify risks of non-communicable diseases like diabetes, Parkinson’s, and heart disease.""")
st.write('\n')

tab1, tab2, tab3 = st.tabs(["Diabetes 🧪", "Heart Disease 🔬", "Parkinson's Disease 🙍"])

with tab1:
    st.header("Diabetes Prediction System")
    working_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(working_dir, '..', 'saved_models', 'diabetes_model.sav')
    diabetes_model = pickle.load(open(model_path, 'rb'))

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Parameter A', key='diabetes_param_a') # Number of Pregnancies

    with col2:
        Glucose = st.text_input('Parameter B', key='diabetes_param_b') # Glucose Level

    with col3:
        BloodPressure = st.text_input('Parameter C', key='diabetes_param_c') # Blood Pressure value

    with col1:
        SkinThickness = st.text_input('Parameter D', key='diabetes_param_d') # Skin Thickness value

    with col2:
        Insulin = st.text_input('Parameter E', key='diabetes_param_e') # Insulin Level

    with col3:
        BMI = st.text_input('Parameter F', key='diabetes_param_f') # BMI value

    with col1:
        DiabetesPedigreeFunction = st.text_input('Parameter G', key='diabetes_param_g') # Diabetes Pedigree Function value

    with col2:
        diabetes_age = st.text_input('Parameter H', key='diabetes_param_h') # Age of the Person

    # code for Prediction
    diab_diagnosis = ''

    # creating a button for Prediction
    if st.button('Diabetes Test Result'):
        try:
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, diabetes_age]
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

with tab2:
    st.header("Heart Disease Prediction System")
    
    working_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(working_dir, '..', 'saved_models', 'heart_disease_model.sav')
    heart_disease_model = pickle.load(open(model_path, 'rb'))

    col1, col2, col3 = st.columns(3)

    with col1:
        heart_age = st.text_input('Parameter A', key='heart_param_a') # Age

    with col2:
        sex = st.text_input('Parameter B', key='heart_param_b') # Sex

    with col3:
        cp = st.text_input('Parameter C', key='heart_param_c') # Chest Pain types

    with col1:
        trestbps = st.text_input('Parameter D', key='heart_param_d') # Resting Blood Pressure

    with col2:
        chol = st.text_input('Parameter E', key='heart_param_e') # Serum Cholestoral in mg/dl

    with col3:
        fbs = st.text_input('Parameter F', key='heart_param_f') # Fasting Blood Sugar > 120 mg/dl

    with col1:
        restecg = st.text_input('Parameter G', key='heart_param_g') # Resting Electrocardiographic results

    with col2:
        thalach = st.text_input('Parameter H', key='heart_param_h') # Maximum Heart Rate achieved'

    with col3:
        exang = st.text_input('Parameter I', key='heart_param_i') # Exercise Induced Angina

    with col1:
        oldpeak = st.text_input('Parameter J', key='heart_param_j') # ST depression induced by exercise

    with col2:
        slope = st.text_input('Parameter K', key='heart_param_k') # Slope of the peak exercise ST segment

    with col3:
        ca = st.text_input('Parameter L', key='heart_param_l') # Major vessels colored by flourosopy

    with col1:
        thal = st.text_input('Parameter M', key='heart_param_m') # thal: 0 = normal; 1 = fixed defect; 2 = reversable defect

    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction
    if st.button('Heart Disease Test Result'):
        try:
            user_input = [heart_age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
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

with tab3:
    st.header("Parkinson's Disease Prediction System")

    working_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(working_dir, '..', 'saved_models', 'parkinsons_model.sav')
    parkinsons_model = pickle.load(open(model_path, 'rb'))

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('Parameter A', key='parkinsons_param_a') # MDVP:Fo(Hz)

    with col2:
        fhi = st.text_input('Parameter B', key='parkinsons_param_b') # MDVP:Fhi(Hz)

    with col3:
        flo = st.text_input('Parameter C', key='parkinsons_param_c') # MDVP:Flo(Hz)

    with col4:
        Jitter_percent = st.text_input('Parameter D', key='parkinsons_param_d') # MDVP:Jitter(%)

    with col5:
        Jitter_Abs = st.text_input('Parameter E', key='parkinsons_param_e') # MDVP:Jitter(Abs)'

    with col1:
        RAP = st.text_input('Parameter F', key='parkinsons_param_f') # MDVP:RAP

    with col2:
        PPQ = st.text_input('Parameter G', key='parkinsons_param_g') # MDVP:PPQ

    with col3:
        DDP = st.text_input('Parameter H', key='parkinsons_param_h') # Jitter:DDP

    with col4:
        Shimmer = st.text_input('Parameter I', key='parkinsons_param_i') # MDVP:Shimmer

    with col5:
        Shimmer_dB = st.text_input('Parameter J', key='parkinsons_param_j') # MDVP:Shimmer(dB)

    with col1:
        APQ3 = st.text_input('Parameter K', key='parkinsons_param_k') # Shimmer:APQ3

    with col2:
        APQ5 = st.text_input('Parameter L', key='parkinsons_param_l') # Shimmer:APQ5

    with col3:
        APQ = st.text_input('Parameter M', key='parkinsons_param_m') # MDVP:APQ

    with col4:
        DDA = st.text_input('Parameter N', key='parkinsons_param_n') # Shimmer:DDA

    with col5:
        NHR = st.text_input('Parameter O', key='parkinsons_param_o') # NHR

    with col1:
        HNR = st.text_input('Parameter P', key='parkinsons_param_p') # HNR

    with col2:
        RPDE = st.text_input('Parameter Q', key='parkinsons_param_q') # RPDE

    with col3:
        DFA = st.text_input('Parameter R', key='parkinsons_param_r') # DFA

    with col4:
        spread1 = st.text_input('Parameter S', key='parkinsons_param_s') # spread1

    with col5:
        spread2 = st.text_input('Parameter T', key='parkinsons_param_t') # spread2

    with col1:
        D2 = st.text_input('Parameter U', key='parkinsons_param_u') # D2

    with col2:
        PPE = st.text_input('Parameter V', key='parkinsons_param_v') # PPE

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction    
    if st.button("Parkinson's Test Result"):
        try:
            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                            RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                            APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
            user_input = [float(x) for x in user_input]

            parkinsons_prediction = parkinsons_model.predict([user_input])

            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "The person has Parkinson's disease"
                st.error(parkinsons_diagnosis)
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"
                st.success(parkinsons_diagnosis)
        except ValueError:
            st.error("Not completed input: Please enter all fields with valid numbers.")
