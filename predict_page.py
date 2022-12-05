import streamlit as st
import pickle
import numpy as np

import i18n


def load_model():
    with open('saved_steps.pk1', 'rb') as file:
        data = pickle.load(file)

    return data


data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_edlevel = data["le_edlevel"]


def show_predict_page():
    st.markdown(i18n.t('predict_title'), unsafe_allow_html=True)
    st.markdown(i18n.t('predict_intro_1'))
    st.markdown(i18n.t('predict_intro_2'))
    st.markdown("\n")
    st.markdown(i18n.t('predict_select_info'))


    countries = (
        "United States of America",                              
        "India",                                             
        "Germany",                                                
        "United Kingdom of Great Britain and Northern Ireland", 
        "Canada",                                                  
        "France",                                               
        "Brazil",                                                  
        "Spain",                                                   
        "Netherlands",                                               
        "Australia",                                               
        "Poland",                                                  
        "Italy",                                                     
        "Russian Federation",                                       
        "Sweden",                                                    
        "Turkey",                                                   
        "Switzerland",                                               
        "Israel",                                                   
        "Norway",
    )

    ed_levels = (
        "Less than a Bachelor’s degree",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox(i18n.t('Country'), countries, format_func = lambda x: i18n.t(f'{x}'))
    ed_level = st.selectbox(i18n.t('Education Level'), ed_levels, format_func = lambda x: i18n.t(f'{x}'))

    experience = st.slider(i18n.t('Years of Experience'), 0, 50, 3)

    salary_btn_clicked = st.button(i18n.t('Calculate Salary'))
    if (salary_btn_clicked):
        X = np.array([[country, ed_level, experience]])
        X[:,0] = le_country.transform(X[:,0])
        X[:,1] = le_edlevel.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"{i18n.t('The estimated salary is')}")
        st.subheader(f"${salary[0]:,.2f}")
