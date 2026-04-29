import streamlit as st
import io
import segno


@st.dialog("Share Subject")
def share_subject_dialog(subject_name, subject_code):
    app_domain = 'class-pulse-main.streamlit.app'
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.markdown(
        f'<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:1.3rem;color:#1a2744;margin-bottom:0.2rem;">'
        f'Invite students to join</div>'
        f'<div style="font-size:0.85rem;color:#6b7280;margin-bottom:1rem;">{subject_name}</div>',
        unsafe_allow_html=True
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns([1, 1], gap='large')
    with col1:
        st.markdown(
            '<div style="font-size:0.82rem;font-weight:600;color:#1a2744;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;">Join Link</div>',
            unsafe_allow_html=True
        )
        st.code(join_url, language='text')
        st.markdown(
            '<div style="font-size:0.82rem;font-weight:600;color:#1a2744;text-transform:uppercase;letter-spacing:0.06em;margin:0.6rem 0 0.4rem;">Subject Code</div>',
            unsafe_allow_html=True
        )
        st.code(subject_code, language='text')
        st.caption("Share this link or code with your students.")

    with col2:
        st.markdown(
            '<div style="font-size:0.82rem;font-weight:600;color:#1a2744;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.4rem;">QR Code</div>',
            unsafe_allow_html=True
        )
        st.image(out.getvalue(), use_container_width=True)