import streamlit as st

def load_css():
    """Loads the custom CSS styles for the SIA application."""
    st.markdown("""
    <style>
    .stApp {
        background-color: #FEFEFE;
        color: #535F80;
    }

    [data-testid="stSidebar"] {
        background-color: #E7E9F0;
        border-right: 1px solid #d1d5db;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #051747 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    p, label, span, li, div {
        color: #535F80;
    }

    div.stButton > button {
        background-color: #D1E3FF;
        color: #051747 !important;
        border-radius: 8px;
        border: 1px solid #B3D3FF;
        padding: 0.6rem 1rem;
        width: 100%;
        font-weight: 600;
    }

    .login-container, div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 25px rgba(5, 23, 71, 0.05);
    }

    .sia-avatar-header, .sia-avatar-large {
        border-radius: 50%;
        background-color: #081F62;
        color: white;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .sia-avatar-header {
        width: 70px;
        height: 70px;
        font-size: 22px;
    }

    .sia-avatar-large {
        width: 80px;
        height: 80px;
        font-size: 26px;
        margin: 0 auto 20px;
    }

    .contact-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #081F62;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
