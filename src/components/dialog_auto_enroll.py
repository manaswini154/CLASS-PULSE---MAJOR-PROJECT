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
        if st.button("Close", type='secondary', use_container_width=True):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.info(f"You are already enrolled in **{subject['subject_name']}**.")
        if st.button("Close", type='secondary', use_container_width=True):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(
        f'<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:1.25rem;color:#1a2744;margin-bottom:0.5rem;">'
        f'Join <em>{subject["subject_name"]}</em>?'
        f'</div>'
        f'<div style="font-size:0.88rem;color:#6b7280;margin-bottom:1rem;">'
        f'You are about to enroll using code <strong>{subject_code}</strong>.'
        f'</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap='medium')
    with col1:
        if st.button("No, Thanks", type='tertiary', use_container_width=True):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Yes, Enroll!", type='primary', use_container_width=True):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.toast(f"Enrolled in {subject['subject_name']}!")
            st.query_params.clear()
            time.sleep(1.5)
            st.rerun()