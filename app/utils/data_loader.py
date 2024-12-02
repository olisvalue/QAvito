# app/utils/data_loader.py
import streamlit as st
import json
import os
import random

def load_data(file_path):
    """Loads data as json file and returns it as a list."""
    if not os.path.exists(file_path):
        st.error(f"Файл с данными не найден. Убедитесь, что файл находится в {file_path}")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def initialize_session_state(config):
    """Inits session state."""
    if "ads_data" not in st.session_state:
        st.session_state.ads_data = load_data(config["ads_path"])
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "selected_ad" not in st.session_state:
        st.session_state.selected_ad = None

def get_random_ad():
    """Chooses random ad from loaded data."""
    if len(st.session_state.ads_data) == 0:
        st.warning("Файл не содержит данных.")
        return None
    return random.choice(st.session_state.ads_data)
