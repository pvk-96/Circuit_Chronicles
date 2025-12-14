import streamlit as st
import plotly.graph_objects as go
from utils.position_engine import compute_custom_positions


def show_position_evolution(session):
    st.markdown("<div class='section-title'>Position Evolution</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    if session.name.lower() != "race":
        st.info("Position evolution is only available for race sessions.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    laps = session.laps

    if laps.empty:
        st.error("Lap data not available.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Compute custom positions
    pos_data = compute_custom_positions(laps)

    drivers = sorted(pos_data["Driver"].unique())

    driver = st.selectbox("Select Driver", drivers, key="pos_evo_driver")

    drv_pos = pos_data[pos_data["Driver"] == driver]

    if drv_pos.empty:
        st.warning("No position data available for this driver.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Plot position vs lap
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=drv_pos["LapNumber"],
        y=drv_pos["Position"],
        mode="lines+markers",
        line=dict(color="#1EA7FF", width=3),
        marker=dict(size=6, color="#1EA7FF"),
        name=f"{driver} Position"
    ))

    fig.update_layout(
        height=450,
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(color="white"),
        xaxis_title="Lap Number",
        yaxis_title="Race Position",
        yaxis=dict(autorange="reversed"),  # P1 at top
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
