import streamlit as st

# Accent colours cycling per card
_ACCENTS = ["#4a7fc1", "#6b9e8c", "#c8973a", "#7c6bc1", "#c16b6b"]

def subject_card(name, code, section, stats=None, footer_callback=None, index=0):
    accent = _ACCENTS[index % len(_ACCENTS)]

    # Build stats HTML — no indentation that renders as whitespace
    stats_html = ""
    if stats:
        chips = ""
        for icon, label, value in stats:
            chips += (
                f'<div style="display:inline-flex;align-items:center;gap:4px;'
                f'background:{accent}14;border:1px solid {accent}28;'
                f'padding:4px 10px;border-radius:20px;margin-right:6px;margin-bottom:4px;">'
                f'<span style="font-size:0.85rem;">{icon}</span>'
                f'<span style="font-size:0.82rem;font-weight:600;color:{accent};">{value}</span>'
                f'<span style="font-size:0.82rem;color:#6b7280;">{label}</span>'
                f'</div>'
            )
        stats_html = f'<div style="margin-top:10px;">{chips}</div>'

    section_badge = (
        f'<span style="font-size:0.78rem;font-weight:500;color:#6b7280;'
        f'background:#f0f2f8;padding:2px 8px;border-radius:6px;margin-left:6px;">§ {section}</span>'
        if section else ""
    )

    html = (
        f'<div style="'
        f'background:#ffffff;'
        f'border-radius:16px;'
        f'border:1px solid #e2e8f0;'
        f'border-left:4px solid {accent};'
        f'padding:20px 22px 16px;'
        f'margin-bottom:12px;'
        f'box-shadow:0 2px 12px rgba(26,39,68,0.06);'
        f'transition:box-shadow 0.2s ease;">'

        f'<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;">'
        f'<div style="font-family:\'DM Serif Display\',Georgia,serif;font-size:1.15rem;font-weight:400;color:#1a2744;line-height:1.25;">{name}</div>'
        f'</div>'

        f'<div style="display:flex;align-items:center;margin-top:6px;flex-wrap:wrap;gap:4px;">'
        f'<span style="font-size:0.8rem;font-weight:600;color:{accent};'
        f'background:{accent}14;padding:3px 10px;border-radius:8px;letter-spacing:0.03em;">{code}</span>'
        f'{section_badge}'
        f'</div>'

        f'{stats_html}'
        f'</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()