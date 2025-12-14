import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show_lap_time_chart(session):
    st.markdown("<div class='section-title'>Lap Time Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    # Always use original session data (safe, unmodified)
    laps = session.laps

    drivers = sorted(laps["Driver"].unique())

    driver = st.selectbox("Select Driver", drivers, key="lap_time_driver")

    # Load clean laps directly from FastF1
    drv_laps = laps.pick_drivers(driver)[["LapNumber", "LapTime", "PitOutTime", "PitInTime"]]

    # Remove invalid LapTime rows
    drv_laps = drv_laps.dropna(subset=["LapTime"])

    # Convert lap times to seconds
    drv_laps["Seconds"] = drv_laps["LapTime"].dt.total_seconds()

    # If no valid laps, show message
    if drv_laps.empty:
        st.warning("No valid lap time available for this driver in this session.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # UI toggles
    remove_pit_laps = st.checkbox("Remove pit laps", value=True, key="remove_pit_laps")
    show_trend = st.checkbox("Show pace trend line", value=True, key="lap_time_trend")

    if remove_pit_laps:
        drv_laps = drv_laps[drv_laps["Seconds"] > 30]  # avoid filtering all laps on small circuits

    if drv_laps.empty:
        st.warning("All laps were filtered out.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Identify fastest lap
    fastest_index = drv_laps["Seconds"].idxmin()
    fastest_seconds = drv_laps.loc[fastest_index, "Seconds"]
    fastest_lap = drv_laps.loc[fastest_index, "LapNumber"]

    # Plot setup
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=drv_laps["LapNumber"],
        y=drv_laps["Seconds"],
        mode="lines+markers",
        name=f"{driver} Lap Times",
        line=dict(color="#1EA7FF", width=2),
        marker=dict(color="#1EA7FF", size=6)
    ))

    # Highlight fastest lap
    fig.add_trace(go.Scatter(
        x=[fastest_lap],
        y=[fastest_seconds],
        mode="markers+text",
        text=["Fastest"],
        textposition="bottom center",
        marker=dict(color="gold", size=12, symbol="star"),
        name="Fastest Lap"
    ))

    # Trend line
    if show_trend:
        drv_laps["Trend"] = drv_laps["Seconds"].rolling(3, min_periods=1).mean()

        fig.add_trace(go.Scatter(
            x=drv_laps["LapNumber"],
            y=drv_laps["Trend"],
            mode="lines",
            line=dict(color="#00CC88", width=3, dash="dot"),
            name="Trend"
        ))

    fig.update_layout(
        height=450,
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(color="white"),
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (seconds)",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Lap Time Data")
    st.dataframe(drv_laps[["LapNumber", "LapTime", "Seconds"]], use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

