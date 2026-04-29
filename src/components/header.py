import streamlit as st

def header_home():
    st.markdown("""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2.5rem 1rem 1.5rem;
            text-align: center;
        ">
            <div style="
                width: 72px; height: 72px;
                background: linear-gradient(135deg, rgba(200,151,58,0.9) 0%, rgba(168,213,194,0.9) 100%);
                border-radius: 20px;
                display: flex; align-items: center; justify-content: center;
                margin-bottom: 1rem;
                box-shadow: 0 4px 20px rgba(200,151,58,0.3);
            ">
                <svg width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 4L34 12V20C34 27.732 27.732 34 20 34H18C10.268 34 4 27.732 4 20V12L19 4Z" fill="white" fill-opacity="0.9"/>
                    <path d="M19 10L28 15V20C28 24.418 24.418 28 20 28H18C13.582 28 10 24.418 10 20V15L19 10Z" fill="#1a2744" fill-opacity="0.35"/>
                    <circle cx="19" cy="19" r="4" fill="white"/>
                </svg>
            </div>
            <div style="
                font-family: 'DM Serif Display', Georgia, serif;
                font-size: 2.8rem;
                font-weight: 400;
                color: #f5f0e8;
                letter-spacing: -0.03em;
                line-height: 1;
                margin-bottom: 0.3rem;
            ">Class Pulse</div>
            <div style="
                font-family: 'DM Sans', sans-serif;
                font-size: 0.85rem;
                font-weight: 400;
                color: rgba(245,240,232,0.65);
                letter-spacing: 0.12em;
                text-transform: uppercase;
            ">AI-Powered Attendance</div>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem 0;
        ">
            <div style="
                width: 44px; height: 44px;
                background: linear-gradient(135deg, #1a2744 0%, #2d4a7a 100%);
                border-radius: 12px;
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 2px 10px rgba(26,39,68,0.2);
                flex-shrink: 0;
            ">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L22 7.5V13C22 17.97 17.97 22 13 22H11C6.03 22 2 17.97 2 13V7.5L12 2Z" fill="white" fill-opacity="0.85"/>
                    <circle cx="12" cy="12" r="2.5" fill="#1a2744" fill-opacity="0.5"/>
                </svg>
            </div>
            <div>
                <div style="
                    font-family: 'DM Serif Display', Georgia, serif;
                    font-size: 1.5rem;
                    font-weight: 400;
                    color: #1a2744;
                    letter-spacing: -0.02em;
                    line-height: 1.1;
                ">Class Pulse</div>
                <div style="
                    font-family: 'DM Sans', sans-serif;
                    font-size: 0.7rem;
                    color: #6b7280;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                ">AI Attendance</div>
            </div>
        </div>
    """, unsafe_allow_html=True)