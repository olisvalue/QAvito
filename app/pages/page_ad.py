# app/pages/page_ad.py
import streamlit as st
from app.services.model_service import qwen_model_base, qwen_model_lora
from app.utils.ad_utils import create_prompt_for_ad
from app.utils.data_loader import get_random_ad

predefined_questions = [
    "Есть ли торг на этот товар?",
    "Опишите, пожалуйста, достоинства товара.",
    "Какая предоставляется гарантия?",
    "В каком состоянии товар?"
]

if "current_question" not in st.session_state:
    st.session_state["current_question"] = None
if "lora_response" not in st.session_state:
    st.session_state["lora_response"] = None
if "base_response" not in st.session_state:
    st.session_state["base_response"] = None
if "selected_ad" not in st.session_state: 
    st.session_state["selected_ad"] = None

def render_ad_page():
    """Renders page for interaction with model finetuned on ads."""
    st.header("Задать вопрос по объявлению")
    if st.button("Выбрать случайное объявление"):
        selected_ad = get_random_ad()
        st.session_state.selected_ad = selected_ad

    if st.session_state["selected_ad"]:
        ad = st.session_state["selected_ad"]
        st.subheader("Выбранное объявление")
        st.markdown(f"**Категория:** {ad.get('category_name', 'Неизвестно')}")
        st.markdown(f"**Заголовок:** {ad.get('title', 'Неизвестно')}")
        st.markdown(f"**Описание:** {ad.get('description', 'Описание отсутствует')}")
        st.markdown(f"**Цена:** {ad.get('price', 'Цена не указана')} руб.")

        st.subheader("Выберите вопрос:")
        columns = st.columns(len(predefined_questions))
        question_clicked = None

        for idx, question in enumerate(predefined_questions):
            if columns[idx].button(question):
                question_clicked = question

        if question_clicked:
            prompt_messages = create_prompt_for_ad(ad, question_clicked)
            lora_response = qwen_model_lora.generate_response(prompt_messages)
            base_response = qwen_model_base.generate_response(prompt_messages)

            st.session_state["current_question"] = question_clicked
            st.session_state["lora_response"] = lora_response
            st.session_state["base_response"] = base_response

        if st.session_state["current_question"]:
            st.subheader(f"Вопрос: **{st.session_state['current_question']}**")

            st.markdown("### 🎯 Ответ Finetuned Qwen:")
            st.markdown(f"<div style='border: 2px solid #4CAF50; padding: 10px; border-radius: 10px;'>{st.session_state['lora_response']}</div>", unsafe_allow_html=True)

            st.markdown("### 🤖 Ответ Base Qwen:")
            st.markdown(f"<div style='border: 2px solid #2196F3; padding: 10px; border-radius: 10px;'>{st.session_state['base_response']}</div>", unsafe_allow_html=True)

        st.subheader("Или задайте свой:")
        custom_question = st.text_input("Введите вопрос", value="")

        if st.button("Спросить"):
            if custom_question:
                prompt_messages = create_prompt_for_ad(ad, custom_question)                
                lora_response = qwen_model_lora.generate_response(prompt_messages)
                base_response = qwen_model_base.generate_response(prompt_messages)

                st.markdown("### 🎯 Ответ Finetuned Qwen:")
                st.markdown(f"<div style='border: 2px solid #4CAF50; padding: 10px; border-radius: 10px;'>{lora_response}</div>", unsafe_allow_html=True)

                st.markdown("### 🤖 Ответ Base Qwen:")
                st.markdown(f"<div style='border: 2px solid #2196F3; padding: 10px; border-radius: 10px;'>{base_response}</div>", unsafe_allow_html=True)
