import plotly.express as px
import plotly.graph_objects as go


def plot_lap_times(laps, driver):
    data = laps.pick_drivers(driver)
    fig = px.line(
        data,
        x="LapNumber",
        y=data["LapTime"].dt.total_seconds(),
        markers=True,
        title=f"Lap Times – {driver}"
    )

    fig.update_layout(
        height=400,
        xaxis_title="Lap",
        yaxis_title="Time (s)"
    )

    return fig


def compare_telemetry(tel_a, tel_b, driver_a, driver_b):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tel_a["Distance"], y=tel_a["Speed"],
        mode="lines", name=f"{driver_a} Speed"
    ))

    fig.add_trace(go.Scatter(
        x=tel_b["Distance"], y=tel_b["Speed"],
        mode="lines", name=f"{driver_b} Speed"
    ))

    fig.update_layout(
        title="Speed Trace Comparison",
        height=450,
        xaxis_title="Distance (m)",
        yaxis_title="Speed (km/h)"
    )

    return fig

