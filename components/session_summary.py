import streamlit as st
import pandas as pd


# Convert raw seconds → F1 timing format M:SS.mmm
def format_timedelta(seconds):
    if pd.isna(seconds):
        return None
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:06.3f}"


def show_session_summary(session, laps):
    st.markdown("<div class='section-title'>Session Summary</div>", unsafe_allow_html=True)

    # Get general session info
    event = session.event
    session_info = session.session_info
    
    session_name = session.name
    date = event.get("EventDate", "N/A")
    circuit = event.get("Location", event["EventName"])

    # Start time (if available)
    start_dt = f"{session_info.get('StartDate', '')} {session_info.get('StartTime', '')}".strip()
    if not start_dt:
        start_dt = "N/A"

    # TOP INFO PANEL
    st.markdown("<div class='panel'>", unsafe_allow_html=True)

    st.write(f"**Event:** {event['EventName']}")
    st.write(f"**Session:** {session_name}")
    st.write(f"**Date:** {date}")
    st.write(f"**Start Time (Local):** {start_dt}")
    st.write(f"**Location:** {circuit}")

    st.markdown("</div>", unsafe_allow_html=True)

    # Normalize session type
    session_type = session_name.lower()

    # ==========================================
    #                RACE SUMMARY
    # ==========================================
    if "race" in session_type:
        st.subheader("Race Results")

        results = session.results.copy()

        # Extract fields safely
        pos = results.get("Position", results.index)
        drv_no = results.get("DriverNumber", ["-"] * len(results))

        # Convert finish times
        if "Time" in results.columns:
            results["Time"] = results["Time"].apply(
                lambda x: format_timedelta(x.total_seconds()) if pd.notna(x) else "DNF"
            )

        df = pd.DataFrame({
            "Pos": pos,
            "No": drv_no,
            "Driver": results["FullName"],
            "Team": results["TeamName"],
            "Laps": results["Laps"],
            "Time / Retired": results["Time"],
            "Pts": results["Points"]
        })

        st.dataframe(df, width="stretch", hide_index=True)

    # ==========================================
    #          PRACTICE / QUALI SUMMARY
    # ==========================================
    else:
        st.subheader("Fastest Laps")

        # Get fastest lap per driver
        fastest = laps.groupby("Driver")["LapTime"].min().sort_values()

        df = pd.DataFrame({
            "DriverCode": fastest.index,
            "Fastest Lap": fastest.dt.total_seconds().apply(format_timedelta)
        })

        # Add full Driver Name
        df["Driver"] = df["DriverCode"].apply(lambda d: session.get_driver(d)["FullName"])

        # Add Team Name
        df["Team"] = df["DriverCode"].apply(lambda d: session.get_driver(d)["TeamName"])

        # Add Driver Number
        df["No"] = df["DriverCode"].apply(lambda d: session.get_driver(d)["DriverNumber"])

        # Add Laps completed
        df["Laps"] = df["DriverCode"].apply(lambda d: len(laps.pick_drivers(d)))

        # Add Position
        df["Pos"] = range(1, len(df) + 1)

        # Reorder columns to FIA style
        df = df[["Pos", "No", "Driver", "Team", "Fastest Lap", "Laps"]]

        st.dataframe(df, width="stretch", hide_index=True)

