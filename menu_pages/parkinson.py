import os
import pickle
import streamlit as st
import pandas as pd

working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(working_dir, '..', 'saved_models', 'parkinsons_model.sav')
parkinsons_model = pickle.load(open(model_path, 'rb'))


st.title("Parkinson's Disease Prediction using ML")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    fo = st.text_input('Parameter A') # MDVP:Fo(Hz)

with col2:
    fhi = st.text_input('Paramater B') # MDVP:Fhi(Hz)

with col3:
    flo = st.text_input('Parameter C') # MDVP:Flo(Hz)

with col4:
    Jitter_percent = st.text_input('Parameter D') # MDVP:Jitter(%)

with col5:
    Jitter_Abs = st.text_input('Parameter E') # MDVP:Jitter(Abs)'

with col1:
    RAP = st.text_input('Paramater F') # MDVP:RAP

with col2:
    PPQ = st.text_input('Parameter G') # MDVP:PPQ

with col3:
    DDP = st.text_input('Parameter H') # Jitter:DDP

with col4:
    Shimmer = st.text_input('Parameter I') # MDVP:Shimmer

with col5:
    Shimmer_dB = st.text_input('Parameter J') # MDVP:Shimmer(dB)

with col1:
    APQ3 = st.text_input('Parameter K') #Shimmer:APQ3

with col2:
    APQ5 = st.text_input('Parameter L') # Shimmer:APQ5

with col3:
    APQ = st.text_input('Parameter M') # MDVP:APQ

with col4:
    DDA = st.text_input('Parameter N') # Shimmer:DDA

with col5:
    NHR = st.text_input('Parameter O') # NHR

with col1:
    HNR = st.text_input('Parameter P') # HNR

with col2:
    RPDE = st.text_input('Parameter Q') # RPDE

with col3:
    DFA = st.text_input('Parameter R') # DFA

with col4:
    spread1 = st.text_input('Parameter S') # spread1

with col5:
    spread2 = st.text_input('Parameter T') # spread2

with col1:
    D2 = st.text_input('Parameter U') # D2

with col2:
    PPE = st.text_input('Parameter V') # PPE

# code for Prediction
parkinsons_diagnosis = ''

# creating a button for Prediction    
if st.button("Parkinson's Test Result"):
    try:
        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                        RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
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


