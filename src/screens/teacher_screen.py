import streamlit as st
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.screens.home_screen import home_screen
from src.database.db import check_teacher_exist,create_teacher, teacher_login
#from src.components.footer import footer_dashboard

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
    st.write("Teacher Dashboard")
    teacher_data = st.session_state.teacher_data
    st.write(f"Welcome {teacher_data['name']}")


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




    