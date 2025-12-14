import streamlit as st

def show_car_loader(text="Loading..."):
    loader_html = f"""
    <div class="car-loader-container">
        <div class="car-track">
            <div class="car">🏎️</div>
        </div>
        <p class="car-loader-text">{text}</p>
    </div>
    """
    placeholder = st.empty()
    placeholder.markdown(loader_html, unsafe_allow_html=True)
    return placeholder
