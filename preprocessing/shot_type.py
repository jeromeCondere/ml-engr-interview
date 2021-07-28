import numpy as np
from scipy.stats import zscore


def get_shot_type_info(arccos_data):
    """add shot info to the dataframe"""

    def get_zscore(x):
        return zscore(x, ddof=1)

    # Impute shot type.
    conditions_shot_type = [
        (arccos_data["shot_startTerrain"] == "Tee") & (arccos_data["hole_par"] != 3),
        (arccos_data["shot_start_distance_yards"] <= 30) & (arccos_data["shot_startTerrain"] != "Green"),
        (arccos_data["shot_startTerrain"] == "Green")
    ]
    values = ["TeeShot", "GreensideShot", "Putt"]
    arccos_data["shot_type"] = np.select(conditions_shot_type, values, default="ApproachShot")

    # Calculate z-scores for shot distance and start distance and by club and shot type.
    arccos_data["shot_distance_yards_zscore"] = (
        arccos_data.groupby(["round_userId", "shot_type", "shot_clubType"])["shot_distance_yards_calculated"]
        .transform(get_zscore)).fillna(0)

    arccos_data["shot_start_distance_yards_zscore"] = (
        arccos_data.groupby(["round_userId", "shot_type", "shot_clubType"])["shot_start_distance_yards"]
        .transform(get_zscore)).fillna(0)

    # Impute shot subtype.
    conditions = [
        arccos_data["shot_type"] == "TeeShot",
        (arccos_data["shot_type"] == "ApproachShot")
        & (arccos_data["shot_distance_yards_zscore"] <= -1)
        & (arccos_data["shot_end_distance_yards"] > 30)
        & (arccos_data["shot_endTerrain"] != "Fairway"),
        (arccos_data["shot_type"] == "ApproachShot")
        & (arccos_data["shot_distance_yards_zscore"] > -1)
        & (arccos_data["shot_start_distance_yards_zscore"] > 1)
        & (arccos_data["shot_end_distance_yards"] > 30),
        arccos_data["shot_type"] == "GreensideShot",
        arccos_data["shot_type"] == "Putt"
    ]

    values = ["TeeShot", "Recovery", "LayUp", "GreensideShot", "Putt"]
    arccos_data["shot_subtype"] = np.select(conditions, values, default="GoingForGreen")

    return arccos_data
