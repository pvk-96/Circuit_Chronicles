import streamlit as st

def sidebar_selectors():
    st.sidebar.title("Session Selector")

    year = st.sidebar.selectbox("Year", list(range(2018, 2025)), index=6)
    gp = st.sidebar.text_input("Grand Prix", "Bahrain")
    session_type = st.sidebar.selectbox(
        "Session",
        ["FP1", "FP2", "FP3", "Qualifying", "Race"]
    )

    return year, gp, session_type

