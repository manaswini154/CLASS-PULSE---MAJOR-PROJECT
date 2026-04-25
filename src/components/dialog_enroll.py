import streamlit as st
from src.database.db import enroll_student_to_subject
import time
import supabase
from src.database.config import supabase

@st.dialog("Enroll in the Subject")
def enroll_dialog():
    st.write("Enter the subject code to enroll")

    join_code = st.text_input("Subject Code", placeholder="CS101")

    if st.button("Enroll now", type = 'primary', width= 'stretch'):
        if join_code:
            res = supabase.table("subjects").select('subject_id, subject_name, subject_code').eq('subject_code', join_code).execute()
        
            if res.data:
                subject= res.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table("subject_students").select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
                if check.data:
                    st.warning("You are already enrolled in this subject!")

                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success(f"Enrolled in {subject['subject_name']} successfully!")
                    time.sleep(2)
                    st.rerun()
        else:
            st.warning("Please enter a subject code to enroll.")

                                            
