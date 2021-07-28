import numpy as np
import pandas as pd

from utils.math_utils import calculate_miss_distance
from utils.math_utils import calculate_start_end_pin_angle
from utils.math_utils import get_bearing


def get_shot_miss_info(arccos_data):
    """add shot miss info to data"""
    def get_start_to_end_bearing(row):
        return get_bearing(row["start_coordinates"], row["end_coordinates"])

    def get_start_to_pin_bearing(row):
        return get_bearing(row["start_coordinates"], row["pin_coordinates"])

    def get_end_to_pin_bearing(row):
        return get_bearing(row["end_coordinates"], row["pin_coordinates"])

    def get_start_end_pin_angle(row):
        return calculate_start_end_pin_angle(
            row["shot_distance_yards_calculated"],
            row["shot_start_distance_yards"],
            row["shot_end_distance_yards"])

    def get_shot_miss_distance(row):
        return calculate_miss_distance(
            row["miss_bearing_left_right"],
            row["start_end_pin_angle"],
            row["shot_end_distance_yards"])

    arccos_data["start_to_end_bearing"] = arccos_data.apply(get_start_to_end_bearing, axis=1)
    arccos_data["start_to_pin_bearing"] = arccos_data.apply(get_start_to_pin_bearing, axis=1)
    arccos_data["miss_bearing_left_right"] = arccos_data["start_to_end_bearing"] - arccos_data["start_to_pin_bearing"]
    arccos_data["miss_bearing_left_right"] = np.where(arccos_data["miss_bearing_left_right"] < 0,
                                                      arccos_data["miss_bearing_left_right"] + 360,
                                                      arccos_data["miss_bearing_left_right"])

    # Determine miss distances.
    arccos_data["end_to_pin_bearing"] = arccos_data.apply(get_end_to_pin_bearing, axis=1)
    arccos_data["start_end_pin_angle"] = arccos_data.apply(get_start_end_pin_angle, axis=1)
    arccos_data["shot_miss_distance"] = arccos_data.apply(get_shot_miss_distance, axis=1)

    arccos_data[["shot_miss_distance_left_right",
                 "shot_miss_distance_short_long"]] = pd.DataFrame(arccos_data["shot_miss_distance"].tolist(),
                                                                  index=arccos_data.index)

    # Impute left/right and short_long miss directions for approach shots.
    conditions = [(arccos_data["shot_type"] == "ApproachShot") & (~arccos_data["hole_isGir"])
                  & (arccos_data["shot_miss_distance_left_right"] < 0),
                  (arccos_data["shot_type"] == "ApproachShot") & (~arccos_data["hole_isGir"])
                  & (arccos_data["shot_miss_distance_left_right"] > 0)]
    values = ["Left", "Right"]
    arccos_data["shot_miss_direction_left_right"] = np.select(conditions, values, default=np.nan)
    conditions = [(arccos_data["shot_type"] == "ApproachShot") & (~arccos_data["hole_isGir"])
                  & (arccos_data["shot_miss_distance_short_long"] < 0),
                  (arccos_data["shot_type"] == "ApproachShot") & (~arccos_data["hole_isGir"])
                  & (arccos_data["shot_miss_distance_short_long"] > 0)]
    values = ["Short", "Long"]
    arccos_data["shot_miss_direction_short_long"] = np.select(conditions, values, default=np.nan)

    # Use miss distance information to impute miss_direction.
    conditions = [(arccos_data["shot_type"] == "TeeShot") & (arccos_data["hole_isFairWayRight"]),
                  (arccos_data["shot_type"] == "TeeShot") & (arccos_data["hole_isFairWayLeft"]),
                  (arccos_data["shot_type"] == "ApproachShot") & (~arccos_data["hole_isGir"])]
    values = ["Right", "Left", arccos_data["shot_miss_direction_short_long"] + " " + arccos_data["shot_miss_direction_left_right"]]
    arccos_data["shot_miss_direction_all_shots"] = np.select(conditions, values, default=np.nan)
    return arccos_data
