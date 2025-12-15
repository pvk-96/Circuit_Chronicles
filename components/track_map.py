import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show_track_map(session, laps):
    st.markdown("<div class='section-title'>Track Layout</div>", unsafe_allow_html=True)

    # Pick fastest lap for layout
    fastest_lap = laps.pick_fastest()
    telemetry = fastest_lap.get_telemetry().dropna()

    x = telemetry["X"].to_numpy()
    y = telemetry["Y"].to_numpy()
    dist = telemetry["Distance"].to_numpy()

    if len(x) == 0:
        st.warning("Track data unavailable for this session.")
        return

    # Normalize distance (0 → 1)
    dist_norm = (dist - dist.min()) / (dist.max() - dist.min())

    # 3 equal segments (~33% each)
    seg1 = dist_norm <= 0.33
    seg2 = (dist_norm > 0.33) & (dist_norm <= 0.66)
    seg3 = dist_norm > 0.66

    fig = go.Figure()

    # RED section
    fig.add_trace(go.Scatter(
        x=x[seg1],
        y=y[seg1],
        mode="lines",
        line=dict(color="#E53935", width=4),
        name="Sector 1"
    ))

    # YELLOW section
    fig.add_trace(go.Scatter(
        x=x[seg2],
        y=y[seg2],
        mode="lines",
        line=dict(color="#FDD835", width=4),
        name="Sector 2"
    ))

    # BLUE section
    fig.add_trace(go.Scatter(
        x=x[seg3],
        y=y[seg3],
        mode="lines",
        line=dict(color="#1E88E5", width=4),
        name="Sector 3"
    ))

    fig.update_layout(
        showlegend=True,
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    st.plotly_chart(fig, width="stretch")
