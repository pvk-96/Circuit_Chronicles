import streamlit as st
import pandas as pd


def format_timedelta(seconds):
    if pd.isna(seconds):
        return None
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:06.3f}"


def show_driver_highlight(laps):
    st.markdown("<div class='section-title'>Driver Highlight</div>", unsafe_allow_html=True)

    driver = st.selectbox("Highlight Driver", sorted(laps["Driver"].unique()))

    laps_driver = laps.pick_drivers(driver).copy()

    # Filter valid laps
    laps_driver = laps_driver[
        laps_driver["LapTime"].notna() &
        laps_driver["Sector1Time"].notna() &
        laps_driver["Sector2Time"].notna() &
        laps_driver["Sector3Time"].notna()
    ]

    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    fastest = laps_driver["LapTime"].min().total_seconds()
    avg = laps_driver["LapTime"].mean().total_seconds()

    st.write(f"**Fastest Lap:** {format_timedelta(fastest)}")
    st.write(f"**Average Lap:** {format_timedelta(avg)}")
    st.write(f"**Total Valid Laps:** {len(laps_driver)}")

    df = laps_driver[["LapNumber", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]].copy()

    for col in ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]:
        df[col] = df[col].dt.total_seconds().apply(format_timedelta)

    st.write("Lap Data:")
    st.dataframe(df, width='stretch')

    st.markdown("</div>", unsafe_allow_html=True)

