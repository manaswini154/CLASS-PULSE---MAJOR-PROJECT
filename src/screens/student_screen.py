import streamlit as st
from src.ui.style_base_layout import style_base_layout, style_background_dashboard, style_background_home

style_background_dashboard()
def student_screen():
    style_background_dashboard()
    style_base_layout()
    st.title("Student Dashboard")
    st.write("This is the student's dashboard where you can view your courses and assignments.")

    if st.button("Return to Home Page", type='secondary', key ='loginbackbtn3'):
            st.session_state['login_type'] = None
            st.rerun()
