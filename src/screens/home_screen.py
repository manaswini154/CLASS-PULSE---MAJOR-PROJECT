import streamlit as st
from src.components.header import header_home
from src.ui.style_base_layout import style_base_layout, style_background_home


def home_screen():
    style_background_home()
    style_base_layout()

    header_home()

    # Sub-heading on dark bg — inline white colour
    st.markdown("""
        <p style="text-align:center;color:rgba(245,240,232,0.65);font-size:0.95rem;
                  margin-bottom:2rem;font-family:'DM Sans',sans-serif;">
            Select your role to continue
        </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # ── Teacher card ──────────────────────────────────────────────
    with col1:
        st.markdown("""
            <div style="text-align:center;padding-bottom:0.75rem;">
                <div style="width:64px;height:64px;
                            background:linear-gradient(135deg,rgba(200,151,58,0.3) 0%,rgba(200,151,58,0.1) 100%);
                            border:1.5px solid rgba(200,151,58,0.4);border-radius:18px;
                            display:flex;align-items:center;justify-content:center;margin:0 auto 0.75rem;">
                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                        <rect x="4" y="8" width="24" height="16" rx="3" fill="rgba(200,151,58,0.7)"/>
                        <rect x="7" y="11" width="10" height="1.5" rx="1" fill="white" fill-opacity="0.9"/>
                        <rect x="7" y="14.5" width="7" height="1.5" rx="1" fill="white" fill-opacity="0.7"/>
                        <rect x="7" y="18" width="8" height="1.5" rx="1" fill="white" fill-opacity="0.7"/>
                        <circle cx="23" cy="15" r="3" fill="white" fill-opacity="0.9"/>
                        <path d="M19 22c0-2.2 1.79-4 4-4s4 1.8 4 4H19z" fill="white" fill-opacity="0.9"/>
                    </svg>
                </div>
                <div style="font-family:'DM Serif Display',Georgia,serif;font-size:1.35rem;
                            color:#f5f0e8;font-weight:400;margin-bottom:0.3rem;">
                    I am a Teacher
                </div>
                <div style="font-size:0.82rem;color:rgba(245,240,232,0.55);
                            font-family:'DM Sans',sans-serif;margin-bottom:1rem;">
                    Manage subjects &amp; attendance
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Continue as Teacher", type="primary", key="home_teacher_login",
                     use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    # ── Student card ──────────────────────────────────────────────
    with col2:
        st.markdown("""
            <div style="text-align:center;padding-bottom:0.75rem;">
                <div style="width:64px;height:64px;
                            background:linear-gradient(135deg,rgba(107,158,140,0.3) 0%,rgba(168,213,194,0.1) 100%);
                            border:1.5px solid rgba(107,158,140,0.4);border-radius:18px;
                            display:flex;align-items:center;justify-content:center;margin:0 auto 0.75rem;">
                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                        <circle cx="16" cy="12" r="5" fill="rgba(107,158,140,0.8)"/>
                        <path d="M8 26c0-4.42 3.58-8 8-8s8 3.58 8 8H8z" fill="rgba(168,213,194,0.7)"/>
                        <path d="M4 16l12-6 12 6-12 4L4 16z" fill="white" fill-opacity="0.9"/>
                    </svg>
                </div>
                <div style="font-family:'DM Serif Display',Georgia,serif;font-size:1.35rem;
                            color:#f5f0e8;font-weight:400;margin-bottom:0.3rem;">
                    I am a Student
                </div>
                <div style="font-size:0.82rem;color:rgba(245,240,232,0.55);
                            font-family:'DM Sans',sans-serif;margin-bottom:1rem;">
                    View subjects &amp; track attendance
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Continue as Student", type="primary", key="home_student_login",
                     use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()

    st.markdown("""
        <div style="text-align:center;margin-top:2.5rem;font-size:0.75rem;
                    color:rgba(245,240,232,0.3);letter-spacing:0.1em;text-transform:uppercase;">
            Powered by Facial &amp; Voice Recognition AI
        </div>
    """, unsafe_allow_html=True)