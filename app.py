# app/main.py
import streamlit as st

st.set_page_config(page_title="Qwen Chatbot Interface", layout="wide")
from app.pages.page_model import render_model_page
from app.pages.page_ad import render_ad_page
from app.utils.data_loader import initialize_session_state
from utils import load_config

config = load_config(config_path="./config/config.yaml")

initialize_session_state(config)

page = st.sidebar.radio("Choose the page", ["Base Qwen page", "Q&A on listings page"])

if page == "Base Qwen page":
    render_model_page()
elif page == "Q&A on listings page":
    render_ad_page()
