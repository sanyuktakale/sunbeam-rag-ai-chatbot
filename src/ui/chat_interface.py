import streamlit as st

def render_chat_interface(agent_executor):

    for msg in st.session_state.messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask SIA about courses, fees, or placements..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("SIA is thinking..."):
                response = agent_executor.invoke({
                    "input": st.session_state.messages[-1]["content"],
                    "chat_history": st.session_state.messages[:-1]
                })
                output = response["output"]
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
