import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def get_expected_shots_info(pga_file, pga_putting_file):
    """Get expected shot info"""

    # Import PGA benchmark.
    tee_app_arg = pd.read_csv(pga_file)
    put = pd.read_csv(pga_putting_file)
    put["Distance"] = put["Distance (feet)"] / 3
    expected_shots_dict = {}

    # Set up interpolation functions.
    expected_shots_dict["Tee"] = interp1d(
        tee_app_arg[["Distance", "Tee"]].dropna()["Distance"],
        tee_app_arg[["Distance", "Tee"]].dropna()["Tee"],
        kind="linear",
        fill_value="extrapolation",
    )
    expected_shots_dict["Fairway"] = interp1d(
        tee_app_arg[["Distance", "Fairway"]].dropna()["Distance"],
        tee_app_arg[["Distance", "Fairway"]].dropna()["Fairway"],
        kind="linear",
        fill_value="extrapolation",
    )
    expected_shots_dict["Rough"] = interp1d(
        tee_app_arg[["Distance", "Rough"]].dropna()["Distance"],
        tee_app_arg[["Distance", "Rough"]].dropna()["Rough"],
        kind="linear",
        fill_value="extrapolation",
    )
    expected_shots_dict["Sand"] = interp1d(
        tee_app_arg[["Distance", "Sand"]].dropna()["Distance"],
        tee_app_arg[["Distance", "Sand"]].dropna()["Sand"],
        kind="linear",
        fill_value="extrapolation",
    )
    expected_shots_dict["Green"] = interp1d(
        put["Distance"], put["Expected putts"], kind="linear"
    )
    return expected_shots_dict


def expected_shots_on_average(x, lie, expected_shots_dict):
    """Get average number of shots expected from a player """

    if lie in expected_shots_dict.keys():
        average_number_of_shots = expected_shots_dict[lie](x)
    else:
        average_number_of_shots = np.nan
    return average_number_of_shots


def strokes_gained_calculation(
    expected_shots_dict,
    start_lie,
    start_distance,
    end_lie,
    end_distance,
    shot_number,
    next_shot_number,
):
    """Get strokes gained"""

    start_average_number_of_shots = expected_shots_on_average(
        start_distance, start_lie, expected_shots_dict
    )
    end_average_number_of_shots = expected_shots_on_average(
        end_distance, end_lie, expected_shots_dict
    )
    if next_shot_number:
        strokes_gained = start_average_number_of_shots - end_average_number_of_shots - 1
    else:
        strokes_gained = (
            start_average_number_of_shots
            - end_average_number_of_shots
            - (next_shot_number - shot_number)
        )
    return strokes_gained


def get_strokes_gained_info(arccos_data, pga_file, pga_putting_file):
    """Add Strokes gained to the dataframe"""

    expected_shots_dict = get_expected_shots_info(pga_file, pga_putting_file)

    # Impute next shot number
    arccos_data.sort_values(
        by=["round_userId", "round_startTime", "roundId", "hole_holeId", "shot_shotId"],
        inplace=True,
    )
    arccos_data["next_shot_shotId"] = arccos_data.groupby(
        ["round_userId", "round_startTime", "roundId", "hole_holeId"]
    )["shot_shotId"].shift(-1)

    # Calculate strokes gained.
    arccos_data["strokes_gained_calculated"] = arccos_data.apply(
        lambda row: strokes_gained_calculation(
            expected_shots_dict,
            row["shot_startTerrain"],
            row["shot_start_distance_yards"],
            row["shot_endTerrain"],
            row["shot_end_distance_yards"],
            row["shot_shotId"],
            row["next_shot_shotId"],
        ),
        axis=1,
    )
    return arccos_data
