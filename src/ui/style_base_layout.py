import streamlit as st
     
def style_background_home():
    st.markdown("""
                <style>
                .stApp{
                background-color: #5865f2 !important;  
                }
                .stApp div[data-testid = "stColumn"]{
                background-color: #ffffff !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important;

                }
                </style>
                """, unsafe_allow_html=True)
    
def style_background_dashboard():
    st.markdown("""
                <style>
                .stApp{
                background-color: #e0e3ff !important;  
                }
                </style>
                """, unsafe_allow_html=True)
    
def style_base_layout():
    st.markdown("""
                <style>
                @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');
            
                   MainMenu, header, footer {
                    visibility: hidden;
                    }
                
                    .block-container {
                        padding-top: 1.5rem;
                    }
                
                    h1{
                        font-family: 'Playfair Display', Lato, sans-serif !important;
                        color: #333333 !important;
                        font-size: 2.5rem !important;  
                        line-height: 1.2 !important;
                        font-weight: 700 !important;
                        Margin-bottom: 0rem !important;
                    }
                    h2{
                        font-family: 'Playfair Display', Lato, sans-serif !important;
                        color: #333333 !important;
                        font-size: 2rem !important;  
                        line-height: 1.2 !important;
                        font-weight: 700 !important;
                        Margin-bottom: 0rem !important;
                    }
                    h3, p, h4{
                        font-family: 'Outfit', sans-serif !important;
                        color: #333333 !important;
                        font-size: 1rem !important;  
                        line-height: 1.5 !important;
                        font-weight: 400 !important;
                    }
                    button[kind="primary"] { 
                        background-color: #5865f2 !important; 
                        border-radius: 1.5rem !important; 
                        padding: 10px 20px !important; 
                        border: none !important; 
                        transition: transform 0.25s ease-in-out !important; 
                        }
                    button[kind = 'secondary']{
                        background-color: #eb459e !important;
                        border-radius: 1.5rem !important;
                        padding: 10px 20px !important;
                        border: none !important;
                        transition: transform 0.25s ease-in-out !important;
                    }
                    button[kind = 'tertiary']{
                        background-color: black !important;
                        border-radius: 1.5rem !important;
                        padding: 10px 20px !important;
                        border: none !important;
                        transition: transform 0.25s ease-in-out !important;
                    }
                    button:hover{
                        transform: scale(1.05) !important;
                    }
                    button[kind="primary"] span,
                    button[kind="secondary"] span,
                    button[kind="tertiary"] span {
                        color: white !important;
                    }
                </style>
                """, unsafe_allow_html=True)
