import streamlit as st
import textwrap

def subject_card(name, code, section, stats=None, footer_callback=None):
    # We start with the first chunk
    html = f"""<div style="background:white; border-left: 8px solid #EB459E; padding:25px; border-radius: 20px; border: 1px solid black; margin-bottom:10px;">
    <h2 style="margin:0; color: #1e293b; font-size: 1.5rem;">{name}</h2>
    <p style="color:#64748b; margin:10px 0;">Code : <span style="background:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius:5px;"> {code} </span> </p>"""

    if stats:
        # Notice we don't indent the internal HTML tags here
        html += '<div style="display:flex; gap:8px; flex-wrap:wrap;">'
        for icon, label, value in stats:
            html += f'<div style="background:#EB459E10; padding:5px 12px; border-radius:12px; font-size:0.9rem;">{icon} <b>{value}</b> {label}</div>'
        html += "</div>"

    html += "</div>"
    
    # Use unsafe_allow_html=True
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
