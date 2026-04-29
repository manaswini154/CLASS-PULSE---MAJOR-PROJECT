import streamlit as st
from src.ui.style_base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.database.db import check_teacher_exist, create_teacher, teacher_login
import numpy as np
from PIL import Image
from src.pipelines.face_pipelines import predict_attendance, trained_classifier, get_face_emb
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
from src.pipelines.voice_pipelines import get_voice_embedding
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data

    # ── Top bar ──
    col1, col2 = st.columns([1, 1], vertical_alignment='center')
    with col1:
        header_dashboard()
    with col2:
        c_name, c_logout = st.columns([2, 1], vertical_alignment='center')
        with c_name:
            st.markdown(
                f'<div style="text-align:right;font-size:0.9rem;color:#6b7280;">'
                f'Welcome, <strong style="color:#1a2744;">{student_data["name"]}</strong>'
                f'</div>',
                unsafe_allow_html=True
            )
        with c_logout:
            if st.button("Sign out", type='secondary', key='logout', use_container_width=True):
                del st.session_state.student_data
                st.session_state['is_logged_in'] = False
                st.rerun()

    st.divider()

    # ── Subjects header ──
    col1, col2 = st.columns([2, 1], vertical_alignment='bottom')
    with col1:
        st.markdown("""
            <div style="font-family:'DM Serif Display',Georgia,serif;font-size:1.55rem;color:#1a2744;font-weight:400;">
                Your Enrolled Subjects
            </div>
            <div style="font-size:0.83rem;color:#6b7280;margin-top:2px;">Track attendance across all your classes</div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("+ Enroll in Subject", type='primary', use_container_width=True):
            enroll_dialog()

    st.divider()

    student_id = student_data['student_id']

    with st.spinner("Loading your subjects…"):
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

    if not subjects:
        st.markdown("""
            <div style="
                text-align:center;padding:3rem 2rem;
                background:#fff;border-radius:16px;border:1.5px dashed #e2e8f0;
            ">
                <div style="font-size:2.5rem;margin-bottom:0.5rem;">🎒</div>
                <div style="font-family:'DM Serif Display',Georgia,serif;font-size:1.2rem;color:#1a2744;margin-bottom:0.3rem;">No subjects yet</div>
                <div style="font-size:0.88rem;color:#6b7280;">Enroll in a subject using the button above</div>
            </div>
        """, unsafe_allow_html=True)
        return

    cols = st.columns(2, gap='medium')
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {'total': 0, 'attended': 0})

        attended = stats['attended']
        total = stats['total']
        pct = int((attended / total * 100)) if total > 0 else 0
        pct_color = "#6b9e8c" if pct >= 75 else "#c8973a" if pct >= 50 else "#c16b6b"

        def unenroll_button(s=sub, s_id=sid):
            col_a, col_b = st.columns([1, 1], gap='small')
            with col_a:
                st.markdown(
                    f'<div style="font-size:0.82rem;font-weight:600;color:{pct_color};padding:6px 0;">{pct}% attendance</div>',
                    unsafe_allow_html=True
                )
            with col_b:
                if st.button("Unenroll", type='tertiary', key=f'unenroll_{s_id}', use_container_width=True):
                    unenroll_student_to_subject(student_id, s_id)
                    st.toast(f"Unenrolled from {s['subject_name']}")
                    st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['subject_name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ("📅", "classes", total),
                    ("✅", "attended", attended),
                ],
                footer_callback=unenroll_button,
                index=i
            )


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    # ── Login top bar ──
    col1, col2 = st.columns([1, 1], vertical_alignment='center')
    with col1:
        header_dashboard()
    with col2:
        btn_col = st.columns([2, 1])[1]
        with btn_col:
            if st.button("← Home", type='secondary', key='loginbackbtn', use_container_width=True):
                st.session_state['login_type'] = None
                st.rerun()

    st.divider()

    st.markdown("""
        <div style="font-family:'DM Serif Display',Georgia,serif;font-size:2rem;color:#1a2744;margin-bottom:0.25rem;text-align:center;">
            Student Face Login
        </div>
        <div style="font-size:0.88rem;color:#6b7280;margin-bottom:1.5rem;text-align:center;">
            Position your face in the camera frame to sign in
        </div>
    """, unsafe_allow_html=True)

    show_registration = False

    photo = st.camera_input("Position your face in the centre")
    if photo:
        img = np.array(Image.open(photo))
        with st.spinner("AI is scanning your face…"):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("No face detected. Please try again with better lighting.")
            elif num_faces > 1:
                st.warning("Multiple faces detected. Please ensure only one face is visible.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome back, {student['name']}! 👋")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info("Face not recognised. You may be a new student — register below.")
                    show_registration = True

    if show_registration:
        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("""
                <div style="font-family:'DM Serif Display',Georgia,serif;font-size:1.4rem;color:#1a2744;margin-bottom:0.5rem;">
                    Register New Profile
                </div>
            """, unsafe_allow_html=True)

            new_name = st.text_input("Your Full Name", placeholder="e.g. Priya Nair")

            st.markdown("""
                <div style="font-size:0.88rem;font-weight:600;color:#1a2744;margin:0.8rem 0 0.2rem;">
                    Voice Enrollment <span style="font-weight:400;color:#6b7280;">(optional)</span>
                </div>
                <div style="font-size:0.82rem;color:#6b7280;margin-bottom:0.6rem;">
                    Record a short clip to enable voice-based attendance
                </div>
            """, unsafe_allow_html=True)

            audio_data = None
            try:
                audio_data = st.audio_input("Record a short voice clip")
            except Exception:
                st.error("Audio input unavailable.")

            st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
            if st.button('Create My Account', type='primary', use_container_width=True):
                if new_name:
                    with st.spinner('Creating your profile…'):
                        img = np.array(Image.open(photo))
                        encodings = get_face_emb(img)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_emb=face_emb, voice_emb=voice_emb)
                            if response_data:
                                trained_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created! Welcome, {new_name}! 🎉")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Couldn't capture your face clearly. Please retake the photo.")
                else:
                    st.warning("Please enter your name to continue.")

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)