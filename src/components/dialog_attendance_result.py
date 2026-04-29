import streamlit as st
from src.database.db import create_attendance


def show_attendance_result(df, logs):
    st.markdown(
        '<div style="font-size:0.88rem;color:#6b7280;margin-bottom:0.75rem;">Review the results before confirming.</div>',
        unsafe_allow_html=True
    )
    st.dataframe(df, hide_index=True, use_container_width=True, column_config={
        "Name":   st.column_config.TextColumn("Student Name"),
        "ID":     st.column_config.TextColumn("Student ID"),
        "Source": st.column_config.TextColumn("Detected From"),
        "Status": st.column_config.TextColumn("Status"),
    })

    st.markdown("<div style='margin-top:0.75rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        if st.button("Discard", use_container_width=True, type='tertiary'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()
    with col2:
        if st.button("Confirm & Save", use_container_width=True, type='primary'):
            try:
                create_attendance(logs)
                st.toast("Attendance saved successfully!")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception:
                st.error("Failed to save attendance. Please try again.")


@st.dialog("Review Attendance")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)