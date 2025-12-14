import pandas as pd


def compute_custom_positions(laps):
    """
    Reconstruct lap-by-lap race positions for every driver using cumulative times.
    Works even when FastF1 does NOT provide position data.
    """

    # Extract only required columns
    df = laps[["Driver", "LapNumber", "LapTime"]].copy()

    # Remove invalid laps
    df = df.dropna(subset=["LapTime"])

    # Convert LapTime to seconds
    df["LapTimeSec"] = df["LapTime"].dt.total_seconds()

    # Compute cumulative race time per driver
    df["CumulativeTime"] = df.groupby("Driver")["LapTimeSec"].cumsum()

    # Create pivot table:
    # Rows = LapNumber
    # Columns = Drivers
    # Values = Cumulative race time
    pivot = df.pivot_table(
        index="LapNumber",
        columns="Driver",
        values="CumulativeTime",
        aggfunc="mean"
    )

    # For each lap → rank drivers by total time
    positions = pivot.rank(axis=1, method="min")

    # Melt back into long format
    pos_long = positions.reset_index().melt(
        id_vars="LapNumber",
        var_name="Driver",
        value_name="Position"
    )

    # Sort for clean structure
    pos_long = pos_long.sort_values(["Driver", "LapNumber"])

    return pos_long

