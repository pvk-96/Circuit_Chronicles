import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def show_telemetry_comparison(session, laps):
    st.markdown("<div class='section-title'>Telemetry Comparison</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    drivers = sorted(laps["Driver"].unique())

    # Driver selectors
    col1, col2 = st.columns(2)
    with col1:
        driver_a = st.selectbox("Driver A", drivers)
    with col2:
        driver_b = st.selectbox("Driver B", drivers)

    if driver_a == driver_b:
        st.warning("Please select two different drivers.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Choose laps (default = fastest lap)
    laps_a = laps.pick_drivers(driver_a).reset_index(drop=True)
    laps_b = laps.pick_drivers(driver_b).reset_index(drop=True)

    fastest_a = laps_a.loc[laps_a["LapTime"].idxmin()]["LapNumber"]
    fastest_b = laps_b.loc[laps_b["LapTime"].idxmin()]["LapNumber"]

    col3, col4 = st.columns(2)
    with col3:
        lap_a = st.number_input(f"Lap for {driver_a}", min_value=1, max_value=int(laps_a["LapNumber"].max()), value=int(fastest_a))
    with col4:
        lap_b = st.number_input(f"Lap for {driver_b}", min_value=1, max_value=int(laps_b["LapNumber"].max()), value=int(fastest_b))

    # Extract telemetry
    try:
        tel_a = laps.pick_drivers(driver_a).pick_laps(lap_a).iloc[0].get_telemetry()
        tel_b = laps.pick_drivers(driver_b).pick_laps(lap_b).iloc[0].get_telemetry()
    except:
        st.error("Telemetry unavailable for the selected laps.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Sync by distance
    merged = pd.DataFrame({
        "Distance": tel_a["Distance"],
        "Speed_A": tel_a["Speed"],
        "Speed_B": tel_b["Speed"].reindex_like(tel_a, method="nearest"),
        "Throttle_A": tel_a["Throttle"],
        "Throttle_B": tel_b["Throttle"].reindex_like(tel_a, method="nearest"),
        "Brake_A": tel_a["Brake"],
        "Brake_B": tel_b["Brake"].reindex_like(tel_a, method="nearest"),
        "Gear_A": tel_a["nGear"],
        "Gear_B": tel_b["nGear"].reindex_like(tel_a, method="nearest")
    })

    # ======================================
    # SPEED TRACE COMPARISON
    # ======================================
    st.subheader("Speed Trace Comparison")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Speed_A"],
        mode="lines",
        name=f"{driver_a} Speed",
        line=dict(width=2, color="#1EA7FF")
    ))

    fig.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Speed_B"],
        mode="lines",
        name=f"{driver_b} Speed",
        line=dict(width=2, color="#00CC88")
    ))

    fig.update_layout(
        height=400,
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(color="white"),
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ======================================
    # THROTTLE / BRAKE COMPARISON
    # ======================================
    st.subheader("Throttle & Brake Comparison")

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Throttle_A"],
        mode="lines",
        name=f"{driver_a} Throttle",
        line=dict(width=2, color="#1EA7FF")
    ))

    fig2.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Throttle_B"],
        mode="lines",
        name=f"{driver_b} Throttle",
        line=dict(width=2, color="#00CC88")
    ))

    fig2.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Brake_A"] * 100,
        mode="lines",
        name=f"{driver_a} Brake (%)",
        line=dict(width=2, color="#FF4444", dash="dot")
    ))

    fig2.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Brake_B"] * 100,
        mode="lines",
        name=f"{driver_b} Brake (%)",
        line=dict(width=2, color="#FF8888", dash="dot")
    ))

    fig2.update_layout(
        height=400,
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(color="white"),
        xaxis_title="Distance (m)",
        yaxis_title="Throttle / Brake (%)"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ======================================
    # GEAR COMPARISON
    # ======================================
    st.subheader("Gear Selection Comparison")

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Gear_A"],
        mode="lines",
        name=f"{driver_a} Gear",
        line=dict(width=2, color="#1EA7FF")
    ))

    fig3.add_trace(go.Scatter(
        x=merged["Distance"],
        y=merged["Gear_B"],
        mode="lines",
        name=f"{driver_b} Gear",
        line=dict(width=2, color="#00CC88")
    ))

    fig3.update_layout(
        height=400,
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(color="white"),
        xaxis_title="Distance (m)",
        yaxis_title="Gear"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

