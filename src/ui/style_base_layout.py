import streamlit as st


def style_background_home():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a2744 0%, #2d4a7a 40%, #1e3a6e 70%, #0f1f3d 100%) !important;
        }
        .stApp div[data-testid="stColumn"] {
            background: rgba(255,255,255,0.07) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            padding: 2.5rem !important;
            border-radius: 2rem !important;
            border: 1px solid rgba(255,255,255,0.13) !important;
            box-shadow: 0 8px 40px rgba(0,0,0,0.25) !important;
        }
        .stApp div[data-testid="stColumn"] * {
            color: #f5f0e8 !important;
        }
        .stApp div[data-testid="stColumn"] button span,
        .stApp div[data-testid="stColumn"] button p,
        .stApp div[data-testid="stColumn"] button * {
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
        .stApp {
            background: #f0f2f8 !important;
        }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

        :root {
            --navy:     #1a2744;
            --blue:     #2d4a7a;
            --sky:      #4a7fc1;
            --sage:     #6b9e8c;
            --mint:     #a8d5c2;
            --gold:     #c8973a;
            --charcoal: #2c3345;
            --muted:    #6b7280;
            --soft-bg:  #f0f2f8;
            --border:   #e2e8f0;
        }

        MainMenu, header, footer { visibility: hidden; }

        .block-container {
            padding-top: 1.2rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            max-width: 1120px !important;
        }

        /* Font family only — no global color override */
        * { font-family: 'DM Sans', sans-serif !important; }

        h1 {
            font-family: 'DM Serif Display', Georgia, serif !important;
            color: var(--navy) !important;
            font-size: 2.5rem !important;
            font-weight: 400 !important;
            line-height: 1.15 !important;
            letter-spacing: -0.02em !important;
            margin-bottom: 0.25rem !important;
        }
        h2 {
            font-family: 'DM Serif Display', Georgia, serif !important;
            color: var(--navy) !important;
            font-size: 1.8rem !important;
            font-weight: 400 !important;
            line-height: 1.2 !important;
            margin-bottom: 0.25rem !important;
        }
        h3 {
            color: var(--charcoal) !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
        }

        /* Streamlit text elements */
        div[data-testid="stMarkdownContainer"] p { color: var(--charcoal) !important; font-size: 0.95rem !important; }
        label { color: var(--charcoal) !important; font-size: 0.88rem !important; font-weight: 500 !important; }

        hr {
            border: none !important;
            border-top: 1.5px solid var(--border) !important;
            margin: 1.2rem 0 !important;
        }

        /* ═══════════════════════════════════════════
           BUTTONS — target every text/icon child
        ═══════════════════════════════════════════ */

        /* PRIMARY — navy gradient */
        button[kind="primary"] {
            background: linear-gradient(135deg, #1a2744, #2d4a7a) !important;
            border: none !important;
            border-radius: 0.75rem !important;
            box-shadow: 0 2px 12px rgba(26,39,68,0.22) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 22px rgba(26,39,68,0.32) !important;
        }
        button[kind="primary"],
        button[kind="primary"] span,
        button[kind="primary"] p,
        button[kind="primary"] div,
        button[kind="primary"] [data-testid="stIconMaterial"],
        button[kind="primary"] .material-symbols-rounded {
            color: #ffffff !important;
        }

        /* SECONDARY — sage green */
        button[kind="secondary"] {
            background: linear-gradient(135deg, #6b9e8c, #4d8272) !important;
            border: none !important;
            border-radius: 0.75rem !important;
            box-shadow: 0 2px 12px rgba(107,158,140,0.25) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        button[kind="secondary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 22px rgba(107,158,140,0.35) !important;
        }
        button[kind="secondary"],
        button[kind="secondary"] span,
        button[kind="secondary"] p,
        button[kind="secondary"] div,
        button[kind="secondary"] [data-testid="stIconMaterial"],
        button[kind="secondary"] .material-symbols-rounded {
            color: #ffffff !important;
        }

        /* TERTIARY — white outlined */
        button[kind="tertiary"] {
            background: #ffffff !important;
            border: 1.5px solid var(--border) !important;
            border-radius: 0.75rem !important;
            transition: background 0.2s ease, border-color 0.2s ease, transform 0.2s ease !important;
        }
        button[kind="tertiary"]:hover {
            background: var(--soft-bg) !important;
            border-color: var(--sky) !important;
            transform: translateY(-1px) !important;
        }
        button[kind="tertiary"],
        button[kind="tertiary"] span,
        button[kind="tertiary"] p,
        button[kind="tertiary"] div,
        button[kind="tertiary"] [data-testid="stIconMaterial"],
        button[kind="tertiary"] .material-symbols-rounded {
            color: #2c3345 !important;
        }

        /* ═══════════════════════════════════════════
           INPUTS
        ═══════════════════════════════════════════ */
        div[data-testid="stTextInput"] input {
            border: 1.5px solid var(--border) !important;
            border-radius: 0.75rem !important;
            background: #ffffff !important;
            color: var(--charcoal) !important;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: var(--sky) !important;
            box-shadow: 0 0 0 3px rgba(74,127,193,0.12) !important;
            outline: none !important;
        }
        div[data-testid="stTextInput"] input::placeholder { color: #9ca3af !important; }

        /* Selectbox */
        div[data-baseweb="select"] > div {
            border-radius: 0.75rem !important;
            border-color: var(--border) !important;
            background: #ffffff !important;
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div { color: var(--charcoal) !important; }
        li[role="option"] { color: var(--charcoal) !important; }
        li[role="option"]:hover { background: var(--soft-bg) !important; }

        /* ═══════════════════════════════════════════
           COMPONENTS
        ═══════════════════════════════════════════ */
        div[data-testid="stDialog"] > div {
            border-radius: 1.5rem !important;
            border: 1px solid var(--border) !important;
            box-shadow: 0 20px 60px rgba(26,39,68,0.18) !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 1rem !important;
            overflow: hidden !important;
            border: 1px solid var(--border) !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 0.85rem !important;
            border-left-width: 4px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 1.2rem !important;
            border: 1px solid var(--border) !important;
            box-shadow: 0 2px 16px rgba(26,39,68,0.06) !important;
            background: #ffffff !important;
        }

        div[data-testid="stCaptionContainer"] p {
            color: var(--muted) !important;
            font-size: 0.82rem !important;
        }

        .stSpinner > div { border-top-color: var(--sky) !important; }

        div[data-testid="stToast"] {
            border-radius: 0.85rem !important;
            border: 1px solid var(--border) !important;
        }
        </style>
    """, unsafe_allow_html=True)