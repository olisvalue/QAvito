# app/pages/page_model.py
import streamlit as st
from app.services.model_service import qwen_model_base

def render_model_page():
    """Renders page for interaction with base model."""
    st.header("Чат с Qwen (no fine-tune)")

    default_sys_message = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
    new_context = st.text_input("System message", default_sys_message)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if st.button("Set system message"):
        st.session_state["messages"] = [{"role": "system", "content": new_context}]
        st.success("Системное сообщение обновлено!")

    user_input = st.text_input("Введите Ваше сообщение")

    if st.button("Отправить"):
        if user_input:
            custom_message = {"role": "user", "content": user_input}
            st.session_state["messages"].append(custom_message)
            response = qwen_model_base.generate_response(st.session_state["messages"])
            st.session_state["messages"].append({"role": "assistant", "content": response})

    st.subheader("История общения")
    for message in st.session_state["messages"]:
        role = "🤖" if message["role"] == "assistant" else ("🧑" if message["role"] == "user" else "📜")
        st.markdown(f"**{role} {message['role'].capitalize()}**: {message['content']}")
