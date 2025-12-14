import streamlit as st
import pandas as pd
from utils.position_engine import compute_custom_positions


def classify_overtake(row, laps):
    """Determine the type of overtake."""
    lap = row["LapNumber"]
    driver = row["Driver"]
    passed = row["Passed"]

    # Check pit stops
    driver_lap = laps[(laps["Driver"] == driver) & (laps["LapNumber"] == lap)]
    passed_lap = laps[(laps["Driver"] == passed) & (laps["LapNumber"] == lap)]

    prev_driver_lap = laps[(laps["Driver"] == driver) & (laps["LapNumber"] == lap - 1)]
    prev_passed_lap = laps[(laps["Driver"] == passed) & (laps["LapNumber"] == lap - 1)]

    # If passed driver pits → undercut
    if not passed_lap["PitInTime"].isna().all():
        return "Undercut (pit stop)"

    # If overtaking driver pits previous lap → overcut
    if not prev_driver_lap["PitOutTime"].isna().all():
        return "Overcut"

    # TODO: Add SC/VSC logic if needed (optional)

    return "On-track"


def show_overtake_detector(session):
    st.markdown("<div class='section-title'>Overtake Detector</div>", unsafe_allow_html=True)
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    if session.name.lower() != "race":
        st.info("Overtake detection is only available for race sessions.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    laps = session.laps

    # Use reconstructed positions
    pos_data = compute_custom_positions(laps)

    overtakes = []

    # Loop through all drivers
    for driver in pos_data["Driver"].unique():
        drv_data = pos_data[pos_data["Driver"] == driver]

        # Check each lap for position improvement
        for i in range(1, len(drv_data)):
            prev_pos = drv_data.iloc[i - 1]["Position"]
            cur_pos = drv_data.iloc[i]["Position"]

            lap_num = int(drv_data.iloc[i]["LapNumber"])

            # Position drop → overtake
            if cur_pos < prev_pos:
                gained = int(prev_pos - cur_pos)

                # Determine who was passed
                lap_positions = pos_data[pos_data["LapNumber"] == lap_num]
                prev_positions = pos_data[pos_data["LapNumber"] == lap_num - 1]

                # Drivers around the position change
                passed_driver = None
                for other in lap_positions["Driver"]:
                    prev_p = prev_positions[prev_positions["Driver"] == other]["Position"].values
                    now_p = lap_positions[lap_positions["Driver"] == other]["Position"].values
                    if len(prev_p) and len(now_p) and now_p[0] > prev_p[0]:
                        passed_driver = other
                        break

                method = classify_overtake(
                    {"LapNumber": lap_num, "Driver": driver, "Passed": passed_driver},
                    laps
                )

                overtakes.append({
                    "Lap": lap_num,
                    "Driver": driver,
                    "Passed": passed_driver,
                    "New Position": int(cur_pos),
                    "Method": method
                })

    if not overtakes:
        st.info("No overtakes detected.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    overtake_df = pd.DataFrame(overtakes)

    st.dataframe(overtake_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
