# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 20:03:51 2025

@author: dines
"""

import numpy as np
import pandas as pd
import pickle
import streamlit as st

loaded_model = pickle.load(open("trained_model (4).sav", 'rb'))
def hypocalcemia_prediction(input_data):
    feature_names = ['CA', 'PHOSPHORUS', 'PTH', 'ALP', 'VIT D', 'NO OF TUMOURS', 'POST OP PTH', 'BMD_N']
    input_df = pd.DataFrame([input_data], columns=feature_names)
    prediction = loaded_model.predict(input_df)
    probability = loaded_model.predict_proba(input_df)
    print("Probability of Hypocalcemia is " , probability[0][1] * 100 ,"%", prediction)

    if prediction[0] == 0:
     return f"Probability of Hypocalcemia is {probability[0][1] * 100:.2f}% - Patient can be Discharged"
    else:
     return f"Probability of Hypocalcemia is {probability[0][1] * 100:.2f}% - Patient will require calcium"


      
def main():
        
        
        # giving a title
        st.title('PrediCal-AI Web App')
        st.markdown("""
    This application predicts the **probability of postoperative hypocalcemia** in patients with primary hyperparathyroidism.
    
    **Features:**
    - Predicts hypocalcemia risk 
    - Suggests early discharge or calcium supplementation
    - Uses an AI-based Logistic Regression model
    
    """)        
        
        # getting the input data from the user
        col1, col2, col3 = st.columns(3)
        
        with col1: 
            CA = st.number_input('CALCIUM(mg/dL)')
        with col1:
            PHOSPHORUS = st.number_input('PHOSPHORUS(mg/dL)')
        with col1:
            PTH = st.number_input('PRE OP PTH(Pg/mL)')
        with col2:
            ALP = st.number_input('ALP(mg/dL)')
        with col2:
            VITD = st.number_input('VITAMIN D(IU/mL)')
        with col2:
           NOOFTUMOURS = st.number_input('NUMBER OF TUMOURS REMOVED')
        with col3:
            POSTOPPTH = st.number_input('POST OP PTH(Pg/mL)')
        with col3:
            BMD_N = st.number_input('OSTEOPOROSIS(1 - YES,0 - NO)')
        
        
        # code for Prediction
        diagnosis = ''
        
        # creating a button for Prediction
        
        if st.button('Hypocalcemia Predictor'):
            diagnosis = hypocalcemia_prediction([CA, PHOSPHORUS, PTH, ALP, VITD, NOOFTUMOURS , POSTOPPTH, BMD_N])
            
            
        st.success(diagnosis)
        
        
if __name__== '__main__':
        main()
        