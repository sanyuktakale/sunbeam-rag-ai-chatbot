import streamlit as st

def render_header():
    """Displays the main SIA Header."""
    st.markdown("""
        <div class="main-header-container">
            <div class="sia-avatar-header">SIA</div>
            <h1 style="margin: 0; font-size: 2.2rem;">Sunbeam Infotech Assistant</h1>
        </div>
        <p style="margin: 0; font-size: 1.1rem;">
        Your AI Partner for IT Career Guidance
        </p>
        <hr style="border-top: 1px solid #E7E9F0; margin-bottom: 30px;">
    """, unsafe_allow_html=True)


def render_sidebar():
    """Displays the Sidebar navigation with New Chat, Chat History, Logout."""
    with st.sidebar:
        st.markdown("### Sunbeam Info")

        if st.session_state.get("username"):
            st.markdown(f"Hello, **{st.session_state.username}**")

        st.markdown("---")

        # =========================
        # NEW CHAT BUTTON
        # =========================
        if st.button(" New Chat"):
            st.session_state.messages = []
            st.session_state.current_view = "chat"
            st.rerun()

        st.markdown("---")

        # =========================
        # CHAT HISTORY
        # =========================
        st.markdown("### History")

        if st.session_state.messages:
            for i, msg in enumerate(st.session_state.messages):
                if msg["role"] == "user":
                    label = msg["content"][:30] + "..."
                    if st.button(label, key=f"history_{i}"):
                        st.session_state.messages = st.session_state.messages[:i+1]
                        st.session_state.current_view = "chat"
                        st.rerun()
        else:
            st.caption("No previous chats")

        st.markdown("---")

        # =========================
        # QUICK NAVIGATION
        # =========================
        if st.button(" About Us"):
            process_button_click("Tell me about Sunbeam Infotech")

        if st.button("All Courses"):
            process_button_click("tell me about all courses in detail?")

        if st.button("Campus Locations"):
            process_button_click("Where are the Sunbeam campuses located?")

        if st.button("Contact Us"):
            st.session_state.current_view = "contact"
            st.rerun()

        st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

        # =========================
        # LOGOUT (AT BOTTOM)
        # =========================
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.session_state.username = ""
            st.session_state.current_view = "chat"
            st.rerun()


def process_button_click(prompt_text):
    """Helper to handle button clicks as chat inputs."""
    st.session_state.current_view = "chat"
    st.session_state.messages.append(
        {"role": "user", "content": prompt_text}
    )
    st.rerun()


def render_contact_page():
    """Displays the Contact Information cards."""
    st.subheader("Get in Touch")
    st.write("We are here to answer any questions you may have about our courses and placements.")
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="contact-card">
            <h4> Pune Campus (Hinjewadi)</h4>
            <p>Sunbeam Infotech,<br>
            Plot No. P 80, Rajiv Gandhi Infotech Park,<br>
            Phase 1, Hinjewadi, Pune - 411057</p>
        </div>
        <div class="contact-card">
            <h4> Karad Campus</h4>
            <p>Sunbeam Institute,<br>
            Anand Nagar, Behind Market Yard,<br>
            Karad - 415110</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="contact-card">
            <h4> Official Contact</h4>
            <p><strong>Email:</strong> admission@sunbeaminfo.com</p>
            <p><strong>Phone:</strong> +91 20 2295 3281</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅ Back to Chat"):
            st.session_state.current_view = "chat"
            st.rerun()
