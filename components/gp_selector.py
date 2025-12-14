import streamlit as st
import fastf1

def select_grand_prix():
    st.markdown("<div class='section-title'>Grand Prix Selector</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    # Year Picker
    year = st.selectbox("Select Year", list(range(2018, 2026)), index=7, key="year_selector")

    # Load schedule
    schedule = fastf1.get_event_schedule(year)

    # Filter: remove testing events
    schedule = schedule[schedule["EventFormat"] != "testing"]

    # Build GP list
    gp_names = schedule["EventName"].tolist()

    # Dropdown
    gp_name = st.selectbox("Select Grand Prix", gp_names, key="gp_selector")

    # Return event info
    event = schedule[schedule["EventName"] == gp_name].iloc[0]

    st.markdown("</div>", unsafe_allow_html=True)
    return year, event
