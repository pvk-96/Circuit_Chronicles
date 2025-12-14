import streamlit as st
import plotly.graph_objects as go


def show_track_map(session, laps):
    st.markdown("<div class='section-title'>Track Map</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    # Try to extract telemetry from one lap
    try:
        driver = laps["Driver"].iloc[0]
        lap = laps.pick_drivers(driver).iloc[0]
        tel = lap.get_telemetry().sort_values("Distance")

        x = tel["X"]
        y = tel["Y"]

    except Exception as e:
        st.error(f"Track map unavailable: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Create the simple track outline
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        line=dict(color="#1EA7FF", width=3),
        name="Circuit Layout"
    ))

    # Style
    fig.update_layout(
        height=600,
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(color="#F2F2F2"),
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

