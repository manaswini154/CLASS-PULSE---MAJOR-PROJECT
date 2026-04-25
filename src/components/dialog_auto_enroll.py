import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']

    res = supabase.table('subjects').select('subject_id, subject_name').eq('subject_code', subject_code).execute()
    if not res.data:
        st.error("Invalid join code. Please check and try again.")
        if st.button("Close", type = 'secondary', width = 'stretch'):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()

    if check.data:
        st.info(f"You are already enrolled in {subject['subject_name']}.")
        if st.button("Close", type = 'secondary', width = 'stretch'):
            st.query_params.clear()
            st.rerun()
    
    st.markdown(f"Would you like to enroll in{subject['subject_name']}**?")

    col1, col2 = st.columns(2, gap = 'large')
    with col1:
        if st.button("No, Thanks!"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Yes, Enroll Now!!", type = 'primary', width = 'stretch'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.toast("Successfully joined!!")
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
