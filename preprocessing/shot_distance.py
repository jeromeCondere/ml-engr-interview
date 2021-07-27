import pandas as pd
import numpy as np
from geopy import distance

def get_shot_distance_coord_info(arccos_data):
    """add coordinate and shot distance to the dataframe"""

    # Calculate starting distance for each shot.
    arccos_data['start_coordinates'] = list(zip(arccos_data['shot_startLat'],
                                                arccos_data['shot_startLong']))
    arccos_data['pin_coordinates'] = list(zip(arccos_data['hole_pinLat'],
                                              arccos_data['hole_pinLong']))
    arccos_data['shot_start_distance_yards'] = arccos_data.apply(
        lambda row: distance.distance(row['start_coordinates'], row['pin_coordinates']).ft / 3, axis=1
    )
    arccos_data['shot_endLat'].fillna(arccos_data['hole_pinLat'], inplace=True)
    arccos_data['shot_endLong'].fillna(arccos_data['hole_pinLong'], inplace=True)
    arccos_data['end_coordinates'] = list(zip(arccos_data['shot_endLat'], arccos_data['shot_endLong']))

    # Calculate shot distance in yards using start and end coordinates.
    arccos_data['shot_distance_yards_calculated'] = arccos_data.apply(
     lambda row: distance.distance(row['start_coordinates'], row['end_coordinates']).ft / 3, axis=1
    )

    # Calculate end distance for each shot.
    arccos_data['shot_end_distance_yards'] = arccos_data.apply(
     lambda row: distance.distance(row['end_coordinates'], row['pin_coordinates']).ft / 3, axis=1
    )
    arccos_data['shot_end_distance_yards'].fillna(0, inplace=True)

    # Take hole length as the distance to CG for first shot.
    arccos_data['hole_yards'] = np.where(arccos_data['shot_shotId'] == 1,
                                     arccos_data['shot_startDistanceToCG'],
                                     np.nan)
    arccos_data['hole_yards'].ffill(inplace=True)
    arccos_data['hole_yards'] = pd.to_numeric(arccos_data['hole_yards'])

    return arccos_data