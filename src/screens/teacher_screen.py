import streamlit as st
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.screens.home_screen import home_screen
from src.database.db import check_teacher_exist,create_teacher, teacher_login, get_teacher_subject
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
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
    st.header("Teacher Dashboard")
    teacher_data = st.session_state.teacher_data
    col1, col2 = st.columns(2, vertical_alignment = 'center', gap ='xxlarge')
    with col1:
        header_dashboard()
    with col2:
        st.write(f"Welcome {teacher_data['name']}")
        if st.button("Logout", type = 'secondary', key = 'logout'):
            del st.session_state.teacher_data
            st.session_state['is_logged_in'] = False
            st.rerun()
    st.space()
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1= "primary" if st.session_state.current_teacher_tab  == 'take_attendance' else 'tertiary'
        if st.button('Take_Attendance', width = 'stretch',type = type1, icon = ':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2= "primary" if st.session_state.current_teacher_tab  == 'manage_subject' else 'tertiary'
        if st.button('Manage_subjects', width = 'stretch', type = type2, icon = ':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subject'
            st.rerun()

    with tab3:
        type3= "primary" if st.session_state.current_teacher_tab  == 'attendance_records' else 'tertiary'
        if st.button('Attendance_records', width = 'stretch', icon = ':material/cards_stack:', type = type3):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab =='manage_subject':
        teacher_tab_manage_subject()
    if st.session_state.current_teacher_tab =='attendance_records':
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take AI Attendance")
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []
    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning("You haven not created any subjects yet. Please create one to begin!")
        return
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1])
    with col1:
        selected_subject_label = st.selectbox("Select Subject: ", options = list(subject_options.keys()))
    with col2:
        if st.button("Add Photos", type = 'primary', icon = ':material/photo_prints:',width = 'stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()


def teacher_tab_manage_subject():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 =  st.columns(2)
    with col1:
        st.header('Manage Subjects', width = 'stretch')
            
    with col2:
        if st.button('Create New Subject', width = 'stretch'):
            create_subject_dialog(teacher_id)
    
    #list all subjects
    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:

            # ✅ ADD THIS LINE HERE
            name = sub.get('subject_name') 

            stats = [
                ("🫂", "Students", sub['total_students']),
                ("⏰", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):
                if st.button(
                    f"Share Code: {name}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:"
                ):
                    share_subject_dialog(name, sub['subject_code'])
                st.space()

            subject_card(
                name=name,  # ✅ use fixed variable
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECT FOUND! CREATE ONE ABOVE!")



def teacher_tab_attendance_records():
    st.header('Attendance Records')


def register_teacher(username, name, pwd, conf_pwd):
    if not username or not name or not pwd:
        return False, 'All Fields are required!'
    
    if check_teacher_exist(username):
        return False, 'Username already exists!'
    if pwd != conf_pwd:
        return False, 'passwords does not match!'
    
    try:
        create_teacher(username, pwd, name)
        return True, 'Successfully created!!!\nLogin Now!'
    except Exception as e:
        return False, "Unexpected Error!"


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

def teacher_screen_login():
    col1, col2 = st.columns(2, vertical_alignment = 'center', gap ='xxlarge')
    with col1:
        header_dashboard()
    with col2:
        if st.button("Return to Home Page", type='secondary', key ='loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()
    st.header("Login using Password", text_alignment = 'center')
    st.space()
    teacher_username = st.text_input("Enter Username: ", placeholder = "Username")
    teacher_password = st.text_input("Enter Password: ", type = "password", placeholder='Password')
    st.divider()

    c1,c2 = st.columns(2)
    with c1:
        if st.button("Login",type='secondary',width = 'stretch'):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome Back!!", icon = "👋")
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid Username or Password")

    with c2:
        if st.button("Register Instead",type = "primary",width = 'stretch',key='loginbackbtn2'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    #footer_dashboard()

def teacher_register():
    col1, col2 = st.columns(2, vertical_alignment = 'center', gap ='xxlarge')
    with col1:
        header_dashboard()
    with col2:
        if st.button("return to home page", type='secondary', key ='loginbackbtn1'):
            st.session_state['login_type'] = None
            st.rerun()
    st.header("Register your Teacher Profile")
    st.space()
    teacher_name = st.text_input("Enter Your Name: ", placeholder = 'Name')
    teacher_username = st.text_input("Enter Username: ", placeholder = "Username1")
    teacher_password = st.text_input("Enter Password: ", type = "password", placeholder='Password1')
    teacher_password_confirm = st.text_input(" confirm Your Password: ", type = "password", placeholder='Confirm Password')
    st.divider()

    c1,c2 = st.columns(2)
    with c1:
        if st.button("Register Now",type='secondary',width = 'stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_password, teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message,width='stretch')
    with c2:
        if st.button("Login Instead",type = "primary",width = 'stretch'):
            st.session_state.teacher_login_type ='login'
            st.rerun()




    