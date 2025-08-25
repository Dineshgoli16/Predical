# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 20:03:51 2025

@author: dines
"""

import numpy as np
import pickle
import streamlit as st

loaded_model = pickle.load(open("trained_model (1).sav", 'rb'))
def hypocalcemia_prediction(input_data):

    input_data_as_numpy_array = np.asarray(input_data)

    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)


    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)

    if (prediction[0] == 0):
      return'Patient can be discharged'
    else:
      return'Patient will require calcium'


      
def main():
        
        
        # giving a title
        st.title('PrediCal Web App')
        
        
        # getting the input data from the user
        col1, col2, col3 = st.columns(3)
        
        with col1: 
            CA = st.number_input('Preop Calcium')
        with col2:
            PHOSPHORUS = st.number_input('PHOSPHORUS')
        with col3:
            PTH = st.number_input('PRE OP PTH')
        with col1:
            ALP = st.number_input('ALP')
        with col2:
            VITD = st.number_input('VITAMIN D')
        with col3:
           NOOFTUMOURS = st.number_input('NUMBER OF TUMOURS REMOVED')
        with col1:
            POSTOPPTH = st.number_input('POST OP PTH')
        with col2:
            BMD_N = st.number_input('OSTEOPOROSIS(1 - yes,0 - no)')
        
        
        # code for Prediction
        diagnosis = ''
        
        # creating a button for Prediction
        
        if st.button('Hypocalcemia Predictor'):
            diagnosis = hypocalcemia_prediction([CA, PHOSPHORUS, PTH, ALP, VITD, NOOFTUMOURS , POSTOPPTH, BMD_N])
            
            
        st.success(diagnosis)
        
        
if __name__== '__main__':
        main()
        