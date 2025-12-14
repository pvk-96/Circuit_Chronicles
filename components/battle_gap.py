import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show_battle_gap(laps):
    st.markdown("<div class='section-title'>Battle Gap Graph</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    drivers = sorted(laps["Driver"].unique())

    col1, col2 = st.columns(2)
    driver_a = col1.selectbox("Driver A", drivers, key="gap_driver_a")
    driver_b = col2.selectbox("Driver B", drivers, key="gap_driver_b")

    if driver_a == driver_b:
        st.warning("Select two different drivers.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Get laps for each driver
    laps_a = laps.pick_drivers(driver_a)[["LapNumber", "LapTime"]].dropna()
    laps_b = laps.pick_drivers(driver_b)[["LapNumber", "LapTime"]].dropna()

    # Convert LapTime to seconds
    laps_a["LapTimeSec"] = laps_a["LapTime"].dt.total_seconds()
    laps_b["LapTimeSec"] = laps_b["LapTime"].dt.total_seconds()

    # Compute cumulative race time
    laps_a["CumTime"] = laps_a["LapTimeSec"].cumsum()
    laps_b["CumTime"] = laps_b["LapTimeSec"].cumsum()

    # Merge by LapNumber (only compare laps both drivers completed)
    merged = pd.merge(
        laps_a[["LapNumber", "CumTime"]],
        laps_b[["LapNumber", "CumTime"]],
        on="LapNumber",
        suffixes=("_A", "_B")
    )

    # Compute gap
    merged["Gap"] = merged["CumTime_A"] - merged["CumTime_B"]

    # Plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=merged["LapNumber"],
        y=merged["Gap"],
        mode="lines+markers",
        line=dict(color="#1EA7FF", width=3),
        marker=dict(size=6, color="#1EA7FF"),
        name=f"Gap: {driver_a} vs {driver_b}"
    ))

    # Zero line (when drivers are equal)
    fig.add_hline(
        y=0,
        line=dict(color="gray", width=1, dash="dot")
    )

    fig.update_layout(
        height=450,
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(color="white"),
        xaxis_title="Lap Number",
        yaxis_title=f"Gap (seconds) — {driver_a} - {driver_b}",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
