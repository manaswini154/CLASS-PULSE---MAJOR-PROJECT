import streamlit as st
from src.ui.style_base_layout import style_base_layout, style_background_dashboard, style_background_home
from src.components.header import header_dashboard
from src.screens.home_screen import home_screen
from src.database.db import check_teacher_exist,create_teacher, teacher_login
import numpy as np
from PIL import Image
from src.pipelines.face_pipelines import predict_attendance,trained_classifier, get_face_emb
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from src.pipelines.voice_pipelines import get_voice_embedding
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
def student_dashboard():
    st.header("Student Dashboard")
    student_data = st.session_state.student_data
    col1, col2 = st.columns(2, vertical_alignment = 'center', gap ='xxlarge')
    with col1:
        header_dashboard()
    with col2:
        st.write(f"Welcome {student_data['name']}")
        if st.button("Logout", type = 'secondary', key = 'logout'):
            del st.session_state.student_data
            st.session_state['is_logged_in'] = False
            st.rerun()
    st.space()

    col1, col2 = st.columns(2)
    with col1:
        st.header("Your Enrolled Subjects")
    with col2:
        if st.button("Enroll in subject",type = 'primary', width = 'stretch'):
            enroll_dialog()
    st.divider()
    student_id = student_data['student_id']
    with st.spinner("Loading your subjects..."):
        subjects = get_student_subjects(student_data['student_id'])
        logs = get_student_attendance(student_data['student_id'])
    
    stats_map = {}
    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {'total': 0, 'attended': 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    
    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {'total': 0, 'attended': 0})
        def unenroll_button():
                if st.button("Unenroll", type = 'tertiary', key = f'unenroll_{sid}', width = 'stretch'):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f"Unenrolled from {sub['subject_name']} successfully!")
                    st.rerun()
        
        with cols[i%2]:
            subject_card(
                name = sub['subject_name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [("📅",'total',stats['total']),
                ("✅",'attended',stats['attended'])],
                footer_callback = unenroll_button
            )


def student_screen():
    style_background_dashboard()
    style_base_layout()
    if "student_data" in st.session_state:
        student_dashboard()
        return
    col1, col2 = st.columns(2, vertical_alignment = 'center', gap ='xxlarge')
    with col1:
        header_dashboard()
    with col2:
        if st.button("Return to Home Page", type='secondary', key ='loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()
    st.title("Login using Face ID", text_alignment = 'center')
    st.space()

    show_registration = False

    photo = st.camera_input("Position your Face in the Center!")
    if photo:
        img = np.array(Image.open(photo))

        with st.spinner("AI is Scanning...."):
            detected, all_ids,num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found!")
            elif num_faces > 1:
                st.warning("Multiple faces found!")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']== student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")   
                        time.sleep(1)
                        st.rerun()            
                else:
                    st.info("Face not recognised! You might be a New Student.")
                    show_registration = True

    if show_registration:
        with st.container(border=True):
            st.header("Register new Profile!")
            new_name = st.text_input("Enter Your Name: ",placeholder = "name")

            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll your voice for voice only attendance")

            audio_data = None

            try:
                audio_data = st.audio_input("Record a short clip of your Voice.")
            except Exception:
                st.error('Audio Data Failed.')

            if st.button('Create Account', type = 'primary'):
                if new_name:
                    with st.spinner('Creating Profile...'):
                        img = np.array(Image.open(photo))
                        encodings = get_face_emb(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_emb = face_emb,voice_emb = voice_emb)

                            if response_data:
                                trained_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created! Hi {new_name}!")   
                                time.sleep(1)
                                st.rerun() 
                        else:
                            st.error("couldn't capture your image for Facial Recognition! Please try again!")

                else:
                    st.warning('Please enter your Name!')
    st.space()
