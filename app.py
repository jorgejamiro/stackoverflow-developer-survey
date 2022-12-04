import streamlit as st

import i18n

from predict_page import show_predict_page
from explore_page import show_explore_page
from languages import language_init

language_init()

page = st.sidebar.selectbox("", ('Explore', 'Predict'),
                            format_func=(lambda x: i18n.t(f'{x}'))
)

if page == "Predict":
    show_predict_page()
else:
    show_explore_page()
