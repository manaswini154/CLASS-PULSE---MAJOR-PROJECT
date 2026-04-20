import streamlit as st

def header_home():
    logo_url = "https://logowik.com/content/uploads/images/education635.logowik.com.webp"    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; flex-direction:column; margin-top: 30px;align-items: center;margin-botton: 30px;">
            <img src="{logo_url}" style="height: 100px;">
            <h1 style='text-align: center, color: #eoe3ff'>CLASS<br/> PULSE</h1>

        </div>
        """,
        unsafe_allow_html=True
    )

def header_dashboard():
    logo_url = "https://logowik.com/content/uploads/images/education635.logowik.com.webp"    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; gap:10px; margin-top: 30px;align-items: center;margin-botton: 30px;">
            <img src="{logo_url}" style="height: 85px;">
            <h1 style='text-align: center, color: #5865f2'>CLASS<br/> PULSE</h1>

        </div>
        """,
        unsafe_allow_html=True
    )