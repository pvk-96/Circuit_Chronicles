import streamlit as st
from utils.plotting import plot_lap_times

def show_lap_analysis(laps):
    st.markdown("<div class='section-title'>Lap-by-Lap Pace</div>", unsafe_allow_html=True)

    driver = st.selectbox("Select Driver", sorted(laps["Driver"].unique()))

    fig = plot_lap_times(laps, driver)

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.plotly_chart(fig, width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)

