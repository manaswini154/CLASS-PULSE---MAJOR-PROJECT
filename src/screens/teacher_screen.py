import streamlit as st
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.screens.home_screen import home_screen
from src.database.db import check_teacher_exist,create_teacher, teacher_login, get_teacher_subject, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
import numpy as np
from src.pipelines.face_pipelines import predict_attendance
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from dateutil import parser


def _section_label(text, subtitle=None):
    sub_html = f'<div style="font-family:\'DM Sans\',sans-serif;font-size:0.83rem;color:#6b7280;margin-top:2px;">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f'<div style="margin-bottom:0.5rem;">'
        f'<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:1.55rem;color:#1a2744;font-weight:400;">{text}</div>'
        f'{sub_html}'
        f'</div>',
        unsafe_allow_html=True
    )


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    # ── Top bar ──
    col1, col2 = st.columns([1, 1], vertical_alignment='center')
    with col1:
        header_dashboard()
    with col2:
        c_name, c_logout = st.columns([2, 1], vertical_alignment='center')
        with c_name:
            st.markdown(
                f'<div style="text-align:right;font-size:0.9rem;color:#6b7280;">'
                f'Welcome back, <strong style="color:#1a2744;">{teacher_data["name"]}</strong>'
                f'</div>',
                unsafe_allow_html=True
            )
        with c_logout:
            if st.button("Sign out", type='secondary', key='logout', use_container_width=True):
                del st.session_state.teacher_data
                st.session_state['is_logged_in'] = False
                st.rerun()

    st.divider()

    # ── Tab navigation ──
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3, gap='small')
    with tab1:
        t = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance', width='stretch', type=t, icon="📈"):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with tab2:
        t = "primary" if st.session_state.current_teacher_tab == 'manage_subject' else 'tertiary'
        if st.button('Manage Subjects', width='stretch', type=t, icon="📝"):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()
    with tab3:
        t = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance Records', width='stretch', icon="📊", type=t):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == 'manage_subject':
        teacher_tab_manage_subject()
    if st.session_state.current_teacher_tab == 'attendance_records':
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    _section_label("Take AI Attendance", "Select a subject, add photos or record voice")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.info("You haven't created any subjects yet. Head to **Manage Subjects** to create one!")
        return

    subject_options = {f"{s['name']} — {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')
    with col1:
        selected_subject_label = st.selectbox("Select Subject", options=list(subject_options.keys()))
    with col2:
        if st.button("Add Photos", type='primary', icon="📷", use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]
    st.divider()

    if st.session_state.attendance_images:
        st.markdown(
            '<div style="font-weight:600;color:#1a2744;margin-bottom:0.6rem;font-size:0.9rem;letter-spacing:0.02em;text-transform:uppercase;">Captured Photos</div>',
            unsafe_allow_html=True
        )
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f"Photo {idx + 1}")
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3, gap='small')

    with c1:
        if st.button("Clear Photos", type='tertiary', use_container_width=True,
                     icon="🚮", disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()
    with c2:
        if st.button("Run Face Analysis", type='primary', use_container_width=True,
                     icon="🔃", disabled=not has_photos):
            with st.spinner("Analysing photos with AI…"):
                all_detected_id = {}
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_id.setdefault(student_id, []).append(f"Photo {idx + 1}")

                enrolled_res = supabase.table('subject_students').select('*,students(*)').eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students are enrolled in this subject yet!")
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_id.get(int(student['student_id']), [])
                        is_present = len(sources) > 0
                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else '—',
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })
                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })
                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)
    with c3:
        if st.button("Voice Analysis", type='primary', use_container_width=True, icon="🎙️"):
            voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_subject():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns([2, 1], vertical_alignment='bottom')
    with col1:
        _section_label("Manage Subjects", "View, share, and organise your subjects")
    with col2:
        if st.button('Create New Subject', type='primary', use_container_width=True, icon='➕'):
            create_subject_dialog(teacher_id)

    st.divider()

    subjects = get_teacher_subject(teacher_id)
    if subjects:
        cols = st.columns(2, gap='medium')
        for i, sub in enumerate(subjects):
            name = sub.get('subject_name', 'Untitled')
            stats = [
                ("👥", "Students", sub['total_students']),
                ("📅", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub, n=name):
                if st.button(
                    f"Share  ·  {sub['subject_code']}",
                    key=f"share_{sub['subject_code']}",
                    icon="⏩",
                    type='tertiary',
                    use_container_width=True
                ):
                    share_subject_dialog(n, sub['subject_code'])
                st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)

            with cols[i % 2]:
                subject_card(
                    name=name,
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=stats,
                    footer_callback=share_btn,
                    index=i
                )
    else:
        st.markdown("""
            <div style="
                text-align:center;padding:3rem 2rem;
                background:#fff;border-radius:16px;border:1.5px dashed #e2e8f0;
            ">
                <div style="font-size:2.5rem;margin-bottom:0.5rem;">📚</div>
                <div style="font-family:'DM Serif Display',Georgia,serif;font-size:1.2rem;color:#1a2744;margin-bottom:0.3rem;">No subjects yet</div>
                <div style="font-size:0.88rem;color:#6b7280;">Create your first subject using the button above</div>
            </div>
        """, unsafe_allow_html=True)


def teacher_tab_attendance_records():
    _section_label("Attendance Records", "Historical attendance grouped by session")

    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)
    if not records:
        st.info("No attendance records found yet.")
        return

    data = []
    for r in records:
        subject = r.get('subjects') or {}
        ts = r.get('timestamp')
        data.append({
            "ts_group": (p := parser.parse(ts)).strftime("%Y-%m-%d %H:%M") if ts else "Unknown",
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else "N/A",
            "Subject": subject.get('subject_name') or subject.get('name') or 'N/A',
            "Subject Code": subject.get('subject_code', 'N/A'),
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)
    summary = (
        df.groupby(['ts_group', 'Subject', 'Subject Code'])
        .agg(Present_Count=('is_present', 'sum'), Total_Count=('is_present', 'count'))
        .reset_index()
    )
    summary['Time'] = summary['ts_group']
    summary['Attendance'] = (
        "✅ " + summary['Present_Count'].astype(str) +
        " / " + summary['Total_Count'].astype(str) + " present"
    )
    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Time', 'Subject', 'Subject Code', 'Attendance']]
    )
    st.dataframe(display_df, hide_index=True, use_container_width=True)


# ── Auth helpers ──────────────────────────────────────────────────────────────

def register_teacher(username, name, pwd, conf_pwd):
    if not username or not name or not pwd:
        return False, 'All fields are required.'
    if check_teacher_exist(username):
        return False, 'Username already exists.'
    if pwd != conf_pwd:
        return False, 'Passwords do not match.'
    try:
        create_teacher(username, pwd, name)
        return True, 'Account created! Please log in.'
    except Exception:
        return False, 'An unexpected error occurred.'


def login_teacher(username, pwd):
    if not username or not pwd:
        return False
    teacher = teacher_login(username, pwd)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def _auth_top_bar(show_back=True):
    col1, col2 = st.columns([1, 1], vertical_alignment='center')
    with col1:
        header_dashboard()
    with col2:
        if show_back:
            btn_col = st.columns([2, 1])[1]
            with btn_col:
                if st.button("← Home", type='secondary', key='loginbackbtn', use_container_width=True):
                    st.session_state['login_type'] = None
                    st.rerun()
    st.divider()


def teacher_screen_login():
    _auth_top_bar()

    st.markdown("""
        <div style="max-width:440px;margin:0 auto;">
            <div style="font-family:'DM Serif Display',Georgia,serif;font-size:2rem;color:#1a2744;margin-bottom:0.25rem;">Teacher Login</div>
            <div style="font-size:0.88rem;color:#6b7280;margin-bottom:1.5rem;">Enter your credentials to access your dashboard</div>
        </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        teacher_username = st.text_input("Username", placeholder="e.g. prof_sharma")
        teacher_password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap='small')
        with c1:
            if st.button("Sign In", type='primary', use_container_width=True):
                if login_teacher(teacher_username, teacher_password):
                    st.toast("Welcome back! 👋")
                    import time; time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        with c2:
            if st.button("Create Account", type='secondary', use_container_width=True, key='loginbackbtn2'):
                st.session_state.teacher_login_type = 'register'
                st.rerun()


def teacher_register():
    _auth_top_bar(show_back=False)
    col_back = st.columns([3, 1])[1]
    with col_back:
        if st.button("← Home", type='secondary', key='loginbackbtn1', use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("""
        <div style="font-family:'DM Serif Display',Georgia,serif;font-size:2rem;color:#1a2744;margin-bottom:0.25rem;">Create Teacher Profile</div>
        <div style="font-size:0.88rem;color:#6b7280;margin-bottom:1.5rem;">Set up your account to get started</div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        teacher_name = st.text_input("Full Name", placeholder="Dr. Anjali Sharma")
        teacher_username = st.text_input("Username", placeholder="prof_sharma")
        teacher_password = st.text_input("Password", type="password", placeholder="••••••••")
        teacher_password_confirm = st.text_input("Confirm Password", type="password", placeholder="••••••••")
        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap='small')
        with c1:
            if st.button("Register", type='primary', use_container_width=True):
                success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm)
                if success:
                    st.success(message)
                    import time; time.sleep(2)
                    st.session_state.teacher_login_type = 'login'
                    st.rerun()
                else:
                    st.error(message)
        with c2:
            if st.button("Back to Login", type='secondary', use_container_width=True):
                st.session_state.teacher_login_type = 'login'
                st.rerun()