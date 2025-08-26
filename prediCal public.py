# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 20:03:51 2025

@author: dines
"""

import numpy as np
import pandas as pd
import pickle
import streamlit as st

loaded_model = pickle.load(open("C:/Users/dines/Downloads/trained_model (1).sav", 'rb'))
def hypocalcemia_prediction(input_data):
    feature_names = ['CA', 'PHOSPHORUS', 'PTH', 'ALP', 'VIT D','NO OF TUMOURS', 'POST OP PTH', 'BMD_N']
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
        st.title('PrediCal Web App')
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
            CA = st.text_input('Preop Calcium')
        with col2:
            PHOSPHORUS = st.text_input('PHOSPHORUS')
        with col3:
            PTH = st.text_input('PRE OP PTH')
        with col1:
            ALP = st.text_input('ALP')
        with col2:
            VITD = st.text_input('VITAMIN D')
        with col3:
           NOOFTUMOURS = st.text_input('NUMBER OF TUMOURS REMOVED')
        with col1:
            POSTOPPTH = st.text_input('POST OP PTH')
        with col2:
            BMD_N = st.text_input('OSTEOPOROSIS(1 - yes,0 - no)')
        
        
        # code for Prediction
        diagnosis = ''
        
        # creating a button for Prediction
        
        if st.button('Hypocalcemia Predictor'):
            diagnosis = hypocalcemia_prediction([CA, PHOSPHORUS, PTH, ALP, VITD, NOOFTUMOURS , POSTOPPTH, BMD_N])
            
            
        st.success(diagnosis)
        
        
if __name__== '__main__':
        main()
        