import streamlit as st
from src.ui.styles import load_css
from src.ui.layout import render_header, render_sidebar, render_contact_page
from src.ui.chat_interface import render_chat_interface
from src.core.agent import initialize_agent

st.set_page_config(
    page_title="SIA - Sunbeam Infotech Assistant",
    layout="wide",
    page_icon="🎓"
)

load_css()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "chat"
if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()


def show_login_page():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown('<div class="sia-avatar-large">SIA</div>', unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            if username:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Hello {username}! How can I help you today?"
                })
                st.rerun()


if not st.session_state.logged_in:
    show_login_page()
else:
    render_sidebar()
    render_header()

    if st.session_state.current_view == "contact":
        render_contact_page()
    else:
        render_chat_interface(st.session_state.agent)
