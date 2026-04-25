import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from src.database.db import create_attendance

def show_attendance_result(df, logs):
    st.write("Please review Attendance before confirming!!")
    st.dataframe(df, hide_index = True, column_config = {
        "Name": st.column_config.TextColumn("Student Name"),
        "ID": st.column_config.TextColumn("Student ID"),
        "Source": st.column_config.TextColumn("Detected From"),
        "Status": st.column_config.TextColumn("Attendance Status")
    }) 

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discard", width = 'stretch', type = 'tertiary'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()
    with col2:
        if st.button("Confirm & Save", width = 'stretch', type = 'tertiary'):
            try:
                create_attendance(logs)
                st.toast("Attendance logged successfully!")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error("sync Failed!")

@st.dialog("Attendance Reports")

def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
    
    