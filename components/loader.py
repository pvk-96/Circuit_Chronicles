import streamlit as st
import time

def show_loader(text="Loading data..."):
    loader_html = f"""
    <div class="loader-container">
        <div class="spinner"></div>
        <p class="loader-text">{text}</p>
    </div>
    """

    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    return placeholder
